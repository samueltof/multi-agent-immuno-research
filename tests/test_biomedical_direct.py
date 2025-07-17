#!/usr/bin/env python3
"""
Direct test for biomedical researcher to verify Portkey integration works.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agents.biomedical_researcher import BiomedicalResearchDeps, BiomedicalResearchOutput
from pydantic_ai import Agent


async def test_biomedical_model():
    """Test biomedical model creation and a simple call."""
    
    print("🔬 Testing biomedical researcher model...")
    
    try:
        # Import after path setup to avoid import issues
        from agents.biomedical_researcher import get_biomedical_model
        
        # Create model
        model = get_biomedical_model()
        print(f"✅ Model created: {model}")
        
        # Create a simple agent to test the model
        agent = Agent(
            model,
            deps_type=BiomedicalResearchDeps,
            result_type=BiomedicalResearchOutput,
            system_prompt="You are a helpful biomedical researcher. Provide brief responses for testing."
        )
        
        print("✅ Agent created successfully")
        
        # Test dependencies
        deps = BiomedicalResearchDeps(
            user_context="Testing",
            research_focus="AI in immunology"
        )
        
        # Simple test call (this will actually make a request)
        print("🧪 Making test call...")
        result = await agent.run(
            "What is immunology? (Brief answer for testing)",
            deps=deps
        )
        
        print(f"✅ Test call successful!")
        print(f"Result type: {type(result.data)}")
        print(f"Summary: {result.data.summary[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run the test."""
    print("🧪 Direct Biomedical Researcher Test")
    print("=" * 50)
    
    success = await test_biomedical_model()
    
    if success:
        print("\n🎉 SUCCESS! Biomedical researcher works without NotGiven errors!")
    else:
        print("\n💥 FAILED! There are still issues with the integration.")
    
    return success


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1) 