from typing import Literal, Union, List, Tuple
from .llm_providers import PREDEFINED_CONFIGS

# Define available LLM types (for backward compatibility)
LLMType = Literal["basic", "reasoning", "vision"]

# New flexible configuration type
# Can be either:
# - A predefined type (string): "reasoning", "basic", etc.
# - A tuple of [provider, model]: ["openai", "gpt-4o"]
# - A dict with full configuration: {"provider": "openai", "model": "gpt-4o", "temperature": 0.1}
AgentLLMConfig = Union[str, List[str], Tuple[str, str], dict]

# Define agent-LLM mapping with flexible configuration
AGENT_LLM_MAP: dict[str, AgentLLMConfig] = {
    "coordinator": "basic",  # Uses predefined config
    "planner": "reasoning",  # Uses predefined config  
    "supervisor": "basic",  # Uses predefined config
    "researcher": "basic",  # Uses predefined config
    "coder": "basic",  # Custom provider/model
    "browser": "vision",  # Uses predefined config
    "reporter": "basic",  # Uses predefined config
    "data_analyst": "reasoning",  # Uses predefined config
    "biomedical_researcher": "reasoning"  # Uses predefined config
}

def resolve_agent_llm_config(agent_name: str) -> Tuple[str, str]:
    """
    Resolve agent LLM configuration to (provider, model) tuple.
    
    Args:
        agent_name: The name of the agent
        
    Returns:
        Tuple of (provider, model)
        
    Raises:
        ValueError: If agent_name is not found or configuration is invalid
    """
    if agent_name not in AGENT_LLM_MAP:
        raise ValueError(f"Agent '{agent_name}' not found in AGENT_LLM_MAP")
    
    config = AGENT_LLM_MAP[agent_name]
    
    # Handle string (predefined config)
    if isinstance(config, str):
        if config in PREDEFINED_CONFIGS:
            return tuple(PREDEFINED_CONFIGS[config])
        else:
            raise ValueError(f"Predefined config '{config}' not found")
    
    # Handle list/tuple [provider, model]
    elif isinstance(config, (list, tuple)) and len(config) == 2:
        return tuple(config)
    
    # Handle dict configuration
    elif isinstance(config, dict):
        if "provider" in config and "model" in config:
            return (config["provider"], config["model"])
        else:
            raise ValueError(f"Dict configuration must include 'provider' and 'model' keys")
    
    else:
        raise ValueError(f"Invalid configuration format for agent '{agent_name}': {config}")


def get_agent_full_config(agent_name: str) -> dict:
    """
    Get the full configuration dictionary for an agent.
    
    Args:
        agent_name: The name of the agent
        
    Returns:
        Dictionary with full configuration including any extra parameters
    """
    if agent_name not in AGENT_LLM_MAP:
        raise ValueError(f"Agent '{agent_name}' not found in AGENT_LLM_MAP")
    
    config = AGENT_LLM_MAP[agent_name]
    provider, model = resolve_agent_llm_config(agent_name)
    
    base_config = {
        "provider": provider,
        "model": model,
        "temperature": 0.0,  # Default temperature
    }
    
    # If config is a dict, merge additional parameters
    if isinstance(config, dict):
        base_config.update({k: v for k, v in config.items() if k not in ["provider", "model"]})
    
    return base_config


# For backward compatibility - map new flexible configs back to old LLMType
def get_legacy_llm_type(agent_name: str) -> LLMType:
    """
    Get the legacy LLMType for backward compatibility.
    Maps agent configurations to the closest legacy type.
    """
    config = AGENT_LLM_MAP[agent_name]
    
    # Direct mapping for predefined types
    if isinstance(config, str):
        if config == "reasoning":
            return "reasoning"
        elif config == "vision":
            return "vision"
        else:
            return "basic"
    
    # For custom configurations, use heuristics
    provider, model = resolve_agent_llm_config(agent_name)
    
    # Vision models
    if "vision" in model.lower() or "gpt-4o" in model.lower():
        return "vision"
    
    # Reasoning models
    if any(term in model.lower() for term in ["o1", "o3", "o4", "reasoner", "claude-3-5"]):
        return "reasoning"
    
    # Default to basic
    return "basic"
