#!/usr/bin/env python3
"""
Test LLM Content Filter vs Default Pruning Filter
Compare the quality and efficiency of different content filtering approaches.
"""

import sys
import os
import asyncio
import time
from typing import Dict, Any

# Add the project root to Python path
project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, project_root)

from src.tools.crawl import crawl_tool


def test_default_pruning_filter():
    """Test the default pruning-based content filtering."""
    print("=" * 60)
    print("Testing Default Pruning Content Filter")
    print("=" * 60)
    
    test_url = "https://docs.crawl4ai.com/core/markdown-generation/"
    
    print(f"Crawling: {test_url}")
    print("Using: Default Pruning Filter")
    
    start_time = time.time()
    
    # Test with default pruning filter (use_llm_filter=False)
    result = crawl_tool(test_url, use_llm_filter=False)
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"Crawl completed in {duration:.2f} seconds")
    print(f"Success: {result['success']}")
    
    if result['success'] and result['markdown']:
        markdown = result['markdown']
        
        analysis = {
            "filter_type": "pruning",
            "length": len(markdown),
            "word_count": len(markdown.split()),
            "line_count": len(markdown.split('\n')),
            "duration": duration,
            "has_headers": sum(1 for line in markdown.split('\n') if line.strip().startswith('#')),
            "has_links": markdown.count('['),
            "has_code": markdown.count('```'),
            "structure_quality": "good" if markdown.count('#') > 5 else "moderate"
        }
        
        print(f"\nPruning Filter Analysis:")
        for key, value in analysis.items():
            print(f"  {key}: {value}")
        
        print(f"\nSample content (first 300 chars):")
        print("-" * 40)
        print(markdown[:300])
        print("-" * 40)
        
        return analysis
    else:
        print(f"Failed: {result['markdown']}")
        return {"filter_type": "pruning", "success": False, "error": result['markdown']}


def test_llm_content_filter():
    """Test the LLM-based content filtering."""
    print("\n" + "=" * 60)
    print("Testing LLM Content Filter")
    print("=" * 60)
    
    test_url = "https://docs.crawl4ai.com/core/markdown-generation/"
    
    # Custom instruction for technical documentation
    custom_instruction = """
    Extract the core technical documentation content.
    Focus on:
    - Main concepts and explanations
    - Code examples and syntax
    - Configuration options and parameters
    - Step-by-step instructions
    - Important warnings and notes
    
    Exclude:
    - Navigation menus and breadcrumbs
    - Sidebar content and advertisements
    - Footer information
    - Search boxes and UI elements
    
    Format as clean markdown with:
    - Clear headers and subheaders
    - Properly formatted code blocks
    - Preserved important links
    - Clean bullet points and lists
    
    Optimize for clarity and token efficiency.
    """
    
    print(f"Crawling: {test_url}")
    print("Using: LLM Content Filter (GPT-4o-mini)")
    
    start_time = time.time()
    
    try:
        # Test with LLM filter
        result = crawl_tool(
            test_url, 
            use_llm_filter=True, 
            llm_instruction=custom_instruction
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"Crawl completed in {duration:.2f} seconds")
        print(f"Success: {result['success']}")
        
        if result['success'] and result['markdown']:
            markdown = result['markdown']
            
            analysis = {
                "filter_type": "llm",
                "length": len(markdown),
                "word_count": len(markdown.split()),
                "line_count": len(markdown.split('\n')),
                "duration": duration,
                "has_headers": sum(1 for line in markdown.split('\n') if line.strip().startswith('#')),
                "has_links": markdown.count('['),
                "has_code": markdown.count('```'),
                "structure_quality": "excellent" if markdown.count('#') > 5 and markdown.count('```') > 2 else "good"
            }
            
            print(f"\nLLM Filter Analysis:")
            for key, value in analysis.items():
                print(f"  {key}: {value}")
            
            print(f"\nSample content (first 300 chars):")
            print("-" * 40)
            print(markdown[:300])
            print("-" * 40)
            
            return analysis
        else:
            print(f"Failed: {result['markdown']}")
            return {"filter_type": "llm", "success": False, "error": result['markdown']}
            
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        print(f"LLM filter failed after {duration:.2f} seconds")
        print(f"Error: {e}")
        return {"filter_type": "llm", "success": False, "error": str(e), "duration": duration}


def test_llm_filter_different_content():
    """Test LLM filter on different types of content."""
    print("\n" + "=" * 60)
    print("Testing LLM Filter on Different Content Types")
    print("=" * 60)
    
    content_types = [
        ("Technical Blog", "https://dev.to/ali_dz/crawl4ai-the-ultimate-guide-to-ai-ready-web-crawling-2620"),
        ("News Article", "https://techcrunch.com/"),
        ("GitHub Repository", "https://github.com/unclecode/crawl4ai"),
    ]
    
    results = []
    
    for content_type, url in content_types:
        print(f"\nTesting {content_type}: {url}")
        
        # Instruction tailored for different content types
        if "blog" in content_type.lower() or "technical" in content_type.lower():
            instruction = """
            Extract the main article content and technical information.
            Include code examples, explanations, and key insights.
            Remove navigation, ads, and comments.
            """
        elif "news" in content_type.lower():
            instruction = """
            Extract the main news article content.
            Include headline, main story, and key facts.
            Remove navigation, ads, and related articles sidebar.
            """
        else:  # GitHub
            instruction = """
            Extract the main README content and documentation.
            Include installation instructions, usage examples, and features.
            Remove navigation, file browser, and sidebar elements.
            """
        
        start_time = time.time()
        
        try:
            result = crawl_tool(
                url, 
                use_llm_filter=True, 
                llm_instruction=instruction
            )
            
            duration = time.time() - start_time
            
            if result['success'] and result['markdown']:
                markdown = result['markdown']
                
                analysis = {
                    "content_type": content_type,
                    "url": url,
                    "word_count": len(markdown.split()),
                    "duration": duration,
                    "quality_score": min(100, (len(markdown.split()) / 10) + (markdown.count('#') * 5))
                }
                
                print(f"  ✅ Success - {analysis['word_count']} words in {duration:.2f}s")
                results.append(analysis)
            else:
                print(f"  ❌ Failed: {result['markdown']}")
                results.append({
                    "content_type": content_type,
                    "url": url,
                    "success": False,
                    "error": result['markdown']
                })
                
        except Exception as e:
            duration = time.time() - start_time
            print(f"  ❌ Error: {e}")
            results.append({
                "content_type": content_type,
                "url": url,
                "success": False,
                "error": str(e),
                "duration": duration
            })
    
    return results


def compare_filters():
    """Compare the two filtering approaches side by side."""
    print("\n" + "=" * 60)
    print("FILTER COMPARISON SUMMARY")
    print("=" * 60)
    
    print("\n🔄 Running comparison tests...")
    
    # Test both filters
    pruning_result = test_default_pruning_filter()
    llm_result = test_llm_content_filter()
    
    print("\n📊 COMPARISON RESULTS:")
    print("=" * 40)
    
    if pruning_result.get("success", True) and llm_result.get("success", True):
        print(f"{'Metric':<20} {'Pruning':<15} {'LLM':<15} {'Winner'}")
        print("-" * 65)
        
        metrics = [
            ("Word Count", "word_count"),
            ("Duration (s)", "duration"),
            ("Headers", "has_headers"),
            ("Code Blocks", "has_code"),
            ("Links", "has_links")
        ]
        
        for metric_name, metric_key in metrics:
            pruning_val = pruning_result.get(metric_key, 0)
            llm_val = llm_result.get(metric_key, 0)
            
            if metric_key == "duration":
                winner = "Pruning" if pruning_val < llm_val else "LLM"
                print(f"{metric_name:<20} {pruning_val:<15.2f} {llm_val:<15.2f} {winner}")
            else:
                winner = "LLM" if llm_val > pruning_val else "Pruning"
                print(f"{metric_name:<20} {pruning_val:<15} {llm_val:<15} {winner}")
        
        print("\n💡 Recommendations:")
        print("   • Use Pruning Filter for: Speed, cost efficiency, simple content")
        print("   • Use LLM Filter for: Complex content, high quality extraction, research")
        
    else:
        print("⚠️  Could not complete comparison due to errors")
        if not pruning_result.get("success", True):
            print(f"   Pruning filter error: {pruning_result.get('error', 'Unknown')}")
        if not llm_result.get("success", True):
            print(f"   LLM filter error: {llm_result.get('error', 'Unknown')}")


def run_comprehensive_llm_filter_test():
    """Run all LLM filter tests."""
    print("🚀 Starting Comprehensive LLM Content Filter Test")
    print("Comparing Pruning vs LLM-based content filtering...")
    
    # Check for OpenAI API key
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        print("⚠️  Warning: OPENAI_API_KEY not set. LLM filter tests may fail.")
        print("   Set your OpenAI API key to test LLM filtering:")
        print("   export OPENAI_API_KEY='your-api-key'")
    else:
        print("✅ OpenAI API key found")
    
    # Run comparison
    compare_filters()
    
    # Test on different content types
    print("\n🔍 Testing LLM filter on different content types...")
    diverse_results = test_llm_filter_different_content()
    
    print(f"\n📈 Diverse Content Test Results:")
    success_count = sum(1 for r in diverse_results if r.get("success", True))
    print(f"   Successful: {success_count}/{len(diverse_results)}")
    
    for result in diverse_results:
        if result.get("success", True):
            print(f"   ✅ {result['content_type']}: {result.get('word_count', 0)} words")
        else:
            print(f"   ❌ {result['content_type']}: Failed")
    
    print(f"\n🎯 LLM Content Filter testing completed!")


if __name__ == "__main__":
    # Check environment
    print("Checking environment...")
    
    # Check for required API keys
    api_keys = {
        "REASONING_API_KEY": os.getenv("REASONING_API_KEY"),
        "BASIC_API_KEY": os.getenv("BASIC_API_KEY"),
        "VL_API_KEY": os.getenv("VL_API_KEY"),
        "TAVILY_API_KEY": os.getenv("TAVILY_API_KEY"),
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY")
    }
    
    for key, value in api_keys.items():
        status = "✓" if value else "✗"
        print(f"  {status} {key}: {'Set' if value else 'Not set'}")
    
    # Run the tests
    run_comprehensive_llm_filter_test() 