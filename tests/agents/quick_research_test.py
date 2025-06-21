#!/usr/bin/env python3
"""
Quick test script for the Research Agent.
Use this for rapid testing after crawling framework modifications.
"""

import os
import sys
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.agents import research_agent
from langchain_core.messages import HumanMessage


def quick_test(query: str = "What are the latest developments in AI?"):
    """Quick test of the research agent."""
    print(f"🔬 Quick Research Test")
    print(f"📋 Query: {query}")
    print("-" * 50)
    
    # Create simple state
    state = {
        "messages": [HumanMessage(content=query)],
        "CURRENT_TIME": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    
    try:
        print("🏁 Starting research...")
        start_time = datetime.now()
        
        result = research_agent.invoke(state)
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print(f"✅ Completed in {duration:.2f} seconds")
        
        if result.get("messages"):
            response = result["messages"][-1].content
            print(f"\n📝 Response ({len(response)} chars):")
            print("-" * 50)
            print(response)
            print("-" * 50)
            
            # Quick analysis
            indicators = {
                "Has URLs": "http" in response.lower(),
                "Has crawled content": "crawled content" in response.lower(),
                "Has search results": "search results" in response.lower(),
                "Proper formatting": "##" in response or "**" in response,
            }
            
            print("\n🔍 Quick Analysis:")
            for indicator, present in indicators.items():
                status = "✅" if present else "❌"
                print(f"   {status} {indicator}")
                
        else:
            print("❌ No response received")
            
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        quick_test(query)
    else:
        print("Usage: python quick_research_test.py [your query here]")
        print("Or run without arguments for default test")
        quick_test() 