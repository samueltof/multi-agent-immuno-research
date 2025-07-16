#!/usr/bin/env python3
"""
Test script for the new LLM configuration system.
This validates that agents can be configured with different providers and models.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config.agents import (
    AGENT_LLM_MAP, 
    resolve_agent_llm_config, 
    get_agent_full_config,
    get_legacy_llm_type
)
from src.config.llm_providers import PREDEFINED_CONFIGS, create_provider_config
from src.agents.llm import get_llm_by_agent
from src.agents.agents import get_agent_config_summary


def test_agent_configurations():
    """Test that all agent configurations resolve correctly."""
    print("🔧 Testing Agent LLM Configurations")
    print("=" * 50)
    
    for agent_name, config in AGENT_LLM_MAP.items():
        print(f"\n📋 Agent: {agent_name}")
        print(f"   Raw config: {config}")
        
        try:
            # Test resolution
            provider, model = resolve_agent_llm_config(agent_name)
            print(f"   ✅ Resolved to: {provider} / {model}")
            
            # Test full config
            full_config = get_agent_full_config(agent_name)
            print(f"   📄 Full config: {full_config}")
            
            # Test legacy mapping
            legacy_type = get_legacy_llm_type(agent_name)
            print(f"   🔄 Legacy type: {legacy_type}")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")


def test_predefined_configs():
    """Test predefined configurations."""
    print("\n\n🎯 Testing Predefined Configurations")
    print("=" * 50)
    
    for name, config in PREDEFINED_CONFIGS.items():
        print(f"\n📦 Predefined: {name}")
        print(f"   Config: {config}")
        
        try:
            provider_config = create_provider_config(config[0], config[1])
            print(f"   ✅ Created config: {provider_config.provider} / {provider_config.model}")
        except Exception as e:
            print(f"   ❌ Error: {e}")


def test_llm_creation():
    """Test actual LLM instance creation (without calling APIs)."""
    print("\n\n🏗️  Testing LLM Instance Creation")
    print("=" * 50)
    
    # Test a few key agents
    test_agents = ["coordinator", "coder", "researcher"]
    
    for agent_name in test_agents:
        print(f"\n🤖 Agent: {agent_name}")
        
        try:
            # This will create the LLM instance but not call it
            llm = get_llm_by_agent(agent_name)
            print(f"   ✅ LLM created: {type(llm).__name__}")
            
            # Try to get the model name
            model_name = getattr(llm, 'model_name', getattr(llm, 'model', 'unknown'))
            print(f"   📄 Model: {model_name}")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")


def test_agent_summary():
    """Test the agent configuration summary function."""
    print("\n\n📊 Testing Agent Configuration Summary")
    print("=" * 50)
    
    try:
        summary = get_agent_config_summary()
        
        for agent_name, config in summary.items():
            print(f"\n🤖 {agent_name}:")
            if "error" in config:
                print(f"   ❌ Error: {config['error']}")
            else:
                print(f"   🏷️  Provider: {config['provider']}")
                print(f"   🎯 Model: {config['model']}")
                print(f"   🌡️  Temperature: {config['temperature']}")
                print(f"   🔄 Legacy type: {config['legacy_type']}")
                
    except Exception as e:
        print(f"❌ Error getting summary: {e}")


def test_example_configurations():
    """Test some example custom configurations."""
    print("\n\n🧪 Testing Example Custom Configurations")
    print("=" * 50)
    
    # Test different configuration formats
    test_configs = {
        "predefined_string": "reasoning",
        "provider_model_list": ["anthropic", "claude-3-haiku-20240307"],
        "provider_model_tuple": ("openai", "gpt-4o-mini"),
        "full_dict": {
            "provider": "openai",
            "model": "gpt-4o-mini",
            "temperature": 0.1,
            "max_tokens": 1000
        }
    }
    
    for config_name, config in test_configs.items():
        print(f"\n🧪 Testing: {config_name}")
        print(f"   Config: {config}")
        
        try:
            # Temporarily set this as a test agent
            from src.config.agents import AGENT_LLM_MAP
            AGENT_LLM_MAP["test_agent"] = config
            
            # Test resolution
            provider, model = resolve_agent_llm_config("test_agent")
            print(f"   ✅ Resolved to: {provider} / {model}")
            
            # Test full config
            full_config = get_agent_full_config("test_agent")
            print(f"   📄 Full config: {full_config}")
            
            # Clean up
            del AGENT_LLM_MAP["test_agent"]
            
        except Exception as e:
            print(f"   ❌ Error: {e}")


if __name__ == "__main__":
    print("🚀 LLM Configuration System Test Suite")
    print("=" * 60)
    
    test_agent_configurations()
    test_predefined_configs()
    test_llm_creation()
    test_agent_summary()
    test_example_configurations()
    
    print("\n\n✅ Test Suite Completed!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Set up your .env file with the appropriate API keys")
    print("2. Customize AGENT_LLM_MAP in src/config/agents.py")
    print("3. Add new predefined configs in src/config/llm_providers.py")
    print("4. Test with actual LLM calls using the agents") 