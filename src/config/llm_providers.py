"""
LLM Provider Configuration System
Defines provider-specific settings and factory functions for different LLM providers.
"""

import os
from typing import Optional, Dict, Any, Union, Tuple
from pydantic import BaseModel, Field
from enum import Enum


class ProviderType(str, Enum):
    """Supported LLM providers."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    DEEPSEEK = "deepseek"
    BEDROCK = "bedrock"
    AZURE = "azure"
    PORTKEY_OPENAI = "portkey_openai"
    PORTKEY_ANTHROPIC = "portkey_anthropic"
    PORTKEY_BEDROCK = "portkey_bedrock"
    PORTKEY_AZURE = "portkey_azure"


class LLMProviderConfig(BaseModel):
    """Base configuration for LLM providers."""
    provider: ProviderType
    model: str
    temperature: float = 0.0
    max_tokens: Optional[int] = None
    max_retries: int = 3
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    extra_kwargs: Dict[str, Any] = Field(default_factory=dict)


class OpenAIConfig(LLMProviderConfig):
    """OpenAI-specific configuration."""
    provider: ProviderType = ProviderType.OPENAI
    api_key: Optional[str] = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY"))
    base_url: Optional[str] = Field(default_factory=lambda: os.getenv("OPENAI_BASE_URL"))


class AnthropicConfig(LLMProviderConfig):
    """Anthropic-specific configuration."""
    provider: ProviderType = ProviderType.ANTHROPIC
    api_key: Optional[str] = Field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY"))


class DeepSeekConfig(LLMProviderConfig):
    """DeepSeek-specific configuration."""
    provider: ProviderType = ProviderType.DEEPSEEK
    api_key: Optional[str] = Field(default_factory=lambda: os.getenv("DEEPSEEK_API_KEY"))
    base_url: Optional[str] = Field(default_factory=lambda: os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"))


class BedrockConfig(LLMProviderConfig):
    """AWS Bedrock-specific configuration."""
    provider: ProviderType = ProviderType.BEDROCK
    region: str = Field(default_factory=lambda: os.getenv("AWS_REGION", "us-east-1"))
    
    
class AzureConfig(LLMProviderConfig):
    """Azure OpenAI-specific configuration."""
    provider: ProviderType = ProviderType.AZURE
    api_key: Optional[str] = Field(default_factory=lambda: os.getenv("AZURE_OPENAI_API_KEY"))
    azure_endpoint: Optional[str] = Field(default_factory=lambda: os.getenv("AZURE_OPENAI_ENDPOINT"))
    api_version: str = Field(default_factory=lambda: os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"))


class PortkeyConfig(LLMProviderConfig):
    """Portkey gateway configuration."""
    virtual_key: Optional[str] = None
    portkey_api_key: Optional[str] = Field(default_factory=lambda: os.getenv("PORTKEY_API_KEY"))
    portkey_base_url: str = Field(default_factory=lambda: os.getenv("PORTKEY_BASE_URL", "https://api.portkey.ai/v1"))
    

class PortkeyOpenAIConfig(PortkeyConfig):
    """Portkey with OpenAI backend configuration."""
    provider: ProviderType = ProviderType.PORTKEY_OPENAI
    virtual_key: Optional[str] = Field(default_factory=lambda: os.getenv("PORTKEY_OPENAI_VIRTUAL_KEY"))


class PortkeyAnthropicConfig(PortkeyConfig):
    """Portkey with Anthropic backend configuration."""
    provider: ProviderType = ProviderType.PORTKEY_ANTHROPIC
    virtual_key: Optional[str] = Field(default_factory=lambda: os.getenv("PORTKEY_ANTHROPIC_VIRTUAL_KEY"))


class PortkeyBedrockConfig(PortkeyConfig):
    """Portkey with Bedrock backend configuration."""
    provider: ProviderType = ProviderType.PORTKEY_BEDROCK
    virtual_key: Optional[str] = Field(default_factory=lambda: os.getenv("PORTKEY_BEDROCK_VIRTUAL_KEY"))


class PortkeyAzureConfig(PortkeyConfig):
    """Portkey with Azure backend configuration."""
    provider: ProviderType = ProviderType.PORTKEY_AZURE
    virtual_key: Optional[str] = Field(default_factory=lambda: os.getenv("PORTKEY_AZURE_VIRTUAL_KEY"))


def create_provider_config(provider: str, model: str, **kwargs) -> LLMProviderConfig:
    """Factory function to create provider-specific configurations."""
    provider_type = ProviderType(provider)
    
    config_classes = {
        ProviderType.OPENAI: OpenAIConfig,
        ProviderType.ANTHROPIC: AnthropicConfig,
        ProviderType.DEEPSEEK: DeepSeekConfig,
        ProviderType.BEDROCK: BedrockConfig,
        ProviderType.AZURE: AzureConfig,
        ProviderType.PORTKEY_OPENAI: PortkeyOpenAIConfig,
        ProviderType.PORTKEY_ANTHROPIC: PortkeyAnthropicConfig,
        ProviderType.PORTKEY_BEDROCK: PortkeyBedrockConfig,
        ProviderType.PORTKEY_AZURE: PortkeyAzureConfig,
    }
    
    config_class = config_classes.get(provider_type)
    if not config_class:
        raise ValueError(f"Unsupported provider: {provider}")
    
    return config_class(model=model, **kwargs)


def create_llm_instance(config: LLMProviderConfig):
    """Factory function to create LLM instances from configuration."""
    from langchain_openai import ChatOpenAI
    
    if config.provider == ProviderType.OPENAI:
        kwargs = {"model": config.model, "temperature": config.temperature}
        if config.base_url:
            kwargs["base_url"] = config.base_url
        if config.api_key:
            kwargs["api_key"] = config.api_key
        if config.max_tokens:
            kwargs["max_tokens"] = config.max_tokens
        kwargs.update(config.extra_kwargs)
        return ChatOpenAI(**kwargs)
    
    elif config.provider == ProviderType.ANTHROPIC:
        from langchain_anthropic import ChatAnthropic
        kwargs = {"model": config.model, "temperature": config.temperature}
        if config.api_key:
            kwargs["api_key"] = config.api_key
        if config.max_tokens:
            kwargs["max_tokens"] = config.max_tokens
        kwargs.update(config.extra_kwargs)
        return ChatAnthropic(**kwargs)
    
    elif config.provider == ProviderType.DEEPSEEK:
        from langchain_deepseek import ChatDeepSeek
        kwargs = {"model": config.model, "temperature": config.temperature}
        if config.base_url:
            kwargs["api_base"] = config.base_url
        if config.api_key:
            kwargs["api_key"] = config.api_key
        if config.max_tokens:
            kwargs["max_tokens"] = config.max_tokens
        kwargs.update(config.extra_kwargs)
        return ChatDeepSeek(**kwargs)
    
    elif config.provider == ProviderType.BEDROCK:
        from langchain_aws import ChatBedrock
        kwargs = {
            "model_id": config.model,
            "model_kwargs": {"temperature": config.temperature}
        }
        if hasattr(config, 'region'):
            kwargs["region"] = config.region
        if config.max_tokens:
            kwargs["model_kwargs"]["max_tokens"] = config.max_tokens
        kwargs.update(config.extra_kwargs)
        return ChatBedrock(**kwargs)
    
    elif config.provider == ProviderType.AZURE:
        from langchain_openai import AzureChatOpenAI
        kwargs = {
            "deployment_name": config.model,
            "temperature": config.temperature
        }
        if config.api_key:
            kwargs["api_key"] = config.api_key
        if hasattr(config, 'azure_endpoint'):
            kwargs["azure_endpoint"] = config.azure_endpoint
        if hasattr(config, 'api_version'):
            kwargs["api_version"] = config.api_version
        if config.max_tokens:
            kwargs["max_tokens"] = config.max_tokens
        kwargs.update(config.extra_kwargs)
        return AzureChatOpenAI(**kwargs)
    
    elif config.provider in [ProviderType.PORTKEY_OPENAI, ProviderType.PORTKEY_ANTHROPIC, ProviderType.PORTKEY_BEDROCK, ProviderType.PORTKEY_AZURE]:
        from portkey_ai import createHeaders
        
        portkey_headers = createHeaders(
            api_key=config.portkey_api_key,
            virtual_key=config.virtual_key
        )
        
        kwargs = {
            "model": config.model,
            "temperature": config.temperature,
            "base_url": config.portkey_base_url,
            "default_headers": portkey_headers,
            "api_key": "portkey"  # Dummy key as auth is handled via headers
        }
        if config.max_tokens:
            kwargs["max_tokens"] = config.max_tokens
        kwargs.update(config.extra_kwargs)
        return ChatOpenAI(**kwargs)
    
    else:
        raise ValueError(f"Unsupported provider: {config.provider}")


# Predefined configurations for common use cases
PREDEFINED_CONFIGS = {
    "reasoning": ["openai", "o3-mini"],
    "basic": ["openai", "gpt-4o-mini"], 
    "vision": ["openai", "gpt-4o"],
    "fast": ["openai", "gpt-4o-mini"],
    "powerful": ["openai", "o3-mini"],
    "anthropic_reasoning": ["anthropic", "claude-3-5-sonnet-20241022"],
    "anthropic_basic": ["anthropic", "claude-3-haiku-20240307"],
    "portkey_anthropic_reasoning": ["portkey_anthropic", "claude-3-5-sonnet-20241022"],
    "portkey_anthropic_basic": ["portkey_anthropic", "claude-3-haiku-20240307"],
    "deepseek_reasoning": ["deepseek", "deepseek-reasoner"],
    "deepseek_basic": ["deepseek", "deepseek-chat"],
} 