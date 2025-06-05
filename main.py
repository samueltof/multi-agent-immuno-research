"""
Entry point script for the LangGraph Demo.
"""

import argparse
from src.workflow import run_agent_workflow

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the LangGraph agent workflow")
    parser.add_argument("query", nargs="*", help="The user query")
    parser.add_argument("--deep-thinking", action="store_true", default=True, 
                       help="Enable deep thinking mode (default: True)")
    parser.add_argument("--no-deep-thinking", action="store_true", 
                       help="Disable deep thinking mode")
    parser.add_argument("--search-before-planning", action="store_true", default=True,
                       help="Enable search before planning mode (default: True)")
    parser.add_argument("--no-search-before-planning", action="store_true",
                       help="Disable search before planning mode")
    
    args = parser.parse_args()
    
    # Handle query input
    if args.query:
        user_query = " ".join(args.query)
    else:
        user_query = input("Enter your query: ")
    
    # Handle boolean flags
    deep_thinking_mode = args.deep_thinking and not args.no_deep_thinking
    search_before_planning = args.search_before_planning and not args.no_search_before_planning

    result = run_agent_workflow(
        user_input=user_query, 
        deep_thinking_mode=deep_thinking_mode,
        search_before_planning=search_before_planning,
        debug=True
    )

    # Print the conversation history
    print("\n=== Conversation History ===")
    for message in result["messages"]:
        role = message.type
        print(f"\n[{role.upper()}]: {message.content}")
