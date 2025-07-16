"""
Test script for the refactored biomedical researcher agent.
Verifies that it properly uses the new modular LLM provider system.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from unittest.mock import patch, MagicMock
from src.agents.biomedical_researcher import get_biomedical_model, _create_pydantic_ai_model_from_config
from src.config.llm_providers import create_provider_config, ProviderType


def test_biomedical_researcher_uses_new_system():
    """Test that biomedical researcher uses the new modular provider system."""
    try:
        model = get_biomedical_model()
        print(f"✅ Model created successfully: {type(model).__name__}")
        
        # Verify it's a PydanticAI model
        assert hasattr(model, 'model_name') or hasattr(model, 'model'), "Model should have model_name or model attribute"
        print(f"✅ Model has proper attributes")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_openai_provider_config():
    """Test OpenAI provider configuration."""
    print("\n🧪 Testing OpenAI provider...")
    try:
        config = create_provider_config("openai", "gpt-4o-mini", temperature=0.1)
        model = _create_pydantic_ai_model_from_config(config)
        
        print(f"✅ OpenAI model created: {type(model).__name__}")
        return True
    except Exception as e:
        print(f"❌ OpenAI test failed: {e}")
        return False


def test_anthropic_provider_config():
    """Test Anthropic provider configuration."""
    print("\n🧪 Testing Anthropic provider...")
    try:
        config = create_provider_config("anthropic", "claude-3-haiku-20240307", temperature=0.1)
        model = _create_pydantic_ai_model_from_config(config)
        
        print(f"✅ Anthropic model created: {type(model).__name__}")
        return True
    except Exception as e:
        print(f"❌ Anthropic test failed: {e}")
        return False


def test_portkey_openai_provider_config():
    """Test Portkey OpenAI provider configuration."""
    print("\n🧪 Testing Portkey OpenAI provider...")
    try:
        config = create_provider_config("portkey_openai", "gpt-4o-mini", temperature=0.1)
        
        # Mock the config to have dummy Portkey values for testing
        config.portkey_api_key = "dummy_portkey_key"
        config.virtual_key = "dummy_virtual_key"
        
        model = _create_pydantic_ai_model_from_config(config)
        
        print(f"✅ Portkey OpenAI model created: {type(model).__name__}")
        return True
    except ImportError:
        print("⚠️  Portkey AI not installed - skipping test")
        return True  # Not a failure if package isn't installed
    except Exception as e:
        print(f"❌ Portkey OpenAI test failed: {e}")
        return False


def test_portkey_anthropic_provider_config():
    """Test Portkey Anthropic provider configuration."""
    print("\n🧪 Testing Portkey Anthropic provider...")
    try:
        config = create_provider_config("portkey_anthropic", "claude-3-haiku-20240307", temperature=0.1)
        
        # Mock the config to have dummy Portkey values for testing
        config.portkey_api_key = "dummy_portkey_key"
        config.virtual_key = "dummy_virtual_key"
        
        model = _create_pydantic_ai_model_from_config(config)
        
        print(f"✅ Portkey Anthropic model created: {type(model).__name__}")
        return True
    except ImportError:
        print("⚠️  Portkey AI not installed - skipping test")
        return True  # Not a failure if package isn't installed
    except Exception as e:
        print(f"❌ Portkey Anthropic test failed: {e}")
        return False


def test_deepseek_provider_config():
    """Test DeepSeek provider configuration."""
    print("\n🧪 Testing DeepSeek provider...")
    try:
        config = create_provider_config("deepseek", "deepseek-chat", temperature=0.1)
        
        # Mock the config to have dummy API key for testing if not set
        if not config.api_key:
            config.api_key = "dummy_deepseek_key"
        
        model = _create_pydantic_ai_model_from_config(config)
        
        print(f"✅ DeepSeek model created: {type(model).__name__}")
        return True
    except Exception as e:
        if "DEEPSEEK_API_KEY" in str(e):
            print("⚠️  DeepSeek API key not configured - skipping test")
            return True  # Not a failure if API key isn't configured
        print(f"❌ DeepSeek test failed: {e}")
        return False


def test_azure_provider_config():
    """Test Azure provider configuration."""
    print("\n🧪 Testing Azure provider...")
    try:
        config = create_provider_config("azure", "gpt-4o-mini", temperature=0.1)
        
        # Mock Azure-specific config
        config.azure_endpoint = "https://dummy.openai.azure.com/"
        config.api_version = "2024-02-15-preview"
        
        model = _create_pydantic_ai_model_from_config(config)
        
        print(f"✅ Azure model created: {type(model).__name__}")
        return True
    except Exception as e:
        print(f"❌ Azure test failed: {e}")
        return False


def test_configuration_resolution():
    """Test that the biomedical researcher resolves its configuration correctly."""
    print("\n🧪 Testing configuration resolution...")
    try:
        from src.config.agents import get_agent_full_config
        
        config = get_agent_full_config("biomedical_researcher")
        print(f"✅ Configuration resolved:")
        print(f"   Provider: {config['provider']}")
        print(f"   Model: {config['model']}")
        print(f"   Temperature: {config['temperature']}")
        
        # Should be using OpenAI with gpt-4o-mini according to current config
        assert config['provider'] == 'openai'
        assert config['model'] == 'gpt-4o-mini'
        
        return True
    except Exception as e:
        print(f"❌ Configuration resolution test failed: {e}")
        return False


def test_backward_compatibility():
    """Test that the fallback to legacy system still works."""
    print("\n🧪 Testing backward compatibility...")
    try:
        from src.agents.biomedical_researcher import _get_biomedical_model_legacy
        
        model = _get_biomedical_model_legacy()
        print(f"✅ Legacy model created: {type(model).__name__}")
        return True
    except Exception as e:
        print(f"❌ Backward compatibility test failed: {e}")
        return False


def main():
    """Run all tests for the refactored biomedical researcher."""
    print("🧪 Biomedical Researcher Refactored Tests")
    print("=" * 60)
    
    tests = [
        test_biomedical_researcher_uses_new_system,
        test_configuration_resolution,
        test_openai_provider_config,
        test_anthropic_provider_config,
        test_portkey_openai_provider_config,
        test_portkey_anthropic_provider_config,
        test_deepseek_provider_config,
        test_azure_provider_config,
        test_backward_compatibility,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! Biomedical researcher refactor is successful!")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 