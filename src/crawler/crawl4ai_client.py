"""
Improved Crawl4AI client based on validated examples.
Simplified implementation focusing on content extraction only.
"""

import asyncio
import logging
import os
import psutil
import logging
from typing import List, Optional, Dict, Any, AsyncGenerator
from dataclasses import dataclass, field
from urllib.parse import urldefrag
import re

from crawl4ai import (
    AsyncWebCrawler, 
    BrowserConfig, 
    CrawlerRunConfig, 
    CacheMode,
    MemoryAdaptiveDispatcher,
    LLMConfig
)
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai.content_filter_strategy import BM25ContentFilter, PruningContentFilter, LLMContentFilter

from .readability_extractor import ReadabilityExtractor
from .article import Article

logger = logging.getLogger(__name__)


@dataclass
class Crawl4AIConfig:
    """Simplified configuration for Crawl4AI crawler."""
    headless: bool = True
    verbose: bool = False
    max_concurrent: int = 5
    memory_threshold_percent: float = 70.0
    check_interval: float = 1.0
    timeout: int = 30
    bypass_cache: bool = True
    # Browser optimizations from examples
    extra_browser_args: List[str] = field(default_factory=lambda: [
        "--disable-gpu", 
        "--disable-dev-shm-usage", 
        "--no-sandbox"
    ])
    
    # LLM Content Filtering Options (DEFAULT: ENABLED)
    use_llm_filter: bool = True  # Default to LLM filtering for better quality
    llm_provider: str = "openai/gpt-4.1-nano"  # Ultra-fast and cost-effective option
    llm_api_token: Optional[str] = None  # Will use environment variable if None
    llm_filter_instruction: Optional[str] = None  # Custom instruction for LLM filtering
    chunk_token_threshold: int = 4096  # Token threshold for chunking
    llm_filter_verbose: bool = False  # Reduce noise in logs by default


class Crawl4AIClient:
    """
    Simplified Crawl4AI client following validated patterns.
    Focuses on content extraction without database operations.
    """
    
    def __init__(self, config: Optional[Crawl4AIConfig] = None):
        self.config = config or Crawl4AIConfig()
        self.readability_extractor = ReadabilityExtractor()
        
        # Browser configuration optimized for performance
        self.browser_config = BrowserConfig(
            browser_type="chromium",  # Standard browser type
            headless=self.config.headless,
            verbose=self.config.verbose
            # Note: extra browser args are handled via browser startup flags
        )
        
        # Content filter setup - choose between Pruning and LLM filtering
        if self.config.use_llm_filter:
            # LLM-based content filtering for high-quality extraction
            # Auto-detect available API keys
            api_token = self.config.llm_api_token
            if not api_token:
                # Try to use available API keys
                import os
                api_token = (
                    os.getenv("OPENAI_API_KEY") or 
                    os.getenv("BASIC_API_KEY") or 
                    os.getenv("REASONING_API_KEY")
                )
            
            llm_config = LLMConfig(
                provider=self.config.llm_provider,
                api_token=api_token
            )
            
            # Default instruction optimized for research and technical content
            default_instruction = """
            Focus on extracting the core educational and informational content.
            Include:
            - Key concepts, explanations, and insights
            - Important code examples and technical details
            - Main article content and research findings
            - Essential documentation and tutorials
            
            Exclude:
            - Navigation menus and sidebars
            - Advertisement content
            - Footer and header boilerplate
            - Cookie notices and popups
            - Social media widgets and sharing buttons
            - Comments sections (unless specifically relevant)
            
            Format the output as clean, well-structured markdown with:
            - Proper headers (# ## ###)
            - Code blocks with appropriate language tags
            - Clean bullet points and numbered lists
            - Preserved links for important references
            
            Optimize for token efficiency while maintaining content quality.
            """
            
            instruction = self.config.llm_filter_instruction or default_instruction
            
            self.content_filter = LLMContentFilter(
                llm_config=llm_config,
                instruction=instruction,
                chunk_token_threshold=self.config.chunk_token_threshold,
                verbose=self.config.llm_filter_verbose
            )
        else:
            # Default: Pruning-based content filtering for speed and efficiency
            self.content_filter = PruningContentFilter(
                threshold=0.48,  # Balanced pruning threshold
                min_word_threshold=30  # Keep sections with at least 30 words
            )
        
        # Advanced markdown generator with content filtering
        self.markdown_generator = DefaultMarkdownGenerator(
            content_source="cleaned_html",  # Use cleaned HTML for better results
            content_filter=self.content_filter,
            options={
                "ignore_links": False,  # Keep links for reference (especially useful with LLM filtering)
                "ignore_images": True,  # Remove images to reduce token usage
                "escape_html": True,
                "body_width": 0,  # No line wrapping
                "skip_internal_links": True,  # Skip internal page anchors
            }
        )
        
        # Crawler run configuration with advanced markdown generation
        self.crawl_config = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS if self.config.bypass_cache else CacheMode.ENABLED,
            stream=False,
            markdown_generator=self.markdown_generator,
            # Add timeout configuration
            page_timeout=self.config.timeout * 1000,  # Convert to milliseconds
            verbose=self.config.verbose
        )
        
        # Memory adaptive dispatcher for parallel crawling
        self.dispatcher = MemoryAdaptiveDispatcher(
            memory_threshold_percent=self.config.memory_threshold_percent,
            check_interval=self.config.check_interval,
            max_session_permit=self.config.max_concurrent
        )
    
    def _create_article_from_result(self, result) -> Article:
        """Create Article object from Crawl4AI result."""
        if not result.success:
            # Return minimal article for failed crawls
            return Article(
                url=result.url,
                title="Failed to crawl",
                content=f"Error: {result.error_message}",
                markdown=None,
                text=None,
                html=None,
                success=False
            )
        
        # Extract title from multiple sources with fallbacks
        title = None
        
        # Try to get title from Crawl4AI metadata first
        if hasattr(result, 'metadata') and result.metadata:
            title = result.metadata.get('title')
        
        # Try readability extraction if no title yet
        if not title:
            try:
                readability_result = self.readability_extractor.extract(
                    html=result.html,
                    url=result.url
                )
                title = readability_result.get('title')
            except Exception:
                pass
        
        # Try extracting from HTML <title> tag as fallback
        if not title and result.html:
            title_match = re.search(r'<title[^>]*>(.*?)</title>', result.html, re.IGNORECASE | re.DOTALL)
            if title_match:
                title = title_match.group(1).strip()
        
        # Final fallback
        if not title:
            title = f"Page from {result.url}"
        
        # Extract content using readability
        try:
            readability_result = self.readability_extractor.extract(
                html=result.html,
                url=result.url
            )
            content = readability_result.get('content', '')
            text = readability_result.get('text_content', '')
        except Exception:
            # Fallback to raw content
            content = result.html or ''
            text = result.cleaned_html or ''
        
        # Handle advanced markdown generation results
        markdown_content = None
        if hasattr(result, 'markdown') and result.markdown:
            # Check if it's a MarkdownGenerationResult object
            if hasattr(result.markdown, 'fit_markdown') and result.markdown.fit_markdown:
                # Use fit_markdown for cleaner, filtered content
                markdown_content = result.markdown.fit_markdown
            elif hasattr(result.markdown, 'raw_markdown') and result.markdown.raw_markdown:
                # Fallback to raw markdown
                markdown_content = result.markdown.raw_markdown
            elif hasattr(result.markdown, 'markdown_with_citations'):
                # Use version with citations if available
                markdown_content = result.markdown.markdown_with_citations
            else:
                # If it's a string (older API), use it directly
                markdown_content = str(result.markdown)
            

        
        return Article(
            url=result.url,
            title=title,
            content=content,
            markdown=markdown_content,
            text=text,
            html=result.html,
            success=True,
            metadata={
                'links': result.links,
                'media': result.media,
                'markdown_info': {
                    'has_fit_markdown': hasattr(result.markdown, 'fit_markdown') if hasattr(result, 'markdown') else False,
                    'has_citations': hasattr(result.markdown, 'markdown_with_citations') if hasattr(result, 'markdown') else False,
                    'content_filtered': self.content_filter is not None,
                    'filter_type': 'llm' if self.config.use_llm_filter else 'pruning',
                    'llm_provider': self.config.llm_provider if self.config.use_llm_filter else None
                },
                **(result.metadata if hasattr(result, 'metadata') and result.metadata else {})
            }
        )
    
    async def crawl(self, url: str) -> Article:
        """
        Crawl a single URL and return an Article.
        Simple, clean implementation following validated patterns.
        """
        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            result = await crawler.arun(url=url, config=self.crawl_config)
            return self._create_article_from_result(result)
    
    async def crawl_many(self, urls: List[str]) -> List[Article]:
        """
        Crawl multiple URLs in parallel using Crawl4AI's built-in arun_many.
        """
        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            results = await crawler.arun_many(
                urls=urls,
                config=self.crawl_config,
                dispatcher=self.dispatcher
            )
            return [self._create_article_from_result(result) for result in results]
    
    async def crawl_many_stream(self, urls: List[str]) -> AsyncGenerator[Article, None]:
        """
        Stream crawl results as they become available.
        """
        # For streaming, we'll use a simple approach - crawl in batches
        batch_size = min(self.config.max_concurrent, len(urls))
        
        for i in range(0, len(urls), batch_size):
            batch_urls = urls[i:i + batch_size]
            batch_results = await self.crawl_many(batch_urls)
            for article in batch_results:
                yield article
    
    async def crawl_recursive(
        self, 
        start_urls: List[str], 
        max_depth: int = 3, 
        domain_filter: Optional[str] = None
    ) -> List[Article]:
        """
        Recursively crawl a site following internal links.
        Based on the validated recursive crawling example.
        """
        visited = set()
        all_articles = []
        
        def normalize_url(url: str) -> str:
            """Remove fragment (part after #) for deduplication."""
            return urldefrag(url)[0]
        
        current_urls = set(normalize_url(url) for url in start_urls)
        
        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            for depth in range(max_depth):
                print(f"Crawling depth {depth + 1}/{max_depth}...")
                
                # Only crawl URLs we haven't seen yet
                urls_to_crawl = [url for url in current_urls if url not in visited]
                
                if not urls_to_crawl:
                    break
                
                # Batch-crawl all URLs at this depth
                results = await crawler.arun_many(
                    urls=urls_to_crawl,
                    config=self.crawl_config,
                    dispatcher=self.dispatcher
                )
                
                next_level_urls = set()
                
                for result in results:
                    norm_url = normalize_url(result.url)
                    visited.add(norm_url)
                    
                    article = self._create_article_from_result(result)
                    all_articles.append(article)
                    
                    if result.success and depth < max_depth - 1:
                        # Collect internal links for next depth
                        internal_links = result.links.get("internal", [])
                        for link in internal_links:
                            next_url = normalize_url(link["href"])
                            if next_url not in visited:
                                # Apply domain filter if specified
                                if domain_filter is None or domain_filter in next_url:
                                    next_level_urls.add(next_url)
                
                current_urls = next_level_urls
        
        return all_articles
    
    def crawl_and_chunk_markdown(
        self, 
        url: str, 
        chunk_size: int = 1000
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Crawl a markdown page and chunk it by headers.
        Based on the validated markdown chunking example.
        """
        async def _chunk_generator():
            article = await self.crawl(url)
            
            if not article.success or not article.markdown:
                yield {
                    'chunk_index': 0,
                    'content': article.content,
                    'url': url,
                    'title': article.title,
                    'headers': [],
                    'success': False
                }
                return
            
            markdown = article.markdown
            
            # Split by headers (# and ##)
            header_pattern = re.compile(r'^(# .+|## .+)$', re.MULTILINE)
            headers = [m.start() for m in header_pattern.finditer(markdown)] + [len(markdown)]
            
            for i, (start, end) in enumerate(zip(headers[:-1], headers[1:])):
                chunk = markdown[start:end].strip()
                if chunk:
                    # Further split if chunk is too large
                    if len(chunk) > chunk_size:
                        # Split by character count
                        for j in range(0, len(chunk), chunk_size):
                            sub_chunk = chunk[j:j + chunk_size]
                            yield {
                                'chunk_index': f"{i}_{j // chunk_size}",
                                'content': sub_chunk,
                                'url': url,
                                'title': article.title,
                                'headers': re.findall(r'^(# .+|## .+)', chunk, re.MULTILINE),
                                'success': True
                            }
                    else:
                        yield {
                            'chunk_index': i,
                            'content': chunk,
                            'url': url,
                            'title': article.title,
                            'headers': re.findall(r'^(# .+|## .+)', chunk, re.MULTILINE),
                            'success': True
                        }
        
        return _chunk_generator()
    
    def get_memory_usage(self) -> Dict[str, float]:
        """Get current memory usage statistics."""
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        
        return {
            'rss_mb': memory_info.rss / (1024 * 1024),
            'vms_mb': memory_info.vms / (1024 * 1024),
            'percent': process.memory_percent()
        }


# Sync wrapper for backward compatibility
class Crawl4AISyncClient:
    """Synchronous wrapper for the async Crawl4AI client."""
    
    def __init__(self, config: Optional[Crawl4AIConfig] = None):
        self.async_client = Crawl4AIClient(config)
    
    def _run_async(self, coro):
        """Safely run async function, handling existing event loops."""
        try:
            # Try to get the current event loop
            loop = asyncio.get_running_loop()
        except RuntimeError:
            # No event loop running, we can use asyncio.run()
            return asyncio.run(coro)
        else:
            # Event loop is running, we need to run in executor
            import concurrent.futures
            import threading
            
            # Create a new event loop in a separate thread
            def run_in_thread():
                new_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(new_loop)
                try:
                    return new_loop.run_until_complete(coro)
                finally:
                    new_loop.close()
            
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(run_in_thread)
                return future.result()
    
    def crawl(self, url: str) -> Article:
        """Sync version of crawl."""
        return self._run_async(self.async_client.crawl(url))
    
    def crawl_many(self, urls: List[str]) -> List[Article]:
        """Sync version of crawl_many."""
        return self._run_async(self.async_client.crawl_many(urls)) 