"""
Test to isolate OpenAI client issues and avoid Portkey interference.
"""

import os
import sys
import asyncio
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider


class SimpleOutput(BaseModel):
    answer: str = Field(description="Simple answer")


async def test_default_openai_model():
    """Test with completely default OpenAI model - no custom providers."""
    print("🧪 Testing default OpenAI model...")
    
    try:
        # Use completely default OpenAI model
        model = OpenAIModel("gpt-4o-mini")
        
        agent = Agent(
            model,
            output_type=SimpleOutput,
            system_prompt="You are helpful."
        )
        
        result = await agent.run("What is 1+1?")
        print(f"✅ Default OpenAI model successful!")
        print(f"   Answer: {result.output.answer}")
        return True
        
    except Exception as e:
        print(f"❌ Default OpenAI model failed: {e}")
        if "NotGiven" in str(e):
            print("   🎯 NotGiven error with default model!")
        if "portkey" in str(e).lower():
            print("   🎯 Portkey interference detected!")
        
        import traceback
        traceback.print_exc()
        return False


async def test_explicit_openai_provider():
    """Test with explicit OpenAI provider creation."""
    print("\n🧪 Testing explicit OpenAI provider...")
    
    try:
        # Create explicit provider with minimal config
        provider = OpenAIProvider(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url="https://api.openai.com/v1"
        )
        
        model = OpenAIModel("gpt-4o-mini", provider=provider)
        
        agent = Agent(
            model,
            output_type=SimpleOutput,
            system_prompt="You are helpful."
        )
        
        result = await agent.run("What is 2+2?")
        print(f"✅ Explicit provider successful!")
        print(f"   Answer: {result.output.answer}")
        return True
        
    except Exception as e:
        print(f"❌ Explicit provider failed: {e}")
        if "NotGiven" in str(e):
            print("   🎯 NotGiven error with explicit provider!")
        if "portkey" in str(e).lower():
            print("   🎯 Portkey interference detected!")
        
        import traceback
        traceback.print_exc()
        return False


async def test_standard_openai_client():
    """Test with standard OpenAI AsyncClient creation."""
    print("\n🧪 Testing standard OpenAI client...")
    
    try:
        # Import standard OpenAI client
        from openai import AsyncOpenAI
        
        # Create standard client
        client = AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url="https://api.openai.com/v1"
        )
        
        # Create provider with explicit client
        provider = OpenAIProvider(openai_client=client)
        model = OpenAIModel("gpt-4o-mini", provider=provider)
        
        agent = Agent(
            model,
            output_type=SimpleOutput,
            system_prompt="You are helpful."
        )
        
        result = await agent.run("What is 3+3?")
        print(f"✅ Standard client successful!")
        print(f"   Answer: {result.output.answer}")
        return True
        
    except Exception as e:
        print(f"❌ Standard client failed: {e}")
        if "NotGiven" in str(e):
            print("   🎯 NotGiven error with standard client!")
        if "portkey" in str(e).lower():
            print("   🎯 Portkey interference detected!")
        
        import traceback
        traceback.print_exc()
        return False


async def test_without_structured_output():
    """Test without structured output to see if that's the issue."""
    print("\n🧪 Testing without structured output...")
    
    try:
        # Default model, no structured output
        model = OpenAIModel("gpt-4o-mini")
        
        agent = Agent(
            model,
            system_prompt="You are helpful."
            # No output_type
        )
        
        result = await agent.run("What is 4+4?")
        print(f"✅ No structured output successful!")
        print(f"   Result: {str(result.output)[:50]}...")
        return True
        
    except Exception as e:
        print(f"❌ No structured output failed: {e}")
        if "NotGiven" in str(e):
            print("   🎯 NotGiven error even without structured output!")
        if "portkey" in str(e).lower():
            print("   🎯 Portkey interference detected!")
        
        import traceback
        traceback.print_exc()
        return False


async def test_portkey_env_cleanup():
    """Test after cleaning up Portkey environment variables."""
    print("\n🧪 Testing after Portkey env cleanup...")
    
    try:
        # Temporarily remove Portkey env vars
        portkey_vars = {}
        for key in list(os.environ.keys()):
            if "PORTKEY" in key:
                portkey_vars[key] = os.environ.pop(key)
        
        print(f"   Removed {len(portkey_vars)} Portkey env vars")
        
        # Use default model
        model = OpenAIModel("gpt-4o-mini")
        
        agent = Agent(
            model,
            output_type=SimpleOutput,
            system_prompt="You are helpful."
        )
        
        result = await agent.run("What is 5+5?")
        print(f"✅ Portkey cleanup successful!")
        print(f"   Answer: {result.output.answer}")
        
        # Restore env vars
        os.environ.update(portkey_vars)
        return True
        
    except Exception as e:
        print(f"❌ Portkey cleanup failed: {e}")
        if "NotGiven" in str(e):
            print("   🎯 NotGiven error persists after Portkey cleanup!")
        
        # Restore env vars
        os.environ.update(portkey_vars)
        
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all OpenAI isolation tests."""
    print("🧪 OpenAI Client Isolation Tests")
    print("=" * 60)
    
    tests = [
        test_without_structured_output,
        test_default_openai_model,
        test_explicit_openai_provider,
        test_standard_openai_client,
        test_portkey_env_cleanup,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if await test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 OpenAI Isolation Results: {passed}/{total} passed")
    
    if passed > 0:
        print("🎉 Found working OpenAI configuration!")
    else:
        print("⚠️  All OpenAI tests failed - deeper investigation needed")
    
    return passed == total


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1) 