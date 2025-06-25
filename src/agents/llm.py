from langchain_openai import ChatOpenAI
from langchain_deepseek import ChatDeepSeek
from typing import Optional

from src.config import (
    REASONING_PROVIDER,
    REASONING_MODEL,
    REASONING_BASE_URL,
    REASONING_API_KEY,
    BASIC_MODEL,
    BASIC_BASE_URL,
    BASIC_API_KEY,
    VL_MODEL,
    VL_BASE_URL,
    VL_API_KEY,
)
from src.config.agents import LLMType


def create_openai_llm(
    model: str,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    temperature: float = 0.0,
    **kwargs,
) -> ChatOpenAI:
    """
    Create a ChatOpenAI instance with the specified configuration
    """
    # Only include base_url in the arguments if it's not None or empty
    llm_kwargs = {"model": model, "temperature": temperature, **kwargs}

    if base_url:  # This will handle None or empty string
        llm_kwargs["base_url"] = base_url

    if api_key:  # This will handle None or empty string
        llm_kwargs["api_key"] = api_key

    return ChatOpenAI(**llm_kwargs)


def create_deepseek_llm(
    model: str,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    temperature: float = 0.0,
    **kwargs,
) -> ChatDeepSeek:
    """
    Create a ChatDeepSeek instance with the specified configuration
    """
    # Only include base_url in the arguments if it's not None or empty
    llm_kwargs = {"model": model, "temperature": temperature, **kwargs}

    if base_url:  # This will handle None or empty string
        llm_kwargs["api_base"] = base_url

    if api_key:  # This will handle None or empty string
        llm_kwargs["api_key"] = api_key

    return ChatDeepSeek(**llm_kwargs)


# Cache for LLM instances
_llm_cache: dict[LLMType, ChatOpenAI | ChatDeepSeek] = {}


def clear_llm_cache() -> None:
    """
    Clear the LLM cache. Useful when configuration changes or for testing.
    """
    global _llm_cache
    cache_keys = list(_llm_cache.keys())
    _llm_cache.clear()
    print(f"✅ LLM cache cleared! Removed: {cache_keys}")


def get_cache_status() -> dict:
    """
    Get the current status of the LLM cache.
    """
    status = {}
    for key, llm in _llm_cache.items():
        model_name = getattr(llm, 'model_name', getattr(llm, 'model', 'unknown'))
        status[key] = {
            'type': type(llm).__name__,
            'model': model_name
        }
    return status


def get_llm_by_type(llm_type: LLMType) -> ChatOpenAI | ChatDeepSeek:
    """
    Get LLM instance by type. Returns cached instance if available.
    """
    if llm_type in _llm_cache:
        return _llm_cache[llm_type]

    if llm_type == "reasoning":
        if REASONING_PROVIDER == "deepseek":
            llm = create_deepseek_llm(
                model=REASONING_MODEL,
                base_url=REASONING_BASE_URL,
                api_key=REASONING_API_KEY,
            )
        else:
            # For OpenAI reasoning models (o1, o3, o4 series), don't set temperature
            # as they don't support custom temperature values
            if REASONING_MODEL and (REASONING_MODEL.startswith('o1') or REASONING_MODEL.startswith('o3') or REASONING_MODEL.startswith('o4')):
                # Create without temperature parameter for reasoning models
                llm_kwargs = {"model": REASONING_MODEL}
                if REASONING_BASE_URL:
                    llm_kwargs["base_url"] = REASONING_BASE_URL
                if REASONING_API_KEY:
                    llm_kwargs["api_key"] = REASONING_API_KEY
                llm = ChatOpenAI(**llm_kwargs)
            else:
                llm = create_openai_llm(
                    model=REASONING_MODEL,
                    base_url=REASONING_BASE_URL,
                    api_key=REASONING_API_KEY,
                )
    elif llm_type == "basic":
        llm = create_openai_llm(
            model=BASIC_MODEL,
            base_url=BASIC_BASE_URL,
            api_key=BASIC_API_KEY,
        )
    elif llm_type == "vision":
        llm = create_openai_llm(
            model=VL_MODEL,
            base_url=VL_BASE_URL,
            api_key=VL_API_KEY,
        )
    else:
        raise ValueError(f"Unknown LLM type: {llm_type}")

    _llm_cache[llm_type] = llm
    return llm


# LLMs will be lazily initialized when first requested via get_llm_by_type()
# This avoids premature caching with potentially incorrect configuration

def get_reasoning_llm():
    """Get reasoning LLM instance (lazy initialization)"""
    return get_llm_by_type("reasoning")

def get_basic_llm():
    """Get basic LLM instance (lazy initialization)"""
    return get_llm_by_type("basic")

def get_vl_llm():
    """Get vision-language LLM instance (lazy initialization)"""
    return get_llm_by_type("vision")

# For backward compatibility with existing code that imports these directly
# These will only be initialized when first accessed
class LazyLLM:
    def __init__(self, llm_type):
        self._llm_type = llm_type
        self._llm = None
    
    def __getattr__(self, name):
        if self._llm is None:
            self._llm = get_llm_by_type(self._llm_type)
        return getattr(self._llm, name)
    
    def __call__(self, *args, **kwargs):
        if self._llm is None:
            self._llm = get_llm_by_type(self._llm_type)
        return self._llm(*args, **kwargs)

reasoning_llm = LazyLLM("reasoning")
basic_llm = LazyLLM("basic")
vl_llm = LazyLLM("vision")


if __name__ == "__main__":
    stream = reasoning_llm.stream("what is mcp?")
    full_response = ""
    for chunk in stream:
        full_response += chunk.content
    print(full_response)

    basic_llm.invoke("Hello")
    vl_llm.invoke("Hello")
