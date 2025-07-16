#!/usr/bin/env python3
"""
Simple usage example of the new LLM configuration system.
This demonstrates the key features without making actual API calls.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config.agents import AGENT_LLM_MAP, resolve_agent_llm_config, get_agent_full_config
from src.agents.llm import get_llm_by_agent
from src.agents.agents import get_agent_config_summary


def main():
    print("🚀 Simple LLM Configuration Usage Demo")
    print("=" * 60)
    
    # Show current configuration
    print("\n📋 Current Agent Configuration:")
    print("-" * 40)
    for agent, config in AGENT_LLM_MAP.items():
        provider, model = resolve_agent_llm_config(agent)
        print(f"  {agent:20} → {provider:12} / {model}")
    
    # Show how to modify configuration
    print("\n🔧 Example Configuration Modifications:")
    print("-" * 40)
    
    # Example: Change coder to use DeepSeek
    print("  # Change coder to use DeepSeek:")
    print('  AGENT_LLM_MAP["coder"] = ["deepseek", "deepseek-coder"]')
    
    # Example: Use full configuration dict
    print("\n  # Use full configuration with custom settings:")
    print('  AGENT_LLM_MAP["researcher"] = {')
    print('      "provider": "anthropic",')
    print('      "model": "claude-3-5-sonnet-20241022",')
    print('      "temperature": 0.1,')
    print('      "max_tokens": 8000')
    print('  }')
    
    # Example: Use predefined config
    print("\n  # Use predefined configuration:")
    print('  AGENT_LLM_MAP["data_analyst"] = "anthropic_reasoning"')
    
    # Show environment variables needed
    print("\n🔑 Environment Variables for Current Configuration:")
    print("-" * 40)
    
    providers_used = set()
    for agent in AGENT_LLM_MAP.keys():
        provider, _ = resolve_agent_llm_config(agent)
        providers_used.add(provider)
    
    env_vars = {
        "openai": ["OPENAI_API_KEY"],
        "anthropic": ["ANTHROPIC_API_KEY"],
        "deepseek": ["DEEPSEEK_API_KEY"],
        "bedrock": ["AWS_REGION", "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"],
        "azure": ["AZURE_OPENAI_API_KEY", "AZURE_OPENAI_ENDPOINT"],
        "portkey_openai": ["PORTKEY_API_KEY", "PORTKEY_OPENAI_VIRTUAL_KEY"],
        "portkey_bedrock": ["PORTKEY_API_KEY", "PORTKEY_BEDROCK_VIRTUAL_KEY"],
    }
    
    for provider in sorted(providers_used):
        if provider in env_vars:
            print(f"  {provider.upper()}:")
            for var in env_vars[provider]:
                print(f"    {var}=your_{provider}_key")
    
    # Show how to use in code
    print("\n💻 Usage in Code:")
    print("-" * 40)
    print("  from src.agents.llm import get_llm_by_agent")
    print("  ")
    print("  # Get configured LLM for any agent")
    print("  coder_llm = get_llm_by_agent('coder')")
    print("  response = coder_llm.invoke('Write a hello world function')")
    print("  ")
    print("  # Get configuration summary")
    print("  from src.agents.agents import get_agent_config_summary")
    print("  summary = get_agent_config_summary()")
    
    # Show actual LLM instances (created but not called)
    print("\n🏗️  Created LLM Instances:")
    print("-" * 40)
    
    for agent_name in ["coordinator", "coder", "researcher"]:
        try:
            llm = get_llm_by_agent(agent_name)
            provider, model = resolve_agent_llm_config(agent_name)
            print(f"  {agent_name:15} → {type(llm).__name__:15} ({provider}/{model})")
        except Exception as e:
            print(f"  {agent_name:15} → Error: {e}")
    
    print("\n✅ Demo completed!")
    print("=" * 60)


if __name__ == "__main__":
    main() 