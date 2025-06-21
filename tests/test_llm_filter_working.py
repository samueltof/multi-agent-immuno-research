#!/usr/bin/env python3
"""
LLM Content Filter - Working Demo
Demonstrates the working LLM content filter with realistic content examples.
"""

import sys
import os
import time
from typing import Dict, Any

# Add the project root to Python path
project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, project_root)

from src.tools.crawl import crawl_tool


def test_llm_filter_showcase():
    """Showcase the LLM filter with different types of content."""
    print("🎯 LLM Content Filter Showcase")
    print("=" * 60)
    
    # Test cases with different content types and instructions
    test_cases = [
        {
            "name": "Simple Documentation",
            "url": "https://example.com",
            "instruction": """
            Extract the main content from this webpage.
            Keep all text content and format as clean markdown.
            Remove navigation and footer elements only.
            """
        },
        {
            "name": "Technical Documentation (Focused)",
            "url": "https://docs.python.org/3/tutorial/introduction.html",
            "instruction": """
            Extract the core tutorial content and code examples.
            Focus on:
            - Main explanations and concepts
            - Code examples with proper formatting
            - Important notes and warnings
            
            Exclude:
            - Navigation menus
            - Sidebar content
            - Footer information
            
            Format as clean markdown with proper code blocks.
            """
        },
        {
            "name": "News Article (Content-Focused)",
            "url": "https://www.bbc.com/news",
            "instruction": """
            Extract the main news headlines and article summaries.
            Include:
            - Headlines and main stories
            - Article summaries
            - Key information
            
            Exclude:
            - Navigation menus
            - Advertisement sections
            - Social media widgets
            - Related links sidebar
            
            Format as clean markdown with clear headers.
            """
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}️⃣ Testing: {test_case['name']}")
        print(f"URL: {test_case['url']}")
        print("-" * 50)
        
        start_time = time.time()
        
        try:
            # Test with LLM filter
            result = crawl_tool(
                test_case['url'],
                use_llm_filter=True,
                llm_instruction=test_case['instruction']
            )
            
            duration = time.time() - start_time
            
            if result['success'] and result.get('markdown'):
                markdown = result['markdown']
                word_count = len(markdown.split())
                
                analysis = {
                    "name": test_case['name'],
                    "url": test_case['url'],
                    "success": True,
                    "duration": duration,
                    "content_length": len(markdown),
                    "word_count": word_count,
                    "has_headers": sum(1 for line in markdown.split('\n') if line.strip().startswith('#')),
                    "has_code": markdown.count('```'),
                    "has_links": markdown.count('['),
                    "quality_score": min(100, (word_count / 5) + (markdown.count('#') * 10))
                }
                
                print(f"✅ Success!")
                print(f"   Duration: {duration:.2f}s")
                print(f"   Content: {len(markdown)} chars, {word_count} words")
                print(f"   Structure: {analysis['has_headers']} headers, {analysis['has_code']} code blocks")
                print(f"   Quality Score: {analysis['quality_score']:.1f}/100")
                
                # Show preview
                print(f"   Preview:")
                preview = markdown[:200].replace('\n', ' ')
                print(f"   \"{preview}...\"")
                
                results.append(analysis)
                
            else:
                print(f"❌ Failed: {result.get('markdown', 'Unknown error')}")
                results.append({
                    "name": test_case['name'],
                    "url": test_case['url'],
                    "success": False,
                    "error": result.get('markdown', 'Unknown error'),
                    "duration": duration
                })
                
        except Exception as e:
            duration = time.time() - start_time
            print(f"❌ Exception: {e}")
            results.append({
                "name": test_case['name'],
                "url": test_case['url'],
                "success": False,
                "error": str(e),
                "duration": duration
            })
    
    return results


def compare_filtering_approaches():
    """Compare pruning vs LLM filtering on the same content."""
    print("\n" + "=" * 60)
    print("🔄 Pruning vs LLM Filter Comparison")
    print("=" * 60)
    
    test_url = "https://docs.python.org/3/tutorial/introduction.html"
    
    print(f"Testing URL: {test_url}")
    print("Comparing both filtering approaches...")
    
    # Test Pruning Filter
    print(f"\n1️⃣ Pruning Filter:")
    start_time = time.time()
    
    try:
        pruning_result = crawl_tool(test_url, use_llm_filter=False)
        pruning_duration = time.time() - start_time
        
        if pruning_result['success'] and pruning_result.get('markdown'):
            pruning_markdown = pruning_result['markdown']
            print(f"   ✅ Success - {pruning_duration:.2f}s")
            print(f"   Content: {len(pruning_markdown)} chars, {len(pruning_markdown.split())} words")
        else:
            print(f"   ❌ Failed: {pruning_result.get('markdown', 'Unknown')}")
            pruning_markdown = ""
            
    except Exception as e:
        pruning_duration = time.time() - start_time
        print(f"   ❌ Exception: {e}")
        pruning_markdown = ""
    
    # Test LLM Filter
    print(f"\n2️⃣ LLM Filter:")
    llm_instruction = """
    Extract the Python tutorial content.
    Include all explanations, code examples, and important notes.
    Remove navigation, sidebar, and footer elements.
    Format as clean markdown with proper code blocks.
    """
    
    start_time = time.time()
    
    try:
        llm_result = crawl_tool(
            test_url,
            use_llm_filter=True,
            llm_instruction=llm_instruction
        )
        llm_duration = time.time() - start_time
        
        if llm_result['success'] and llm_result.get('markdown'):
            llm_markdown = llm_result['markdown']
            print(f"   ✅ Success - {llm_duration:.2f}s")
            print(f"   Content: {len(llm_markdown)} chars, {len(llm_markdown.split())} words")
        else:
            print(f"   ❌ Failed: {llm_result.get('markdown', 'Unknown')}")
            llm_markdown = ""
            
    except Exception as e:
        llm_duration = time.time() - start_time
        print(f"   ❌ Exception: {e}")
        llm_markdown = ""
    
    # Comparison Summary
    print(f"\n📊 Comparison Summary:")
    print(f"   {'Method':<12} {'Duration':<10} {'Length':<8} {'Words':<8} {'Winner'}")
    print(f"   {'-'*50}")
    
    pruning_len = len(pruning_markdown)
    llm_len = len(llm_markdown)
    pruning_words = len(pruning_markdown.split()) if pruning_markdown else 0
    llm_words = len(llm_markdown.split()) if llm_markdown else 0
    
    speed_winner = "Pruning" if pruning_duration < llm_duration else "LLM"
    content_winner = "LLM" if llm_len > pruning_len else "Pruning"
    
    print(f"   {'Pruning':<12} {pruning_duration:<10.2f} {pruning_len:<8} {pruning_words:<8}")
    print(f"   {'LLM':<12} {llm_duration:<10.2f} {llm_len:<8} {llm_words:<8}")
    
    print(f"\n🏆 Winners:")
    print(f"   Speed: {speed_winner} ({min(pruning_duration, llm_duration):.2f}s)")
    print(f"   Content Quality: {content_winner} ({max(pruning_len, llm_len)} chars)")
    
    return {
        "pruning": {"duration": pruning_duration, "length": pruning_len, "words": pruning_words},
        "llm": {"duration": llm_duration, "length": llm_len, "words": llm_words}
    }


def demonstrate_custom_instructions():
    """Demonstrate how custom instructions affect LLM filtering."""
    print("\n" + "=" * 60)
    print("🎨 Custom Instruction Examples")
    print("=" * 60)
    
    test_url = "https://example.com"
    
    instruction_examples = [
        {
            "name": "Minimal Extraction",
            "instruction": "Extract only the main heading and first paragraph. Keep it very short."
        },
        {
            "name": "Detailed Extraction",
            "instruction": """
            Extract all content from this webpage.
            Include every piece of text, all links, and any available information.
            Format everything as detailed markdown with full structure.
            """
        },
        {
            "name": "Research-Focused",
            "instruction": """
            Extract content optimized for research purposes.
            Focus on:
            - Key facts and information
            - Important links and references
            - Any data or statistics
            - Main concepts and explanations
            
            Format as structured markdown for easy analysis.
            """
        }
    ]
    
    results = []
    
    for example in instruction_examples:
        print(f"\n🔍 {example['name']}:")
        print(f"Instruction: {example['instruction'][:100]}...")
        
        start_time = time.time()
        
        try:
            result = crawl_tool(
                test_url,
                use_llm_filter=True,
                llm_instruction=example['instruction']
            )
            
            duration = time.time() - start_time
            
            if result['success'] and result.get('markdown'):
                markdown = result['markdown']
                word_count = len(markdown.split())
                
                print(f"   ✅ Result: {len(markdown)} chars, {word_count} words ({duration:.2f}s)")
                print(f"   Preview: \"{markdown[:100].replace(chr(10), ' ')}...\"")
                
                results.append({
                    "name": example['name'],
                    "length": len(markdown),
                    "words": word_count,
                    "duration": duration
                })
            else:
                print(f"   ❌ Failed: {result.get('markdown', 'Unknown')}")
                
        except Exception as e:
            duration = time.time() - start_time
            print(f"   ❌ Exception: {e}")
    
    return results


def run_llm_filter_showcase():
    """Run the complete LLM filter showcase."""
    print("🚀 LLM Content Filter - Complete Showcase")
    print("Demonstrating advanced content filtering with LLM...")
    
    # Check API availability
    api_keys = ["OPENAI_API_KEY", "BASIC_API_KEY", "REASONING_API_KEY"]
    available = [key for key in api_keys if os.getenv(key)]
    
    print(f"\n🔑 API Keys Available: {len(available)}/{len(api_keys)}")
    if available:
        print(f"   Using: {available[0]} for LLM filtering")
    else:
        print("   ⚠️  No API keys found - tests may fail")
    
    # Run showcase tests
    print("\n" + "=" * 60)
    showcase_results = test_llm_filter_showcase()
    
    # Run comparison
    comparison_results = compare_filtering_approaches()
    
    # Run custom instruction examples
    custom_results = demonstrate_custom_instructions()
    
    # Final summary
    print(f"\n" + "=" * 60)
    print("📋 FINAL SUMMARY")
    print("=" * 60)
    
    successful_tests = sum(1 for r in showcase_results if r.get('success', False))
    total_tests = len(showcase_results)
    
    print(f"✅ Showcase Tests: {successful_tests}/{total_tests} successful")
    print(f"🔄 Comparison: LLM vs Pruning filtering completed")
    print(f"🎨 Custom Instructions: {len(custom_results)} examples demonstrated")
    
    print(f"\n💡 Key Benefits of LLM Content Filter:")
    print(f"   • Higher quality content extraction")
    print(f"   • Customizable filtering instructions")
    print(f"   • Better understanding of content context")
    print(f"   • Optimized for specific use cases")
    
    print(f"\n⚡ When to Use:")
    print(f"   • Use LLM Filter: High-quality extraction, research, complex content")
    print(f"   • Use Pruning Filter: Speed priority, simple content, cost efficiency")
    
    print(f"\n🎯 LLM Content Filter showcase completed successfully!")


if __name__ == "__main__":
    run_llm_filter_showcase() 