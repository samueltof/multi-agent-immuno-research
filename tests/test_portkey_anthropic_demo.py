"""
Demo script showing how to use Portkey Anthropic in agent configurations.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config.agents import AGENT_LLM_MAP, get_agent_full_config
from src.agents.llm import get_llm_by_agent

def demo_portkey_anthropic_usage():
    """Demonstrate how to use Portkey Anthropic with agents."""
    print("🚀 Portkey Anthropic Usage Demo")
    print("=" * 50)
    
    # Store original AGENT_LLM_MAP to restore later
    original_map = AGENT_LLM_MAP.copy()
    
    try:
        # Example 1: Using predefined configuration
        print("\n📋 Example 1: Using predefined Portkey Anthropic configuration")
        example_configs_1 = {
            "research_agent": "portkey_anthropic_reasoning",
            "summary_agent": "portkey_anthropic_basic"
        }
        
        # Temporarily update the global map
        AGENT_LLM_MAP.update(example_configs_1)
        
        for agent_name, config in example_configs_1.items():
            try:
                full_config = get_agent_full_config(agent_name)
                print(f"✅ {agent_name}: {config}")
                print(f"   Provider: {full_config['provider']}")
                print(f"   Model: {full_config['model']}")
            except Exception as e:
                print(f"❌ Error with {agent_name}: {e}")
        
        # Example 2: Using direct provider/model specification
        print("\n🎯 Example 2: Direct provider/model specification")
        example_configs_2 = {
            "analysis_agent": ["portkey_anthropic", "claude-3-5-sonnet-20241022"],
            "chat_agent": ["portkey_anthropic", "claude-3-haiku-20240307"]
        }
        
        AGENT_LLM_MAP.update(example_configs_2)
        
        for agent_name, config in example_configs_2.items():
            try:
                full_config = get_agent_full_config(agent_name)
                print(f"✅ {agent_name}: {config}")
                print(f"   Provider: {full_config['provider']}")
                print(f"   Model: {full_config['model']}")
            except Exception as e:
                print(f"❌ Error with {agent_name}: {e}")
        
        # Example 3: Full configuration with custom parameters
        print("\n⚙️  Example 3: Full configuration with custom parameters")
        example_configs_3 = {
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
        
        AGENT_LLM_MAP.update(example_configs_3)
        
        for agent_name, config in example_configs_3.items():
            try:
                full_config = get_agent_full_config(agent_name)
                print(f"✅ {agent_name}: Custom configuration")
                print(f"   Provider: {full_config['provider']}")
                print(f"   Model: {full_config['model']}")
                print(f"   Temperature: {full_config['temperature']}")
                print(f"   Max Tokens: {full_config['max_tokens']}")
            except Exception as e:
                print(f"❌ Error with {agent_name}: {e}")
        
        # Example 4: Mixed configurations
        print("\n🔀 Example 4: Mixed provider configurations")
        mixed_configs = {
            "coordinator_demo": "reasoning",  # OpenAI reasoning
            "coder_demo": ["anthropic", "claude-3-5-sonnet-20241022"],  # Direct Anthropic
            "researcher_demo": "portkey_anthropic_reasoning",  # Portkey Anthropic
            "analyst_demo": ["portkey_anthropic", "claude-3-haiku-20240307"]  # Direct Portkey Anthropic
        }
        
        AGENT_LLM_MAP.update(mixed_configs)
        
        for agent_name, config in mixed_configs.items():
            try:
                full_config = get_agent_full_config(agent_name)
                print(f"✅ {agent_name}: {config}")
                print(f"   Provider: {full_config['provider']}")
                print(f"   Model: {full_config['model']}")
            except Exception as e:
                print(f"❌ Error with {agent_name}: {e}")
        
    finally:
        # Restore original AGENT_LLM_MAP
        AGENT_LLM_MAP.clear()
        AGENT_LLM_MAP.update(original_map)
    
    print("\n" + "=" * 50)
    print("🎉 Portkey Anthropic demo completed!")
    
    # Setup instructions
    print("\n📝 Setup Instructions:")
    print("1. Set your Portkey API key:")
    print("   export PORTKEY_API_KEY='your_portkey_api_key'")
    print("\n2. Set your Portkey Anthropic virtual key:")
    print("   export PORTKEY_ANTHROPIC_VIRTUAL_KEY='your_anthropic_virtual_key'")
    print("\n3. Optional - Set custom Portkey base URL:")
    print("   export PORTKEY_BASE_URL='https://your-custom-portkey-endpoint.com/v1'")
    
    print("\n🔧 Usage in your agent configuration:")
    print("   Update src/config/agents.py:")
    print("   AGENT_LLM_MAP = {")
    print("       'my_agent': 'portkey_anthropic_reasoning',")
    print("       'other_agent': ['portkey_anthropic', 'claude-3-haiku-20240307'],")
    print("   }")

if __name__ == "__main__":
    demo_portkey_anthropic_usage() 