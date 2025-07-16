"""
Minimal test to debug the NotGiven serialization issue.
This test isolates PydanticAI usage to find where the error occurs.
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
    """Simple output schema for testing."""
    answer: str = Field(description="A simple answer")


async def test_minimal_pydantic_ai():
    """Test minimal PydanticAI usage to isolate NotGiven error."""
    print("🧪 Testing minimal PydanticAI usage...")
    
    try:
        # Create a simple OpenAI model
        model = OpenAIModel("gpt-4o-mini")
        
        # Create a simple agent
        agent = Agent(
            model,
            output_type=SimpleOutput,
            system_prompt="You are a helpful assistant. Always provide a simple answer."
        )
        
        # Test basic run
        query = "What is 1+1?"
        print(f"   Running query: {query}")
        result = await agent.run(query)
        print(f"✅ Minimal test successful!")
        print(f"   Answer: {result.output.answer}")
        return True
        
    except Exception as e:
        print(f"❌ Minimal test failed: {e}")
        print(f"   Error type: {type(e).__name__}")
        
        if "NotGiven" in str(e):
            print("   🎯 NotGiven error in minimal test!")
        
        # Print full traceback for debugging
        import traceback
        print("   Full traceback:")
        traceback.print_exc()
        
        return False


async def test_with_custom_provider():
    """Test with custom OpenAI provider to see if the issue is provider-specific."""
    print("\n🧪 Testing with custom OpenAI provider...")
    
    try:
        # Create custom provider with explicit settings
        provider = OpenAIProvider(
            api_key=os.getenv("OPENAI_API_KEY", "dummy-key"),
            base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        )
        
        # Create model with custom provider
        model = OpenAIModel("gpt-4o-mini", provider=provider)
        
        # Create agent
        agent = Agent(
            model,
            output_type=SimpleOutput,
            system_prompt="You are a helpful assistant."
        )
        
        # Test run
        query = "What is the capital of France?"
        result = await agent.run(query)
        print(f"✅ Custom provider test successful!")
        print(f"   Answer: {result.output.answer}")
        return True
        
    except Exception as e:
        print(f"❌ Custom provider test failed: {e}")
        if "NotGiven" in str(e):
            print("   🎯 NotGiven error with custom provider!")
            
        import traceback
        traceback.print_exc()
        return False


async def test_biomedical_model_isolated():
    """Test just the biomedical model creation without running it."""
    print("\n🧪 Testing isolated biomedical model creation...")
    
    try:
        from src.agents.biomedical_researcher import get_biomedical_model
        
        # Just create the model, don't run it
        model = get_biomedical_model()
        print(f"✅ Biomedical model created: {type(model).__name__}")
        
        # Try to get model info without running
        print(f"   Model name: {model.model_name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Biomedical model creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_simple_agent_without_output_type():
    """Test agent without structured output to see if that's the issue."""
    print("\n🧪 Testing agent without structured output...")
    
    try:
        # Create simple model
        model = OpenAIModel("gpt-4o-mini")
        
        # Create agent without output_type
        agent = Agent(
            model,
            system_prompt="You are a helpful assistant."
            # No output_type specified
        )
        
        # Test run
        query = "What is 2+2?"
        result = await agent.run(query)
        print(f"✅ No-output-type test successful!")
        print(f"   Result type: {type(result.output)}")
        print(f"   Result: {str(result.output)[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ No-output-type test failed: {e}")
        if "NotGiven" in str(e):
            print("   🎯 NotGiven error even without output type!")
            
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all debug tests."""
    print("🧪 NotGiven Serialization Debug Tests")
    print("=" * 60)
    
    tests = [
        test_minimal_pydantic_ai,
        test_simple_agent_without_output_type,
        test_with_custom_provider,
        test_biomedical_model_isolated,
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
    print(f"📊 Debug Test Results: {passed}/{total} passed")
    
    return passed == total


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1) 