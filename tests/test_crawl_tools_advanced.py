#!/usr/bin/env python3
"""
Advanced Crawl Tools Testing Script
Tests crawl tools directly with advanced Markdown Generation features from Crawl4AI.
"""

import sys
import os
import asyncio
import time
from typing import List, Dict, Any

# Add the project root to Python path
project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, project_root)

from src.tools.crawl import crawl_tool, crawl_many_tool


def test_single_crawl_tool():
    """Test single URL crawling with advanced markdown generation."""
    print("=" * 60)
    print("Testing Single URL Crawl Tool with Advanced Markdown Generation")
    print("=" * 60)
    
    test_url = "https://docs.crawl4ai.com/core/markdown-generation/"
    
    print(f"Crawling: {test_url}")
    start_time = time.time()
    
    result = crawl_tool(test_url)
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"Crawl completed in {duration:.2f} seconds")
    print(f"Success: {result['success']}")
    print(f"URL: {result['url']}")
    print(f"Title: {result['title']}")
    
    if result['success']:
        markdown_content = result['markdown']
        if markdown_content:
            print(f"Markdown length: {len(markdown_content)} characters")
            print("\nFirst 500 characters of markdown:")
            print("-" * 50)
            print(markdown_content[:500])
            print("-" * 50)
            
            # Check for markdown quality indicators
            indicators = {
                "Has headers": any(line.startswith('#') for line in markdown_content.split('\n')),
                "Has links": '[' in markdown_content and '](' in markdown_content,
                "Has code blocks": '```' in markdown_content,
                "Has bullet points": any(line.strip().startswith('*') or line.strip().startswith('-') 
                                       for line in markdown_content.split('\n')),
                "Contains clean text": len(markdown_content.split()) > 50,
                "Well structured": markdown_content.count('#') > 2,
                "Has numbered lists": any(line.strip() and line.strip()[0].isdigit() 
                                        for line in markdown_content.split('\n')),
                "Token efficient": len(markdown_content.split()) < 5000  # Target for token efficiency
            }
            
            print("\nMarkdown Quality Indicators:")
            for indicator, present in indicators.items():
                status = "✓" if present else "✗"
                print(f"  {status} {indicator}")
            
            # Calculate quality score
            quality_score = sum(indicators.values()) / len(indicators) * 100
            print(f"\nOverall Quality Score: {quality_score:.1f}%")
            
        else:
            print("No markdown content extracted")
    else:
        print(f"Error: {result['markdown']}")
    
    return result


def test_multiple_crawl_tool():
    """Test multiple URL crawling."""
    print("\n" + "=" * 60)
    print("Testing Multiple URL Crawl Tool")
    print("=" * 60)
    
    test_urls = [
        "https://docs.crawl4ai.com/core/markdown-generation/",
        "https://docs.crawl4ai.com/core/simple-crawling/",
        "https://example.com"
    ]
    
    print(f"Crawling {len(test_urls)} URLs:")
    for url in test_urls:
        print(f"  - {url}")
    
    start_time = time.time()
    
    results = crawl_many_tool(test_urls)
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\nBatch crawl completed in {duration:.2f} seconds")
    print(f"Average time per URL: {duration/len(test_urls):.2f} seconds")
    
    success_count = sum(1 for r in results if r['success'])
    print(f"Successful crawls: {success_count}/{len(results)}")
    
    for i, result in enumerate(results):
        print(f"\nResult {i+1}:")
        print(f"  URL: {result['url']}")
        print(f"  Success: {result['success']}")
        print(f"  Title: {result['title']}")
        
        if result['success'] and result['markdown']:
            print(f"  Markdown length: {len(result['markdown'])} characters")
            print(f"  Word count: {len(result['markdown'].split())} words")
            print(f"  Preview: {result['markdown'][:100]}...")
        else:
            print(f"  Error: {result['markdown']}")
    
    return results


def test_markdown_quality():
    """Test different types of content for markdown quality."""
    print("\n" + "=" * 60)
    print("Testing Markdown Quality on Different Content Types")
    print("=" * 60)
    
    content_types = [
        ("Documentation", "https://docs.crawl4ai.com/core/markdown-generation/"),
        ("News Article", "https://techcrunch.com/"),
        ("Simple Page", "https://example.com"),
        ("GitHub README", "https://github.com/unclecode/crawl4ai"),
    ]
    
    results = []
    
    for content_type, url in content_types:
        print(f"\nTesting {content_type}: {url}")
        
        start_time = time.time()
        result = crawl_tool(url)
        duration = time.time() - start_time
        
        print(f"  Time: {duration:.2f}s")
        print(f"  Success: {result['success']}")
        
        if result['success'] and result['markdown']:
            markdown = result['markdown']
            
            # Analyze markdown quality
            analysis = {
                "length": len(markdown),
                "word_count": len(markdown.split()),
                "line_count": len(markdown.split('\n')),
                "has_headers": sum(1 for line in markdown.split('\n') if line.strip().startswith('#')),
                "has_links": markdown.count('[') if '[' in markdown else 0,
                "has_code": markdown.count('```'),
                "has_lists": sum(1 for line in markdown.split('\n') if line.strip().startswith(('*', '-', '1.', '2.'))),
                "structure_score": 0,
                "token_efficiency": "good" if len(markdown.split()) < 3000 else "moderate" if len(markdown.split()) < 6000 else "poor"
            }
            
            # Calculate structure score
            if analysis["has_headers"] > 0:
                analysis["structure_score"] += 30
            if analysis["has_links"] > 0:
                analysis["structure_score"] += 20
            if analysis["word_count"] > 100:
                analysis["structure_score"] += 30
            if analysis["has_code"] > 0:
                analysis["structure_score"] += 20
                
            print(f"  Analysis: {analysis}")
            results.append((content_type, url, result, analysis))
        else:
            print(f"  Failed: {result['markdown']}")
            results.append((content_type, url, result, None))
    
    return results


def test_markdown_generation_comparison():
    """Test and compare different markdown generation approaches."""
    print("\n" + "=" * 60)
    print("Testing Markdown Generation Comparison")
    print("=" * 60)
    
    test_url = "https://docs.crawl4ai.com/core/markdown-generation/"
    
    print(f"Testing URL: {test_url}")
    print("Testing advanced markdown generation with content filtering...")
    
    start_time = time.time()
    result = crawl_tool(test_url)
    duration = time.time() - start_time
    
    print(f"Crawl completed in {duration:.2f} seconds")
    
    if result['success'] and result['markdown']:
        markdown = result['markdown']
        
        print(f"\nAdvanced Markdown Results:")
        print(f"  Length: {len(markdown)} characters")
        print(f"  Word count: {len(markdown.split())} words")
        lines_count = len(markdown.split('\n'))
        print(f"  Lines: {lines_count}")
        
        # Analyze structure
        headers = [line for line in markdown.split('\n') if line.strip().startswith('#')]
        links = markdown.count('[')
        code_blocks = markdown.count('```')
        
        print(f"  Headers: {len(headers)}")
        print(f"  Links: {links}")
        print(f"  Code blocks: {code_blocks}")
        
        # Sample content
        print(f"\nSample content (first 300 chars):")
        print("-" * 40)
        print(markdown[:300])
        print("-" * 40)
        
        # Check for advanced features
        advanced_features = {
            "Clean structure": len(headers) > 2,
            "Good content density": 5 <= len(markdown.split()) / lines_count <= 20,
            "Token efficient": len(markdown.split()) < 4000,
            "Rich formatting": code_blocks > 0 or links > 5,
            "Well organized": any('##' in line for line in headers)
        }
        
        print(f"\nAdvanced Features Analysis:")
        for feature, present in advanced_features.items():
            status = "✓" if present else "✗"
            print(f"  {status} {feature}")
        
        return {
            "result": result,
            "analysis": {
                "word_count": len(markdown.split()),
                "headers": len(headers),
                "links": links,
                "code_blocks": code_blocks,
                "advanced_features": advanced_features,
                "quality_score": sum(advanced_features.values()) / len(advanced_features)
            }
        }
    else:
        print(f"Failed: {result['markdown']}")
        return {"result": result, "analysis": None}


def run_comprehensive_test():
    """Run all tests and provide summary."""
    print("🚀 Starting Comprehensive Crawl Tools Test")
    print("Testing advanced markdown generation features...")
    
    all_results = []
    
    # Test 1: Single URL
    try:
        single_result = test_single_crawl_tool()
        all_results.append(("Single URL", single_result))
    except Exception as e:
        print(f"Single URL test failed: {e}")
        all_results.append(("Single URL", {"success": False, "error": str(e)}))
    
    # Test 2: Multiple URLs
    try:
        multi_results = test_multiple_crawl_tool()
        all_results.append(("Multiple URLs", multi_results))
    except Exception as e:
        print(f"Multiple URL test failed: {e}")
        all_results.append(("Multiple URLs", {"success": False, "error": str(e)}))
    
    # Test 3: Quality analysis
    try:
        quality_results = test_markdown_quality()
        all_results.append(("Quality Analysis", quality_results))
    except Exception as e:
        print(f"Quality analysis test failed: {e}")
        all_results.append(("Quality Analysis", {"success": False, "error": str(e)}))
    
    # Test 4: Advanced comparison
    try:
        comparison_result = test_markdown_generation_comparison()
        all_results.append(("Advanced Comparison", comparison_result))
    except Exception as e:
        print(f"Advanced comparison test failed: {e}")
        all_results.append(("Advanced Comparison", {"success": False, "error": str(e)}))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for test_name, results in all_results:
        print(f"\n{test_name}:")
        if isinstance(results, dict) and not results.get("success", True):
            print(f"  ❌ Failed: {results.get('error', 'Unknown error')}")
        elif isinstance(results, list):
            success_count = sum(1 for r in results if isinstance(r, dict) and r.get("success", False))
            total_count = len(results)
            print(f"  ✅ {success_count}/{total_count} successful")
        else:
            success = results.get("success", False) if isinstance(results, dict) else True
            print(f"  {'✅' if success else '❌'} {'Passed' if success else 'Failed'}")
    
    print(f"\n🎯 Advanced crawl tools testing completed!")
    print("📊 Key improvements with advanced markdown generation:")
    print("   • Content filtering for token efficiency")
    print("   • Better structured markdown output")
    print("   • Preserved links and formatting")
    print("   • Reduced noise and boilerplate")


if __name__ == "__main__":
    # Check environment
    print("Checking environment...")
    
    # Check for required API keys
    api_keys = {
        "REASONING_API_KEY": os.getenv("REASONING_API_KEY"),
        "BASIC_API_KEY": os.getenv("BASIC_API_KEY"),
        "VL_API_KEY": os.getenv("VL_API_KEY"),
        "TAVILY_API_KEY": os.getenv("TAVILY_API_KEY")
    }
    
    for key, value in api_keys.items():
        status = "✓" if value else "✗"
        print(f"  {status} {key}: {'Set' if value else 'Not set'}")
    
    # Run the tests
    run_comprehensive_test() 