import logging
from langchain_tavily import TavilySearch
from src.config import TAVILY_MAX_RESULTS
from .decorators import create_logged_tool

logger = logging.getLogger(__name__)

# Initialize Tavily search tool with logging using the new TavilySearch implementation
LoggedTavilySearch = create_logged_tool(TavilySearch)
tavily_tool = LoggedTavilySearch(
    max_results=TAVILY_MAX_RESULTS,
    topic="general"
)
