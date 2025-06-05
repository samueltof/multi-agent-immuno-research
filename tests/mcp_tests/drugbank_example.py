#!/usr/bin/env python3
"""
Example of using DrugBank with the biomedical researcher agent.

This script demonstrates:
1. How DrugBank is conditionally enabled based on API key availability
2. How to check if DrugBank tools are available
3. How to run research with and without DrugBank
"""

import asyncio
import os
from src.agents.biomedical_researcher import (
    biomedical_researcher_wrapper,
    BiomedicalResearchDeps,
    create_biomedical_mcp_servers
)

async def check_drugbank_availability():
    """Check if DrugBank is available based on API key."""
    drugbank_api_key = os.getenv('DRUGBANK_API_KEY')
    print(f"DrugBank API Key: {'✓ Configured' if drugbank_api_key else '✗ Not configured'}")
    
    # Check MCP servers
    servers = create_biomedical_mcp_servers()
    print(f"Total MCP servers enabled: {len(servers)}")
    
    if drugbank_api_key:
        print("✓ DrugBank tools will be available for drug research")
    else:
        print("✗ DrugBank tools will be skipped")
        print("  To enable DrugBank, set the DRUGBANK_API_KEY environment variable")
    
    return bool(drugbank_api_key)

async def run_research_example():
    """Run a biomedical research example with or without DrugBank."""
    print("\n" + "="*60)
    print("Biomedical Research Example")
    print("="*60)
    
    # Check DrugBank availability
    has_drugbank = await check_drugbank_availability()
    
    # Create research dependencies
    deps = BiomedicalResearchDeps(
        research_focus='cancer treatment',
        time_range='last 2 years'
    )
    
    # Choose research query based on DrugBank availability
    if has_drugbank:
        query = "What are the latest FDA-approved drugs for cancer treatment and their mechanisms of action?"
        print(f"\nResearch Query (with DrugBank): {query}")
    else:
        query = "What are the latest developments in cancer treatment based on recent literature?"
        print(f"\nResearch Query (without DrugBank): {query}")
    
    # Run the research
    print("\nStarting research...")
    try:
        async with biomedical_researcher_wrapper as researcher:
            result = await researcher.run_research(query, deps)
            
            print(f"\nResearch completed!")
            print(f"Summary: {result.summary[:200]}...")
            print(f"Key findings: {len(result.key_findings)} findings")
            print(f"Sources: {len(result.sources)} sources")
            print(f"Confidence: {result.confidence_level:.2f}")
            
            if has_drugbank:
                print("\n✓ Research included access to DrugBank drug database")
            else:
                print("\n⚠ Research was limited to literature databases only")
                print("  For comprehensive drug information, configure DRUGBANK_API_KEY")
                
    except Exception as e:
        print(f"Error during research: {e}")

async def main():
    """Main function to run the example."""
    print("DrugBank Integration Example")
    print("="*30)
    
    await run_research_example()
    
    print(f"\n{'='*60}")
    print("Example completed!")
    print("\nTo enable DrugBank integration:")
    print("1. Get a DrugBank API key from https://drugbank.com/")
    print("2. Set it as an environment variable: export DRUGBANK_API_KEY=your_key_here")
    print("3. Run this example again to see DrugBank tools in action")

if __name__ == "__main__":
    asyncio.run(main()) 