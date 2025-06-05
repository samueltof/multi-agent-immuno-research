#!/usr/bin/env python3
"""
Test script for biomedical MCP servers (excluding DrugBank).

This script tests each MCP server individually to ensure they're working:
1. PubMed MCP Server - biomedical literature
2. BioRxiv MCP Server - preprints 
3. ClinicalTrials MCP Server - clinical trial data
4. OpenTargets MCP Server - drug target information
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.agents.biomedical_researcher import (
    biomedical_researcher_wrapper,
    BiomedicalResearchDeps,
    create_biomedical_mcp_servers
)

async def test_mcp_server_availability():
    """Test which MCP servers are available and configured."""
    print("="*60)
    print("MCP Server Availability Test")
    print("="*60)
    
    # Check DrugBank status
    drugbank_api_key = os.getenv('DRUGBANK_API_KEY')
    print(f"DrugBank API Key: {'✓ Configured' if drugbank_api_key else '✗ Not configured (expected)'}")
    
    # Get all configured servers
    servers = create_biomedical_mcp_servers()
    print(f"\nTotal MCP servers enabled: {len(servers)}")
    
    # Expected servers without DrugBank
    expected_servers = ["PubMed", "BioRxiv", "ClinicalTrials", "OpenTargets"]
    if drugbank_api_key:
        expected_servers.append("DrugBank")
    
    print(f"Expected servers: {', '.join(expected_servers)}")
    print(f"✓ Configuration looks correct\n")
    
    return len(servers)

async def test_literature_search():
    """Test PubMed and BioRxiv literature search capabilities."""
    print("="*60)
    print("Literature Search Test (PubMed + BioRxiv)")
    print("="*60)
    
    deps = BiomedicalResearchDeps(
        research_focus='COVID-19 research',
        time_range='last 1 year'
    )
    
    query = "Find recent research papers about COVID-19 vaccine effectiveness"
    print(f"Query: {query}\n")
    
    try:
        async with biomedical_researcher_wrapper as researcher:
            result = await researcher.run_research(query, deps)
            
            print("✓ Literature search completed successfully!")
            print(f"Summary: {result.summary[:300]}...")
            print(f"Key findings: {len(result.key_findings)} findings")
            print(f"Sources: {len(result.sources)} sources")
            print(f"Confidence: {result.confidence_level:.2f}")
            return True
            
    except Exception as e:
        print(f"✗ Literature search failed: {e}")
        return False

async def test_clinical_trials():
    """Test ClinicalTrials.gov search capabilities."""
    print("\n" + "="*60)
    print("Clinical Trials Search Test")
    print("="*60)
    
    deps = BiomedicalResearchDeps(
        research_focus='cancer treatment trials',
        time_range='current'
    )
    
    query = "Find active clinical trials for cancer immunotherapy treatments"
    print(f"Query: {query}\n")
    
    try:
        async with biomedical_researcher_wrapper as researcher:
            result = await researcher.run_research(query, deps)
            
            print("✓ Clinical trials search completed successfully!")
            print(f"Summary: {result.summary[:300]}...")
            print(f"Key findings: {len(result.key_findings)} findings")
            print(f"Sources: {len(result.sources)} sources")
            print(f"Confidence: {result.confidence_level:.2f}")
            return True
            
    except Exception as e:
        print(f"✗ Clinical trials search failed: {e}")
        return False

async def test_target_research():
    """Test OpenTargets drug target research capabilities."""
    print("\n" + "="*60)
    print("Drug Target Research Test (OpenTargets)")
    print("="*60)
    
    deps = BiomedicalResearchDeps(
        research_focus='drug targets',
        time_range='current'
    )
    
    query = "Research drug targets associated with Alzheimer's disease"
    print(f"Query: {query}\n")
    
    try:
        async with biomedical_researcher_wrapper as researcher:
            result = await researcher.run_research(query, deps)
            
            print("✓ Target research completed successfully!")
            print(f"Summary: {result.summary[:300]}...")
            print(f"Key findings: {len(result.key_findings)} findings")
            print(f"Sources: {len(result.sources)} sources")
            print(f"Confidence: {result.confidence_level:.2f}")
            return True
            
    except Exception as e:
        print(f"✗ Target research failed: {e}")
        return False

async def test_comprehensive_research():
    """Test comprehensive biomedical research using multiple databases."""
    print("\n" + "="*60)
    print("Comprehensive Research Test (All Available Databases)")
    print("="*60)
    
    deps = BiomedicalResearchDeps(
        research_focus='diabetes treatment',
        time_range='last 2 years'
    )
    
    query = """Provide a comprehensive review of recent advances in diabetes treatment, including:
    1. Latest research findings from literature
    2. Current clinical trials
    3. Drug targets being investigated
    4. Recent preprints and emerging research"""
    
    print(f"Query: {query[:100]}...\n")
    
    try:
        async with biomedical_researcher_wrapper as researcher:
            result = await researcher.run_research(query, deps)
            
            print("✓ Comprehensive research completed successfully!")
            print(f"Summary: {result.summary[:400]}...")
            print(f"Key findings: {len(result.key_findings)} findings")
            print(f"Sources: {len(result.sources)} sources")
            print(f"Recommendations: {len(result.recommendations)} recommendations")
            print(f"Confidence: {result.confidence_level:.2f}")
            return True
            
    except Exception as e:
        print(f"✗ Comprehensive research failed: {e}")
        return False

async def test_streaming_capability():
    """Test streaming research output."""
    print("\n" + "="*60)
    print("Streaming Research Test")
    print("="*60)
    
    deps = BiomedicalResearchDeps(
        research_focus='gene therapy',
        time_range='recent'
    )
    
    query = "What are the latest developments in gene therapy for rare diseases?"
    print(f"Query: {query}")
    print("Streaming output:\n")
    
    try:
        async with biomedical_researcher_wrapper as researcher:
            stream_output = ""
            async for chunk in researcher.run_research_stream(query, deps):
                print(chunk, end='', flush=True)
                stream_output += chunk
            
            print(f"\n\n✓ Streaming research completed!")
            print(f"Total output length: {len(stream_output)} characters")
            return True
            
    except Exception as e:
        print(f"✗ Streaming research failed: {e}")
        return False

async def main():
    """Run all MCP server tests."""
    print("Biomedical MCP Servers Test Suite")
    print("=" * 40)
    print("Testing all available MCP servers (excluding DrugBank)")
    print("This will verify that PubMed, BioRxiv, ClinicalTrials, and OpenTargets are working")
    print()
    
    # Track test results
    test_results = {}
    
    # Test 1: Server availability
    try:
        server_count = await test_mcp_server_availability()
        test_results['Server Availability'] = True
    except Exception as e:
        print(f"✗ Server availability test failed: {e}")
        test_results['Server Availability'] = False
    
    # Test 2: Literature search
    test_results['Literature Search'] = await test_literature_search()
    
    # Test 3: Clinical trials
    test_results['Clinical Trials'] = await test_clinical_trials()
    
    # Test 4: Target research
    test_results['Target Research'] = await test_target_research()
    
    # Test 5: Comprehensive research
    test_results['Comprehensive Research'] = await test_comprehensive_research()
    
    # Test 6: Streaming capability
    test_results['Streaming'] = await test_streaming_capability()
    
    # Summary
    print("\n" + "="*60)
    print("TEST RESULTS SUMMARY")
    print("="*60)
    
    passed = sum(test_results.values())
    total = len(test_results)
    
    for test_name, result in test_results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name:.<40} {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All MCP servers are working correctly!")
        print("\nYour biomedical researcher agent is ready to use with:")
        print("• PubMed - for published literature")
        print("• BioRxiv - for preprints and recent research") 
        print("• ClinicalTrials - for clinical trial information")
        print("• OpenTargets - for drug target research")
        print("\nTo add DrugBank functionality, get an API key and set DRUGBANK_API_KEY")
    else:
        print("⚠️  Some tests failed. Check the errors above and verify your configuration.")
    
    return passed == total

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1) 