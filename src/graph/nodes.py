import logging
import json
from copy import deepcopy
from typing import Literal, Union
from langchain_core.messages import HumanMessage
from langgraph.types import Command
from langgraph.graph import END

from src.agents import research_agent, coder_agent, browser_agent, data_analyst_agent
from src.agents.biomedical_researcher import biomedical_researcher_node
from src.agents.llm import get_llm_by_type, get_llm_by_agent
from src.config import TEAM_MEMBERS
from src.config.agents import AGENT_LLM_MAP
from src.prompts.template import apply_prompt_template
from src.tools.search import tavily_tool
from .types import State, Router

logger = logging.getLogger(__name__)

RESPONSE_FORMAT = "Response from {}:\n\n<response>\n{}\n</response>\n\n*Please execute the next step.*"


def research_node(state: State) -> Command[Literal["supervisor"]]:
    """Node for the researcher agent that performs research tasks."""
    logger.info("Research agent starting task")
    result = research_agent.invoke(state)
    logger.info("Research agent completed task")
    logger.debug(f"Research agent response: {result['messages'][-1].content}")
    return Command(
        update={
            "messages": [
                HumanMessage(
                    content=RESPONSE_FORMAT.format(
                        "researcher", result["messages"][-1].content
                    ),
                    name="researcher",
                )
            ]
        },
        goto="supervisor",
    )


def code_node(state: State) -> Command[Literal["supervisor"]]:
    """Node for the coder agent that executes Python code."""
    logger.info("Code agent starting task")
    result = coder_agent.invoke(state)
    logger.info("Code agent completed task")
    logger.debug(f"Code agent response: {result['messages'][-1].content}")
    return Command(
        update={
            "messages": [
                HumanMessage(
                    content=RESPONSE_FORMAT.format(
                        "coder", result["messages"][-1].content
                    ),
                    name="coder",
                )
            ]
        },
        goto="supervisor",
    )


def browser_node(state: State) -> Command[Literal["supervisor"]]:
    """Node for the browser agent that performs web browsing tasks."""
    logger.info("Browser agent starting task")
    result = browser_agent.invoke(state)
    logger.info("Browser agent completed task")
    logger.debug(f"Browser agent response: {result['messages'][-1].content}")
    return Command(
        update={
            "messages": [
                HumanMessage(
                    content=RESPONSE_FORMAT.format(
                        "browser", result["messages"][-1].content
                    ),
                    name="browser",
                )
            ]
        },
        goto="supervisor",
    )


def data_analyst_node(state: State) -> Command[Literal["supervisor"]]:
    """Node for the data analyst agent that performs SQL queries and database analysis."""
    logger.info("Data analyst agent starting task")
    result = data_analyst_agent(state)
    logger.info("Data analyst agent completed task")
    logger.debug(f"Data analyst agent response: {result['messages'][-1].content}")
    return Command(
        update={
            "messages": [
                HumanMessage(
                    content=RESPONSE_FORMAT.format(
                        "data_analyst", result["messages"][-1].content
                    ),
                    name="data_analyst",
                )
            ]
        },
        goto="supervisor",
    )


def biomedical_researcher_graph_node(state: State) -> Command[Literal["supervisor"]]:
    """Node for the biomedical researcher agent that performs biomedical research using PydanticAI and MCP."""
    logger.info("Biomedical researcher agent starting task")
    
    # Use the biomedical_researcher_node directly (it's an async function that we need to handle)
    import asyncio
    
    # Run the biomedical researcher node asynchronously
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result = loop.run_until_complete(biomedical_researcher_node(state))
        
        # Convert the result to LangGraph compatible format
        messages = result.get("messages", [])
        biomedical_result = result.get("biomedical_research_result")
        
        if messages:
            # Get the last message which should be the research summary
            last_message = messages[-1]
            if isinstance(last_message, dict):
                message_content = last_message.get('content', str(last_message))
            else:
                message_content = last_message.content if hasattr(last_message, 'content') else str(last_message)
            
            response = {
                "messages": [
                    HumanMessage(
                        content=RESPONSE_FORMAT.format(
                            "biomedical_researcher", message_content
                        ),
                        name="biomedical_researcher",
                    )
                ]
            }
            
            # Include biomedical research result if available
            if biomedical_result:
                response["biomedical_research_result"] = biomedical_result
                
        else:
            # Fallback if no messages in result
            response = {
                "messages": [
                    HumanMessage(
                        content=RESPONSE_FORMAT.format(
                            "biomedical_researcher", "Biomedical research completed successfully."
                        ),
                        name="biomedical_researcher",
                    )
                ]
            }
            
            # Include biomedical research result if available
            if biomedical_result:
                response["biomedical_research_result"] = biomedical_result
                
        logger.info("Biomedical researcher agent completed task")
        logger.debug(f"Biomedical researcher agent response: {message_content if 'message_content' in locals() else 'No content'}")
        
        return Command(
            update=response,
            goto="supervisor",
        )
    finally:
        loop.close()


def supervisor_node(state: State) -> Command[Union[Literal["researcher"], Literal["coder"], Literal["reporter"], Literal["data_analyst"], Literal["biomedical_researcher"], Literal["__end__"]]]:
    """Supervisor node that decides which agent should act next."""
    logger.info("Supervisor evaluating next action")
    deep_thinking_mode = state.get("deep_thinking_mode", False)
    
    messages = apply_prompt_template("supervisor", state)
    response = (
        get_llm_by_agent("supervisor")  # Use new agent-specific LLM system
        .with_structured_output(Router)
        .invoke(messages)
    )
    goto = response["next"]
    
    if deep_thinking_mode:
        reasoning = response.get("reasoning", "No reasoning provided")
        logger.info(f"🧠 Deep Thinking Mode - Supervisor reasoning: {reasoning}")
    else:
        logger.info("🎯 Standard Mode - Basic supervisor routing")
    
    logger.debug(f"Current state messages: {state['messages']}")
    logger.debug(f"Supervisor response: {response}")

    if goto == "FINISH":
        goto = "__end__"
        logger.info("Workflow completed")
    else:
        logger.info(f"Supervisor delegating to: {goto}")

    return Command(goto=goto, update={"next": goto})


def planner_node(state: State) -> Command[Literal["supervisor", "__end__"]]:
    """Planner node that generate the full plan."""
    logger.info("Planner generating full plan")
    messages = apply_prompt_template("planner", state)
    # Use the agent-specific LLM for planner
    llm = get_llm_by_agent("planner")
    if state.get("search_before_planning"):
        searched_content = tavily_tool.invoke({"query": state["messages"][-1].content})
        messages = deepcopy(messages)
        messages[
            -1
        ].content += f"\n\n# Relative Search Results\n\n{json.dumps([{'titile': elem['title'], 'content': elem['content']} for elem in searched_content], ensure_ascii=False)}"
    stream = llm.stream(messages)
    full_response = ""
    for chunk in stream:
        full_response += chunk.content
    logger.debug(f"Current state messages: {state['messages']}")
    logger.debug(f"Planner response: {full_response}")

    # Clean up the response - strip whitespace and code block markers
    cleaned_response = full_response.strip()
    
    # More robust code block removal
    if cleaned_response.startswith("```json"):
        cleaned_response = cleaned_response.removeprefix("```json").strip()
    elif cleaned_response.startswith("```"):
        cleaned_response = cleaned_response.removeprefix("```").strip()

    if cleaned_response.endswith("```"):
        cleaned_response = cleaned_response.removesuffix("```").strip()

    # Try to extract JSON from the response if it contains extra text
    json_start = cleaned_response.find('{')
    
    if json_start != -1:
        # Try to find the end of the first complete JSON object
        # by counting braces from the start
        brace_count = 0
        json_end = -1
        
        for i in range(json_start, len(cleaned_response)):
            char = cleaned_response[i]
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    json_end = i
                    break
        
        if json_end != -1:
            # Extract the first complete JSON object
            potential_json = cleaned_response[json_start:json_end + 1]
            
            # Try parsing the extracted JSON
            try:
                json.loads(potential_json)
                # If parsing succeeds, use the extracted JSON
                logger.debug(f"Successfully extracted JSON from response: {potential_json}")
                cleaned_response = potential_json
            except json.JSONDecodeError:
                # If extracted JSON is invalid, try the full response
                logger.debug("Extracted JSON failed to parse, using full response")
                pass

    goto = "supervisor"
    try:
        # Validate JSON structure
        parsed_json = json.loads(cleaned_response)
        
        # Validate required fields for Plan interface
        required_fields = ["thought", "title", "steps"]
        missing_fields = [field for field in required_fields if field not in parsed_json]
        
        if missing_fields:
            logger.warning(f"Planner response missing required fields: {missing_fields}")
            logger.debug(f"Invalid plan structure: {cleaned_response}")
            goto = "__end__"
        else:
            # Validate steps structure
            if not isinstance(parsed_json["steps"], list):
                logger.warning("Planner response 'steps' field is not a list")
                goto = "__end__"
            else:
                # Validate each step has required fields
                for i, step in enumerate(parsed_json["steps"]):
                    step_required_fields = ["agent_name", "title", "description"]
                    step_missing_fields = [field for field in step_required_fields if field not in step]
                    if step_missing_fields:
                        logger.warning(f"Step {i} missing required fields: {step_missing_fields}")
                        goto = "__end__"
                        break
                        
    except json.JSONDecodeError as e:
        logger.warning(f"Planner response is not valid JSON: {str(e)}")
        logger.warning(f"Error at position {e.pos}: {cleaned_response[max(0, e.pos-20):e.pos+20]}")
        logger.debug(f"Full invalid JSON response: {cleaned_response}")
        
        # Try one more time with more aggressive cleaning
        # Remove any trailing content after the last }
        if '}' in cleaned_response:
            last_brace = cleaned_response.rfind('}')
            retry_json = cleaned_response[:last_brace + 1]
            try:
                json.loads(retry_json)
                logger.info("Successfully recovered JSON by removing trailing content")
                cleaned_response = retry_json
                goto = "supervisor"  # Continue with recovered JSON
            except json.JSONDecodeError:
                logger.warning("JSON recovery attempt failed")
                goto = "__end__"
        else:
            goto = "__end__"
    except Exception as e:
        logger.error(f"Unexpected error validating planner response: {str(e)}")
        goto = "__end__"

    return Command(
        update={
            "messages": [HumanMessage(content=cleaned_response, name="planner")],
            "full_plan": cleaned_response,
        },
        goto=goto,
    )


def coordinator_node(state: State) -> Command[Literal["planner", "__end__"]]:
    """Coordinator node that communicate with customers."""
    logger.info("Coordinator talking.")
    messages = apply_prompt_template("coordinator", state)
    response = get_llm_by_agent("coordinator").invoke(messages)  # Use new agent-specific LLM system
    logger.debug(f"Current state messages: {state['messages']}")
    logger.debug(f"reporter response: {response}")

    goto = "__end__"
    if "handoff_to_planner" in response.content:
        goto = "planner"

    return Command(
        goto=goto,
    )


def reporter_node(state: State) -> Command[Literal["supervisor"]]:
    """Reporter node that write a final report."""
    logger.info("Reporter write final report")
    messages = apply_prompt_template("reporter", state)
    response = get_llm_by_agent("reporter").invoke(messages)  # Use new agent-specific LLM system
    logger.debug(f"Current state messages: {state['messages']}")
    logger.debug(f"reporter response: {response}")

    return Command(
        update={
            "messages": [
                HumanMessage(
                    content=RESPONSE_FORMAT.format("reporter", response.content),
                    name="reporter",
                )
            ]
        },
        goto="supervisor",
    )
