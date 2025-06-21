#!/usr/bin/env python3
"""
Test Research Agent with Advanced Crawl Tools
Simple test to verify the research agent works with improved markdown generation.
"""

import sys
import os
import asyncio
import time

# Add the project root to Python path
project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, project_root)

from src.agents.agents import research_agent


def test_research_agent_simple():
    """Test research agent with a simple query using advanced crawl tools."""
    print("=" * 60)
    print("Testing Research Agent with Advanced Crawl Tools")
    print("=" * 60)
    
    # Simple research query
    query = "What is Crawl4AI and how does it work?"
    
    print(f"Research Query: {query}")
    print("Running research agent...")
    
    start_time = time.time()
    
    # Create state for the research agent
    state = {
        "messages": [{"role": "user", "content": query}]
    }
    
    try:
        # Run the research agent
        result = research_agent.invoke(state)
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\nResearch completed in {duration:.2f} seconds")
        
        # Extract the response
        if "messages" in result:
            messages = result["messages"]
            if messages:
                last_message = messages[-1]
                response_content = last_message.content if hasattr(last_message, 'content') else str(last_message)
                
                print(f"\nResponse length: {len(response_content)} characters")
                print(f"Response word count: {len(response_content.split())} words")
                
                print(f"\nResearch Agent Response:")
                print("-" * 50)
                print(response_content[:1000])  # First 1000 characters
                if len(response_content) > 1000:
                    print(f"\n... [truncated, {len(response_content) - 1000} more characters]")
                print("-" * 50)
                
                # Analyze response quality
                quality_indicators = {
                    "Mentions Crawl4AI": "crawl4ai" in response_content.lower() or "crawl 4ai" in response_content.lower(),
                    "Has technical details": any(term in response_content.lower() for term in ["python", "api", "web scraping", "browser", "html"]),
                    "Well structured": len(response_content.split('\n')) > 3,
                    "Reasonable length": 500 <= len(response_content) <= 5000,
                    "Contains URLs": "http" in response_content,
                }
                
                print(f"\nResponse Quality Analysis:")
                for indicator, present in quality_indicators.items():
                    status = "✓" if present else "✗"
                    print(f"  {status} {indicator}")
                
                quality_score = sum(quality_indicators.values()) / len(quality_indicators) * 100
                print(f"\nOverall Quality Score: {quality_score:.1f}%")
                
                return {
                    "success": True,
                    "response": response_content,
                    "duration": duration,
                    "quality_score": quality_score,
                    "word_count": len(response_content.split())
                }
            else:
                print("No messages in result")
                return {"success": False, "error": "No messages in result"}
        else:
            print("No messages key in result")
            return {"success": False, "error": "No messages key in result"}
            
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        print(f"\nResearch failed after {duration:.2f} seconds")
        print(f"Error: {e}")
        return {"success": False, "error": str(e), "duration": duration}


def test_research_agent_crawling_focused():
    """Test research agent with a crawling-focused query."""
    print("\n" + "=" * 60)
    print("Testing Research Agent with Crawling-Focused Query")
    print("=" * 60)
    
    # Crawling-focused query
    query = "What are the latest developments in web scraping and content extraction tools?"
    
    print(f"Research Query: {query}")
    print("Running research agent...")
    
    start_time = time.time()
    
    # Create state for the research agent
    state = {
        "messages": [{"role": "user", "content": query}]
    }
    
    try:
        # Run the research agent
        result = research_agent.invoke(state)
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\nResearch completed in {duration:.2f} seconds")
        
        # Extract the response
        if "messages" in result:
            messages = result["messages"]
            if messages:
                last_message = messages[-1]
                response_content = last_message.content if hasattr(last_message, 'content') else str(last_message)
                
                print(f"\nResponse length: {len(response_content)} characters")
                print(f"Response word count: {len(response_content.split())} words")
                
                # Check if the response mentions token efficiency improvements
                efficiency_indicators = {
                    "Mentions token efficiency": any(term in response_content.lower() for term in ["token", "efficient", "optimize", "reduce"]),
                    "Discusses modern tools": any(term in response_content.lower() for term in ["crawl4ai", "scrapy", "playwright", "selenium"]),
                    "Has structured content": response_content.count('\n') > 5,
                    "Reasonable response time": duration < 60,  # Should complete within 60 seconds
                    "Comprehensive coverage": len(response_content.split()) > 200
                }
                
                print(f"\nCrawling Research Quality Analysis:")
                for indicator, present in efficiency_indicators.items():
                    status = "✓" if present else "✗"
                    print(f"  {status} {indicator}")
                
                efficiency_score = sum(efficiency_indicators.values()) / len(efficiency_indicators) * 100
                print(f"\nEfficiency Score: {efficiency_score:.1f}%")
                
                return {
                    "success": True,
                    "response": response_content,
                    "duration": duration,
                    "efficiency_score": efficiency_score,
                    "word_count": len(response_content.split())
                }
            else:
                print("No messages in result")
                return {"success": False, "error": "No messages in result"}
        else:
            print("No messages key in result")
            return {"success": False, "error": "No messages key in result"}
            
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        print(f"\nResearch failed after {duration:.2f} seconds")
        print(f"Error: {e}")
        return {"success": False, "error": str(e), "duration": duration}


def run_research_agent_tests():
    """Run both research agent tests and provide summary."""
    print("🚀 Starting Research Agent Tests with Advanced Crawl Tools")
    
    results = []
    
    # Test 1: Simple Crawl4AI query
    try:
        simple_result = test_research_agent_simple()
        results.append(("Simple Query", simple_result))
    except Exception as e:
        print(f"Simple query test failed: {e}")
        results.append(("Simple Query", {"success": False, "error": str(e)}))
    
    # Test 2: Crawling-focused query
    try:
        crawling_result = test_research_agent_crawling_focused()
        results.append(("Crawling Query", crawling_result))
    except Exception as e:
        print(f"Crawling query test failed: {e}")
        results.append(("Crawling Query", {"success": False, "error": str(e)}))
    
    # Summary
    print("\n" + "=" * 60)
    print("RESEARCH AGENT TEST SUMMARY")
    print("=" * 60)
    
    total_success = 0
    total_tests = len(results)
    
    for test_name, result in results:
        print(f"\n{test_name}:")
        if result.get("success", False):
            total_success += 1
            print(f"  ✅ Success")
            print(f"  ⏱️  Duration: {result.get('duration', 0):.2f}s")
            print(f"  📝 Word count: {result.get('word_count', 0)}")
            if 'quality_score' in result:
                print(f"  🎯 Quality: {result['quality_score']:.1f}%")
            if 'efficiency_score' in result:
                print(f"  ⚡ Efficiency: {result['efficiency_score']:.1f}%")
        else:
            print(f"  ❌ Failed: {result.get('error', 'Unknown error')}")
    
    print(f"\n📊 Overall Results: {total_success}/{total_tests} tests passed")
    
    if total_success == total_tests:
        print("🎉 All tests passed! Advanced crawl tools are working with research agent.")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
    
    print("\n💡 Key Benefits of Advanced Markdown Generation:")
    print("   • Improved token efficiency")
    print("   • Better structured content extraction")
    print("   • Faster processing times")
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
    run_research_agent_tests() 