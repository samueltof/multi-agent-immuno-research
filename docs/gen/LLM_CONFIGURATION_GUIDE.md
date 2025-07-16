# LLM Configuration Guide

This guide explains the new modular LLM configuration system that allows you to specify different providers and models for each agent in the system.

## Overview

The new system supports:
- **Multiple providers**: OpenAI, Anthropic, DeepSeek, AWS Bedrock, Azure OpenAI, Portkey
- **Flexible configuration**: Per-agent customization with provider-specific settings
- **Backward compatibility**: Existing configurations continue to work
- **Predefined configurations**: Common setups for easy reuse

## Configuration Formats

### 1. Predefined Configurations (Recommended)

Use predefined configuration names for common setups:

```python
AGENT_LLM_MAP = {
    "coordinator": "basic",        # Uses OpenAI gpt-4o-mini
    "researcher": "reasoning",     # Uses OpenAI o3-mini
    "browser": "vision",          # Uses OpenAI gpt-4o
}
```

Available predefined configurations:
- `"reasoning"`: `["openai", "o3-mini"]`
- `"basic"`: `["openai", "gpt-4o-mini"]`
- `"vision"`: `["openai", "gpt-4o"]`
- `"fast"`: `["openai", "gpt-4o-mini"]`
- `"powerful"`: `["openai", "o3-mini"]`
- `"anthropic_reasoning"`: `["anthropic", "claude-3-5-sonnet-20241022"]`
- `"anthropic_basic"`: `["anthropic", "claude-3-haiku-20240307"]`
- `"portkey_anthropic_reasoning"`: `["portkey_anthropic", "claude-3-5-sonnet-20241022"]`
- `"portkey_anthropic_basic"`: `["portkey_anthropic", "claude-3-haiku-20240307"]`
- `"deepseek_reasoning"`: `["deepseek", "deepseek-reasoner"]`
- `"deepseek_basic"`: `["deepseek", "deepseek-chat"]`

### 2. Provider and Model Specification

Specify provider and model directly:

```python
AGENT_LLM_MAP = {
    "coder": ["anthropic", "claude-3-5-sonnet-20241022"],
    "data_analyst": ["openai", "o3-mini"],
    "reporter": ["deepseek", "deepseek-chat"],
}
```

### 3. Full Configuration Dictionary

For maximum control, use a dictionary with all parameters:

```python
AGENT_LLM_MAP = {
    "coder": {
        "provider": "anthropic",
        "model": "claude-3-5-sonnet-20241022",
        "temperature": 0.1,
        "max_tokens": 4000,
    },
    "researcher": {
        "provider": "openai", 
        "model": "gpt-4o",
        "temperature": 0.0,
        "base_url": "https://api.openai.com/v1",  # Custom endpoint
        "api_key": "custom-key",  # Override default API key
    }
}
```

## Supported Providers

### OpenAI
```python
{
    "provider": "openai",
    "model": "gpt-4o",
    "api_key": "your-openai-key",     # Optional, uses OPENAI_API_KEY env var
    "base_url": "custom-url",         # Optional, uses OPENAI_BASE_URL env var
    "temperature": 0.0,
    "max_tokens": 4000,
}
```

### Anthropic
```python
{
    "provider": "anthropic",
    "model": "claude-3-5-sonnet-20241022",
    "api_key": "your-anthropic-key",  # Optional, uses ANTHROPIC_API_KEY env var
    "temperature": 0.0,
    "max_tokens": 4000,
}
```

### DeepSeek
```python
{
    "provider": "deepseek",
    "model": "deepseek-reasoner",
    "api_key": "your-deepseek-key",   # Optional, uses DEEPSEEK_API_KEY env var
    "base_url": "https://api.deepseek.com",  # Optional, uses DEEPSEEK_BASE_URL env var
    "temperature": 0.0,
}
```

### AWS Bedrock
```python
{
    "provider": "bedrock",
    "model": "anthropic.claude-3-5-sonnet-20241022-v2:0",
    "region": "us-east-1",            # Optional, uses AWS_REGION env var
    "temperature": 0.0,
}
```

### Azure OpenAI
```python
{
    "provider": "azure",
    "model": "gpt-4o",                # Deployment name
    "api_key": "your-azure-key",      # Optional, uses AZURE_OPENAI_API_KEY env var
    "azure_endpoint": "your-endpoint", # Optional, uses AZURE_OPENAI_ENDPOINT env var
    "api_version": "2024-02-15-preview", # Optional, uses AZURE_OPENAI_API_VERSION env var
    "temperature": 0.0,
}
```

### Portkey (LLM Gateway)

Portkey with OpenAI backend:
```python
{
    "provider": "portkey_openai",
    "model": "gpt-4o",
    "virtual_key": "your-virtual-key", # Uses PORTKEY_OPENAI_VIRTUAL_KEY env var
    "portkey_api_key": "your-portkey-key", # Uses PORTKEY_API_KEY env var
    "temperature": 0.0,
}
```

Portkey with Bedrock backend:
```python
{
    "provider": "portkey_bedrock", 
    "model": "anthropic.claude-3-5-sonnet-20240620-v1:0",
    "virtual_key": "your-virtual-key", # Uses PORTKEY_BEDROCK_VIRTUAL_KEY env var
    "portkey_api_key": "your-portkey-key", # Uses PORTKEY_API_KEY env var
    "temperature": 0.0,
}
```

## Environment Variables

### Required API Keys
```bash
# OpenAI
OPENAI_API_KEY=your_openai_api_key
OPENAI_BASE_URL=https://api.openai.com/v1  # Optional

# Anthropic
ANTHROPIC_API_KEY=your_anthropic_api_key

# DeepSeek
DEEPSEEK_API_KEY=your_deepseek_api_key
DEEPSEEK_BASE_URL=https://api.deepseek.com  # Optional

# AWS Bedrock
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key

# Azure OpenAI
AZURE_OPENAI_API_KEY=your_azure_api_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# Portkey
PORTKEY_API_KEY=your_portkey_api_key
PORTKEY_BASE_URL=https://api.portkey.ai/v1
PORTKEY_OPENAI_VIRTUAL_KEY=your_openai_virtual_key
PORTKEY_BEDROCK_VIRTUAL_KEY=your_bedrock_virtual_key
PORTKEY_AZURE_VIRTUAL_KEY=your_azure_virtual_key
```

### Legacy Environment Variables (Still Supported)
```bash
# For backward compatibility
REASONING_PROVIDER=openai
REASONING_MODEL=o3-mini
REASONING_API_KEY=your_reasoning_api_key
REASONING_BASE_URL=https://api.openai.com/v1

BASIC_MODEL=gpt-4o-mini
BASIC_API_KEY=your_basic_api_key
BASIC_BASE_URL=https://api.openai.com/v1

VL_MODEL=gpt-4o
VL_API_KEY=your_vision_api_key
VL_BASE_URL=https://api.openai.com/v1
```

## Usage Examples

### Basic Setup with Mixed Providers

```python
# src/config/agents.py
AGENT_LLM_MAP = {
    "coordinator": "basic",                                    # OpenAI gpt-4o-mini
    "planner": "reasoning",                                    # OpenAI o3-mini
    "supervisor": "basic",                                     # OpenAI gpt-4o-mini
    "researcher": "basic",                                     # OpenAI gpt-4o-mini
    "coder": ["anthropic", "claude-3-5-sonnet-20241022"],    # Anthropic Claude
    "browser": "vision",                                       # OpenAI gpt-4o
    "reporter": ["deepseek", "deepseek-chat"],               # DeepSeek
    "data_analyst": "reasoning",                               # OpenAI o3-mini
    "biomedical_researcher": "anthropic_reasoning"             # Anthropic Claude
}
```

### Advanced Setup with Custom Configuration

```python
AGENT_LLM_MAP = {
    "coordinator": "basic",
    "planner": {
        "provider": "openai",
        "model": "o3-mini",
        "temperature": 0.2,  # Higher temperature for creative planning
    },
    "supervisor": "basic",
    "researcher": {
        "provider": "anthropic",
        "model": "claude-3-5-sonnet-20241022",
        "temperature": 0.0,
        "max_tokens": 8000,  # Longer responses for research
    },
    "coder": {
        "provider": "deepseek",
        "model": "deepseek-coder",
        "temperature": 0.0,
    },
    "browser": "vision",
    "reporter": {
        "provider": "anthropic",
        "model": "claude-3-haiku-20240307",  # Faster, cheaper for reports
        "temperature": 0.1,
    },
    "data_analyst": "reasoning",
    "biomedical_researcher": {
        "provider": "portkey_openai",
        "model": "gpt-4o",
        "virtual_key": "biomedical-key",
        "temperature": 0.0,
    }
}
```

## Adding New Predefined Configurations

To add new predefined configurations, edit `src/config/llm_providers.py`:

```python
PREDEFINED_CONFIGS = {
    # Existing configs...
    "claude_fast": ["anthropic", "claude-3-haiku-20240307"],
    "openai_latest": ["openai", "gpt-4o"],
    "azure_reasoning": ["azure", "gpt-4o-deployment-name"],
    "bedrock_claude": ["bedrock", "anthropic.claude-3-5-sonnet-20241022-v2:0"],
}
```

## Testing the Configuration

Run the test script to validate your configuration:

```bash
python tests/test_llm_configuration.py
```

This will:
- Validate all agent configurations
- Test predefined configurations  
- Create LLM instances (without API calls)
- Show configuration summaries

## Using the New System in Code

### Get an agent's LLM
```python
from src.agents.llm import get_llm_by_agent

# Get the configured LLM for the coder agent
coder_llm = get_llm_by_agent("coder")
response = coder_llm.invoke("Write a hello world function")
```

### Get configuration summary
```python
from src.agents.agents import get_agent_config_summary

summary = get_agent_config_summary()
for agent, config in summary.items():
    print(f"{agent}: {config['provider']} / {config['model']}")
```

### Backward compatibility
```python
from src.agents.llm import get_llm_by_type

# Still works with legacy types
reasoning_llm = get_llm_by_type("reasoning")
basic_llm = get_llm_by_type("basic")
vision_llm = get_llm_by_type("vision")
```

## Migration Guide

### From Legacy Configuration

**Old way:**
```python
AGENT_LLM_MAP = {
    "coder": "reasoning",  # Uses REASONING_* env vars
}
```

**New way (equivalent):**
```python
AGENT_LLM_MAP = {
    "coder": "reasoning",  # Still works, uses predefined config
    # OR
    "coder": ["openai", "o3-mini"],  # Direct specification
    # OR 
    "coder": {
        "provider": "openai",
        "model": "o3-mini",
        "temperature": 0.0,
    }
}
```

### Adding New Providers

To add support for a new provider:

1. Add provider enum to `src/config/llm_providers.py`:
```python
class ProviderType(str, Enum):
    # Existing providers...
    NEW_PROVIDER = "new_provider"
```

2. Create configuration class:
```python
class NewProviderConfig(LLMProviderConfig):
    provider: ProviderType = ProviderType.NEW_PROVIDER
    api_key: Optional[str] = Field(default_factory=lambda: os.getenv("NEW_PROVIDER_API_KEY"))
```

3. Add to factory functions and LLM creation logic.

## Best Practices

1. **Use predefined configurations** for common setups
2. **Group similar agents** with the same provider for cost efficiency
3. **Use appropriate models** for each task (e.g., vision models for image processing)
4. **Set temperature to 0.0** for deterministic tasks like coding
5. **Use environment variables** for API keys, never hardcode them
6. **Test configurations** before deploying to production
7. **Monitor costs** when using multiple premium providers

## Troubleshooting

### Common Issues

1. **Missing API keys**: Ensure all required environment variables are set
2. **Invalid model names**: Check provider documentation for correct model names
3. **Rate limits**: Consider using different providers or models for high-volume agents
4. **Authentication errors**: Verify API keys and endpoint URLs
5. **Import errors**: Ensure all required packages are installed (`uv add` for new providers)

### Debug Configuration

```python
from src.agents.agents import get_agent_config_summary

# Print all agent configurations
summary = get_agent_config_summary()
print(json.dumps(summary, indent=2))
```

### Clear LLM Cache

```python
from src.agents.llm import clear_llm_cache

# Clear cached LLM instances (useful during development)
clear_llm_cache()
```

## Additional Setup Guides

- **[Portkey Anthropic Setup](../PORTKEY_ANTHROPIC_SETUP.md)**: Detailed guide for configuring Portkey as an AI gateway for Anthropic Claude models 