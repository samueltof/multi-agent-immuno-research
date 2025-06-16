import logging
import json
from copy import deepcopy
from typing import Literal, Union
from langchain_core.messages import HumanMessage
from langgraph.types import Command
from langgraph.graph import END

from src.agents import research_agent, coder_agent, browser_agent, data_analyst_agent, biomedical_researcher_agent
from src.agents.llm import get_llm_by_type
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
    result = biomedical_researcher_agent(state)
    logger.info("Biomedical researcher agent completed task")
    
    # Handle the case where result['messages'][-1] is a dict with 'content' key
    last_message = result['messages'][-1]
    if isinstance(last_message, dict):
        message_content = last_message.get('content', str(last_message))
    else:
        message_content = last_message.content if hasattr(last_message, 'content') else str(last_message)
    
    logger.debug(f"Biomedical researcher agent response: {message_content}")
    
    # Extract biomedical research result if available
    biomedical_result = result.get('biomedical_research_result')
    
    update_data = {
        "messages": [
            HumanMessage(
                content=RESPONSE_FORMAT.format(
                    "biomedical_researcher", message_content
                ),
                name="biomedical_researcher",
            )
        ]
    }
    
    # Add biomedical research result to state if available
    if biomedical_result:
        update_data["biomedical_research_result"] = biomedical_result
    
    return Command(
        update=update_data,
        goto="supervisor",
    )


def supervisor_node(state: State) -> Command[Union[Literal["researcher"], Literal["coder"], Literal["browser"], Literal["reporter"], Literal["data_analyst"], Literal["biomedical_researcher"], Literal["__end__"]]]:
    """Supervisor node that decides which agent should act next."""
    logger.info("Supervisor evaluating next action")
    messages = apply_prompt_template("supervisor", state)
    response = (
        get_llm_by_type(AGENT_LLM_MAP["supervisor"])
        .with_structured_output(Router)
        .invoke(messages)
    )
    goto = response["next"]
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
    # whether to enable deep thinking mode
    llm = get_llm_by_type("basic")
    if state.get("deep_thinking_mode"):
        llm = get_llm_by_type("reasoning")
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
    json_end = cleaned_response.rfind('}')
    
    if json_start != -1 and json_end != -1 and json_end > json_start:
        # Extract just the JSON part
        potential_json = cleaned_response[json_start:json_end + 1]
        # If this looks more like pure JSON, use it instead
        if len(potential_json) < len(cleaned_response) * 0.8:  # JSON is less than 80% of total
            logger.debug(f"Extracted JSON from response: {potential_json}")
            cleaned_response = potential_json

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
        logger.debug(f"Invalid JSON response: {cleaned_response}")
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
    response = get_llm_by_type(AGENT_LLM_MAP["coordinator"]).invoke(messages)
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
    response = get_llm_by_type(AGENT_LLM_MAP["reporter"]).invoke(messages)
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
