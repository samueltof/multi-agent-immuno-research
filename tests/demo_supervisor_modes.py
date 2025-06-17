#!/usr/bin/env python3
"""
Demo script showing the difference between Standard and Deep Thinking supervisor modes.
"""

from src.prompts.template import apply_prompt_template
from langchain_core.messages import HumanMessage

def demo_supervisor_modes():
    """Demonstrate the two supervisor modes."""
    
    # Sample state for testing
    base_state = {
        "messages": [
            HumanMessage(content="Find TCR sequences associated with COVID-19 response"),
            HumanMessage(
                content='{"thought": "Research COVID-19 TCR sequences", "title": "COVID-19 TCR Analysis", "steps": [{"agent_name": "data_analyst", "title": "Query VDJdb", "description": "Search VDJdb for COVID-19 TCR sequences"}, {"agent_name": "biomedical_researcher", "title": "Literature search", "description": "Find papers on COVID-19 TCR analysis"}]}',
                name="planner"
            ),
            HumanMessage(
                content="Response from data_analyst:\n\n<response>\nFound 15 TCR sequences in VDJdb associated with COVID-19. Notable patterns show HLA-A*02:01 restriction and specific CDR3 motifs.\n</response>\n\n*Please execute the next step.*",
                name="data_analyst"
            ),
        ],
        "TEAM_MEMBERS": ["researcher", "coder", "browser", "reporter", "data_analyst", "biomedical_researcher"],
        "next": "",
        "full_plan": '{"thought": "Research COVID-19 TCR sequences", "title": "COVID-19 TCR Analysis", "steps": [{"agent_name": "data_analyst", "title": "Query VDJdb", "description": "Search VDJdb for COVID-19 TCR sequences"}]}',
        "search_before_planning": False,
    }
    
    print("=" * 80)
    print("🎯 STANDARD MODE SUPERVISOR")
    print("=" * 80)
    
    # Standard mode
    standard_state = {**base_state, "deep_thinking_mode": False}
    standard_result = apply_prompt_template("supervisor", standard_state)
    
    print("System Prompt (first 500 chars):")
    print("-" * 40)
    system_content = standard_result[0]["content"]
    print(system_content[:500] + "...")
    print("\n")
    
    print("Key Features:")
    print("- Simple routing decisions")
    print("- Basic JSON response format: {\"next\": \"agent_name\"}")
    print("- No specialized TCR/BCR logic")
    print("- No iterative research instructions")
    
    print("\n" + "=" * 80)
    print("🧠 DEEP THINKING MODE SUPERVISOR")
    print("=" * 80)
    
    # Deep thinking mode
    deep_thinking_state = {**base_state, "deep_thinking_mode": True}
    deep_thinking_result = apply_prompt_template("supervisor", deep_thinking_state)
    
    print("System Prompt (first 500 chars):")
    print("-" * 40)
    system_content = deep_thinking_result[0]["content"]
    print(system_content[:500] + "...")
    print("\n")
    
    print("Key Features:")
    print("- Enhanced iterative research orchestration")
    print("- JSON response with reasoning: {\"next\": \"agent_name\", \"reasoning\": \"...\"}")
    print("- Specialized TCR/BCR research patterns")
    print("- Cross-validation between database and literature")
    print("- Discovery analysis and follow-up triggers")
    
    print("\n" + "=" * 80)
    print("CONTENT COMPARISON")
    print("=" * 80)
    
    standard_content = standard_result[0]["content"]
    deep_thinking_content = deep_thinking_result[0]["content"]
    
    print(f"Standard mode length: {len(standard_content)} characters")
    print(f"Deep thinking mode length: {len(deep_thinking_content)} characters")
    
    # Check for key differences
    standard_features = [
        "🎯 STANDARD MODE" in standard_content,
        "🧠 DEEP THINKING MODE" not in standard_content,
        "Research Philosophy" not in standard_content,
        "Decision Framework" not in standard_content,
    ]
    
    deep_thinking_features = [
        "🧠 DEEP THINKING MODE ACTIVATED" in deep_thinking_content,
        "🎯 STANDARD MODE" not in deep_thinking_content,
        "Research Philosophy" in deep_thinking_content,
        "Decision Framework" in deep_thinking_content,
        "Specialized Routing Logic" in deep_thinking_content,
        "Iterative Deepening Triggers" in deep_thinking_content,
    ]
    
    print(f"\nStandard mode features present: {all(standard_features)}")
    print(f"Deep thinking mode features present: {all(deep_thinking_features)}")
    
    if all(standard_features) and all(deep_thinking_features):
        print("\n✅ Both modes are working correctly!")
    else:
        print("\n❌ There may be an issue with mode switching")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    demo_supervisor_modes() 