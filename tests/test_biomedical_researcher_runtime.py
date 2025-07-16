"""
Test script for runtime behavior of the biomedical researcher agent.
This script tests actual research execution to identify the NotGiven serialization error.
"""

import os
import sys
import asyncio
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from unittest.mock import patch, MagicMock
from src.agents.biomedical_researcher import (
    BiomedicalResearcherWrapper, 
    BiomedicalResearchDeps,
    create_biomedical_researcher_agent
)


async def test_simple_research_query():
    """Test a simple biomedical research query to check for runtime issues."""
    print("\n🧪 Testing simple biomedical research query...")
    
    try:
        # Create a simple research query
        query = "What are the latest findings on T-cell receptors in COVID-19 immunity?"
        
        # Create dependencies
        deps = BiomedicalResearchDeps(
            user_context="Research on COVID-19 immunity",
            research_focus="T-cell receptors",
            time_range="2020-2024",
            preferred_databases=["pubmed"]
        )
        
        # Test with BiomedicalResearcherWrapper
        async with BiomedicalResearcherWrapper() as researcher:
            result = await researcher.run_research(query, deps)
            print(f"✅ Research completed successfully!")
            print(f"   Summary: {result.summary[:100]}...")
            print(f"   Key findings: {len(result.key_findings)}")
            print(f"   Sources: {len(result.sources)}")
            print(f"   Confidence: {result.confidence_level}")
            return True
            
    except Exception as e:
        print(f"❌ Runtime test failed: {e}")
        print(f"   Error type: {type(e).__name__}")
        
        # Check if it's the NotGiven serialization error
        if "NotGiven" in str(e) and "JSON serializable" in str(e):
            print("   🎯 This is the NotGiven serialization error!")
        
        return False


async def test_minimal_agent_creation():
    """Test minimal agent creation without MCP servers."""
    print("\n🧪 Testing minimal agent creation...")
    
    try:
        # Create agent without MCP servers for isolation
        agent = create_biomedical_researcher_agent()
        print(f"✅ Agent created successfully: {type(agent).__name__}")
        
        # Try to create a run context (this might trigger the error)
        query = "What is a T-cell receptor?"
        deps = BiomedicalResearchDeps()
        
        # Test basic run without MCP servers
        print("   Testing basic agent run...")
        result = await agent.run(query, deps=deps)
        print(f"✅ Basic run successful!")
        print(f"   Result type: {type(result.output)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Minimal agent test failed: {e}")
        print(f"   Error type: {type(e).__name__}")
        
        # Check for specific error patterns
        if "NotGiven" in str(e):
            print("   🎯 NotGiven error detected in minimal test!")
        if "JSON serializable" in str(e):
            print("   🎯 JSON serialization error detected!")
            
        return False


async def test_openai_direct_vs_portkey():
    """Test OpenAI direct vs Portkey to isolate provider-specific issues."""
    print("\n🧪 Testing OpenAI direct vs Portkey providers...")
    
    # Test with direct OpenAI first
    print("   Testing with direct OpenAI...")
    try:
        # Temporarily change config to use direct OpenAI
        from src.config.agents import AGENT_LLM_MAP
        original_config = AGENT_LLM_MAP["biomedical_researcher"]
        AGENT_LLM_MAP["biomedical_researcher"] = ["openai", "gpt-4o-mini"]
        
        query = "What is immunology?"
        deps = BiomedicalResearchDeps()
        
        async with BiomedicalResearcherWrapper() as researcher:
            result = await researcher.run_research(query, deps)
            print(f"✅ OpenAI direct test successful!")
            
    except Exception as e:
        print(f"❌ OpenAI direct test failed: {e}")
        if "NotGiven" in str(e):
            print("   🎯 NotGiven error with OpenAI direct!")
    finally:
        # Restore original config
        AGENT_LLM_MAP["biomedical_researcher"] = original_config
    
    # Test with Portkey OpenAI
    print("   Testing with Portkey OpenAI...")
    try:
        # Change config to use Portkey OpenAI
        AGENT_LLM_MAP["biomedical_researcher"] = ["portkey_openai", "gpt-4o-mini"]
        
        async with BiomedicalResearcherWrapper() as researcher:
            result = await researcher.run_research(query, deps)
            print(f"✅ Portkey OpenAI test successful!")
            
    except Exception as e:
        print(f"❌ Portkey OpenAI test failed: {e}")
        if "NotGiven" in str(e):
            print("   🎯 NotGiven error with Portkey OpenAI!")
    finally:
        # Restore original config
        AGENT_LLM_MAP["biomedical_researcher"] = original_config
    
    return True


async def test_without_mcp_servers():
    """Test the agent without MCP servers to isolate MCP-related issues."""
    print("\n🧪 Testing without MCP servers...")
    
    try:
        # Mock MCP servers to return empty list
        with patch('src.agents.biomedical_researcher.create_biomedical_mcp_servers', return_value=[]):
            query = "What is a T-cell?"
            deps = BiomedicalResearchDeps()
            
            async with BiomedicalResearcherWrapper() as researcher:
                result = await researcher.run_research(query, deps)
                print(f"✅ Test without MCP servers successful!")
                return True
                
    except Exception as e:
        print(f"❌ Test without MCP servers failed: {e}")
        if "NotGiven" in str(e):
            print("   🎯 NotGiven error persists without MCP servers!")
        return False


async def main():
    """Run all runtime tests for the biomedical researcher."""
    print("🧪 Biomedical Researcher Runtime Tests")
    print("=" * 60)
    
    tests = [
        test_minimal_agent_creation,
        test_without_mcp_servers,
        test_openai_direct_vs_portkey,
        test_simple_research_query,
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
    print(f"📊 Runtime Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All runtime tests passed! No NotGiven issues detected!")
    else:
        print("⚠️  Some runtime tests failed. Check the output above for details.")
    
    return passed == total


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1) 