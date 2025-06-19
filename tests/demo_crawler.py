#!/usr/bin/env python3
"""
Demo script for testing the Crawler class with custom URLs.
This script allows you to test the crawler functionality interactively.

Usage:
    python tests/demo_crawler.py [URL]
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from crawler.crawler import Crawler


def demo_crawler(url: str = None):
    """Demo the crawler with a specific URL."""
    if not url:
        # Default to a reliable test URL
        url = "https://httpbin.org/html"
    
    print(f"🚀 Testing Crawler with URL: {url}")
    print("-" * 50)
    
    try:
        # Initialize crawler
        crawler = Crawler()
        print("✅ Crawler initialized successfully")
        
        # Crawl the URL
        print(f"🌐 Crawling: {url}")
        result = crawler.crawl(url)
        print("✅ Crawling completed successfully")
        
        # Display results
        print("\n📊 Results:")
        print(f"  - URL: {result.url}")
        print(f"  - Title: {result.title}")
        print(f"  - HTML Content Length: {len(result.html_content)} characters")
        
        # Convert to markdown
        markdown = result.to_markdown()
        print(f"  - Markdown Length: {len(markdown)} characters")
        
        # Show first 200 characters of markdown
        print("\n📝 Markdown Preview (first 200 chars):")
        print("-" * 30)
        print(markdown[:200] + "..." if len(markdown) > 200 else markdown)
        
        # Show message format
        message = result.to_message()
        print(f"\n💬 Message Format: {len(message)} parts")
        for i, part in enumerate(message[:3]):  # Show first 3 parts
            if part['type'] == 'text':
                preview = part['text'][:100] + "..." if len(part['text']) > 100 else part['text']
                print(f"  Part {i+1} (text): {preview}")
            elif part['type'] == 'image_url':
                print(f"  Part {i+1} (image): {part['image_url']['url']}")
        
        if len(message) > 3:
            print(f"  ... and {len(message) - 3} more parts")
        
        return True
        
    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        
        # Check if it's a Jina API issue
        if "balance" in str(e).lower() or "402" in str(e):
            print("\n💡 This appears to be a Jina API balance issue.")
            print("   The crawler is working correctly, but the external service requires payment.")
            print("   You can:")
            print("   1. Set up a Jina API key with credits")
            print("   2. Use the mocked tests instead (tests/test_crawler_standalone.py)")
        
        return False


def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        # Interactive mode
        print("🎯 Crawler Demo")
        print("=" * 30)
        print("Enter a URL to crawl, or press Enter for default test URL")
        user_url = input("URL: ").strip()
        url = user_url if user_url else None
    
    success = demo_crawler(url)
    
    if success:
        print("\n🎉 Demo completed successfully!")
    else:
        print("\n❌ Demo encountered issues.")
        print("💡 Try running the mocked tests: python tests/test_crawler_standalone.py")


if __name__ == "__main__":
    main() 