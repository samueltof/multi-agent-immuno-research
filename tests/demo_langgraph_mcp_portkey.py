#!/usr/bin/env python3
"""
Simple demo script to test LangGraph MCP integration with Portkey.

This is a streamlined version of the comprehensive test that focuses on
demonstrating whether Portkey + MCP works with LangGraph vs PydanticAI.

Usage:
    uv run python tests/demo_langgraph_mcp_portkey.py
"""

import asyncio
import os
import sys
import logging

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.test_langgraph_mcp_portkey_integration_fixed import LangGraphMCPTester

async def main():
    """Run the demo."""
    print("🚀 LangGraph + MCP + Portkey Integration Demo")
    print("=" * 60)
    print()
    
    # Setup logging to show progress
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s: %(message)s'
    )
    
    # Environment check
    print("📋 Checking Environment...")
    required_vars = ["OPENAI_API_KEY"]
    optional_vars = ["PORTKEY_API_KEY", "PORTKEY_OPENAI_VIRTUAL_KEY", "DRUGBANK_API_KEY"]
    
    all_good = True
    for var in required_vars:
        if os.getenv(var):
            print(f"  ✅ {var}: Set")
        else:
            print(f"  ❌ {var}: Missing (Required)")
            all_good = False
    
    for var in optional_vars:
        if os.getenv(var):
            print(f"  ✅ {var}: Set")
        else:
            print(f"  ⚠️  {var}: Not set (Optional)")
    
    if not all_good:
        print("\n❌ Missing required environment variables. Please set them and try again.")
        return
    
    print("\n🔬 Running Integration Test...")
    print("-" * 40)
    
    # Run the test
    tester = LangGraphMCPTester()
    try:
        results = await tester.run_comprehensive_test()
        
        print("\n" + "=" * 60)
        print("🎯 FINAL ANALYSIS")
        print("=" * 60)
        
        if results:
            direct_works = results.get("direct_openai", False)
            portkey_works = results.get("portkey", False)
            
            if direct_works and portkey_works:
                print("🎉 SUCCESS: Both Direct OpenAI and Portkey work with LangGraph MCP!")
                print("📝 CONCLUSION: The NotGiven issue may be specific to PydanticAI")
                
            elif direct_works and not portkey_works:
                print("⚠️  PARTIAL: Direct OpenAI works, but Portkey fails with LangGraph MCP")
                print("📝 CONCLUSION: Portkey has broader MCP compatibility issues (not just PydanticAI)")
                
            elif not direct_works:
                print("❌ FAILURE: Even Direct OpenAI fails - MCP setup issue")
                print("📝 CONCLUSION: Problem with MCP server setup or environment")
                
            else:
                print("❓ UNEXPECTED: Portkey works but Direct OpenAI doesn't")
                print("📝 CONCLUSION: Investigation needed")
        else:
            print("❌ TEST FAILED: Could not complete integration test")
            
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main()) 