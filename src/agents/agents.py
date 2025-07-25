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

from .llm import get_llm_by_type
from src.config.agents import AGENT_LLM_MAP
from .data_team import create_data_team_graph
from .biomedical_researcher import (
    biomedical_researcher_node
)

# Create agents using configured LLM types
research_agent = create_react_agent(
    get_llm_by_type(AGENT_LLM_MAP["researcher"]),
    tools=[
        tavily_tool, 
        crawl_tool,
        crawl_many_tool
    ],
    prompt=lambda state: apply_prompt_template("researcher", state),
)

coder_agent = create_react_agent(
    get_llm_by_type(AGENT_LLM_MAP["coder"]),
    tools=[python_repl_tool, bash_tool, read_csv_file, load_csv_as_dataframe, extract_file_paths_from_conversation],
    prompt=lambda state: apply_prompt_template("coder", state),
)

browser_agent = create_react_agent(
    get_llm_by_type(AGENT_LLM_MAP["browser"]),
    tools=[browser_tool],
    prompt=lambda state: apply_prompt_template("browser", state),
)

# Create the data analyst as a custom workflow agent (lazy initialization)
_data_analyst_workflow = None

def get_data_analyst_workflow():
    """Get data analyst workflow with lazy initialization"""
    global _data_analyst_workflow
    if _data_analyst_workflow is None:
        _data_analyst_workflow = create_data_team_graph(get_llm_by_type(AGENT_LLM_MAP["data_analyst"]))
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



# Biomedical researcher agent (PydanticAI + MCP integration)
def biomedical_researcher_agent(state):
    """
    Biomedical researcher agent that uses PydanticAI with MCP servers.
    This integrates the PydanticAI biomedical researcher with LangGraph.
    """
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
            response = {
                "messages": [{"role": "assistant", "content": last_message}]
            }
            
            # Include biomedical research result if available
            if biomedical_result:
                response["biomedical_research_result"] = biomedical_result
                
            return response
        else:
            # Fallback if no messages in result
            response = {
                "messages": [{"role": "assistant", "content": "Biomedical research completed successfully."}]
            }
            
            # Include biomedical research result if available
            if biomedical_result:
                response["biomedical_research_result"] = biomedical_result
                
            return response
    finally:
        loop.close()

# Make all agents available for import
__all__ = [
    "research_agent",
    "coder_agent", 
    "browser_agent",
    "data_analyst_agent",
    "biomedical_researcher_agent",
]
