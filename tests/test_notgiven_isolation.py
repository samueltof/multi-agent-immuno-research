"""
Isolate exactly where the NotGiven error occurs in biomedical researcher.
"""

import os
import sys
import asyncio
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pydantic import BaseModel, Field
from pydantic_ai import Agent
from src.agents.biomedical_researcher import (
    get_biomedical_model,
    BiomedicalResearchOutput,
    BiomedicalResearchDeps,
    create_biomedical_researcher_agent
)


async def test_simple_agent_with_biomedical_output():
    """Test PydanticAI agent with the exact biomedical output schema."""
    print("🧪 Testing agent with biomedical output schema...")
    
    try:
        # Use simple model
        model = get_biomedical_model()
        
        # Create agent with biomedical output schema but no other complexity
        agent = Agent(
            model,
            output_type=BiomedicalResearchOutput,
            system_prompt="You are a helpful assistant. Provide biomedical research insights."
        )
        
        # Test simple query
        query = "What is a virus?"
        result = await agent.run(query)
        print(f"✅ Biomedical output schema test successful!")
        print(f"   Summary: {result.output.summary[:50]}...")
        return True
        
    except Exception as e:
        print(f"❌ Biomedical output schema test failed: {e}")
        if "NotGiven" in str(e):
            print("   🎯 NotGiven error with biomedical output schema!")
        
        import traceback
        traceback.print_exc()
        return False


async def test_agent_with_deps():
    """Test agent with dependencies but no MCP servers."""
    print("\n🧪 Testing agent with dependencies...")
    
    try:
        model = get_biomedical_model()
        
        # Create agent with deps but no MCP
        agent = Agent(
            model,
            deps_type=BiomedicalResearchDeps,
            output_type=BiomedicalResearchOutput,
            system_prompt="You are a helpful assistant."
        )
        
        # Create deps
        deps = BiomedicalResearchDeps(
            user_context="Test research",
            research_focus="virology"
        )
        
        query = "What is a virus?"
        result = await agent.run(query, deps=deps)
        print(f"✅ Dependencies test successful!")
        print(f"   Summary: {result.output.summary[:50]}...")
        return True
        
    except Exception as e:
        print(f"❌ Dependencies test failed: {e}")
        if "NotGiven" in str(e):
            print("   🎯 NotGiven error with dependencies!")
        
        import traceback
        traceback.print_exc()
        return False


async def test_agent_with_retries():
    """Test agent with retries parameter."""
    print("\n🧪 Testing agent with retries...")
    
    try:
        model = get_biomedical_model()
        
        # Add retries parameter
        agent = Agent(
            model,
            deps_type=BiomedicalResearchDeps,
            output_type=BiomedicalResearchOutput,
            retries=3,
            system_prompt="You are a helpful assistant."
        )
        
        deps = BiomedicalResearchDeps()
        query = "What is a virus?"
        result = await agent.run(query, deps=deps)
        print(f"✅ Retries test successful!")
        print(f"   Summary: {result.output.summary[:50]}...")
        return True
        
    except Exception as e:
        print(f"❌ Retries test failed: {e}")
        if "NotGiven" in str(e):
            print("   🎯 NotGiven error with retries!")
        
        import traceback
        traceback.print_exc()
        return False


async def test_agent_with_instructions():
    """Test agent with instructions parameter."""
    print("\n🧪 Testing agent with instructions...")
    
    try:
        model = get_biomedical_model()
        
        # Add instructions parameter
        agent = Agent(
            model,
            deps_type=BiomedicalResearchDeps,
            output_type=BiomedicalResearchOutput,
            retries=3,
            system_prompt="You are a helpful assistant.",
            instructions="Focus on providing comprehensive, evidence-based biomedical research insights."
        )
        
        deps = BiomedicalResearchDeps()
        query = "What is a virus?"
        result = await agent.run(query, deps=deps)
        print(f"✅ Instructions test successful!")
        print(f"   Summary: {result.output.summary[:50]}...")
        return True
        
    except Exception as e:
        print(f"❌ Instructions test failed: {e}")
        if "NotGiven" in str(e):
            print("   🎯 NotGiven error with instructions!")
        
        import traceback
        traceback.print_exc()
        return False


async def test_exact_biomedical_agent_no_mcp():
    """Test the exact biomedical agent creation but without MCP servers."""
    print("\n🧪 Testing exact biomedical agent (no MCP)...")
    
    try:
        from unittest.mock import patch
        
        # Mock MCP servers to return empty list
        with patch('src.agents.biomedical_researcher.create_biomedical_mcp_servers', return_value=[]):
            agent = create_biomedical_researcher_agent()
            
            deps = BiomedicalResearchDeps()
            query = "What is a virus?"
            result = await agent.run(query, deps=deps)
            print(f"✅ Exact biomedical agent (no MCP) test successful!")
            print(f"   Summary: {result.output.summary[:50]}...")
            return True
        
    except Exception as e:
        print(f"❌ Exact biomedical agent (no MCP) test failed: {e}")
        if "NotGiven" in str(e):
            print("   🎯 NotGiven error with exact biomedical agent!")
        
        import traceback
        traceback.print_exc()
        return False


async def test_debug_request_params():
    """Test with debug logging to see what parameters are being sent."""
    print("\n🧪 Testing with debug request parameters...")
    
    try:
        import logging
        logging.getLogger("openai").setLevel(logging.DEBUG)
        logging.getLogger("httpx").setLevel(logging.DEBUG)
        
        from unittest.mock import patch
        
        # Mock MCP servers to return empty list
        with patch('src.agents.biomedical_researcher.create_biomedical_mcp_servers', return_value=[]):
            agent = create_biomedical_researcher_agent()
            
            deps = BiomedicalResearchDeps()
            query = "What is a virus?"
            result = await agent.run(query, deps=deps)
            print(f"✅ Debug request test successful!")
            return True
        
    except Exception as e:
        print(f"❌ Debug request test failed: {e}")
        if "NotGiven" in str(e):
            print("   🎯 NotGiven error in debug request!")
            print("   This suggests the error is in the HTTP request parameters")
        
        # Don't print full traceback for this one to keep output clean
        return False


async def main():
    """Run all isolation tests."""
    print("🧪 NotGiven Error Isolation Tests")
    print("=" * 60)
    
    tests = [
        test_simple_agent_with_biomedical_output,
        test_agent_with_deps,
        test_agent_with_retries,
        test_agent_with_instructions,
        test_exact_biomedical_agent_no_mcp,
        test_debug_request_params,
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
    print(f"📊 Isolation Test Results: {passed}/{total} passed")
    
    if passed < total:
        print("\n🔍 Analysis:")
        print("   - If early tests pass but later ones fail, the issue is with specific parameters")
        print("   - If all tests fail, the issue is fundamental to the biomedical output schema")
        print("   - If only the exact agent test fails, the issue is with MCP or prompt processing")
    
    return passed == total


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1) 