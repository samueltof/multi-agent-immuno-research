"""
Crawler module for web scraping with Crawl4AI integration.

This module provides both synchronous and asynchronous web crawling capabilities
using Crawl4AI instead of JinaAI to avoid API rate limits. It maintains backward
compatibility with the existing interface while adding parallel crawling features.
"""

from .article import Article
from .crawler import Crawler
from .crawl4ai_client import Crawl4AIClient, Crawl4AIConfig
from .readability_extractor import ReadabilityExtractor

__all__ = [
    "Article",
    "Crawler", 
    "Crawl4AIClient",
    "Crawl4AIConfig",
    "ReadabilityExtractor"
]
