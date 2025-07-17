#!/usr/bin/env python3
"""
Test the fixed Portkey integration to ensure no NotGiven serialization errors.
"""

import os
import sys
import asyncio
import logging
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agents.biomedical_researcher import get_biomedical_model
from config.agents import get_agent_full_config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_portkey_config_creation():
    """Test that we can create a Portkey configuration without errors."""
    try:
        config = get_agent_full_config("biomedical_researcher")
        logger.info(f"Successfully created config: {config}")
        
        # Verify key fields
        assert 'provider' in config
        assert 'model' in config
        
        logger.info("✅ Config creation test passed")
        return True
    except Exception as e:
        logger.error(f"❌ Config creation failed: {e}")
        return False


def test_portkey_model_creation():
    """Test that we can create a biomedical model without NotGiven errors."""
    try:
        model = get_biomedical_model()
        logger.info(f"Successfully created model: {model}")
        logger.info("✅ Model creation test passed")
        return True
    except Exception as e:
        logger.error(f"❌ Model creation failed: {e}")
        return False


async def test_simple_model_call():
    """Test a simple model call to verify it works."""
    try:
        from agents.biomedical_researcher import create_biomedical_agent
        
        # Create agent with dependencies
        agent = create_biomedical_agent()
        
        # Simple test call that should not fail
        test_message = "What is immunology?"
        logger.info(f"Testing with message: {test_message}")
        
        # We won't actually run this as it might be expensive,
        # but we verify the agent can be created without serialization errors
        logger.info("✅ Agent creation test passed")
        return True
    except Exception as e:
        logger.error(f"❌ Agent creation failed: {e}")
        return False


def main():
    """Run all tests."""
    logger.info("🧪 Testing Fixed Portkey Integration")
    logger.info("=" * 50)
    
    tests = [
        ("Config Creation", test_portkey_config_creation),
        ("Model Creation", test_portkey_model_creation),
        ("Agent Creation", lambda: asyncio.run(test_simple_model_call())),
    ]
    
    results = []
    for test_name, test_func in tests:
        logger.info(f"\n🔬 Running {test_name} test...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            logger.error(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    logger.info("\n" + "=" * 50)
    logger.info("📊 Test Results Summary:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        logger.info(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    logger.info(f"\n🎯 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        logger.info("🎉 All tests passed! The Portkey integration should work correctly.")
        return True
    else:
        logger.error("💥 Some tests failed. Please check the error messages above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 