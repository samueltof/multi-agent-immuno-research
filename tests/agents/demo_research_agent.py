#!/usr/bin/env python3
"""
Demo script for testing the Research Agent individually.

This script demonstrates how to test the research agent with different 
queries and configurations, especially useful after modifying the 
crawling framework.
"""

import asyncio
import os
import sys
import json
import logging
from typing import Dict, Any, List
from datetime import datetime

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.agents import research_agent
from src.tools import tavily_tool, crawl_tool, crawl_many_tool
from langchain_core.messages import HumanMessage

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def create_test_state(query: str, **kwargs) -> Dict[str, Any]:
    """
    Create a test state for the research agent.
    
    Args:
        query: The research query to test
        **kwargs: Additional state parameters
        
    Returns:
        Dictionary containing the state for the research agent
    """
    state = {
        "messages": [HumanMessage(content=query)],
        "CURRENT_TIME": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "TEAM_MEMBERS": ["researcher"],  # Only researcher for this test
        **kwargs
    }
    
    return state


def test_individual_tools():
    """Test the individual tools used by the research agent."""
    print("\n" + "="*80)
    print("🔧 TESTING INDIVIDUAL TOOLS")
    print("="*80)
    
    # Test search tool
    print("\n📊 Testing Tavily Search Tool")
    print("-" * 40)
    try:
        search_result = tavily_tool.invoke("latest developments in AI research 2024")
        print(f"✅ Tavily search successful: Found {len(search_result.get('results', []))} results")
        if search_result.get('results'):
            first_result = search_result['results'][0]
            print(f"   First result: {first_result.get('title', 'No title')[:100]}...")
    except Exception as e:
        print(f"❌ Tavily search failed: {e}")
    
    # Test single crawl tool
    print("\n🕷️ Testing Single Crawl Tool")
    print("-" * 40)
    try:
        test_url = "https://example.com"
        crawl_result = crawl_tool.invoke({"url": test_url})
        print(f"✅ Single crawl successful for {test_url}")
        print(f"   Success: {crawl_result.get('success', False)}")
        print(f"   Title: {crawl_result.get('title', 'No title')[:50]}...")
        print(f"   Content length: {crawl_result.get('content_length', 0)} characters")
    except Exception as e:
        print(f"❌ Single crawl failed: {e}")
    
    # Test multiple crawl tool
    print("\n🕷️🕷️ Testing Multiple Crawl Tool")
    print("-" * 40)
    try:
        test_urls = ["https://example.com", "https://httpbin.org/html"]
        crawl_results = crawl_many_tool.invoke({"urls": test_urls})
        print(f"✅ Multiple crawl successful for {len(test_urls)} URLs")
        for i, result in enumerate(crawl_results):
            print(f"   URL {i+1}: {result.get('success', False)} - {result.get('title', 'No title')[:30]}...")
    except Exception as e:
        print(f"❌ Multiple crawl failed: {e}")


def test_research_agent_basic():
    """Test the research agent with basic queries."""
    print("\n" + "="*80)
    print("🔬 TESTING RESEARCH AGENT - BASIC QUERIES")
    print("="*80)
    
    test_queries = [
        "What are the latest developments in quantum computing?",
        "Explain the current state of renewable energy technology",
        "Find information about recent advances in machine learning",
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n📋 Test {i}: {query}")
        print("-" * 60)
        
        try:
            state = create_test_state(query)
            
            print("🏁 Starting research agent...")
            start_time = datetime.now()
            
            result = research_agent.invoke(state)
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            print(f"✅ Research completed in {duration:.2f} seconds")
            
            # Analyze the result
            if result.get("messages"):
                response_content = result["messages"][-1].content
                print(f"📝 Response length: {len(response_content)} characters")
                print(f"🔍 Response preview: {response_content[:200]}...")
                
                # Check if response contains expected sections
                sections = ["Problem Statement", "Search Results", "Conclusion", "SEO Search Results", "Crawled Content"]
                found_sections = [section for section in sections if section.lower() in response_content.lower()]
                print(f"📊 Found sections: {found_sections}")
                
                # Check if URLs were mentioned (indicating crawling was attempted)
                if "http" in response_content.lower():
                    print("🌐 URLs found in response - crawling likely occurred")
                else:
                    print("⚠️  No URLs in response - check crawling behavior")
                    
            else:
                print("❌ No messages returned in result")
                
        except Exception as e:
            print(f"❌ Research agent failed for query '{query}': {e}")
            logger.exception(f"Research agent error for query: {query}")


def test_research_agent_crawling_focus():
    """Test the research agent with queries that should trigger crawling."""
    print("\n" + "="*80)
    print("🕷️ TESTING RESEARCH AGENT - CRAWLING FOCUSED")
    print("="*80)
    
    crawling_queries = [
        "Search for information about OpenAI's latest models and crawl their official documentation",
        "Find recent GitHub repositories about AI agents and read their README files",
        "Look up information about Python web scraping libraries and get detailed documentation",
    ]
    
    for i, query in enumerate(crawling_queries, 1):
        print(f"\n🔍 Crawling Test {i}: {query}")
        print("-" * 70)
        
        try:
            state = create_test_state(query)
            
            print("🏁 Starting research with crawling focus...")
            start_time = datetime.now()
            
            result = research_agent.invoke(state)
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            print(f"✅ Research completed in {duration:.2f} seconds")
            
            if result.get("messages"):
                response_content = result["messages"][-1].content
                
                # Analyze crawling indicators
                crawling_indicators = {
                    "URLs mentioned": "http" in response_content.lower(),
                    "Crawled content section": "crawled content" in response_content.lower(),
                    "Content length": len(response_content),
                    "Markdown formatting": "```" in response_content or "##" in response_content,
                }
                
                print("🔍 Crawling Analysis:")
                for indicator, found in crawling_indicators.items():
                    status = "✅" if found else "❌"
                    print(f"   {status} {indicator}: {found}")
                    
                # Look for specific crawling tool usage patterns
                if "content_length" in response_content.lower():
                    print("🎯 Detected crawl tool output patterns")
                    
            else:
                print("❌ No response content to analyze")
                
        except Exception as e:
            print(f"❌ Crawling test failed: {e}")
            logger.exception(f"Crawling test error: {query}")


def test_research_agent_error_handling():
    """Test the research agent's error handling capabilities."""
    print("\n" + "="*80)
    print("⚠️  TESTING RESEARCH AGENT - ERROR HANDLING")
    print("="*80)
    
    error_test_queries = [
        "Search for information on a completely made-up topic: xyztechnofrazzle",
        "Find information about invalid-url-test-12345",
        "",  # Empty query
        "A" * 10000,  # Very long query
    ]
    
    for i, query in enumerate(error_test_queries, 1):
        print(f"\n⚠️  Error Test {i}: {query[:50]}{'...' if len(query) > 50 else ''}")
        print("-" * 60)
        
        try:
            state = create_test_state(query)
            
            print("🏁 Testing error handling...")
            start_time = datetime.now()
            
            result = research_agent.invoke(state)
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            print(f"✅ Agent handled error case in {duration:.2f} seconds")
            
            if result.get("messages"):
                response_content = result["messages"][-1].content
                print(f"📝 Response length: {len(response_content)} characters")
                
                # Check for error handling patterns
                error_patterns = ["error", "failed", "unable", "not found", "sorry"]
                found_patterns = [pattern for pattern in error_patterns if pattern in response_content.lower()]
                
                if found_patterns:
                    print(f"🎯 Error handling detected: {found_patterns}")
                else:
                    print("🤔 No obvious error handling patterns found")
                    
        except Exception as e:
            print(f"⚠️  Exception occurred (this might be expected): {e}")


def test_research_agent_configuration():
    """Test the research agent with different configurations."""
    print("\n" + "="*80)
    print("⚙️  TESTING RESEARCH AGENT - DIFFERENT CONFIGURATIONS")
    print("="*80)
    
    base_query = "What are the benefits of renewable energy?"
    
    configurations = [
        {"deep_thinking_mode": True, "name": "Deep Thinking Mode"},
        {"search_before_planning": True, "name": "Search Before Planning"},
        {"TEAM_MEMBERS": ["researcher", "data_analyst"], "name": "Extended Team"},
    ]
    
    for i, config in enumerate(configurations, 1):
        config_name = config.pop("name")
        print(f"\n⚙️  Config Test {i}: {config_name}")
        print(f"   Config: {config}")
        print("-" * 60)
        
        try:
            state = create_test_state(base_query, **config)
            
            print("🏁 Testing configuration...")
            start_time = datetime.now()
            
            result = research_agent.invoke(state)
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            print(f"✅ Configuration test completed in {duration:.2f} seconds")
            
            if result.get("messages"):
                response_content = result["messages"][-1].content
                print(f"📝 Response length: {len(response_content)} characters")
                print(f"🔍 Response preview: {response_content[:150]}...")
                
        except Exception as e:
            print(f"❌ Configuration test failed: {e}")


def interactive_research_test():
    """Interactive mode for testing the research agent."""
    print("\n" + "="*80)
    print("🎮 INTERACTIVE RESEARCH AGENT TEST")
    print("="*80)
    print("Enter research queries to test the agent (type 'quit' to exit)")
    print("Special commands:")
    print("  - 'status': Show current tool status")
    print("  - 'help': Show this help message")
    print("  - 'quit' or 'exit': Exit interactive mode")
    
    while True:
        try:
            query = input("\n🔬 Enter research query: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
                
            elif query.lower() == 'status':
                print("🔧 Tool Status:")
                test_individual_tools()
                continue
                
            elif query.lower() == 'help':
                print("💡 Interactive mode commands:")
                print("  - Enter any research query to test the agent")
                print("  - 'status': Test individual tools")
                print("  - 'help': Show this help")
                print("  - 'quit': Exit")
                continue
                
            elif not query:
                print("Please enter a valid query.")
                continue
            
            print(f"\n🔍 Testing: {query}")
            print("-" * 50)
            
            state = create_test_state(query)
            
            print("🏁 Starting research...")
            start_time = datetime.now()
            
            result = research_agent.invoke(state)
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            print(f"\n✅ Research completed in {duration:.2f} seconds")
            
            if result.get("messages"):
                response_content = result["messages"][-1].content
                print(f"\n📊 Results:")
                print(f"📝 Response length: {len(response_content)} characters")
                print(f"\n📄 Full Response:")
                print("-" * 50)
                print(response_content)
                print("-" * 50)
            else:
                print("❌ No response received")
                
        except KeyboardInterrupt:
            print("\n👋 Interactive mode interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error during interactive test: {e}")
            logger.exception("Interactive test error")


def main():
    """Run all research agent tests."""
    print("🔬 RESEARCH AGENT INDIVIDUAL TESTING SUITE")
    print("🕷️ Testing Enhanced Crawling Framework Integration")
    print("=" * 80)
    
    # Check environment
    print("\n🔍 Environment Check:")
    api_keys = {
        "OPENAI_API_KEY": bool(os.getenv('OPENAI_API_KEY')),
        "ANTHROPIC_API_KEY": bool(os.getenv('ANTHROPIC_API_KEY')),
        "TAVILY_API_KEY": bool(os.getenv('TAVILY_API_KEY')),
        "LLM_API_KEY": bool(os.getenv('LLM_API_KEY')),
    }
    
    for key, present in api_keys.items():
        status = "✅" if present else "❌"
        print(f"   {status} {key}: {'Present' if present else 'Missing'}")
    
    if not any(api_keys.values()):
        print("\n⚠️  WARNING: No API keys found. Some tests may fail.")
        print("Set appropriate API keys in your environment variables.")
    
    try:
        # Run test suites
        test_individual_tools()
        test_research_agent_basic()
        test_research_agent_crawling_focus()
        test_research_agent_error_handling()
        test_research_agent_configuration()
        
        # Optionally run interactive mode
        if '--interactive' in sys.argv or '-i' in sys.argv:
            interactive_research_test()
        else:
            print(f"\n💡 To run interactive mode, use: python {sys.argv[0]} --interactive")
    
    except Exception as e:
        print(f"❌ Test suite failed: {e}")
        logger.exception("Test suite execution failed")
    
    print("\n✅ Research Agent Testing Suite Completed!")
    print("🕷️ Check the output above to analyze crawling framework performance")


if __name__ == "__main__":
    main() 