"""
Enhanced Crawler implementation using improved Crawl4AI client.
Maintains backward compatibility while adding powerful new features.
"""

import asyncio
import logging
from typing import List, Optional, AsyncGenerator

from .jina_client import JinaClient
from .crawl4ai_client import Crawl4AIClient, Crawl4AIConfig, Crawl4AISyncClient
from .article import Article

logger = logging.getLogger(__name__)


class Crawler:
    """
    Enhanced crawler with support for both JinaAI and Crawl4AI backends.
    Maintains backward compatibility while providing advanced crawling features.
    """
    
    def __init__(
        self, 
        backend: str = "crawl4ai",
        jina_api_key: Optional[str] = None,
        crawl4ai_config: Optional[Crawl4AIConfig] = None
    ):
        """
        Initialize crawler with specified backend.
        
        Args:
            backend: "jina" or "crawl4ai" (default: "crawl4ai")
            jina_api_key: API key for JinaAI (required if backend="jina")
            crawl4ai_config: Configuration for Crawl4AI client
        """
        self.backend = backend.lower()
        
        if self.backend == "jina":
            if not jina_api_key:
                raise ValueError("jina_api_key is required when using JinaAI backend")
            self.client = JinaClient(api_key=jina_api_key)
        elif self.backend == "crawl4ai":
            self.client = Crawl4AISyncClient(config=crawl4ai_config)
            self.async_client = Crawl4AIClient(config=crawl4ai_config)
        else:
            raise ValueError(f"Unsupported backend: {backend}. Use 'jina' or 'crawl4ai'")
    
    def crawl(self, url: str) -> Article:
        """
        Crawl a single URL and return an Article object.
        Maintains backward compatibility.
        """
        try:
            if self.backend == "jina":
                return self.client.crawl(url)
            else:
                return self.client.crawl(url)
        except Exception as e:
            logger.error(f"Failed to crawl {url} with {self.backend}: {e}")
            # Return failed article
            return Article(
                url=url,
                title="Failed to crawl",
                content=f"Error: {str(e)}",
                markdown=None,
                text=None,
                html=None,
                success=False
            )
    
    async def acrawl(self, url: str) -> Article:
        """
        Asynchronously crawl a single URL.
        """
        if self.backend == "jina":
            # JinaAI doesn't have async support, so run in executor
            return await asyncio.get_event_loop().run_in_executor(
                None, self.crawl, url
            )
        else:
            return await self.async_client.crawl(url)
    
    def crawl_many(self, urls: List[str]) -> List[Article]:
        """
        Crawl multiple URLs and return list of Articles.
        Uses parallel processing when available.
        """
        if self.backend == "jina":
            # JinaAI: fallback to sequential crawling
            articles = []
            for url in urls:
                try:
                    article = self.client.crawl(url)
                    articles.append(article)
                except Exception as e:
                    logger.error(f"Failed to crawl {url}: {e}")
                    articles.append(Article(
                        url=url,
                        title="Failed to crawl",
                        content=f"Error: {str(e)}",
                        markdown=None,
                        text=None,
                        html=None,
                        success=False
                    ))
            return articles
        else:
            return self.client.crawl_many(urls)
    
    async def acrawl_many(self, urls: List[str]) -> List[Article]:
        """
        Asynchronously crawl multiple URLs in parallel.
        """
        if self.backend == "jina":
            # JinaAI: run sequential crawling in executor
            return await asyncio.get_event_loop().run_in_executor(
                None, self.crawl_many, urls
            )
        else:
            return await self.async_client.crawl_many(urls)
    
    async def acrawl_many_stream(self, urls: List[str]) -> AsyncGenerator[Article, None]:
        """
        Stream crawl results as they become available.
        Only available with Crawl4AI backend.
        """
        if self.backend == "jina":
            raise NotImplementedError("Streaming not available with JinaAI backend")
        
        async for article in self.async_client.crawl_many_stream(urls):
            yield article
    
    async def crawl_recursive(
        self, 
        start_urls: List[str], 
        max_depth: int = 3,
        domain_filter: Optional[str] = None
    ) -> List[Article]:
        """
        Recursively crawl a site following internal links.
        Only available with Crawl4AI backend.
        """
        if self.backend == "jina":
            raise NotImplementedError("Recursive crawling not available with JinaAI backend")
        
        return await self.async_client.crawl_recursive(
            start_urls=start_urls,
            max_depth=max_depth,
            domain_filter=domain_filter
        )
    
    async def crawl_and_chunk_markdown(
        self, 
        url: str, 
        chunk_size: int = 1000
    ) -> AsyncGenerator[dict, None]:
        """
        Crawl a markdown page and chunk it by headers.
        Only available with Crawl4AI backend.
        """
        if self.backend == "jina":
            raise NotImplementedError("Markdown chunking not available with JinaAI backend")
        
        async for chunk in self.async_client.crawl_and_chunk_markdown(url, chunk_size):
            yield chunk
    
    def get_memory_usage(self) -> dict:
        """
        Get memory usage statistics.
        Only available with Crawl4AI backend.
        """
        if self.backend == "jina":
            return {"message": "Memory monitoring not available with JinaAI backend"}
        
        return self.async_client.get_memory_usage()


# Legacy imports for backward compatibility
__all__ = [
    "Crawler",
    "Crawl4AIConfig", 
    "Crawl4AIClient",
    "Crawl4AISyncClient"
]
