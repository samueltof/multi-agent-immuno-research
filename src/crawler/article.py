import re
from typing import Optional, Dict, Any
from urllib.parse import urljoin

from markdownify import markdownify as md


class Article:
    """
    Enhanced Article class supporting both legacy and new crawling backends.
    Maintains backward compatibility while adding new features.
    """
    
    def __init__(
        self, 
        title: str, 
        html_content: Optional[str] = None,
        # New parameters for improved implementation
        url: Optional[str] = None,
        content: Optional[str] = None,
        markdown: Optional[str] = None,
        text: Optional[str] = None,
        html: Optional[str] = None,
        success: bool = True,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize Article with support for both legacy and new parameters.
        
        Legacy parameters:
            title: Article title
            html_content: HTML content (legacy parameter)
            
        New parameters:
            url: Source URL
            content: Clean content text
            markdown: Markdown formatted content
            text: Plain text content
            html: Raw HTML content
            success: Whether the crawl was successful
            metadata: Additional metadata
        """
        self.title = title
        self.url = url or ""
        self.success = success
        self.metadata = metadata or {}
        
        # Handle both legacy and new content parameters
        self.html_content = html_content or html or content or ""
        self.content = content or html_content or ""
        self.markdown = markdown
        self.text = text
        self.html = html or html_content

    def to_markdown(self, including_title: bool = True) -> str:
        """Convert article to markdown format."""
        markdown = ""
        if including_title and self.title:
            markdown += f"# {self.title}\n\n"
        
        # Use existing markdown if available, otherwise convert from HTML
        if self.markdown:
            markdown += self.markdown
        elif self.html_content:
            markdown += md(self.html_content)
        elif self.content:
            markdown += self.content
        
        return markdown

    def to_message(self) -> list[dict]:
        """Convert article to message format with image support."""
        image_pattern = r"!\[.*?\]\((.*?)\)"

        content: list[dict[str, str]] = []
        parts = re.split(image_pattern, self.to_markdown())

        for i, part in enumerate(parts):
            if i % 2 == 1:
                # Handle image URLs
                if self.url:
                    image_url = urljoin(self.url, part.strip())
                else:
                    image_url = part.strip()
                content.append({"type": "image_url", "image_url": {"url": image_url}})
            else:
                content.append({"type": "text", "text": part.strip()})

        return content
    
    def get_content_length(self) -> int:
        """Get the length of the main content."""
        if self.content:
            return len(self.content)
        elif self.html_content:
            return len(self.html_content)
        elif self.text:
            return len(self.text)
        return 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert article to dictionary format."""
        return {
            "url": self.url,
            "title": self.title,
            "content": self.content,
            "markdown": self.markdown,
            "text": self.text,
            "html": self.html,
            "success": self.success,
            "content_length": self.get_content_length(),
            "metadata": self.metadata
        }
    
    def __repr__(self) -> str:
        """String representation of the article."""
        return f"Article(url='{self.url}', title='{self.title}', success={self.success})"
