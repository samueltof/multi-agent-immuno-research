#!/usr/bin/env python3
"""
Test 04: Interactive TCR Analysis Demo

Interactive demonstration of the complete TCR analysis system with real agent execution.
This is the most complex test - allows manual testing with full system integration.
"""

import sys
import os
import json
import time
from typing import Dict, Any, Optional
sys.path.append('src')

from langchain_core.messages import HumanMessage, AIMessage
from src.agents.agents import tcr_data_analyst_agent

class TCRInteractiveDemo:
    """Interactive demo system for TCR analysis"""
    
    def __init__(self):
        self.session_history = []
        self.demo_scenarios = self._load_demo_scenarios()
        self.current_scenario = None
    
    def _load_demo_scenarios(self):
        """Load predefined demo scenarios"""
        return {
            "1": {
                "name": "VDJdb Database Exploration",
                "description": "Explore the VDJdb database structure and sample data",
                "queries": [
                    "What is the VDJdb database schema?",
                    "Show me some sample TCR sequences from the database"
                ]
            },
            "2": {
                "name": "TCR Diversity Analysis",
                "description": "Analyze TCR repertoire diversity metrics",
                "queries": [
                    "Calculate diversity metrics for the sample TCR dataset"
                ]
            },
            "3": {
                "name": "CDR3 Motif Discovery", 
                "description": "Analyze CDR3 sequence patterns and motifs",
                "queries": [
                    "Analyze these CDR3 sequences for motifs: CASSLAPGATNEKLFF,CASSLKPSYNEQFF,CASSIRDSSGANVLTF"
                ]
            }
        }
    
    def display_welcome(self):
        """Display welcome message and system info"""
        print("🧬" + "=" * 60)
        print("   TCR DATA ANALYST INTERACTIVE DEMO")
        print("=" * 60)
        print("\n🎯 SYSTEM CAPABILITIES:")
        print("   • VDJdb database analysis")
        print("   • TCR diversity metrics")
        print("   • CDR3 motif analysis")
        print("   • Repertoire comparison")
        
        self._check_environment()
    
    def _check_environment(self):
        """Check if environment is ready"""
        print("\n🔍 ENVIRONMENT CHECK:")
        
        if os.path.exists('.env'):
            print("   ✅ .env file found")
        else:
            print("   ⚠️  .env file missing")
        
        vdjdb_path = os.getenv("VDJDB_SQLITE_PATH", "data/vdjdb.db")
        if os.path.exists(vdjdb_path):
            print(f"   ✅ VDJdb database found")
        else:
            print(f"   ⚠️  VDJdb database missing")
    
    def display_scenarios(self):
        """Display available demo scenarios"""
        print("\n📋 DEMO SCENARIOS:")
        print("-" * 40)
        
        for key, scenario in self.demo_scenarios.items():
            print(f"   {key}. {scenario['name']}")
            print(f"      {scenario['description']}")
            print()
    
    def run_scenario(self, scenario_key: str):
        """Run a specific demo scenario"""
        if scenario_key not in self.demo_scenarios:
            print(f"❌ Invalid scenario: {scenario_key}")
            return
        
        scenario = self.demo_scenarios[scenario_key]
        print(f"\n🧪 RUNNING: {scenario['name']}")
        print("=" * 50)
        
        for i, query in enumerate(scenario['queries'], 1):
            print(f"Query {i}: {query}")
            print("-" * 30)
            
            self._execute_query(query)
            
            if i < len(scenario['queries']):
                input("\nPress Enter to continue...")
    
    def _execute_query(self, query: str) -> bool:
        """Execute a single query with the TCR agent"""
        try:
            state = {
                "messages": [HumanMessage(content=query)],
                "TEAM_MEMBERS": ["tcr_data_analyst"],
                "next": "",
                "full_plan": "",
                "deep_thinking_mode": True,
                "search_before_planning": True,
            }
            
            start_time = time.time()
            print("🤖 Processing...")
            
            result = tcr_data_analyst_agent(state)
            execution_time = time.time() - start_time
            
            print(f"\n✅ Completed in {execution_time:.2f}s")
            print("📊 RESULTS:")
            print("-" * 30)
            
            if "messages" in result and result["messages"]:
                for msg in result["messages"]:
                    if hasattr(msg, 'content'):
                        print(msg.content)
                    else:
                        print(str(msg))
            else:
                print(f"Result: {result}")
            
            self.session_history.append({
                "query": query,
                "result": result,
                "execution_time": execution_time
            })
            
            return True
            
        except Exception as e:
            print(f"❌ Failed: {e}")
            return False
    
    def custom_query_mode(self):
        """Allow custom queries"""
        print("\n🛠️  CUSTOM QUERY MODE")
        print("=" * 30)
        print("Type 'quit' to exit")
        
        while True:
            query = input("\n🧬 Query > ").strip()
            
            if query.lower() == 'quit':
                break
            elif not query:
                continue
            
            self._execute_query(query)
    
    def run(self):
        """Main demo loop"""
        self.display_welcome()
        
        while True:
            print("\n🚀 OPTIONS:")
            print("   s) Demo scenarios")
            print("   c) Custom queries")
            print("   q) Quit")
            
            choice = input("\nSelect: ").strip().lower()
            
            if choice == 'q':
                print("\n👋 Demo complete!")
                break
            elif choice == 's':
                self.display_scenarios()
                scenario = input("Select (1-3): ").strip()
                self.run_scenario(scenario)
            elif choice == 'c':
                self.custom_query_mode()

def main():
    """Main entry point"""
    print("🔬 TCR Interactive Demo")
    demo = TCRInteractiveDemo()
    demo.run()

if __name__ == "__main__":
    main() 