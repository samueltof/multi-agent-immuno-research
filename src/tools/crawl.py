"""
Enhanced crawl tools using improved Crawl4AI implementation.
Provides clean content extraction with minimal output for token efficiency.
"""

import asyncio
import logging
from typing import List, Optional, AsyncGenerator

from src.crawler.crawler import Crawler, Crawl4AIConfig

logger = logging.getLogger(__name__)


def crawl_tool(
    url: str,
    backend: str = "crawl4ai",
    use_llm_filter: bool = True,  # Default to LLM filtering
    llm_instruction: str = None,
) -> dict:
    """
    Crawl a single URL and extract clean content.

    Args:
        url: URL to crawl
        backend: Backend to use ("crawl4ai" or "jina")
        use_llm_filter: Whether to use LLM-based content filtering (default: True)
        llm_instruction: Custom instruction for LLM filtering (optional)

    Returns:
        Dictionary with essential crawled content (url, title, markdown, success)
    """
    try:
        # Configure for optimal performance
        config = Crawl4AIConfig(
            bypass_cache=True,
            timeout=30,
            verbose=False,
            use_llm_filter=use_llm_filter,
            llm_filter_instruction=llm_instruction,
        )

        crawler = Crawler(backend=backend, crawl4ai_config=config)
        article = crawler.crawl(url)

        # Use fit_markdown if available, otherwise fall back to markdown
        markdown_content = None
        if hasattr(article, "markdown") and article.markdown:
            if (
                hasattr(article.markdown, "fit_markdown")
                and article.markdown.fit_markdown
            ):
                markdown_content = article.markdown.fit_markdown
            elif (
                hasattr(article.markdown, "raw_markdown")
                and article.markdown.raw_markdown
            ):
                markdown_content = article.markdown.raw_markdown
            else:
                # If it's a string (older API), use it directly
                markdown_content = str(article.markdown)

        return {
            "url": article.url,
            "title": article.title,
            "markdown": markdown_content,
            "success": article.success,
        }

    except Exception as e:
        logger.error(f"Failed to crawl {url}: {e}")
        return {
            "url": url,
            "title": "Failed to crawl",
            "markdown": f"Error: {str(e)}",
            "success": False,
        }


def crawl_many_tool(
    urls: List[str],
    backend: str = "crawl4ai",
    use_llm_filter: bool = True,  # Default to LLM filtering
    llm_instruction: str = None,
) -> List[dict]:
    """
    Crawl multiple URLs concurrently and extract clean content.

    Args:
        urls: List of URLs to crawl
        backend: Backend to use ("crawl4ai" or "jina")
        use_llm_filter: Whether to use LLM-based content filtering (default: True)
        llm_instruction: Custom instruction for LLM filtering (optional)

    Returns:
        List of dictionaries with crawled content for each URL
    """
    try:
        # Configure for optimal performance
        config = Crawl4AIConfig(
            bypass_cache=True,
            timeout=30,
            verbose=False,
            use_llm_filter=use_llm_filter,
            llm_filter_instruction=llm_instruction,
        )

        crawler = Crawler(backend=backend, crawl4ai_config=config)
        results = []

        for url in urls:
            try:
                article = crawler.crawl(url)

                # Use fit_markdown if available, otherwise fall back to markdown
                markdown_content = None
                if hasattr(article, "markdown") and article.markdown:
                    if (
                        hasattr(article.markdown, "fit_markdown")
                        and article.markdown.fit_markdown
                    ):
                        markdown_content = article.markdown.fit_markdown
                    elif (
                        hasattr(article.markdown, "raw_markdown")
                        and article.markdown.raw_markdown
                    ):
                        markdown_content = article.markdown.raw_markdown
                    else:
                        # If it's a string (older API), use it directly
                        markdown_content = str(article.markdown)

                results.append(
                    {
                        "url": article.url,
                        "title": article.title,
                        "markdown": markdown_content,
                        "success": article.success,
                    }
                )

            except Exception as e:
                logger.error(f"Failed to crawl {url}: {e}")
                results.append(
                    {
                        "url": url,
                        "title": "Failed to crawl",
                        "markdown": f"Error: {str(e)}",
                        "success": False,
                    }
                )

        return results

    except Exception as e:
        logger.error(f"Failed to crawl multiple URLs: {e}")
        return [
            {
                "url": url,
                "title": "Failed to crawl",
                "markdown": f"Error: {str(e)}",
                "success": False,
            }
            for url in urls
        ]


async def crawl_many_tool_async(
    urls: List[str], backend: str = "crawl4ai"
) -> AsyncGenerator[dict, None]:
    """
    Asynchronously crawl multiple URLs and yield results as they complete.

    Args:
        urls: List of URLs to crawl
        backend: Backend to use ("crawl4ai" or "jina")

    Yields:
        Dictionary with crawled content for each completed URL
    """
    # Configure for optimal performance
    config = Crawl4AIConfig(bypass_cache=True, timeout=30, verbose=False)

    crawler = Crawler(backend=backend, crawl4ai_config=config)

    async def crawl_single(url: str) -> dict:
        """Crawl a single URL asynchronously."""
        try:
            # For async operations, we might need to run in executor
            # This depends on the crawler implementation
            article = await asyncio.get_event_loop().run_in_executor(
                None, crawler.crawl, url
            )

            # Use fit_markdown if available, otherwise fall back to markdown
            markdown_content = None
            if hasattr(article, "markdown") and article.markdown:
                if (
                    hasattr(article.markdown, "fit_markdown")
                    and article.markdown.fit_markdown
                ):
                    markdown_content = article.markdown.fit_markdown
                elif (
                    hasattr(article.markdown, "raw_markdown")
                    and article.markdown.raw_markdown
                ):
                    markdown_content = article.markdown.raw_markdown
                else:
                    # If it's a string (older API), use it directly
                    markdown_content = str(article.markdown)

            return {
                "url": article.url,
                "title": article.title,
                "markdown": markdown_content,
                "success": article.success,
            }

        except Exception as e:
            logger.error(f"Failed to crawl {url}: {e}")
            return {
                "url": url,
                "title": "Failed to crawl",
                "markdown": f"Error: {str(e)}",
                "success": False,
            }

    # Create tasks for all URLs
    tasks = [crawl_single(url) for url in urls]

    # Yield results as they complete
    for coro in asyncio.as_completed(tasks):
        result = await coro
        yield result


async def crawl_stream_tool(
    urls: List[str], backend: str = "crawl4ai", max_concurrent: int = 3
) -> AsyncGenerator[dict, None]:
    """
    Crawl multiple URLs with streaming results (async generator).

    Args:
        urls: List of URLs to crawl
        backend: Backend to use ("crawl4ai" or "jina")
        max_concurrent: Maximum number of concurrent crawls

    Yields:
        Dictionary with crawled content for each URL as completed
    """
    # Configure for optimal performance
    config = Crawl4AIConfig(
        word_count_threshold=10,
        exclude_external_links=True,
        remove_overlay_elements=True,
        process_iframes=True,
    )

    async def crawl_single_async(url: str) -> dict:
        """Async wrapper for single crawl"""
        try:
            crawler = Crawler(backend=backend, crawl4ai_config=config)
            article = crawler.crawl(url)

            # Use fit_markdown for cleaner output if available, fallback to markdown
            markdown_content = (
                getattr(article, "fit_markdown", None) or article.markdown
            )

            return {
                "url": article.url,
                "title": article.title,
                "markdown": markdown_content,
                "success": article.success,
            }
        except Exception as e:
            logger.error(f"Failed to crawl {url}: {e}")
            return {
                "url": url,
                "title": "Failed to crawl",
                "markdown": f"Error: {str(e)}",
                "success": False,
            }

    # Create semaphore for concurrency control
    semaphore = asyncio.Semaphore(max_concurrent)

    async def crawl_with_semaphore(url):
        async with semaphore:
            return await crawl_single_async(url)

    # Create tasks and yield results as they complete
    tasks = [asyncio.create_task(crawl_with_semaphore(url)) for url in urls]

    for task in asyncio.as_completed(tasks):
        result = await task
        yield result


async def acrawl_tool(url: str, backend: str = "crawl4ai") -> dict:
    """
    Asynchronously crawl a single URL and extract clean content.

    Args:
        url: URL to crawl
        backend: Backend to use ("crawl4ai" or "jina")

    Returns:
        Dictionary with essential crawled content
    """
    try:
        config = Crawl4AIConfig(
            headless=True,
            verbose=False,
            max_concurrent=10,
            memory_threshold_percent=70.0,
            bypass_cache=True,
        )

        crawler = Crawler(backend=backend, crawl4ai_config=config)
        article = await crawler.acrawl(url)

        return {
            "url": article.url,
            "title": article.title,
            "markdown": article.markdown,
            "success": article.success,
        }

    except Exception as e:
        logger.error(f"Failed to crawl {url}: {e}")
        return {
            "url": url,
            "title": "Failed to crawl",
            "markdown": f"Error: {str(e)}",
            "success": False,
        }


async def acrawl_many_tool(
    urls: List[str], backend: str = "crawl4ai", max_concurrent: int = 10
) -> List[dict]:
    """
    Asynchronously crawl multiple URLs in parallel.

    Args:
        urls: List of URLs to crawl
        backend: Backend to use ("crawl4ai" or "jina")
        max_concurrent: Maximum concurrent requests

    Returns:
        List of dictionaries with essential crawled content
    """
    try:
        config = Crawl4AIConfig(
            headless=True,
            verbose=False,
            max_concurrent=max_concurrent,
            memory_threshold_percent=70.0,
            bypass_cache=True,
        )

        crawler = Crawler(backend=backend, crawl4ai_config=config)
        articles = await crawler.acrawl_many(urls)

        results = []
        for article in articles:
            results.append(
                {
                    "url": article.url,
                    "title": article.title,
                    "markdown": article.markdown,
                    "success": article.success,
                }
            )

        return results

    except Exception as e:
        logger.error(f"Failed to crawl URLs: {e}")
        return [
            {
                "url": url,
                "title": "Failed to crawl",
                "markdown": f"Error: {str(e)}",
                "success": False,
            }
            for url in urls
        ]


async def acrawl_many_stream_tool(
    urls: List[str], max_concurrent: int = 10
) -> AsyncGenerator[dict, None]:
    """
    Stream crawl results as they become available.
    Only available with Crawl4AI backend.

    Args:
        urls: List of URLs to crawl
        max_concurrent: Maximum concurrent requests

    Yields:
        Dictionaries with essential crawled content as they complete
    """
    try:
        config = Crawl4AIConfig(
            headless=True,
            verbose=False,
            max_concurrent=max_concurrent,
            memory_threshold_percent=70.0,
            bypass_cache=True,
        )

        crawler = Crawler(backend="crawl4ai", crawl4ai_config=config)

        async for article in crawler.acrawl_many_stream(urls):
            yield {
                "url": article.url,
                "title": article.title,
                "markdown": article.markdown,
                "success": article.success,
            }

    except Exception as e:
        logger.error(f"Failed to stream crawl URLs: {e}")
        for url in urls:
            yield {
                "url": url,
                "title": "Failed to crawl",
                "markdown": f"Error: {str(e)}",
                "success": False,
            }


async def crawl_recursive_tool(
    start_urls: List[str],
    max_depth: int = 3,
    domain_filter: Optional[str] = None,
    max_concurrent: int = 10,
) -> List[dict]:
    """
    Recursively crawl URLs up to a specified depth.

    Args:
        start_urls: Initial URLs to start crawling from
        max_depth: Maximum depth to crawl (default: 3)
        domain_filter: Optional domain filter to limit crawling scope
        max_concurrent: Maximum concurrent requests

    Returns:
        List of dictionaries with essential crawled content
    """
    try:
        config = Crawl4AIConfig(
            headless=True,
            verbose=False,
            max_concurrent=max_concurrent,
            memory_threshold_percent=70.0,
            bypass_cache=True,
        )

        crawler = Crawler(backend="crawl4ai", crawl4ai_config=config)
        articles = await crawler.acrawl_recursive(
            start_urls=start_urls, max_depth=max_depth, domain_filter=domain_filter
        )

        results = []
        for article in articles:
            results.append(
                {
                    "url": article.url,
                    "title": article.title,
                    "markdown": article.markdown,
                    "success": article.success,
                }
            )

        return results

    except Exception as e:
        logger.error(f"Failed to recursively crawl URLs: {e}")
        return [
            {
                "url": url,
                "title": "Failed to crawl",
                "markdown": f"Error: {str(e)}",
                "success": False,
            }
            for url in start_urls
        ]


async def crawl_and_chunk_markdown_tool(
    url: str, chunk_size: int = 1000, max_concurrent: int = 10
) -> List[dict]:
    """
    Crawl a URL and chunk the markdown content.

    Args:
        url: URL to crawl
        chunk_size: Size of each chunk in characters
        max_concurrent: Maximum concurrent requests

    Returns:
        List of dictionaries with chunked markdown content
    """
    try:
        config = Crawl4AIConfig(
            headless=True,
            verbose=False,
            max_concurrent=max_concurrent,
            memory_threshold_percent=70.0,
            bypass_cache=True,
        )

        crawler = Crawler(backend="crawl4ai", crawl4ai_config=config)
        chunks = await crawler.acrawl_and_chunk_markdown(url, chunk_size=chunk_size)

        results = []
        for i, chunk_content in enumerate(chunks):
            results.append(
                {
                    "url": url,
                    "title": f"Chunk {i + 1}",
                    "markdown": chunk_content,
                    "success": True,
                }
            )

        return results

    except Exception as e:
        logger.error(f"Failed to crawl and chunk {url}: {e}")
        return [
            {
                "url": url,
                "title": "Failed to crawl",
                "markdown": f"Error: {str(e)}",
                "success": False,
            }
        ]


def crawl_recursive_sync_tool(
    start_urls: List[str],
    max_depth: int = 3,
    domain_filter: Optional[str] = None,
    max_concurrent: int = 10,
) -> List[dict]:
    """
    Synchronous wrapper for recursive crawling.

    Args:
        start_urls: Initial URLs to start crawling from
        max_depth: Maximum depth to crawl (default: 3)
        domain_filter: Optional domain filter to limit crawling scope
        max_concurrent: Maximum concurrent requests

    Returns:
        List of dictionaries with essential crawled content
    """
    return asyncio.run(
        crawl_recursive_tool(
            start_urls=start_urls,
            max_depth=max_depth,
            domain_filter=domain_filter,
            max_concurrent=max_concurrent,
        )
    )


def crawl_and_chunk_markdown_sync_tool(
    url: str, chunk_size: int = 1000, max_concurrent: int = 10
) -> List[dict]:
    """
    Synchronous wrapper for crawling and chunking markdown.

    Args:
        url: URL to crawl
        chunk_size: Size of each chunk in characters
        max_concurrent: Maximum concurrent requests

    Returns:
        List of dictionaries with chunked markdown content
    """
    return asyncio.run(
        crawl_and_chunk_markdown_tool(
            url=url, chunk_size=chunk_size, max_concurrent=max_concurrent
        )
    )


# Export the main tools that are used by agents
__all__ = [
    "crawl_tool",
    "crawl_many_tool",
    # Async versions for advanced usage
    "acrawl_tool",
    "acrawl_many_tool",
    "acrawl_many_stream_tool",
    "crawl_recursive_tool",
    "crawl_and_chunk_markdown_tool",
    # Sync wrappers
    "crawl_recursive_sync_tool",
    "crawl_and_chunk_markdown_sync_tool",
    "crawl_stream_tool",
]
