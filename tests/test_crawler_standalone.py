#!/usr/bin/env python3
"""
Standalone test script for the Crawler class.
This script can be run directly to test the crawler functionality.

Usage:
    python tests/test_crawler_standalone.py
"""

import sys
import os
from unittest.mock import Mock, patch

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from crawler.crawler import Crawler
from crawler.article import Article


def test_crawler_with_mocked_dependencies():
    """Test crawler with mocked dependencies to avoid external calls."""
    print("🧪 Testing Crawler with mocked dependencies...")
    
    with patch('crawler.crawler.JinaClient') as mock_jina_class, \
         patch('crawler.crawler.ReadabilityExtractor') as mock_extractor_class:
        
        # Setup mocks
        mock_jina = Mock()
        mock_jina_class.return_value = mock_jina
        mock_jina.crawl.return_value = """
        <html>
            <head><title>Test Article</title></head>
            <body>
                <h1>Test Article Title</h1>
                <p>This is a test paragraph with some content.</p>
                <p>Another paragraph with more content.</p>
            </body>
        </html>
        """
        
        mock_extractor = Mock()
        mock_extractor_class.return_value = mock_extractor
        mock_article = Article(
            title="Test Article Title", 
            html_content="<h1>Test Article Title</h1><p>This is a test paragraph with some content.</p><p>Another paragraph with more content.</p>"
        )
        mock_extractor.extract_article.return_value = mock_article
        
        # Test the crawler
        crawler = Crawler()
        test_url = "https://example.com/test-article"
        result = crawler.crawl(test_url)
        
        # Verify results
        assert isinstance(result, Article), "Result should be an Article instance"
        assert result.url == test_url, f"URL should be {test_url}"
        assert result.title == "Test Article Title", "Title should match"
        assert len(result.html_content) > 0, "HTML content should not be empty"
        
        # Test markdown conversion
        markdown = result.to_markdown()
        assert isinstance(markdown, str), "Markdown should be a string"
        assert "Test Article Title" in markdown, "Markdown should contain title"
        assert len(markdown) > 0, "Markdown should not be empty"
        
        # Verify method calls
        mock_jina.crawl.assert_called_once_with(test_url, return_format="html")
        mock_extractor.extract_article.assert_called_once()
        
        print("✅ Mocked test passed!")
        return True


def test_crawler_with_real_url():
    """Test crawler with a real URL (requires internet connection)."""
    print("\n🌐 Testing Crawler with real URL...")
    print("Note: This test requires internet connection and may take a few seconds.")
    
    try:
        crawler = Crawler()
        # Using httpbin.org which provides a simple HTML page for testing
        test_url = "https://httpbin.org/html"
        
        print(f"Crawling: {test_url}")
        result = crawler.crawl(test_url)
        
        # Verify results
        assert isinstance(result, Article), "Result should be an Article instance"
        assert result.url == test_url, f"URL should be {test_url}"
        assert hasattr(result, 'title'), "Article should have a title attribute"
        assert hasattr(result, 'html_content'), "Article should have html_content attribute"
        
        # Test markdown conversion
        markdown = result.to_markdown()
        assert isinstance(markdown, str), "Markdown should be a string"
        assert len(markdown) > 0, "Markdown should not be empty"
        
        print("✅ Real URL test passed!")
        print(f"Article title: {result.title}")
        print(f"Content length: {len(result.html_content)} characters")
        print(f"Markdown length: {len(markdown)} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Real URL test failed: {str(e)}")
        print("This might be due to network issues or external service unavailability.")
        return False


def test_crawler_error_handling():
    """Test crawler error handling scenarios."""
    print("\n🚨 Testing Crawler error handling...")
    
    with patch('crawler.crawler.JinaClient') as mock_jina_class:
        # Test network error handling
        mock_jina = Mock()
        mock_jina_class.return_value = mock_jina
        mock_jina.crawl.side_effect = Exception("Network error")
        
        crawler = Crawler()
        
        try:
            result = crawler.crawl("https://example.com")
            print("❌ Expected exception was not raised")
            return False
        except Exception as e:
            if "Network error" in str(e):
                print("✅ Error handling test passed!")
                return True
            else:
                print(f"❌ Unexpected error: {str(e)}")
                return False


def test_crawler_edge_cases():
    """Test crawler with edge cases."""
    print("\n🔍 Testing Crawler edge cases...")
    
    with patch('crawler.crawler.JinaClient') as mock_jina_class, \
         patch('crawler.crawler.ReadabilityExtractor') as mock_extractor_class:
        
        # Test empty HTML response
        mock_jina = Mock()
        mock_jina_class.return_value = mock_jina
        mock_jina.crawl.return_value = ""
        
        mock_extractor = Mock()
        mock_extractor_class.return_value = mock_extractor
        mock_article = Article(title="", html_content="")
        mock_extractor.extract_article.return_value = mock_article
        
        crawler = Crawler()
        result = crawler.crawl("https://example.com")
        
        assert isinstance(result, Article), "Should return Article even with empty content"
        assert result.url == "https://example.com", "URL should still be set"
        
        print("✅ Edge cases test passed!")
        return True


def main():
    """Run all tests."""
    print("🚀 Starting Crawler Tests")
    print("=" * 50)
    
    tests = [
        test_crawler_with_mocked_dependencies,
        test_crawler_error_handling,
        test_crawler_edge_cases,
        test_crawler_with_real_url,  # Real URL test last as it requires internet
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {str(e)}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 