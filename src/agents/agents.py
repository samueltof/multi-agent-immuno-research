from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from langgraph.types import Command
from typing import Literal

from src.prompts import apply_prompt_template
from src.tools import (
    bash_tool,
    browser_tool,
    crawl_tool,
    python_repl_tool,
    tavily_tool,
    execute_sql_query,
    get_database_schema,
)

from .llm import get_llm_by_type
from src.config.agents import AGENT_LLM_MAP
from .data_team import create_data_team_graph
from .biomedical_researcher import (
    biomedical_researcher_wrapper
)

# Create agents using configured LLM types
research_agent = create_react_agent(
    get_llm_by_type(AGENT_LLM_MAP["researcher"]),
    tools=[tavily_tool, crawl_tool],
    prompt=lambda state: apply_prompt_template("researcher", state),
)

coder_agent = create_react_agent(
    get_llm_by_type(AGENT_LLM_MAP["coder"]),
    tools=[python_repl_tool, bash_tool],
    prompt=lambda state: apply_prompt_template("coder", state),
)

browser_agent = create_react_agent(
    get_llm_by_type(AGENT_LLM_MAP["browser"]),
    tools=[browser_tool],
    prompt=lambda state: apply_prompt_template("browser", state),
)

# Create the data analyst as a custom workflow agent
data_analyst_workflow = create_data_team_graph(get_llm_by_type(AGENT_LLM_MAP["data_analyst"]))

def data_analyst_agent(state):
    """
    Custom data analyst agent that uses the data team workflow.
    This wraps the complex data analysis workflow in a simple interface.
    """
    # Add the data analyst prompt context to the state
    prompt_state = apply_prompt_template("data_analyst", state)
    
    # Create input state for the data team workflow
    workflow_input = {
        "messages": prompt_state,
        "TEAM_MEMBERS": state.get("TEAM_MEMBERS", []),
        "next": state.get("next", ""),
        "full_plan": state.get("full_plan", ""),
        "deep_thinking_mode": state.get("deep_thinking_mode", False),
        "search_before_planning": state.get("search_before_planning", False),
    }
    
    # Run the data team workflow
    result = data_analyst_workflow.invoke(workflow_input)
    
    # Return the result in the expected format
    return result

# Create TCR-specialized data analyst workflow
from .tcr_data_team import create_tcr_data_team_graph
tcr_data_analyst_workflow = create_tcr_data_team_graph(get_llm_by_type(AGENT_LLM_MAP["data_analyst"]))

def tcr_data_analyst_agent(state):
    """
    Specialized TCR data analyst agent for immunogenomics research.
    This agent is optimized for T-cell receptor analysis using VDJdb and similar databases.
    """
    # Add the TCR data analyst prompt context to the state
    prompt_state = apply_prompt_template("tcr_data_analyst", state)
    
    # Create input state for the TCR data team workflow
    workflow_input = {
        "messages": prompt_state,
        "TEAM_MEMBERS": state.get("TEAM_MEMBERS", []),
        "next": state.get("next", ""),
        "full_plan": state.get("full_plan", ""),
        "deep_thinking_mode": state.get("deep_thinking_mode", False),
        "search_before_planning": state.get("search_before_planning", False),
    }
    
    # Run the TCR data team workflow
    result = tcr_data_analyst_workflow.invoke(workflow_input)
    
    # Return the result in the expected format
    return result

# Biomedical researcher agent (PydanticAI + MCP integration)
def biomedical_researcher_agent(state):
    """
    Biomedical researcher agent that uses PydanticAI with MCP servers.
    This integrates the PydanticAI biomedical researcher with LangGraph.
    """
    import asyncio
    from .biomedical_researcher import biomedical_researcher_node
    
    # Run the biomedical researcher node asynchronously
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result = loop.run_until_complete(biomedical_researcher_node(state))
        
        # Convert the result to LangGraph compatible format
        messages = result.get("messages", [])
        if messages:
            # Get the last message which should be the research summary
            last_message = messages[-1]
            return {
                "messages": [{"role": "assistant", "content": last_message}]
            }
        else:
            # Fallback if no messages in result
            return {
                "messages": [{"role": "assistant", "content": "Biomedical research completed successfully."}]
            }
    finally:
        loop.close()

# Make all agents available for import
__all__ = [
    "research_agent",
    "coder_agent", 
    "browser_agent",
    "data_analyst_agent",
    "tcr_data_analyst_agent",
    "biomedical_researcher_agent",
]
