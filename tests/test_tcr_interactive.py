#!/usr/bin/env python3
"""
Interactive test for TCR Data Analyst Agent

Run this script to interactively test the TCR agent with real queries.
"""

import sys
import os
sys.path.append('src')

from langchain_core.messages import HumanMessage
from src.agents.agents import tcr_data_analyst_agent

def test_tcr_agent_interactive():
    """Interactive testing of the TCR agent."""
    print("🧬 TCR Data Analyst Agent - Interactive Test")
    print("=" * 50)
    print("This will test the TCR agent with sample queries.")
    print("Note: Make sure your .env file has LLM API keys configured.\n")
    
    # Sample test queries
    test_queries = [
        "What is the VDJdb database schema?",
        "Show me sample data from the TCR sequences table",
        "Calculate diversity metrics for TCR clonotypes",
        "Analyze CDR3 motifs: CASSLAPGATNEKLFF,CASSLKPSYNEQFF,CASSIRDSSGANVLTF"
    ]
    
    print("Available test queries:")
    for i, query in enumerate(test_queries, 1):
        print(f"{i}. {query}")
    
    print("\nSelect a query to test (1-4) or type 'custom' for your own query:")
    
    while True:
        choice = input("\nEnter choice (1-4, 'custom', or 'quit'): ").strip().lower()
        
        if choice == 'quit':
            print("Goodbye!")
            break
        elif choice == 'custom':
            query = input("Enter your TCR analysis query: ").strip()
        elif choice in ['1', '2', '3', '4']:
            query = test_queries[int(choice) - 1]
        else:
            print("Invalid choice. Please try again.")
            continue
        
        if not query:
            print("Empty query. Please try again.")
            continue
        
        print(f"\n🧬 Testing query: {query}")
        print("-" * 50)
        
        try:
            # Create test state
            test_state = {
                "messages": [HumanMessage(content=query)],
                "TEAM_MEMBERS": ["tcr_data_analyst"],
                "next": "",
                "full_plan": "",
                "deep_thinking_mode": False,
                "search_before_planning": False,
            }
            
            print("Calling TCR data analyst agent...")
            result = tcr_data_analyst_agent(test_state)
            
            print("\n✅ Result:")
            if "messages" in result and result["messages"]:
                for msg in result["messages"]:
                    if hasattr(msg, 'content'):
                        print(msg.content)
                    else:
                        print(msg)
            else:
                print("No messages in result:", result)
            
        except Exception as e:
            print(f"❌ Error testing query: {e}")
            import traceback
            traceback.print_exc()
        
        print("\n" + "=" * 50)

if __name__ == "__main__":
    # Check if environment is set up
    if not os.path.exists('.env'):
        print("⚠️  No .env file found. Create one with your LLM API keys.")
        print("Example:")
        print("REASONING_API_KEY=your_api_key")
        print("REASONING_MODEL=gpt-4o")
        print("")
    
    test_tcr_agent_interactive() 