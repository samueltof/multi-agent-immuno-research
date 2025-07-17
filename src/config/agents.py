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
    "coordinator": ["openai", "gpt-4o-mini"],
    "planner": ["openai", "o3-mini"],
    "supervisor": ["openai", "gpt-4o-mini"],
    "researcher": ["openai", "gpt-4o-mini"],
    "coder": ["openai", "gpt-4o-mini"],
    "browser": ["openai", "gpt-4o"],
    "reporter": ["openai", "gpt-4o-mini"],
    "data_analyst": ["openai", "o3-mini"],
    "biomedical_researcher": ["openai", "gpt-4o-mini"]  # Using Portkey for biomedical researcher
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
    from .llm_providers import ProviderType
    import os
    
    if agent_name not in AGENT_LLM_MAP:
        raise ValueError(f"Agent '{agent_name}' not found in AGENT_LLM_MAP")
    
    config = AGENT_LLM_MAP[agent_name]
    provider, model = resolve_agent_llm_config(agent_name)
    
    base_config = {
        "provider": provider,
        "model": model,
        "temperature": 0.0,  # Default temperature
    }
    
    # Add provider-specific configuration
    if provider == ProviderType.OPENAI:
        base_config.update({
            "api_key": os.getenv("OPENAI_API_KEY"),
            "base_url": os.getenv("OPENAI_BASE_URL"),
        })
    elif provider == ProviderType.ANTHROPIC:
        base_config.update({
            "api_key": os.getenv("ANTHROPIC_API_KEY"),
        })
    elif provider == ProviderType.PORTKEY_OPENAI:
        base_config.update({
            "portkey_api_key": os.getenv("PORTKEY_API_KEY"),
            "virtual_key": os.getenv("PORTKEY_OPENAI_VIRTUAL_KEY", "@openai"),
            "portkey_base_url": os.getenv("PORTKEY_BASE_URL", "https://api.portkey.ai/v1"),
        })
    elif provider == ProviderType.PORTKEY_ANTHROPIC:
        base_config.update({
            "portkey_api_key": os.getenv("PORTKEY_API_KEY"),
            "virtual_key": os.getenv("PORTKEY_ANTHROPIC_VIRTUAL_KEY", "@anthropic"),
            "portkey_base_url": os.getenv("PORTKEY_BASE_URL", "https://api.portkey.ai/v1"),
        })
    elif provider == ProviderType.PORTKEY_BEDROCK:
        base_config.update({
            "portkey_api_key": os.getenv("PORTKEY_API_KEY"),
            "virtual_key": os.getenv("PORTKEY_BEDROCK_VIRTUAL_KEY", "@bedrock"),
            "portkey_base_url": os.getenv("PORTKEY_BASE_URL", "https://api.portkey.ai/v1"),
        })
    elif provider == ProviderType.PORTKEY_AZURE:
        base_config.update({
            "portkey_api_key": os.getenv("PORTKEY_API_KEY"),
            "virtual_key": os.getenv("PORTKEY_AZURE_VIRTUAL_KEY", "@azure"),
            "portkey_base_url": os.getenv("PORTKEY_BASE_URL", "https://api.portkey.ai/v1"),
        })
    elif provider == ProviderType.DEEPSEEK:
        base_config.update({
            "api_key": os.getenv("DEEPSEEK_API_KEY"),
            "base_url": os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
        })
    elif provider == ProviderType.AZURE:
        base_config.update({
            "api_key": os.getenv("AZURE_OPENAI_API_KEY"),
            "azure_endpoint": os.getenv("AZURE_OPENAI_ENDPOINT"),
            "api_version": os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
        })
    elif provider == ProviderType.BEDROCK:
        base_config.update({
            "region": os.getenv("AWS_REGION", "us-east-1"),
        })
    
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
