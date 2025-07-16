# Portkey Anthropic Configuration Guide

This guide explains how to use Portkey as an LLM gateway to access Anthropic's Claude models in your multi-agent system.

## What is Portkey?

[Portkey](https://portkey.ai/) is an AI Gateway that provides:
- **Unified API**: Single interface for multiple LLM providers
- **Monitoring & Analytics**: Track usage, costs, and performance
- **Rate Limiting**: Control API usage and costs
- **Fallback & Load Balancing**: Ensure reliability across providers
- **Caching**: Reduce costs with intelligent response caching

## Setup Instructions

### 1. Environment Variables

Add these environment variables to your `.env` file:

```bash
# Portkey Configuration
PORTKEY_API_KEY="your_portkey_api_key"
PORTKEY_ANTHROPIC_VIRTUAL_KEY="your_anthropic_virtual_key"

# Optional: Custom Portkey endpoint
PORTKEY_BASE_URL="https://api.portkey.ai/v1"  # Default value
```

### 2. Getting Your Keys

1. **Portkey API Key**: 
   - Sign up at [portkey.ai](https://portkey.ai/)
   - Generate an API key from your dashboard

2. **Anthropic Virtual Key**:
   - In your Portkey dashboard, create a virtual key
   - Configure it to use Anthropic as the provider
   - Add your Anthropic API key to the virtual key configuration

### 3. Agent Configuration

You can configure agents to use Portkey Anthropic in several ways:

#### Option 1: Predefined Configurations

```python
# In src/config/agents.py
AGENT_LLM_MAP = {
    "research_agent": "portkey_anthropic_reasoning",  # Claude 3.5 Sonnet
    "summary_agent": "portkey_anthropic_basic",       # Claude 3 Haiku
}
```

#### Option 2: Direct Provider/Model Specification

```python
AGENT_LLM_MAP = {
    "analysis_agent": ["portkey_anthropic", "claude-3-5-sonnet-20241022"],
    "chat_agent": ["portkey_anthropic", "claude-3-haiku-20240307"],
}
```

#### Option 3: Full Configuration with Custom Parameters

```python
AGENT_LLM_MAP = {
    "creative_agent": {
        "provider": "portkey_anthropic",
        "model": "claude-3-5-sonnet-20241022",
        "temperature": 0.8,
        "max_tokens": 4000,
        "extra_kwargs": {
            "top_p": 0.9,
            "stop_sequences": ["Human:", "Assistant:"]
        }
    }
}
```

## Available Models

The configuration supports all Anthropic Claude models available through Portkey:

### Claude 3.5 Sonnet
- `claude-3-5-sonnet-20241022` (Latest)
- Best for complex reasoning, analysis, and creative tasks

### Claude 3 Haiku
- `claude-3-haiku-20240307`
- Fast and cost-effective for simple tasks

### Claude 3 Opus
- `claude-3-opus-20240229`
- Most capable model for complex tasks (higher cost)

## Predefined Configurations

The following predefined configurations are available:

| Configuration | Provider | Model | Use Case |
|---------------|----------|-------|----------|
| `portkey_anthropic_reasoning` | portkey_anthropic | claude-3-5-sonnet-20241022 | Complex reasoning tasks |
| `portkey_anthropic_basic` | portkey_anthropic | claude-3-haiku-20240307 | Simple, fast tasks |

## Testing Your Setup

Run the demo script to verify your configuration:

```bash
uv run python tests/test_portkey_anthropic_demo.py
```

This will test all configuration methods and show example usage.

## Benefits of Using Portkey

1. **Cost Monitoring**: Track your Anthropic API usage and costs
2. **Rate Limiting**: Prevent unexpected API overuse
3. **Fallback Options**: Configure fallback providers if Anthropic is unavailable
4. **Caching**: Reduce costs with intelligent response caching
5. **Analytics**: Detailed insights into model performance and usage patterns

## Troubleshooting

### Common Issues

1. **Invalid Virtual Key**: Ensure your Portkey virtual key is configured for Anthropic
2. **API Key Missing**: Check that both PORTKEY_API_KEY and PORTKEY_ANTHROPIC_VIRTUAL_KEY are set
3. **Network Issues**: Verify PORTKEY_BASE_URL is correct (usually the default works)

### Debug Mode

To debug Portkey issues, you can add logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Testing Individual Components

```python
from src.config.llm_providers import create_provider_config, create_llm_instance

# Test configuration creation
config = create_provider_config("portkey_anthropic", "claude-3-haiku-20240307")
print(f"Config: {config}")

# Test LLM instance creation (requires valid API keys)
llm = create_llm_instance(config)
print(f"LLM: {llm}")
```

## Migration from Direct Anthropic

If you're currently using direct Anthropic configuration, you can easily migrate:

```python
# Before (direct Anthropic)
AGENT_LLM_MAP = {
    "my_agent": ["anthropic", "claude-3-5-sonnet-20241022"]
}

# After (Portkey Anthropic)
AGENT_LLM_MAP = {
    "my_agent": ["portkey_anthropic", "claude-3-5-sonnet-20241022"]
}
```

The API interface remains the same - only the provider changes to enable Portkey's additional features. 