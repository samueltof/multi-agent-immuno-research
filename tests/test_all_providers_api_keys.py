"""
Comprehensive test script to verify API key recognition and provider functionality.
Tests all supported LLM providers to ensure proper configuration.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config.llm_providers import (
    ProviderType, 
    create_provider_config, 
    create_llm_instance,
    PREDEFINED_CONFIGS
)
from src.config.env import *

def check_environment_variables():
    """Check which environment variables are configured."""
    print("🔍 Environment Variables Check")
    print("=" * 50)
    
    env_vars = {
        "OpenAI": {
            "OPENAI_API_KEY": OPENAI_API_KEY,
            "OPENAI_BASE_URL": OPENAI_BASE_URL,
        },
        "Anthropic": {
            "ANTHROPIC_API_KEY": ANTHROPIC_API_KEY,
        },
        "DeepSeek": {
            "DEEPSEEK_API_KEY": DEEPSEEK_API_KEY,
            "DEEPSEEK_BASE_URL": DEEPSEEK_BASE_URL,
        },
        "AWS Bedrock": {
            "AWS_REGION": AWS_REGION,
            "AWS_ACCESS_KEY_ID": AWS_ACCESS_KEY_ID,
            "AWS_SECRET_ACCESS_KEY": AWS_SECRET_ACCESS_KEY,
        },
        "Azure OpenAI": {
            "AZURE_OPENAI_API_KEY": AZURE_OPENAI_API_KEY,
            "AZURE_OPENAI_ENDPOINT": AZURE_OPENAI_ENDPOINT,
            "AZURE_OPENAI_API_VERSION": AZURE_OPENAI_API_VERSION,
        },
        "Portkey": {
            "PORTKEY_API_KEY": PORTKEY_API_KEY,
            "PORTKEY_BASE_URL": PORTKEY_BASE_URL,
            "PORTKEY_OPENAI_VIRTUAL_KEY": PORTKEY_OPENAI_VIRTUAL_KEY,
            "PORTKEY_ANTHROPIC_VIRTUAL_KEY": PORTKEY_ANTHROPIC_VIRTUAL_KEY,
            "PORTKEY_BEDROCK_VIRTUAL_KEY": PORTKEY_BEDROCK_VIRTUAL_KEY,
            "PORTKEY_AZURE_VIRTUAL_KEY": PORTKEY_AZURE_VIRTUAL_KEY,
        }
    }
    
    provider_status = {}
    
    for provider_name, vars_dict in env_vars.items():
        print(f"\n🔧 {provider_name}:")
        configured_vars = []
        missing_vars = []
        
        for var_name, var_value in vars_dict.items():
            if var_value and var_value.strip():
                configured_vars.append(var_name)
                # Mask sensitive values
                if "KEY" in var_name or "SECRET" in var_name:
                    display_value = f"{var_value[:8]}..." if len(var_value) > 8 else "***"
                else:
                    display_value = var_value
                print(f"   ✅ {var_name}: {display_value}")
            else:
                missing_vars.append(var_name)
                print(f"   ❌ {var_name}: Not set")
        
        # Determine provider status
        if provider_name == "OpenAI" and "OPENAI_API_KEY" in configured_vars:
            provider_status[provider_name] = "ready"
        elif provider_name == "Anthropic" and "ANTHROPIC_API_KEY" in configured_vars:
            provider_status[provider_name] = "ready"
        elif provider_name == "DeepSeek" and "DEEPSEEK_API_KEY" in configured_vars:
            provider_status[provider_name] = "ready"
        elif provider_name == "AWS Bedrock" and all(key in configured_vars for key in ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]):
            provider_status[provider_name] = "ready"
        elif provider_name == "Azure OpenAI" and all(key in configured_vars for key in ["AZURE_OPENAI_API_KEY", "AZURE_OPENAI_ENDPOINT"]):
            provider_status[provider_name] = "ready"
        elif provider_name == "Portkey" and "PORTKEY_API_KEY" in configured_vars:
            # Check which Portkey providers are ready
            portkey_providers = []
            if "PORTKEY_OPENAI_VIRTUAL_KEY" in configured_vars:
                portkey_providers.append("OpenAI")
            if "PORTKEY_ANTHROPIC_VIRTUAL_KEY" in configured_vars:
                portkey_providers.append("Anthropic")
            if "PORTKEY_BEDROCK_VIRTUAL_KEY" in configured_vars:
                portkey_providers.append("Bedrock")
            if "PORTKEY_AZURE_VIRTUAL_KEY" in configured_vars:
                portkey_providers.append("Azure")
            
            if portkey_providers:
                provider_status[provider_name] = f"ready ({', '.join(portkey_providers)})"
            else:
                provider_status[provider_name] = "partial (no virtual keys)"
        else:
            provider_status[provider_name] = "not configured"
    
    return provider_status

def test_provider_config_creation():
    """Test provider configuration creation for each provider type."""
    print("\n🏗️  Provider Configuration Creation Test")
    print("=" * 50)
    
    test_configs = [
        ("openai", "gpt-4o-mini"),
        ("anthropic", "claude-3-haiku-20240307"),
        ("deepseek", "deepseek-chat"),
        ("bedrock", "anthropic.claude-3-haiku-20240307-v1:0"),
        ("azure", "gpt-4o-mini"),
        ("portkey_openai", "gpt-4o-mini"),
        ("portkey_anthropic", "claude-3-haiku-20240307"),
        ("portkey_bedrock", "anthropic.claude-3-haiku-20240307-v1:0"),
        ("portkey_azure", "gpt-4o-mini"),
    ]
    
    config_results = {}
    
    for provider, model in test_configs:
        try:
            config = create_provider_config(provider, model, temperature=0.1)
            config_results[provider] = {
                "status": "success",
                "config": config,
                "error": None
            }
            print(f"✅ {provider}: Configuration created successfully")
            print(f"   Model: {config.model}")
            print(f"   Temperature: {config.temperature}")
            
            # Check API key configuration
            if hasattr(config, 'api_key') and config.api_key:
                key_display = f"{config.api_key[:8]}..." if len(config.api_key) > 8 else "***"
                print(f"   API Key: {key_display}")
            elif hasattr(config, 'virtual_key') and config.virtual_key:
                key_display = f"{config.virtual_key[:8]}..." if len(config.virtual_key) > 8 else "***"
                print(f"   Virtual Key: {key_display}")
            
        except Exception as e:
            config_results[provider] = {
                "status": "error", 
                "config": None,
                "error": str(e)
            }
            print(f"❌ {provider}: {e}")
    
    return config_results

def test_llm_instance_creation(config_results):
    """Test LLM instance creation for successfully configured providers."""
    print("\n🤖 LLM Instance Creation Test")
    print("=" * 50)
    
    instance_results = {}
    
    for provider, result in config_results.items():
        if result["status"] != "success":
            print(f"⏭️  {provider}: Skipping (configuration failed)")
            continue
        
        try:
            config = result["config"]
            
            # For testing, we'll only create instances if we have valid API keys
            # For Portkey providers, we need both Portkey API key and virtual keys
            can_test = False
            
            if provider == "openai" and config.api_key:
                can_test = True
            elif provider == "anthropic" and config.api_key:
                can_test = True
            elif provider == "deepseek" and config.api_key:
                can_test = True
            elif provider == "bedrock":
                # Bedrock uses AWS credentials
                can_test = bool(AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY)
            elif provider == "azure" and config.api_key:
                can_test = True
            elif provider.startswith("portkey_") and config.portkey_api_key and config.virtual_key:
                can_test = True
            
            if not can_test:
                print(f"⚠️  {provider}: Skipping instance creation (missing API keys)")
                instance_results[provider] = {
                    "status": "skipped",
                    "reason": "missing_api_keys"
                }
                continue
            
            # Create LLM instance
            llm = create_llm_instance(config)
            instance_results[provider] = {
                "status": "success",
                "llm_type": type(llm).__name__,
                "error": None
            }
            print(f"✅ {provider}: LLM instance created successfully")
            print(f"   Type: {type(llm).__name__}")
            print(f"   Model: {getattr(llm, 'model_name', getattr(llm, 'model', 'Unknown'))}")
            
        except ImportError as e:
            instance_results[provider] = {
                "status": "missing_dependency",
                "error": str(e)
            }
            print(f"📦 {provider}: Missing dependency - {e}")
            
        except Exception as e:
            instance_results[provider] = {
                "status": "error",
                "error": str(e)
            }
            print(f"❌ {provider}: {e}")
    
    return instance_results

def test_predefined_configurations():
    """Test predefined configuration resolution."""
    print("\n📋 Predefined Configurations Test")
    print("=" * 50)
    
    predefined_results = {}
    
    for config_name, (provider, model) in PREDEFINED_CONFIGS.items():
        try:
            config = create_provider_config(provider, model)
            predefined_results[config_name] = {
                "status": "success",
                "provider": provider,
                "model": model
            }
            print(f"✅ {config_name}: {provider} -> {model}")
            
        except Exception as e:
            predefined_results[config_name] = {
                "status": "error",
                "error": str(e)
            }
            print(f"❌ {config_name}: {e}")
    
    return predefined_results

def generate_summary_report(env_status, config_results, instance_results, predefined_results):
    """Generate a comprehensive summary report."""
    print("\n📊 Summary Report")
    print("=" * 50)
    
    # Environment status summary
    print("\n🔧 Environment Configuration:")
    ready_providers = [name for name, status in env_status.items() if "ready" in status]
    partial_providers = [name for name, status in env_status.items() if "partial" in status]
    missing_providers = [name for name, status in env_status.items() if "not configured" in status]
    
    print(f"   ✅ Ready: {len(ready_providers)} ({', '.join(ready_providers)})")
    if partial_providers:
        print(f"   ⚠️  Partial: {len(partial_providers)} ({', '.join(partial_providers)})")
    if missing_providers:
        print(f"   ❌ Missing: {len(missing_providers)} ({', '.join(missing_providers)})")
    
    # Configuration creation summary
    print("\n🏗️  Configuration Creation:")
    successful_configs = [p for p, r in config_results.items() if r["status"] == "success"]
    failed_configs = [p for p, r in config_results.items() if r["status"] == "error"]
    
    print(f"   ✅ Successful: {len(successful_configs)}/{len(config_results)}")
    if failed_configs:
        print(f"   ❌ Failed: {failed_configs}")
    
    # Instance creation summary
    print("\n🤖 Instance Creation:")
    successful_instances = [p for p, r in instance_results.items() if r["status"] == "success"]
    skipped_instances = [p for p, r in instance_results.items() if r["status"] == "skipped"]
    failed_instances = [p for p, r in instance_results.items() if r["status"] == "error"]
    
    print(f"   ✅ Successful: {len(successful_instances)}")
    if skipped_instances:
        print(f"   ⏭️  Skipped: {len(skipped_instances)} (missing API keys)")
    if failed_instances:
        print(f"   ❌ Failed: {len(failed_instances)}")
    
    # Predefined configurations summary
    print("\n📋 Predefined Configurations:")
    successful_predefined = [p for p, r in predefined_results.items() if r["status"] == "success"]
    failed_predefined = [p for p, r in predefined_results.items() if r["status"] == "error"]
    
    print(f"   ✅ Working: {len(successful_predefined)}/{len(predefined_results)}")
    if failed_predefined:
        print(f"   ❌ Failed: {failed_predefined}")
    
    # Recommendations
    print("\n💡 Recommendations:")
    if missing_providers:
        print("   🔑 Configure API keys for missing providers to enable full functionality")
    if "Portkey" in partial_providers:
        print("   🔑 Add Portkey virtual keys to enable gateway functionality")
    if failed_configs or failed_instances:
        print("   🔧 Check error messages above for specific configuration issues")
    
    print(f"\n🎯 Overall Status: {len(ready_providers)}/{len(env_status)} providers ready")

def main():
    """Run comprehensive provider and API key test."""
    print("🧪 Comprehensive Provider and API Key Test")
    print("=" * 60)
    
    # Run all tests
    env_status = check_environment_variables()
    config_results = test_provider_config_creation()
    instance_results = test_llm_instance_creation(config_results)
    predefined_results = test_predefined_configurations()
    
    # Generate summary
    generate_summary_report(env_status, config_results, instance_results, predefined_results)
    
    print("\n🎉 Provider and API key test completed!")
    print("\nℹ️  Note: Instance creation is only tested for providers with valid API keys.")
    print("   Configure missing API keys to test full functionality.")

if __name__ == "__main__":
    main() 