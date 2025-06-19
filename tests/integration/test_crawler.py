import pytest
from unittest.mock import Mock, patch, MagicMock
from src.crawler import Crawler
from src.crawler.article import Article
import requests


def test_crawler_initialization():
    """Test that crawler can be properly initialized."""
    crawler = Crawler()
    assert isinstance(crawler, Crawler)


def test_crawler_crawl_valid_url():
    """Test crawling with a valid URL."""
    crawler = Crawler()
    test_url = "https://finance.sina.com.cn/stock/relnews/us/2024-08-15/doc-incitsya6536375.shtml"
    result = crawler.crawl(test_url)
    assert result is not None
    assert hasattr(result, "to_markdown")


def test_crawler_markdown_output():
    """Test that crawler output can be converted to markdown."""
    crawler = Crawler()
    test_url = "https://finance.sina.com.cn/stock/relnews/us/2024-08-15/doc-incitsya6536375.shtml"
    result = crawler.crawl(test_url)
    markdown = result.to_markdown()
    assert isinstance(markdown, str)
    assert len(markdown) > 0


class TestCrawlerMocked:
    """Comprehensive tests using mocked dependencies to avoid external API calls."""
    
    @patch('src.crawler.crawler.JinaClient')
    @patch('src.crawler.crawler.ReadabilityExtractor')
    def test_crawl_success(self, mock_extractor_class, mock_jina_class):
        """Test successful crawling with mocked dependencies."""
        # Setup mocks
        mock_jina = Mock()
        mock_jina_class.return_value = mock_jina
        mock_jina.crawl.return_value = "<html><body><h1>Test</h1><p>Content</p></body></html>"
        
        mock_extractor = Mock()
        mock_extractor_class.return_value = mock_extractor
        mock_article = Article(title="Test Article", html_content="<p>Test content</p>")
        mock_extractor.extract_article.return_value = mock_article
        
        # Test
        crawler = Crawler()
        result = crawler.crawl("https://example.com")
        
        # Assertions
        assert isinstance(result, Article)
        assert result.url == "https://example.com"
        mock_jina.crawl.assert_called_once_with("https://example.com", return_format="html")
        mock_extractor.extract_article.assert_called_once_with("<html><body><h1>Test</h1><p>Content</p></body></html>")
    
    @patch('src.crawler.crawler.JinaClient')
    @patch('src.crawler.crawler.ReadabilityExtractor')
    def test_crawl_with_different_urls(self, mock_extractor_class, mock_jina_class):
        """Test crawling with different URL formats."""
        # Setup mocks
        mock_jina = Mock()
        mock_jina_class.return_value = mock_jina
        mock_jina.crawl.return_value = "<html><body><h1>Test</h1></body></html>"
        
        mock_extractor = Mock()
        mock_extractor_class.return_value = mock_extractor
        mock_article = Article(title="Test", html_content="<p>Content</p>")
        mock_extractor.extract_article.return_value = mock_article
        
        crawler = Crawler()
        
        # Test different URL formats
        test_urls = [
            "https://example.com",
            "https://example.com/path/to/article",
            "https://subdomain.example.com/article?param=value",
            "http://example.com/article#section"
        ]
        
        for url in test_urls:
            result = crawler.crawl(url)
            assert result.url == url
            assert isinstance(result, Article)
    
    @patch('src.crawler.crawler.JinaClient')
    def test_crawl_jina_client_error(self, mock_jina_class):
        """Test handling of JinaClient errors."""
        # Setup mock to raise exception
        mock_jina = Mock()
        mock_jina_class.return_value = mock_jina
        mock_jina.crawl.side_effect = requests.RequestException("Network error")
        
        crawler = Crawler()
        
        # Test that exception is propagated
        with pytest.raises(requests.RequestException):
            crawler.crawl("https://example.com")
    
    @patch('src.crawler.crawler.JinaClient')
    @patch('src.crawler.crawler.ReadabilityExtractor')
    def test_crawl_readability_extractor_error(self, mock_extractor_class, mock_jina_class):
        """Test handling of ReadabilityExtractor errors."""
        # Setup mocks
        mock_jina = Mock()
        mock_jina_class.return_value = mock_jina
        mock_jina.crawl.return_value = "<html><body><h1>Test</h1></body></html>"
        
        mock_extractor = Mock()
        mock_extractor_class.return_value = mock_extractor
        mock_extractor.extract_article.side_effect = Exception("Extraction error")
        
        crawler = Crawler()
        
        # Test that exception is propagated
        with pytest.raises(Exception):
            crawler.crawl("https://example.com")
    
    @patch('src.crawler.crawler.JinaClient')
    @patch('src.crawler.crawler.ReadabilityExtractor')
    def test_crawl_empty_html_response(self, mock_extractor_class, mock_jina_class):
        """Test handling of empty HTML response."""
        # Setup mocks
        mock_jina = Mock()
        mock_jina_class.return_value = mock_jina
        mock_jina.crawl.return_value = ""
        
        mock_extractor = Mock()
        mock_extractor_class.return_value = mock_extractor
        mock_article = Article(title="", html_content="")
        mock_extractor.extract_article.return_value = mock_article
        
        crawler = Crawler()
        result = crawler.crawl("https://example.com")
        
        # Should still return an Article object, even if empty
        assert isinstance(result, Article)
        assert result.url == "https://example.com"
        mock_extractor.extract_article.assert_called_once_with("")
    
    @patch('src.crawler.crawler.JinaClient')
    @patch('src.crawler.crawler.ReadabilityExtractor')
    def test_crawl_malformed_html(self, mock_extractor_class, mock_jina_class):
        """Test handling of malformed HTML."""
        # Setup mocks
        mock_jina = Mock()
        mock_jina_class.return_value = mock_jina
        mock_jina.crawl.return_value = "<html><body><h1>Unclosed tag<p>Content</body>"
        
        mock_extractor = Mock()
        mock_extractor_class.return_value = mock_extractor
        mock_article = Article(title="Test", html_content="<p>Content</p>")
        mock_extractor.extract_article.return_value = mock_article
        
        crawler = Crawler()
        result = crawler.crawl("https://example.com")
        
        assert isinstance(result, Article)
        assert result.url == "https://example.com"
        # Verify that malformed HTML was passed to extractor
        mock_extractor.extract_article.assert_called_once_with("<html><body><h1>Unclosed tag<p>Content</body>")


class TestCrawlerIntegration:
    """Integration tests that actually hit external services (use sparingly)."""
    
    @pytest.mark.slow  # Mark as slow test for optional execution
    def test_crawl_real_url_basic(self):
        """Test crawling a real URL - basic functionality."""
        crawler = Crawler()
        # Using a reliable test URL
        test_url = "https://httpbin.org/html"
        result = crawler.crawl(test_url)
        
        assert isinstance(result, Article)
        assert result.url == test_url
        assert hasattr(result, 'title')
        assert hasattr(result, 'html_content')
        
        # Should be able to convert to markdown
        markdown = result.to_markdown()
        assert isinstance(markdown, str)
        assert len(markdown) > 0


def test_crawler_command_line_usage():
    """Test the command line usage pattern shown in the module."""
    # This tests the pattern shown in the if __name__ == "__main__" block
    # We can't easily test sys.argv manipulation without subprocess, 
    # but we can test the core functionality it uses
    crawler = Crawler()
    
    # Test with the default URL from the module
    with patch('src.crawler.crawler.JinaClient') as mock_jina_class, \
         patch('src.crawler.crawler.ReadabilityExtractor') as mock_extractor_class:
        
        mock_jina = Mock()
        mock_jina_class.return_value = mock_jina
        mock_jina.crawl.return_value = "<html><body><h1>Test</h1></body></html>"
        
        mock_extractor = Mock()
        mock_extractor_class.return_value = mock_extractor
        mock_article = Article(title="Test", html_content="<p>Content</p>")
        mock_extractor.extract_article.return_value = mock_article
        
        # Test the default URL from the module
        result = crawler.crawl("https://fintel.io/zh-hant/s/br/nvdc34")
        
        assert isinstance(result, Article)
        assert result.url == "https://fintel.io/zh-hant/s/br/nvdc34"
        
        # Test that to_markdown works (as used in the main block)
        markdown = result.to_markdown()
        assert isinstance(markdown, str)
