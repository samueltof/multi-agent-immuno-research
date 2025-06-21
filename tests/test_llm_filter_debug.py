#!/usr/bin/env python3
"""
Debug LLM Content Filter
Simple test to debug why LLM filter is returning empty content.
"""

import sys
import os
import time

# Add the project root to Python path
project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, project_root)

from src.tools.crawl import crawl_tool


def test_simple_llm_filter():
    """Test LLM filter with a simple page and debug output."""
    print("🔍 Debugging LLM Content Filter")
    print("=" * 50)
    
    # Use a simple, reliable test page
    test_url = "https://example.com"
    
    print(f"Testing URL: {test_url}")
    print("Using LLM filter with simple instruction...")
    
    # Very simple instruction
    simple_instruction = """
    Extract the main content from this webpage.
    Include all text content.
    Remove only navigation and footer elements.
    Keep the content as-is in markdown format.
    """
    
    start_time = time.time()
    
    try:
        result = crawl_tool(
            test_url, 
            use_llm_filter=True, 
            llm_instruction=simple_instruction
        )
        
        duration = time.time() - start_time
        
        print(f"Duration: {duration:.2f} seconds")
        print(f"Success: {result['success']}")
        print(f"URL: {result['url']}")
        print(f"Title: {result['title']}")
        
        if result['success']:
            markdown = result.get('markdown', '')
            print(f"Markdown length: {len(markdown) if markdown else 0}")
            
            if markdown:
                print(f"Content preview:")
                print("-" * 30)
                print(repr(markdown[:200]))  # Use repr to see whitespace
                print("-" * 30)
            else:
                print("❌ No markdown content returned!")
                
        else:
            print(f"❌ Crawl failed: {result.get('markdown', 'Unknown error')}")
            
        return result
        
    except Exception as e:
        duration = time.time() - start_time
        print(f"❌ Exception after {duration:.2f}s: {e}")
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}


def test_pruning_vs_llm():
    """Compare pruning and LLM filters side by side."""
    print("\n" + "=" * 50)
    print("🔄 Comparing Pruning vs LLM Filter")
    print("=" * 50)
    
    test_url = "https://example.com"
    
    # Test pruning filter first
    print("\n1️⃣ Testing Pruning Filter:")
    start_time = time.time()
    pruning_result = crawl_tool(test_url, use_llm_filter=False)
    pruning_duration = time.time() - start_time
    
    print(f"   Duration: {pruning_duration:.2f}s")
    print(f"   Success: {pruning_result['success']}")
    if pruning_result['success'] and pruning_result.get('markdown'):
        print(f"   Content length: {len(pruning_result['markdown'])}")
        print(f"   Word count: {len(pruning_result['markdown'].split())}")
    else:
        print(f"   Failed: {pruning_result.get('markdown', 'Unknown')}")
    
    # Test LLM filter
    print("\n2️⃣ Testing LLM Filter:")
    start_time = time.time()
    llm_result = crawl_tool(
        test_url, 
        use_llm_filter=True, 
        llm_instruction="Extract all main content. Keep everything readable."
    )
    llm_duration = time.time() - start_time
    
    print(f"   Duration: {llm_duration:.2f}s")
    print(f"   Success: {llm_result['success']}")
    if llm_result['success'] and llm_result.get('markdown'):
        print(f"   Content length: {len(llm_result['markdown'])}")
        print(f"   Word count: {len(llm_result['markdown'].split())}")
    else:
        print(f"   Failed or empty: {llm_result.get('markdown', 'Unknown')}")
    
    # Comparison
    print(f"\n📊 Comparison:")
    print(f"   Pruning: {len(pruning_result.get('markdown', '')) if pruning_result['success'] else 0} chars")
    print(f"   LLM: {len(llm_result.get('markdown', '')) if llm_result['success'] else 0} chars")
    
    return pruning_result, llm_result


def check_api_keys():
    """Check which API keys are available."""
    print("🔑 Checking API Keys:")
    keys_to_check = [
        "OPENAI_API_KEY",
        "BASIC_API_KEY", 
        "REASONING_API_KEY",
        "VL_API_KEY",
        "TAVILY_API_KEY"
    ]
    
    available_keys = []
    for key in keys_to_check:
        value = os.getenv(key)
        status = "✓" if value else "✗"
        print(f"   {status} {key}: {'Set' if value else 'Not set'}")
        if value:
            available_keys.append(key)
    
    print(f"\n📋 Available keys: {len(available_keys)}/{len(keys_to_check)}")
    return available_keys


if __name__ == "__main__":
    print("🚀 LLM Content Filter Debug Test")
    
    # Check API keys
    available_keys = check_api_keys()
    
    if not any(key in available_keys for key in ["OPENAI_API_KEY", "BASIC_API_KEY", "REASONING_API_KEY"]):
        print("\n⚠️  Warning: No suitable API keys found for LLM filtering")
        print("   LLM filter tests may fail")
    
    # Run tests
    print("\n" + "=" * 50)
    test_simple_llm_filter()
    test_pruning_vs_llm()
    
    print("\n🎯 Debug test completed!") 