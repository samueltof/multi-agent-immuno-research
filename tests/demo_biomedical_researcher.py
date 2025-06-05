#!/usr/bin/env python3
"""
Demo script for the Biomedical Researcher Agent.

This script demonstrates how to use the PydanticAI + MCP biomedical researcher
agent both standalone and integrated with LangGraph.
"""

import asyncio
import os
import sys
from typing import Dict, Any
import logging

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agents.biomedical_researcher import (
    BiomedicalResearchDeps,
    BiomedicalResearchOutput,
    biomedical_researcher_wrapper,
    biomedical_researcher_node,
    biomedical_researcher_agent
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def demo_standalone_research():
    """Demonstrate standalone biomedical research."""
    print("\n" + "="*60)
    print("DEMO: Standalone Biomedical Research")
    print("="*60)
    
    # Example research query
    query = "What are the latest developments in CAR-T cell therapy for cancer treatment?"
    
    # Set up research context
    deps = BiomedicalResearchDeps(
        user_context="Clinical oncologist",
        research_focus="cancer immunotherapy",
        time_range="last 18 months",
        preferred_databases=["pubmed", "clinicaltrials", "biorxiv"]
    )
    
    print(f"Research Query: {query}")
    print(f"Research Context: {deps}")
    print("\nConducting research...\n")
    
    try:
        # Use the biomedical researcher wrapper
        async with biomedical_researcher_wrapper as researcher:
            result = await researcher.run_research(query, deps)
            
            # Display results
            print("📊 RESEARCH RESULTS")
            print("-" * 40)
            print(f"📝 Summary: {result.summary}")
            print(f"\n🔍 Key Findings:")
            for i, finding in enumerate(result.key_findings, 1):
                print(f"  {i}. {finding}")
            
            print(f"\n📚 Sources:")
            for i, source in enumerate(result.sources, 1):
                print(f"  {i}. {source}")
            
            print(f"\n💡 Recommendations:")
            for i, rec in enumerate(result.recommendations, 1):
                print(f"  {i}. {rec}")
            
            print(f"\n🎯 Confidence Level: {result.confidence_level:.1%}")
    
    except Exception as e:
        print(f"❌ Error during research: {e}")
        logger.exception("Research failed")


async def demo_streaming_research():
    """Demonstrate streaming research output."""
    print("\n" + "="*60)
    print("DEMO: Streaming Biomedical Research")
    print("="*60)
    
    query = "Compare the effectiveness of different COVID-19 vaccines"
    deps = BiomedicalResearchDeps(
        user_context="Public health researcher",
        research_focus="vaccine effectiveness",
        time_range="last 2 years"
    )
    
    print(f"Research Query: {query}")
    print("Streaming results...\n")
    
    try:
        async with biomedical_researcher_wrapper as researcher:
            print("📊 STREAMING RESEARCH OUTPUT:")
            print("-" * 40)
            
            async for chunk in researcher.run_research_stream(query, deps):
                print(chunk, end='', flush=True)
            
            print("\n\n✅ Streaming completed!")
    
    except Exception as e:
        print(f"❌ Error during streaming research: {e}")
        logger.exception("Streaming research failed")


async def demo_langgraph_integration():
    """Demonstrate LangGraph integration."""
    print("\n" + "="*60)
    print("DEMO: LangGraph Integration")
    print("="*60)
    
    # Create a state similar to what LangGraph would use
    state = {
        "messages": ["Research the current state of gene therapy for treating inherited blindness"],
        "user_context": "Ophthalmology researcher",
        "research_focus": "gene therapy",
        "time_range": "last 3 years",
        "preferred_databases": ["pubmed", "clinicaltrials"]
    }
    
    print("Initial State:")
    for key, value in state.items():
        print(f"  {key}: {value}")
    
    print("\nRunning biomedical research node...\n")
    
    try:
        # Run the LangGraph node
        result_state = await biomedical_researcher_node(state)
        
        print("📊 LANGGRAPH NODE RESULTS")
        print("-" * 40)
        
        # Display the research result
        if "biomedical_research_result" in result_state:
            research_result = result_state["biomedical_research_result"]
            print(f"📝 Research Summary: {research_result.summary}")
            print(f"🔍 Number of Key Findings: {len(research_result.key_findings)}")
            print(f"📚 Number of Sources: {len(research_result.sources)}")
            print(f"🎯 Confidence Level: {research_result.confidence_level:.1%}")
        
        # Display updated messages
        print(f"\n💬 Updated Messages ({len(result_state.get('messages', []))}):")
        for i, msg in enumerate(result_state.get('messages', []), 1):
            print(f"  {i}. {str(msg)[:100]}...")
    
    except Exception as e:
        print(f"❌ Error in LangGraph integration: {e}")
        logger.exception("LangGraph integration failed")


async def demo_multiple_queries():
    """Demonstrate handling multiple research queries."""
    print("\n" + "="*60)
    print("DEMO: Multiple Research Queries")
    print("="*60)
    
    queries = [
        "What are the latest biomarkers for early Alzheimer's detection?",
        "How effective are new treatments for multiple sclerosis?",
        "What progress has been made in CRISPR-based therapies?"
    ]
    
    deps = BiomedicalResearchDeps(
        user_context="Neurologist and researcher",
        research_focus="neurological disorders",
        time_range="last year"
    )
    
    async with biomedical_researcher_wrapper as researcher:
        for i, query in enumerate(queries, 1):
            print(f"\n🔬 Research Query {i}: {query}")
            print("-" * 50)
            
            try:
                result = await researcher.run_research(query, deps)
                print(f"✅ Summary: {result.summary[:150]}...")
                print(f"📊 Findings: {len(result.key_findings)} key findings")
                print(f"🎯 Confidence: {result.confidence_level:.1%}")
            
            except Exception as e:
                print(f"❌ Error: {e}")


def demo_configuration():
    """Demonstrate configuration options."""
    print("\n" + "="*60)
    print("DEMO: Configuration Options")
    print("="*60)
    
    print("🔧 Available Configuration:")
    print("1. Environment Variables:")
    print("   - OPENAI_API_KEY or LLM_API_KEY")
    print("   - ANTHROPIC_API_KEY")
    print("   - DRUGBANK_API_KEY (optional)")
    print("   - BASE_URL (for custom LLM endpoints)")
    
    print("\n2. Biomedical MCP Servers:")
    print("   - PubMed (pubmed_*)")
    print("   - BioRxiv/MedRxiv (biorxiv_*)")
    print("   - ClinicalTrials.gov (clinicaltrials_*)")
    print("   - DrugBank (drugbank_*) - requires API key")
    print("   - Open Targets (opentargets_*)")
    
    print("\n3. Research Dependencies:")
    print("   - user_context: Context about the researcher")
    print("   - research_focus: Specific area of research")
    print("   - time_range: Time frame for the research")
    print("   - preferred_databases: List of preferred databases")
    
    print("\n4. LangGraph Integration:")
    print("   - Use biomedical_researcher_node() for standard integration")
    print("   - Use biomedical_researcher_streaming_node() for streaming")
    print("   - State should include 'messages' and optional context")


async def interactive_demo():
    """Interactive demo allowing user input."""
    print("\n" + "="*60)
    print("INTERACTIVE DEMO: Biomedical Research")
    print("="*60)
    print("Enter your biomedical research queries (type 'quit' to exit)")
    
    deps = BiomedicalResearchDeps(
        user_context="Researcher",
        research_focus="General biomedical research",
        time_range="last year"
    )
    
    async with biomedical_researcher_wrapper as researcher:
        while True:
            try:
                query = input("\n🔬 Enter your research query: ").strip()
                
                if query.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if not query:
                    print("Please enter a valid query.")
                    continue
                
                print(f"\n🔍 Researching: {query}")
                print("⏳ Please wait...")
                
                result = await researcher.run_research(query, deps)
                
                print(f"\n📊 Results:")
                print(f"📝 {result.summary}")
                if result.key_findings:
                    print(f"🔍 Key findings: {len(result.key_findings)}")
                if result.sources:
                    print(f"📚 Sources found: {len(result.sources)}")
                print(f"🎯 Confidence: {result.confidence_level:.1%}")
            
            except KeyboardInterrupt:
                print("\n👋 Demo interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")


async def main():
    """Run all demos."""
    print("🧬 BIOMEDICAL RESEARCHER AGENT DEMO")
    print("🔬 PydanticAI + MCP + LangGraph Integration")
    
    # Show configuration
    demo_configuration()
    
    # Check if we can run the demos (need API keys)
    if not (os.getenv('OPENAI_API_KEY') or os.getenv('LLM_API_KEY') or os.getenv('ANTHROPIC_API_KEY')):
        print("\n⚠️  WARNING: No API keys found in environment variables.")
        print("Set OPENAI_API_KEY, LLM_API_KEY, or ANTHROPIC_API_KEY to run live demos.")
        print("Demos will run in mock mode for illustration purposes.")
        return
    
    try:
        # Run the demos
        await demo_standalone_research()
        await demo_streaming_research()
        await demo_langgraph_integration()
        await demo_multiple_queries()
        
        # Optionally run interactive demo
        if '--interactive' in sys.argv:
            await interactive_demo()
    
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        logger.exception("Demo execution failed")
    
    print("\n✅ Demo completed!")


if __name__ == "__main__":
    asyncio.run(main()) 