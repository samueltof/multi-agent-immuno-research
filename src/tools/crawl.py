"""
Enhanced crawl tools using improved Crawl4AI implementation.
Provides clean content extraction with advanced features.
"""

import asyncio
import logging
from typing import List, Optional, AsyncGenerator

from src.crawler.crawler import Crawler, Crawl4AIConfig

logger = logging.getLogger(__name__)


def crawl_tool(url: str, backend: str = "crawl4ai") -> dict:
    """
    Crawl a single URL and extract clean content.
    
    Args:
        url: URL to crawl
        backend: Backend to use ("crawl4ai" or "jina")
        
    Returns:
        Dictionary with crawled content
    """
    try:
        # Configure for optimal performance
        config = Crawl4AIConfig(
            headless=True,
            verbose=False,
            max_concurrent=10,
            memory_threshold_percent=70.0,
            bypass_cache=True
        )
        
        crawler = Crawler(backend=backend, crawl4ai_config=config)
        article = crawler.crawl(url)
        
        return {
            "url": article.url,
            "title": article.title,
            "content": article.content,
            "markdown": article.markdown,
            "text": article.text,
            "success": article.success,
            "content_length": len(article.content) if article.content else 0,
            "metadata": getattr(article, 'metadata', {})
        }
        
    except Exception as e:
        logger.error(f"Failed to crawl {url}: {e}")
        return {
            "url": url,
            "title": "Failed to crawl",
            "content": f"Error: {str(e)}",
            "markdown": None,
            "text": None,
            "success": False,
            "content_length": 0,
            "metadata": {}
        }


def crawl_many_tool(
    urls: List[str], 
    backend: str = "crawl4ai",
    max_concurrent: int = 10
) -> List[dict]:
    """
    Crawl multiple URLs in parallel and extract clean content.
    
    Args:
        urls: List of URLs to crawl
        backend: Backend to use ("crawl4ai" or "jina")
        max_concurrent: Maximum concurrent requests
        
    Returns:
        List of dictionaries with crawled content
    """
    try:
        config = Crawl4AIConfig(
            headless=True,
            verbose=False,
            max_concurrent=max_concurrent,
            memory_threshold_percent=70.0,
            bypass_cache=True
        )
        
        crawler = Crawler(backend=backend, crawl4ai_config=config)
        articles = crawler.crawl_many(urls)
        
        results = []
        for article in articles:
            results.append({
                "url": article.url,
                "title": article.title,
                "content": article.content,
                "markdown": article.markdown,
                "text": article.text,
                "success": article.success,
                "content_length": len(article.content) if article.content else 0,
                "metadata": getattr(article, 'metadata', {})
            })
        
        return results
        
    except Exception as e:
        logger.error(f"Failed to crawl URLs: {e}")
        # Return error results for all URLs
        return [
            {
                "url": url,
                "title": "Failed to crawl",
                "content": f"Error: {str(e)}",
                "markdown": None,
                "text": None,
                "success": False,
                "content_length": 0,
                "metadata": {}
            }
            for url in urls
        ]


async def acrawl_tool(url: str, backend: str = "crawl4ai") -> dict:
    """
    Asynchronously crawl a single URL and extract clean content.
    
    Args:
        url: URL to crawl
        backend: Backend to use ("crawl4ai" or "jina")
        
    Returns:
        Dictionary with crawled content
    """
    try:
        config = Crawl4AIConfig(
            headless=True,
            verbose=False,
            max_concurrent=10,
            memory_threshold_percent=70.0,
            bypass_cache=True
        )
        
        crawler = Crawler(backend=backend, crawl4ai_config=config)
        article = await crawler.acrawl(url)
        
        return {
            "url": article.url,
            "title": article.title,
            "content": article.content,
            "markdown": article.markdown,
            "text": article.text,
            "success": article.success,
            "content_length": len(article.content) if article.content else 0,
            "metadata": getattr(article, 'metadata', {})
        }
        
    except Exception as e:
        logger.error(f"Failed to crawl {url}: {e}")
        return {
            "url": url,
            "title": "Failed to crawl",
            "content": f"Error: {str(e)}",
            "markdown": None,
            "text": None,
            "success": False,
            "content_length": 0,
            "metadata": {}
        }


async def acrawl_many_tool(
    urls: List[str], 
    backend: str = "crawl4ai",
    max_concurrent: int = 10
) -> List[dict]:
    """
    Asynchronously crawl multiple URLs in parallel.
    
    Args:
        urls: List of URLs to crawl
        backend: Backend to use ("crawl4ai" or "jina")
        max_concurrent: Maximum concurrent requests
        
    Returns:
        List of dictionaries with crawled content
    """
    try:
        config = Crawl4AIConfig(
            headless=True,
            verbose=False,
            max_concurrent=max_concurrent,
            memory_threshold_percent=70.0,
            bypass_cache=True
        )
        
        crawler = Crawler(backend=backend, crawl4ai_config=config)
        articles = await crawler.acrawl_many(urls)
        
        results = []
        for article in articles:
            results.append({
                "url": article.url,
                "title": article.title,
                "content": article.content,
                "markdown": article.markdown,
                "text": article.text,
                "success": article.success,
                "content_length": len(article.content) if article.content else 0,
                "metadata": getattr(article, 'metadata', {})
            })
        
        return results
        
    except Exception as e:
        logger.error(f"Failed to crawl URLs: {e}")
        return [
            {
                "url": url,
                "title": "Failed to crawl",
                "content": f"Error: {str(e)}",
                "markdown": None,
                "text": None,
                "success": False,
                "content_length": 0,
                "metadata": {}
            }
            for url in urls
        ]


async def acrawl_many_stream_tool(
    urls: List[str], 
    max_concurrent: int = 10
) -> AsyncGenerator[dict, None]:
    """
    Stream crawl results as they become available.
    Only available with Crawl4AI backend.
    
    Args:
        urls: List of URLs to crawl
        max_concurrent: Maximum concurrent requests
        
    Yields:
        Dictionaries with crawled content as they complete
    """
    try:
        config = Crawl4AIConfig(
            headless=True,
            verbose=False,
            max_concurrent=max_concurrent,
            memory_threshold_percent=70.0,
            bypass_cache=True
        )
        
        crawler = Crawler(backend="crawl4ai", crawl4ai_config=config)
        
        async for article in crawler.acrawl_many_stream(urls):
            yield {
                "url": article.url,
                "title": article.title,
                "content": article.content,
                "markdown": article.markdown,
                "text": article.text,
                "success": article.success,
                "content_length": len(article.content) if article.content else 0,
                "metadata": getattr(article, 'metadata', {})
            }
            
    except Exception as e:
        logger.error(f"Failed to stream crawl URLs: {e}")
        for url in urls:
            yield {
                "url": url,
                "title": "Failed to crawl",
                "content": f"Error: {str(e)}",
                "markdown": None,
                "text": None,
                "success": False,
                "content_length": 0,
                "metadata": {}
            }


async def crawl_recursive_tool(
    start_urls: List[str],
    max_depth: int = 3,
    domain_filter: Optional[str] = None,
    max_concurrent: int = 10
) -> List[dict]:
    """
    Recursively crawl a site following internal links.
    Only available with Crawl4AI backend.
    
    Args:
        start_urls: Starting URLs to crawl
        max_depth: Maximum depth to crawl
        domain_filter: Optional domain filter for links
        max_concurrent: Maximum concurrent requests
        
    Returns:
        List of dictionaries with crawled content
    """
    try:
        config = Crawl4AIConfig(
            headless=True,
            verbose=False,
            max_concurrent=max_concurrent,
            memory_threshold_percent=70.0,
            bypass_cache=True
        )
        
        crawler = Crawler(backend="crawl4ai", crawl4ai_config=config)
        articles = await crawler.crawl_recursive(
            start_urls=start_urls,
            max_depth=max_depth,
            domain_filter=domain_filter
        )
        
        results = []
        for article in articles:
            results.append({
                "url": article.url,
                "title": article.title,
                "content": article.content,
                "markdown": article.markdown,
                "text": article.text,
                "success": article.success,
                "content_length": len(article.content) if article.content else 0,
                "metadata": getattr(article, 'metadata', {})
            })
        
        return results
        
    except Exception as e:
        logger.error(f"Failed to recursively crawl: {e}")
        return [
            {
                "url": url,
                "title": "Failed to crawl",
                "content": f"Error: {str(e)}",
                "markdown": None,
                "text": None,
                "success": False,
                "content_length": 0,
                "metadata": {}
            }
            for url in start_urls
        ]


async def crawl_and_chunk_markdown_tool(
    url: str,
    chunk_size: int = 1000,
    max_concurrent: int = 10
) -> List[dict]:
    """
    Crawl a markdown page and chunk it by headers.
    Only available with Crawl4AI backend.
    
    Args:
        url: URL to crawl
        chunk_size: Maximum size per chunk
        max_concurrent: Maximum concurrent requests
        
    Returns:
        List of chunks with metadata
    """
    try:
        config = Crawl4AIConfig(
            headless=True,
            verbose=False,
            max_concurrent=max_concurrent,
            memory_threshold_percent=70.0,
            bypass_cache=True
        )
        
        crawler = Crawler(backend="crawl4ai", crawl4ai_config=config)
        chunks = []
        
        async for chunk in crawler.crawl_and_chunk_markdown(url, chunk_size):
            chunks.append(chunk)
        
        return chunks
        
    except Exception as e:
        logger.error(f"Failed to crawl and chunk markdown: {e}")
        return [
            {
                'chunk_index': 0,
                'content': f"Error: {str(e)}",
                'url': url,
                'title': "Failed to crawl",
                'headers': [],
                'success': False
            }
        ]


# Sync wrappers for async tools (for LangGraph compatibility)
def crawl_recursive_sync_tool(
    start_urls: List[str],
    max_depth: int = 3,
    domain_filter: Optional[str] = None,
    max_concurrent: int = 10
) -> List[dict]:
    """
    Sync wrapper for recursive crawling tool.
    
    Args:
        start_urls: Starting URLs to crawl
        max_depth: Maximum depth to crawl
        domain_filter: Optional domain filter for links
        max_concurrent: Maximum concurrent requests
        
    Returns:
        List of dictionaries with crawled content
    """
    try:
        # Run the async function in a new event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(
                crawl_recursive_tool(start_urls, max_depth, domain_filter, max_concurrent)
            )
        finally:
            loop.close()
    except Exception as e:
        logger.error(f"Failed to run recursive crawl sync: {e}")
        return [
            {
                "url": url,
                "title": "Failed to crawl",
                "content": f"Error: {str(e)}",
                "markdown": None,
                "text": None,
                "success": False,
                "content_length": 0,
                "metadata": {}
            }
            for url in start_urls
        ]


def crawl_and_chunk_markdown_sync_tool(
    url: str,
    chunk_size: int = 1000,
    max_concurrent: int = 10
) -> List[dict]:
    """
    Sync wrapper for markdown chunking tool.
    
    Args:
        url: URL to crawl
        chunk_size: Maximum size per chunk
        max_concurrent: Maximum concurrent requests
        
    Returns:
        List of chunks with metadata
    """
    try:
        # Run the async function in a new event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(
                crawl_and_chunk_markdown_tool(url, chunk_size, max_concurrent)
            )
        finally:
            loop.close()
    except Exception as e:
        logger.error(f"Failed to run markdown chunking sync: {e}")
        return [
            {
                'chunk_index': 0,
                'content': f"Error: {str(e)}",
                'url': url,
                'title': "Failed to crawl",
                'headers': [],
                'success': False
            }
        ]


# Export tools for use by agents
__all__ = [
    "crawl_tool",
    "crawl_many_tool", 
    "crawl_recursive_sync_tool",
    "crawl_and_chunk_markdown_sync_tool",
    "acrawl_tool",
    "acrawl_many_tool",
    "acrawl_many_stream_tool",
    "crawl_recursive_tool",
    "crawl_and_chunk_markdown_tool"
]
