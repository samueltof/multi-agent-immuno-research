from typing import Literal, Union, Optional, Any
from typing_extensions import TypedDict
from langgraph.graph import MessagesState

from src.config import TEAM_MEMBERS

# Define routing options
OPTIONS = TEAM_MEMBERS + ["FINISH"]


class Router(TypedDict):
    """Worker to route to next. If no workers needed, route to FINISH."""

    next: Union[Literal["researcher"], Literal["coder"], Literal["browser"], Literal["reporter"], Literal["data_analyst"], Literal["biomedical_researcher"], Literal["FINISH"]]


class State(MessagesState):
    """State for the agent system, extends MessagesState with next field."""

    # Constants
    TEAM_MEMBERS: list[str]

    # Runtime Variables
    next: str
    full_plan: str
    deep_thinking_mode: bool
    search_before_planning: bool
    
    # Agent-specific results
    biomedical_research_result: Optional[Any]  # Stores detailed biomedical research results
