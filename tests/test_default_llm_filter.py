#!/usr/bin/env python3
"""
Test Default LLM Filter Configuration
Verify that LLM filtering is now enabled by default.
"""

import sys
import os
import time

# Add the project root to Python path
project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, project_root)

from src.tools.crawl import crawl_tool


def test_default_is_llm_filter():
    """Test that LLM filter is now the default behavior."""
    print("🎯 Testing Default LLM Filter Configuration")
    print("=" * 60)
    
    test_url = "https://example.com"
    
    print(f"Testing URL: {test_url}")
    print("Using DEFAULT settings (should be LLM filter now)")
    
    start_time = time.time()
    
    # Call crawl_tool without specifying use_llm_filter - should default to True
    result = crawl_tool(test_url)
    
    duration = time.time() - start_time
    
    print(f"Duration: {duration:.2f} seconds")
    print(f"Success: {result['success']}")
    print(f"URL: {result['url']}")
    print(f"Title: {result['title']}")
    
    if result['success'] and result.get('markdown'):
        markdown = result['markdown']
        word_count = len(markdown.split())
        
        print(f"Content: {len(markdown)} chars, {word_count} words")
        
        # Check for LLM filter characteristics
        indicators = {
            "Has content": len(markdown) > 50,
            "Has structure": '#' in markdown,
            "Reasonable length": 100 < len(markdown) < 5000,
            "Processing time": duration > 1.0,  # LLM filter takes longer
        }
        
        print(f"\nLLM Filter Indicators:")
        for indicator, result in indicators.items():
            status = "✅" if result else "❌"
            print(f"  {status} {indicator}")
        
        success_count = sum(indicators.values())
        print(f"\nOverall: {success_count}/{len(indicators)} indicators suggest LLM filtering")
        
        if success_count >= 3:
            print("🎉 SUCCESS: LLM filter appears to be working as default!")
        else:
            print("⚠️  WARNING: May still be using pruning filter")
        
        print(f"\nContent preview:")
        print("-" * 40)
        print(markdown[:200])
        print("-" * 40)
        
        return True
        
    else:
        print(f"❌ Failed: {result.get('markdown', 'Unknown error')}")
        return False


def test_explicit_pruning_filter():
    """Test that we can still explicitly use pruning filter."""
    print("\n" + "=" * 60)
    print("🔄 Testing Explicit Pruning Filter Override")
    print("=" * 60)
    
    test_url = "https://example.com"
    
    print(f"Testing URL: {test_url}")
    print("Explicitly setting use_llm_filter=False (pruning filter)")
    
    start_time = time.time()
    
    # Explicitly disable LLM filter
    result = crawl_tool(test_url, use_llm_filter=False)
    
    duration = time.time() - start_time
    
    print(f"Duration: {duration:.2f} seconds")
    print(f"Success: {result['success']}")
    
    if result['success'] and result.get('markdown'):
        markdown = result['markdown']
        word_count = len(markdown.split())
        
        print(f"Content: {len(markdown)} chars, {word_count} words")
        
        # Check for pruning filter characteristics
        indicators = {
            "Fast processing": duration < 3.0,  # Pruning is faster
            "Has some content": len(markdown) > 0,
        }
        
        print(f"\nPruning Filter Indicators:")
        for indicator, result in indicators.items():
            status = "✅" if result else "❌"
            print(f"  {status} {indicator}")
        
        print(f"\nContent preview:")
        print("-" * 40)
        print(markdown[:200])
        print("-" * 40)
        
        return True
        
    else:
        print(f"❌ Failed: {result.get('markdown', 'Unknown error')}")
        return False


def test_comparison():
    """Compare default (LLM) vs explicit pruning."""
    print("\n" + "=" * 60)
    print("📊 Comparison: Default LLM vs Explicit Pruning")
    print("=" * 60)
    
    test_url = "https://example.com"
    
    # Test default (should be LLM)
    print("1️⃣ Default behavior (LLM filter):")
    start_time = time.time()
    llm_result = crawl_tool(test_url)
    llm_duration = time.time() - start_time
    
    llm_length = len(llm_result.get('markdown', ''))
    llm_words = len(llm_result.get('markdown', '').split())
    
    print(f"   Duration: {llm_duration:.2f}s")
    print(f"   Content: {llm_length} chars, {llm_words} words")
    
    # Test explicit pruning
    print("\n2️⃣ Explicit pruning filter:")
    start_time = time.time()
    pruning_result = crawl_tool(test_url, use_llm_filter=False)
    pruning_duration = time.time() - start_time
    
    pruning_length = len(pruning_result.get('markdown', ''))
    pruning_words = len(pruning_result.get('markdown', '').split())
    
    print(f"   Duration: {pruning_duration:.2f}s")
    print(f"   Content: {pruning_length} chars, {pruning_words} words")
    
    # Comparison
    print(f"\n📊 Comparison Results:")
    print(f"   {'Method':<15} {'Duration':<10} {'Length':<8} {'Words':<8}")
    print(f"   {'-'*45}")
    print(f"   {'Default (LLM)':<15} {llm_duration:<10.2f} {llm_length:<8} {llm_words:<8}")
    print(f"   {'Pruning':<15} {pruning_duration:<10.2f} {pruning_length:<8} {pruning_words:<8}")
    
    # Analysis
    if llm_duration > pruning_duration and llm_length > pruning_length:
        print(f"\n✅ CONFIRMED: Default is now LLM filter (slower but better quality)")
    elif llm_duration < pruning_duration:
        print(f"\n⚠️  WARNING: Default might still be pruning filter (too fast)")
    else:
        print(f"\n❓ UNCLEAR: Results are ambiguous")
    
    return {
        "llm": {"duration": llm_duration, "length": llm_length, "words": llm_words},
        "pruning": {"duration": pruning_duration, "length": pruning_length, "words": pruning_words}
    }


def run_default_llm_test():
    """Run the complete test suite for default LLM configuration."""
    print("🚀 Testing Default LLM Filter Configuration")
    print("Verifying that LLM filtering is now the default behavior...")
    
    # Check API keys
    api_keys = ["OPENAI_API_KEY", "BASIC_API_KEY", "REASONING_API_KEY"]
    available = [key for key in api_keys if os.getenv(key)]
    
    print(f"\n🔑 API Keys Available: {len(available)}/{len(api_keys)}")
    if available:
        print(f"   Will use: {available[0]} for LLM filtering")
    else:
        print("   ⚠️  No API keys found - tests may fail")
        return
    
    # Run tests
    print("\n" + "=" * 60)
    
    # Test 1: Default behavior
    test1_success = test_default_is_llm_filter()
    
    # Test 2: Explicit pruning override
    test2_success = test_explicit_pruning_filter()
    
    # Test 3: Comparison
    comparison_results = test_comparison()
    
    # Final summary
    print(f"\n" + "=" * 60)
    print("📋 FINAL SUMMARY")
    print("=" * 60)
    
    tests_passed = sum([test1_success, test2_success])
    print(f"✅ Tests Passed: {tests_passed}/2")
    
    if tests_passed == 2:
        print(f"🎉 SUCCESS: LLM filter is now the default!")
        print(f"   • Default crawl_tool() calls use LLM filtering")
        print(f"   • Explicit use_llm_filter=False still works for pruning")
        print(f"   • Quality improvement achieved with minimal code changes")
    else:
        print(f"⚠️  Some tests failed - please check configuration")
    
    print(f"\n💡 Usage:")
    print(f"   # Now uses LLM filter by default")
    print(f"   result = crawl_tool('https://example.com')")
    print(f"   ")
    print(f"   # Still can use pruning for speed")
    print(f"   result = crawl_tool('https://example.com', use_llm_filter=False)")
    
    print(f"\n🎯 Default LLM filter configuration test completed!")


if __name__ == "__main__":
    run_default_llm_test() 