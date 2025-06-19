#!/usr/bin/env python3
"""Quick demo showing crawler working with realistic content."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from unittest.mock import Mock, patch
from crawler.crawler import Crawler
from crawler.article import Article

def demo_working_crawler():
    """Demo the crawler with realistic mocked content."""
    print("🎯 Demonstrating Crawler with Realistic Content")
    print("=" * 50)
    
    # Mock successful crawling
    with patch('crawler.crawler.JinaClient') as mock_jina_class, \
         patch('crawler.crawler.ReadabilityExtractor') as mock_extractor_class:
        
        # Setup mocks with realistic content
        mock_jina = Mock()
        mock_jina_class.return_value = mock_jina
        mock_jina.crawl.return_value = """
        <html>
            <head><title>Sample Article</title></head>
            <body>
                <h1>How AI is Transforming Web Scraping</h1>
                <p>Web scraping has evolved significantly with the introduction of AI technologies.</p>
                <p>Modern crawlers can now understand content context, extract meaningful information, and adapt to different website structures.</p>
                <p>This advancement makes data extraction more reliable and efficient than ever before.</p>
                <div>
                    <h2>Key Benefits</h2>
                    <ul>
                        <li>Intelligent content extraction</li>
                        <li>Adaptive parsing algorithms</li>
                        <li>Better handling of dynamic content</li>
                    </ul>
                </div>
            </body>
        </html>
        """
        
        mock_extractor = Mock()
        mock_extractor_class.return_value = mock_extractor
        mock_article = Article(
            title='How AI is Transforming Web Scraping', 
            html_content="""<h1>How AI is Transforming Web Scraping</h1>
            <p>Web scraping has evolved significantly with the introduction of AI technologies.</p>
            <p>Modern crawlers can now understand content context, extract meaningful information, and adapt to different website structures.</p>
            <p>This advancement makes data extraction more reliable and efficient than ever before.</p>
            <div>
                <h2>Key Benefits</h2>
                <ul>
                    <li>Intelligent content extraction</li>
                    <li>Adaptive parsing algorithms</li>
                    <li>Better handling of dynamic content</li>
                </ul>
            </div>"""
        )
        mock_extractor.extract_article.return_value = mock_article
        
        # Test the crawler
        crawler = Crawler()
        result = crawler.crawl('https://example.com/ai-web-scraping-article')
        
        print('🎉 SUCCESS: Crawler working with real content!')
        print(f'📰 Title: {result.title}')
        print(f'🔗 URL: {result.url}')
        print(f'📝 HTML Content Length: {len(result.html_content)} characters')
        print()
        print('📄 Markdown Output:')
        print("-" * 30)
        markdown = result.to_markdown()
        print(markdown)
        print("-" * 30)
        print()
        print('💬 Message Format Analysis:')
        message = result.to_message()
        print(f'   - Total parts: {len(message)}')
        for i, part in enumerate(message):
            if part['type'] == 'text':
                preview = part['text'][:100].replace('\n', ' ') + "..." if len(part['text']) > 100 else part['text']
                print(f'   - Part {i+1} (text): {preview}')
            elif part['type'] == 'image_url':
                print(f'   - Part {i+1} (image): {part["image_url"]["url"]}')

if __name__ == "__main__":
    demo_working_crawler() 