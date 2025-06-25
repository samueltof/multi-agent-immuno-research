from typing import Literal

# Define available LLM types
LLMType = Literal["basic", "reasoning", "vision"]

# Define agent-LLM mapping
AGENT_LLM_MAP: dict[str, LLMType] = {
    "coordinator": "basic", 
    "planner": "reasoning", 
    "supervisor": "basic", 
    "researcher": "basic", 
    "coder": "reasoning", 
    "browser": "vision", 
    "reporter": "basic", 
    "data_analyst": "reasoning",
    "biomedical_researcher": "reasoning"  # New biomedical agent using reasoning model
}
