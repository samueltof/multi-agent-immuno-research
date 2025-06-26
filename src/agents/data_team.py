"""
Data Team Agent - Custom LangGraph workflow for SQL generation and database analysis.

This module provides a sophisticated data analysis agent that can:
- Convert natural language to SQL queries
- Validate and execute SQL queries  
- Provide database schema information
- Handle query retries and error recovery
- Get random data samples for exploration
"""

from langgraph.graph import StateGraph, END, MessagesState
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage, ToolMessage
from typing import List, Dict, Any, Optional, Literal
from functools import partial
import re
from pydantic import BaseModel, Field
import logging

from src.tools.database import get_database_schema, execute_sql_query, execute_sql_query_and_save, get_random_subsamples
from src.prompts import apply_workflow_prompt_template

logger = logging.getLogger(__name__)

# Constants
MAX_SQL_RETRIES = 2

# Extended state for data team operations
class DataTeamState(MessagesState):
    """Extended state for data team operations."""
    # Constants
    TEAM_MEMBERS: list[str]
    
    # Runtime Variables
    next: str
    full_plan: str
    deep_thinking_mode: bool
    search_before_planning: bool
    
    # Data team specific state
    natural_language_query: Optional[str] = None
    schema: Optional[str] = None
    generated_sql: Optional[str] = None
    validation_status: Optional[str] = None  # "valid", "invalid", "error"
    validation_feedback: Optional[str] = None
    execution_result: Optional[str] = None
    error_message: Optional[str] = None
    sql_generation_retries: int = 0
    provided_schema_text: Optional[str] = None

# Note: ReAct agent prompt is now loaded from src/prompts/data_analyst/react_sql_generator.md

# SQL Validation Model
class SQLValidationResult(BaseModel):
    status: Literal["valid", "invalid", "error"] = Field(description="The validation status of the SQL query.")
    feedback: str = Field(description="Detailed feedback on the validation, including reasons for invalidity or confirmation of validity.")

# Note: SQL validator prompt is now loaded from src/prompts/data_analyst/sql_validator.md

def get_schema_node(state: DataTeamState) -> Dict[str, Any]:
    """Automatically gets the database schema before SQL generation."""
    logger.info("👨‍💻 DATA TEAM: Getting database schema automatically...")
    
    try:
        # Get the schema using the tool
        schema_result = get_database_schema.invoke({})
        logger.info("👨‍💻 DATA TEAM: Schema retrieved successfully")
        return {"schema": schema_result}
    except Exception as e:
        error_msg = f"Failed to get database schema: {str(e)}"
        logger.error(f"👨‍💻 DATA TEAM: {error_msg}")
        return {"error_message": error_msg}

def prepare_data_query_node(state: DataTeamState) -> Dict[str, Any]:
    """Extracts the latest user query and prepares the initial message for the ReAct agent."""
    logger.info("👨‍💻 DATA TEAM: Preparing query for ReAct agent...")

    last_human_message_content = None
    # Find the last human message to get the core query
    for msg in reversed(state['messages']):
        if isinstance(msg, HumanMessage):
            last_human_message_content = msg.content
            break

    if last_human_message_content is None:
        error_msg = "No HumanMessage found in the state history to process."
        logger.error(f"👨‍💻 DATA TEAM: {error_msg}")
        return {"error_message": error_msg}

    logger.info(f"👨‍💻 DATA TEAM: Found user query: '{last_human_message_content}'")

    # Prepare template variables for the workflow prompt
    retry_feedback = state.get("validation_feedback", "")
    is_retrying_sql = state.get("generated_sql") is not None and state.get("validation_status") == "invalid"
    
    # Build retry feedback text
    retry_feedback_text = ""
    if is_retrying_sql and retry_feedback:
        retry_feedback_text = f"You previously generated SQL that failed validation with the following feedback: '{retry_feedback}'. Please analyze this feedback and generate a corrected query."
    
    # Prepare template variables
    template_vars = {
        "USER_QUERY": last_human_message_content,
        "DATABASE_SCHEMA": state.get("schema", ""),
        "RETRY_FEEDBACK": retry_feedback_text,
    }
    
    # Generate the prompt using the workflow template
    initial_prompt = apply_workflow_prompt_template(
        "data_analyst", 
        "react_sql_generator", 
        template_vars
    )

    return {
        "messages": [HumanMessage(content=initial_prompt)],
        "natural_language_query": last_human_message_content,
        "schema": state.get("schema"), 
        "generated_sql": None,  # Reset for this run
        "provided_schema_text": None,  # Reset for this run
        "validation_status": None,
        "validation_feedback": None,
        "execution_result": None,
        "error_message": None,
        "sql_generation_retries": state.get("sql_generation_retries", 0) if not is_retrying_sql else state["sql_generation_retries"]
    }

def extract_schema_or_sql_node(state: DataTeamState) -> Dict[str, Any]:
    """Extracts schema text or SQL query from the last message of the ReAct agent."""
    logger.info("👨‍💻 DATA TEAM: Extracting schema or SQL from ReAct agent output...")
    if state.get("error_message"):
        return {}

    last_message = state["messages"][-1] if state["messages"] else None
    return_dict = {}

    if isinstance(last_message, AIMessage) and last_message.content:
        content = last_message.content.strip()
        
        is_likely_schema = "database schema:" in content.lower() or ("table:" in content.lower() and "columns:" in content.lower())
        sql_keywords = ["SELECT ", "INSERT ", "UPDATE ", "DELETE ", "CREATE ", "DROP ", "ALTER ", "WITH "]
        is_sql = any(kw in content.upper() for kw in sql_keywords)
        
        # Check for SQL in markdown blocks
        sql_match = re.search(r"```sql\s*(.*?)\s*```", content, re.DOTALL | re.IGNORECASE)
        extracted_sql_from_markdown = None
        if sql_match:
            extracted_sql_from_markdown = sql_match.group(1).strip()
            if extracted_sql_from_markdown and any(kw in extracted_sql_from_markdown.upper() for kw in sql_keywords):
                logger.info(f"👨‍💻 DATA TEAM: Extracted SQL (from markdown block): {extracted_sql_from_markdown}")
                return {"generated_sql": extracted_sql_from_markdown, "provided_schema_text": None, "validation_feedback": None}

        # Prioritize SQL detection over schema detection
        if is_sql:
            logger.info(f"👨‍💻 DATA TEAM: Extracted SQL (raw content): {content}")
            return {"generated_sql": content, "provided_schema_text": None, "validation_feedback": None}
        elif is_likely_schema:
            logger.info(f"👨‍💻 DATA TEAM: Identified as schema description: {content[:150]}...")
            return {"provided_schema_text": content, "generated_sql": None}
        else:
            natural_query = state.get("natural_language_query", "").lower()
            if "schema" in natural_query or "database schema" in natural_query:
                logger.warning(f"👨‍💻 DATA TEAM: Expected schema, treating as schema: {content[:150]}...")
                return {"provided_schema_text": content, "generated_sql": None}
            else:
                logger.error(f"👨‍💻 DATA TEAM: Failed to extract valid SQL or schema: {content}")
                return {"error_message": f"Agent did not produce a recognizable SQL query or schema. Response: {content}"}
    else:
        logger.error(f"👨‍💻 DATA TEAM: No valid AIMessage content found. Last message: {last_message}")
        return {"error_message": "ReAct agent did not return a final message with content."}

def sql_validator_node(state: DataTeamState, llm_client: Any) -> Dict[str, Any]:
    """Validates the generated SQL using an LLM with structured output."""
    logger.info("👨‍💻 DATA TEAM: Validating SQL...")
    if state.get("error_message") or not state.get("generated_sql") or state.get("provided_schema_text"):
        logger.warning("👨‍💻 DATA TEAM: Skipping SQL validation due to prior error, missing SQL, or schema was provided directly.")
        return {}

    schema = state.get("schema", "Schema not available for validation.")
    
    # Get schema from message history if not in state
    if not schema or schema == "Schema not available for validation.":
        logger.warning("👨‍💻 DATA TEAM: Schema not found in state. Checking message history...")
        fetched_schema = None
        schema_tool_call_id = None
        messages = state.get("messages", [])

        # Find the latest schema tool call
        for msg in reversed(messages):
            if isinstance(msg, AIMessage) and msg.tool_calls:
                for tc in msg.tool_calls:
                    if tc.get("name") == "get_database_schema":
                        schema_tool_call_id = tc.get("id")
                        break
                if schema_tool_call_id:
                    break
        
        # Find the corresponding ToolMessage result
        if schema_tool_call_id:
            for msg in reversed(messages):
                if isinstance(msg, ToolMessage) and msg.tool_call_id == schema_tool_call_id:
                    if "Error" not in msg.content and msg.content:
                        fetched_schema = msg.content
                        logger.info("👨‍💻 DATA TEAM: Found schema in ToolMessage history.")
                        break

        if fetched_schema:
            schema = fetched_schema

    # Prepare template variables for SQL validation
    template_vars = {
        "DATABASE_SCHEMA": schema,
        "USER_QUERY": state["natural_language_query"],
        "GENERATED_SQL": state["generated_sql"]
    }
    
    # Generate the validation prompt using the workflow template
    prompt_str = apply_workflow_prompt_template(
        "data_analyst", 
        "sql_validator", 
        template_vars
    )

    try:
        llm = llm_client
        structured_llm = llm.with_structured_output(SQLValidationResult)
        logger.info("Attempting SQL validation...")
        validation_result = structured_llm.invoke([HumanMessage(content=prompt_str)])
        logger.info(f"👨‍💻 DATA TEAM: Validation result: {validation_result}")
        return {"validation_status": validation_result.status, "validation_feedback": validation_result.feedback}
    except Exception as e:
        logger.error(f"👨‍💻 DATA TEAM: Error validating SQL: {e}")
        return {"validation_status": "error", "validation_feedback": f"Failed during validation: {str(e)}"}

def sql_executor_node(state: DataTeamState) -> Dict[str, Any]:
    """Executes the validated SQL query using the appropriate tool based on expected result size."""
    logger.info("👨‍💻 DATA TEAM: Executing SQL...")
    if state.get("error_message") or not state.get("generated_sql") or state.get("validation_status") != "valid" or state.get("provided_schema_text"):
        if state.get("validation_status") != "valid" and not state.get("provided_schema_text"):
            logger.warning(f"👨‍💻 DATA TEAM: Skipping execution because SQL validation status is '{state.get('validation_status')}'.")
        return {}

    try:
        # First, try to estimate the result size by running a COUNT query
        sql_query = state["generated_sql"]
        query_lower = sql_query.lower().strip()
        
        # Determine if we should use file-based approach based on query characteristics
        use_file_approach = False
        
        # Check for patterns that typically return large datasets
        large_dataset_indicators = [
            "join" in query_lower and "group by" in query_lower,  # Complex aggregations
            "cross join" in query_lower,  # Cartesian products
            "window" in query_lower or "over(" in query_lower,  # Window functions
            sql_query.count("join") > 2,  # Multiple joins
            "statistical" in state.get("natural_language_query", "").lower(),
            "significance" in state.get("natural_language_query", "").lower(),
            "diversity" in state.get("natural_language_query", "").lower(),
        ]
        
        # Use file approach if query suggests large results or complex analysis
        if any(large_dataset_indicators):
            use_file_approach = True
            logger.info("👨‍💻 DATA TEAM: Using file-based execution for potentially large/complex results")
        
        if use_file_approach:
            # Generate a meaningful description for the saved file
            query_description = state.get("natural_language_query", "data_analysis")
            if len(query_description) > 100:
                query_description = query_description[:100] + "..."
            
            execution_result = execute_sql_query_and_save.invoke({
                "query": sql_query,
                "description": query_description
            })
        else:
            # Use regular execution for smaller expected results
            logger.info("👨‍💻 DATA TEAM: Using standard execution for smaller expected results")
            execution_result = execute_sql_query.invoke({"query": sql_query})
        
        logger.info("👨‍💻 DATA TEAM: Execution result obtained.")
        return {"execution_result": execution_result}
    except Exception as e:
        logger.error(f"👨‍💻 DATA TEAM: Error executing SQL: {e}")
        return {"error_message": f"Failed during SQL execution: {str(e)}"}

def handle_error_node(state: DataTeamState) -> Dict[str, Any]:
    """Handles errors encountered during the process."""
    error_msg = state.get('error_message', "An unspecified error occurred.")
    logger.warning(f"👨‍💻 DATA TEAM: Handling error: {error_msg}")
    return {"error_message": error_msg}

def format_final_response_node(state: DataTeamState, llm_client: Any) -> Dict[str, Any]:
    """Formats the final response message using LLM-powered formatting for better presentation."""
    logger.info("👨‍💻 DATA TEAM: Formatting final response with LLM...")
    
    error_message = state.get("error_message")
    execution_result = state.get("execution_result")
    provided_schema_text = state.get("provided_schema_text")
    query = state.get("natural_language_query", "your query")
    generated_sql = state.get("generated_sql", "")
    
    # Determine query type for the formatter
    if provided_schema_text:
        query_type = "schema_request"
        raw_results = provided_schema_text
    elif error_message:
        query_type = "error"
        raw_results = ""
    elif execution_result:
        query_type = "data_query"
        raw_results = execution_result
    else:
        query_type = "validation_failure"
        raw_results = f"Validation feedback: {state.get('validation_feedback', 'No specific feedback available.')}"
    
    # Prepare template variables for response formatting
    template_vars = {
        "USER_QUERY": query,
        "QUERY_TYPE": query_type,
        "RAW_RESULTS": raw_results,
        "GENERATED_SQL": generated_sql,
        "ERROR_MESSAGE": error_message or ""
    }
    
    # Generate the formatting prompt using the workflow template
    try:
        formatting_prompt = apply_workflow_prompt_template(
            "data_analyst", 
            "response_formatter", 
            template_vars
        )
        
        # Use LLM to format the response
        formatted_response = llm_client.invoke([HumanMessage(content=formatting_prompt)])
        final_message_content = formatted_response.content
        logger.info("👨‍💻 DATA TEAM: Response formatted successfully using LLM")
        
    except Exception as e:
        # Fallback to simple formatting if LLM formatting fails
        logger.warning(f"👨‍💻 DATA TEAM: LLM formatting failed, using fallback: {e}")
        if provided_schema_text:
            final_message_content = f"Here is the database schema you requested:\n\n{provided_schema_text}"
        elif error_message:
            final_message_content = f"I encountered an error while processing '{query}': {error_message}"
        elif execution_result:
            final_message_content = f"Here are the results for '{query}':\n\n{execution_result}"
        else:
            final_message_content = f"I processed '{query}' but couldn't validate or execute the SQL query. Validation feedback: {state.get('validation_feedback', 'No specific feedback available.')}"

    final_message = AIMessage(content=final_message_content, name="data_analyst")
    
    return {
        "messages": [final_message],
        "natural_language_query": state.get("natural_language_query"),
        "schema": state.get("schema"),
        "generated_sql": state.get("generated_sql"),
        "validation_status": state.get("validation_status"),
        "validation_feedback": state.get("validation_feedback"),
        "execution_result": state.get("execution_result"),
        "error_message": state.get("error_message"),
        "sql_generation_retries": state.get("sql_generation_retries"),
        "provided_schema_text": state.get("provided_schema_text")
    }

# Conditional edge functions
def check_extraction_result(state: DataTeamState) -> str:
    """Checks if schema or SQL was successfully extracted."""
    if state.get("error_message"):
        return "handle_error"
    elif state.get("provided_schema_text"):
        return "format_response"
    elif state.get("generated_sql"):
        return "validate_sql"
    else:
        return "handle_error"

def decide_after_validation(state: DataTeamState) -> str:
    """Decides the next step after SQL validation."""
    if state.get("error_message"):
        return "handle_error"

    validation_status = state.get("validation_status")
    retries = state.get("sql_generation_retries", 0)

    if validation_status == "valid":
        return "execute_sql"
    elif retries < MAX_SQL_RETRIES:
        logger.warning(f"👨‍💻 DATA TEAM: SQL Invalid. Retrying generation (Attempt {retries + 1})")
        return "retry_sql_generation"
    else:
        logger.error(f"👨‍💻 DATA TEAM: SQL Invalid after {MAX_SQL_RETRIES} retries.")
        return "handle_error"

def check_for_errors_before_agent(state: DataTeamState) -> str:
    """Check for errors before proceeding to agent."""
    if state.get("error_message"):
        return "handle_error"
    return "continue_to_agent"

def check_for_errors_after_execution(state: DataTeamState) -> str:
    """Check for errors after SQL execution."""
    if state.get("error_message"):
        return "handle_error"
    return "continue_to_format"

def create_data_team_graph(config=None):
    """Creates and compiles the LangGraph StateGraph for the data team."""
    from ..config.agents import AGENT_LLM_MAP
    from ..agents.llm import get_llm_by_type
    
    # Get the LLM client for the data team
    llm_client = get_llm_by_type(AGENT_LLM_MAP["data_analyst"])
    
    workflow = StateGraph(DataTeamState)

    # Create the ReAct agent for SQL generation with database tools
    # Note: get_database_schema removed since we get it automatically in get_schema_node
    sql_generating_agent = create_react_agent(llm_client, tools=[get_random_subsamples])
    
    # Bind the llm_client to the validation and formatting nodes
    validate_sql_with_llm = partial(sql_validator_node, llm_client=llm_client)
    format_response_with_llm = partial(format_final_response_node, llm_client=llm_client)

    # Add nodes
    workflow.add_node("get_schema", get_schema_node)
    workflow.add_node("prepare_query", prepare_data_query_node)
    workflow.add_node("sql_generating_agent", sql_generating_agent)
    workflow.add_node("extract_schema_or_sql", extract_schema_or_sql_node)
    workflow.add_node("validate_sql", validate_sql_with_llm)
    workflow.add_node("execute_sql", sql_executor_node)
    workflow.add_node("handle_error", handle_error_node)
    workflow.add_node("format_response", format_response_with_llm)

    # Helper node to increment retry counter
    workflow.add_node("increment_retry", lambda state: {
        "sql_generation_retries": state.get("sql_generation_retries", 0) + 1,
        "messages": [],
        "provided_schema_text": None
    })

    # Set entry point
    workflow.set_entry_point("get_schema")

    # Add edges
    workflow.add_edge("get_schema", "prepare_query")
    
    workflow.add_conditional_edges(
        "prepare_query",
        check_for_errors_before_agent,
        {
            "handle_error": "handle_error",
            "continue_to_agent": "sql_generating_agent"
        }
    )

    workflow.add_edge("sql_generating_agent", "extract_schema_or_sql")

    workflow.add_conditional_edges(
        "extract_schema_or_sql",
        check_extraction_result,
        {
            "validate_sql": "validate_sql",
            "format_response": "format_response",
            "handle_error": "handle_error"
        }
    )

    workflow.add_conditional_edges(
        "validate_sql",
        decide_after_validation,
        {
            "execute_sql": "execute_sql",
            "retry_sql_generation": "increment_retry",
            "handle_error": "handle_error",
        },
    )

    workflow.add_edge("increment_retry", "get_schema")

    workflow.add_conditional_edges(
        "execute_sql",
        check_for_errors_after_execution,
        {
            "handle_error": "handle_error",
            "continue_to_format": "format_response"
        }
    )

    workflow.add_edge("handle_error", "format_response")
    workflow.add_edge("format_response", END)

    # Compile the graph
    data_team_app = workflow.compile()
    data_team_app.name = "data_analysis_team"
    logger.info("👨‍💻 DATA TEAM: Compiled data team graph.")
    return data_team_app 