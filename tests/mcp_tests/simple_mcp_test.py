#!/usr/bin/env python3
"""
Simple MCP servers test - focuses on core functionality.

This script tests the raw MCP server capabilities without complex validation.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.agents.biomedical_researcher import create_biomedical_mcp_servers
from pydantic_ai.mcp import MCPServerStdio

async def test_individual_mcp_servers():
    """Test each MCP server individually to see their raw capabilities."""
    print("="*60)
    print("Individual MCP Server Tests")
    print("="*60)
    
    # Get MCP servers
    servers = create_biomedical_mcp_servers()
    print(f"Testing {len(servers)} MCP servers\n")
    
    results = {}
    
    for i, server in enumerate(servers):
        server_name = f"Server {i+1}"
        print(f"Testing {server_name}...")
        
        try:
            # Start the server
            async with server:
                # List available tools
                tools_response = await server.list_tools()
                tools = tools_response.tools if hasattr(tools_response, 'tools') else []
                
                print(f"  ✓ {server_name} started successfully")
                print(f"  ✓ Found {len(tools)} tools:")
                
                for tool in tools[:3]:  # Show first 3 tools
                    print(f"    - {tool.name}: {tool.description[:60]}...")
                
                if len(tools) > 3:
                    print(f"    ... and {len(tools) - 3} more tools")
                
                results[server_name] = True
                print(f"  ✓ {server_name} test PASSED\n")
                
        except Exception as e:
            print(f"  ✗ {server_name} test FAILED: {e}\n")
            results[server_name] = False
    
    return results

async def test_pubmed_search():
    """Test PubMed search directly using MCP."""
    print("="*60)
    print("Direct PubMed Search Test")
    print("="*60)
    
    # Find PubMed server
    servers = create_biomedical_mcp_servers()
    pubmed_server = None
    
    for server in servers:
        try:
            async with server:
                tools_response = await server.list_tools()
                tools = tools_response.tools if hasattr(tools_response, 'tools') else []
                
                # Check if this server has PubMed tools
                tool_names = [tool.name for tool in tools]
                if any('pubmed' in name.lower() for name in tool_names):
                    pubmed_server = server
                    break
        except:
            continue
    
    if not pubmed_server:
        print("✗ PubMed server not found")
        return False
    
    try:
        async with pubmed_server:
            # Try a simple PubMed search
            result = await pubmed_server.call_tool(
                "pubmed_search_articles",
                arguments={"query": "COVID-19", "max_results": 3}
            )
            
            print("✓ PubMed search successful!")
            print(f"Result: {str(result.content)[:300]}...")
            return True
            
    except Exception as e:
        print(f"✗ PubMed search failed: {e}")
        return False

async def test_clinical_trials_search():
    """Test ClinicalTrials search directly using MCP."""
    print("\n" + "="*60)
    print("Direct ClinicalTrials Search Test")
    print("="*60)
    
    # Find ClinicalTrials server
    servers = create_biomedical_mcp_servers()
    ct_server = None
    
    for server in servers:
        try:
            async with server:
                tools_response = await server.list_tools()
                tools = tools_response.tools if hasattr(tools_response, 'tools') else []
                
                # Check if this server has ClinicalTrials tools
                tool_names = [tool.name for tool in tools]
                if any('clinical' in name.lower() for name in tool_names):
                    ct_server = server
                    break
        except:
            continue
    
    if not ct_server:
        print("✗ ClinicalTrials server not found")
        return False
    
    try:
        async with ct_server:
            # Try a simple ClinicalTrials search
            result = await ct_server.call_tool(
                "clinicaltrials_search_studies",
                arguments={"query": "cancer", "max_results": 3}
            )
            
            print("✓ ClinicalTrials search successful!")
            print(f"Result: {str(result.content)[:300]}...")
            return True
            
    except Exception as e:
        print(f"✗ ClinicalTrials search failed: {e}")
        return False

async def main():
    """Run simplified MCP tests."""
    print("Simple MCP Servers Test")
    print("=" * 30)
    print("Testing core MCP functionality without complex validation\n")
    
    # Test 1: Individual server capabilities
    server_results = await test_individual_mcp_servers()
    
    # Test 2: Direct PubMed functionality
    pubmed_result = await test_pubmed_search()
    
    # Test 3: Direct ClinicalTrials functionality
    ct_result = await test_clinical_trials_search()
    
    # Summary
    print("\n" + "="*60)
    print("SIMPLE TEST RESULTS")
    print("="*60)
    
    total_servers = len(server_results)
    working_servers = sum(server_results.values())
    
    print(f"MCP Server Initialization: {working_servers}/{total_servers} servers working")
    for server, result in server_results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {server}: {status}")
    
    print(f"\nDirect API Tests:")
    print(f"  PubMed Search: {'✓ PASS' if pubmed_result else '✗ FAIL'}")
    print(f"  ClinicalTrials Search: {'✓ PASS' if ct_result else '✗ FAIL'}")
    
    # Overall assessment
    all_basic_working = working_servers == total_servers
    api_tests_working = pubmed_result and ct_result
    
    if all_basic_working and api_tests_working:
        print("\n🎉 Core MCP functionality is working!")
        print("✓ All MCP servers can be initialized")
        print("✓ PubMed database access is working") 
        print("✓ ClinicalTrials database access is working")
        print("\nYour biomedical research agent has solid database connectivity!")
    elif all_basic_working:
        print("\n✅ MCP servers are initializing correctly")
        print("⚠️  Some API calls may need refinement, but the foundation is solid")
    else:
        print("\n⚠️  Some MCP servers have issues - check your configuration")
    
    return all_basic_working

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1) 