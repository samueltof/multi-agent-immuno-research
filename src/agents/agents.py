from langgraph.prebuilt import create_react_agent

from src.prompts import apply_prompt_template
from src.tools import (
    bash_tool,
    browser_tool,
    crawl_tool,
    crawl_many_tool,
    # python_sandbox_tool,
    python_repl_tool,
    tavily_tool,
    # execute_sql_query,
    # get_database_schema,
    read_csv_file,
    load_csv_as_dataframe,
    extract_file_paths_from_conversation,
)

from .llm import get_llm_by_type, get_llm_by_agent
from src.config.agents import AGENT_LLM_MAP, get_legacy_llm_type
from .data_team import create_data_team_graph
from .biomedical_researcher import (
    biomedical_researcher_node
)

# Create agents using the new flexible LLM system
# Each agent can now have its own specific provider and model configuration

research_agent = create_react_agent(
    get_llm_by_agent("researcher"),  # Uses new flexible system
    tools=[
        tavily_tool, 
        crawl_tool,
        crawl_many_tool
    ],
    prompt=lambda state: apply_prompt_template("researcher", state),
)

coder_agent = create_react_agent(
    get_llm_by_agent("coder"),  # Now uses Anthropic Claude as configured
    tools=[python_repl_tool, bash_tool, read_csv_file, load_csv_as_dataframe, extract_file_paths_from_conversation],
    prompt=lambda state: apply_prompt_template("coder", state),
)

browser_agent = create_react_agent(
    get_llm_by_agent("browser"),  # Uses configured vision model
    tools=[browser_tool],
    prompt=lambda state: apply_prompt_template("browser", state),
)

# Create the data analyst as a custom workflow agent (lazy initialization)
_data_analyst_workflow = None

def get_data_analyst_workflow():
    """Get data analyst workflow with lazy initialization"""
    global _data_analyst_workflow
    if _data_analyst_workflow is None:
        # Use the new agent-specific LLM system for data analyst
        _data_analyst_workflow = create_data_team_graph(get_llm_by_agent("data_analyst"))
    return _data_analyst_workflow

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
    result = get_data_analyst_workflow().invoke(workflow_input)
    
    # Return the result in the expected format
    return result

# Additional agent-specific functions for easy access

def get_agent_llm(agent_name: str):
    """
    Get the LLM instance for a specific agent.
    This is a convenience function that wraps get_llm_by_agent.
    
    Args:
        agent_name: Name of the agent (e.g., "coder", "researcher")
        
    Returns:
        Configured LLM instance for the agent
    """
    return get_llm_by_agent(agent_name)

def get_agent_config_summary():
    """
    Get a summary of all agent LLM configurations for debugging/monitoring.
    
    Returns:
        Dictionary with agent names and their LLM configurations
    """
    from src.config.agents import resolve_agent_llm_config, get_agent_full_config
    
    summary = {}
    for agent_name in AGENT_LLM_MAP.keys():
        try:
            provider, model = resolve_agent_llm_config(agent_name)
            full_config = get_agent_full_config(agent_name)
            summary[agent_name] = {
                "provider": provider,
                "model": model,
                "temperature": full_config.get("temperature", 0.0),
                "legacy_type": get_legacy_llm_type(agent_name)
            }
        except Exception as e:
            summary[agent_name] = {"error": str(e)}
    
    return summary

# Export the agent instances for external use
__all__ = [
    "research_agent",
    "coder_agent", 
    "browser_agent",
    "data_analyst_agent",
    "biomedical_researcher_node",
    "get_agent_llm",
    "get_agent_config_summary",
]
