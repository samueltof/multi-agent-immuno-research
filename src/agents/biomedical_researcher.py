"""
Biomedical Researcher Agent - A PydanticAI agent integrated with biomedical MCP servers.

This agent combines PydanticAI's powerful agent capabilities with Model Context Protocol (MCP)
servers for accessing biomedical databases like PubMed, BioRxiv, ClinicalTrials.gov, etc.
It's designed to work within the LangGraph orchestration framework using centralized prompts.
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional
import asyncio
import os
import logging

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.models.anthropic import AnthropicModel

from ..config.agents import AGENT_LLM_MAP
from ..config import (
    REASONING_API_KEY,
    REASONING_BASE_URL,
    BASIC_API_KEY,
    BASIC_BASE_URL,
)
from ..prompts import get_processed_prompt

logger = logging.getLogger(__name__)


@dataclass
class BiomedicalResearchDeps:
    """Dependencies for the biomedical research agent."""
    user_context: Optional[str] = None
    research_focus: Optional[str] = None
    time_range: Optional[str] = None
    preferred_databases: Optional[List[str]] = None


class BiomedicalResearchOutput(BaseModel):
    """Structured output for biomedical research results."""
    summary: str = Field(description="Summary of the research findings")
    key_findings: List[str] = Field(description="List of key findings from the research")
    sources: List[Dict[str, str]] = Field(description="Sources used in the research")
    recommendations: List[str] = Field(description="Research recommendations and next steps")
    confidence_level: float = Field(description="Confidence level of the findings (0-1)", ge=0, le=1)


def get_biomedical_model():
    """Get the appropriate PydanticAI model for the biomedical researcher agent."""
    # Get configuration directly without creating LangChain LLM first
    agent_type = AGENT_LLM_MAP["biomedical_researcher"]
    
    if agent_type == "reasoning":
        from ..config import REASONING_MODEL, REASONING_API_KEY, REASONING_BASE_URL
        model_name = REASONING_MODEL
        api_key = REASONING_API_KEY
        base_url = REASONING_BASE_URL
    elif agent_type == "basic":
        from ..config import BASIC_MODEL, BASIC_API_KEY, BASIC_BASE_URL
        model_name = BASIC_MODEL
        api_key = BASIC_API_KEY
        base_url = BASIC_BASE_URL
    else:  # vision
        from ..config import VL_MODEL, VL_API_KEY, VL_BASE_URL
        model_name = VL_MODEL
        api_key = VL_API_KEY
        base_url = VL_BASE_URL
    
    # Fallback to environment variables if config is not set
    if not api_key:
        api_key = os.getenv('OPENAI_API_KEY') or os.getenv('LLM_API_KEY', 'no-api-key-provided')
    if not base_url:
        base_url = os.getenv('BASE_URL', 'https://api.openai.com/v1')
    if not model_name:
        model_name = "gpt-4o"  # fallback
    
    # Create PydanticAI model
    if 'claude' in model_name.lower():
        return AnthropicModel(
            model_name,
            api_key=os.getenv('ANTHROPIC_API_KEY', api_key)
        )
    else:
        # Import provider classes for PydanticAI
        from pydantic_ai.providers.openai import OpenAIProvider
        
        # Create provider with custom settings
        provider = OpenAIProvider(
            base_url=base_url,
            api_key=api_key
        )
        
        # Use OpenAI model with custom provider
        return OpenAIModel(
            model_name,
            provider=provider
        )


def create_biomedical_mcp_servers():
    """Create MCP servers for biomedical databases."""
    mcp_servers = []
    
    # Get the absolute path to the MCP servers
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    mcps_dir = os.path.join(project_root, "src", "service", "mcps")
    
    # PubMed MCP Server
    pubmed_server = MCPServerStdio(
        'python',
        [os.path.join(mcps_dir, 'pubmed_mcp.py')],
        tool_prefix='pubmed'
    )
    mcp_servers.append(pubmed_server)
    
    # BioRxiv MCP Server
    biorxiv_server = MCPServerStdio(
        'python',
        [os.path.join(mcps_dir, 'bioarxiv_mcp.py')],
        tool_prefix='biorxiv'
    )
    mcp_servers.append(biorxiv_server)
    
    # ClinicalTrials.gov MCP Server
    clinicaltrials_server = MCPServerStdio(
        'python',
        [os.path.join(mcps_dir, 'clinicaltrialsgov_mcp.py')],
        tool_prefix='clinicaltrials'
    )
    mcp_servers.append(clinicaltrials_server)
    
    # DrugBank MCP Server (if API key is available)
    drugbank_api_key = os.getenv('DRUGBANK_API_KEY')
    if drugbank_api_key:
        logger.info("DrugBank API key found - enabling DrugBank MCP server")
        drugbank_server = MCPServerStdio(
            'python',
            [os.path.join(mcps_dir, 'drugbank_mcp.py')],
            env={"DRUGBANK_API_KEY": drugbank_api_key},
            tool_prefix='drugbank'
        )
        mcp_servers.append(drugbank_server)
    else:
        logger.info("DrugBank API key not found - skipping DrugBank MCP server (set DRUGBANK_API_KEY to enable)")
    
    # OpenTargets MCP Server
    opentargets_server = MCPServerStdio(
        'python',
        [os.path.join(mcps_dir, 'opentargets_mcp.py')],
        tool_prefix='opentargets'
    )
    mcp_servers.append(opentargets_server)
    
    return mcp_servers


def create_biomedical_researcher_agent(template_vars: Optional[Dict[str, Any]] = None):
    """Create the biomedical researcher agent using centralized prompt system."""
    if template_vars is None:
        template_vars = {}
    
    # Get the processed prompt from the centralized system
    system_prompt = get_processed_prompt("biomedical_researcher", template_vars)
    
    return Agent(
        get_biomedical_model(),
        deps_type=BiomedicalResearchDeps,
        output_type=BiomedicalResearchOutput,
        mcp_servers=create_biomedical_mcp_servers(),
        retries=3,
        system_prompt=system_prompt,
        instructions="""Focus on providing comprehensive, evidence-based biomedical research insights. 
        Use the available biomedical database tools to gather information from multiple sources. 
        Always cite your sources and provide confidence assessments for your findings.
        Ensure your response follows the exact JSON structure required."""
    )


# LangGraph integration wrapper
class BiomedicalResearcherWrapper:
    """Wrapper class to integrate the PydanticAI biomedical researcher with LangGraph."""
    
    def __init__(self, template_vars: Optional[Dict[str, Any]] = None):
        self.template_vars = template_vars or {}
        self.agent = None
        self._mcp_context = None
    
    def _ensure_agent(self):
        """Ensure the agent is created with current template vars."""
        if self.agent is None:
            self.agent = create_biomedical_researcher_agent(self.template_vars)
    
    async def __aenter__(self):
        """Start MCP servers when entering async context."""
        self._ensure_agent()
        self._mcp_context = self.agent.run_mcp_servers()
        await self._mcp_context.__aenter__()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Stop MCP servers when exiting async context."""
        if self._mcp_context:
            await self._mcp_context.__aexit__(exc_type, exc_val, exc_tb)
    
    def update_template_vars(self, template_vars: Dict[str, Any]):
        """Update template variables and recreate agent."""
        self.template_vars.update(template_vars)
        self.agent = None  # Force recreation with new vars
    
    async def run_research(self, query: str, deps: Optional[BiomedicalResearchDeps] = None) -> BiomedicalResearchOutput:
        """Run biomedical research with the given query and dependencies."""
        if deps is None:
            deps = BiomedicalResearchDeps()
        
        self._ensure_agent()
        
        try:
            result = await self.agent.run(query, deps=deps)
            return result.data
        except Exception as e:
            logger.error(f"Error in biomedical research: {e}")
            # Return a structured error response
            return BiomedicalResearchOutput(
                summary=f"Error occurred during biomedical research: {str(e)}",
                key_findings=[],
                sources=[],
                recommendations=["Please check the configuration and try again"],
                confidence_level=0.0
            )
    
    async def run_research_stream(self, query: str, deps: Optional[BiomedicalResearchDeps] = None):
        """Run biomedical research with streaming output."""
        if deps is None:
            deps = BiomedicalResearchDeps()
        
        self._ensure_agent()
        
        try:
            async with self.agent.run_stream(query, deps=deps) as result:
                async for chunk in result.stream_text(delta=True):
                    yield chunk
        except Exception as e:
            logger.error(f"Error in streaming biomedical research: {e}")
            yield f"Error occurred during research: {str(e)}"


# Function to be used by LangGraph nodes
async def biomedical_researcher_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    LangGraph node function for biomedical research.
    
    This function integrates the PydanticAI biomedical researcher agent
    into the LangGraph workflow using the centralized prompt system.
    """
    from ..prompts import apply_prompt_template
    
    # Apply prompt template to get the processed query
    try:
        prompt_messages = apply_prompt_template("biomedical_researcher", state)
        query = prompt_messages[-1]["content"] if prompt_messages else state.get("messages", [""])[-1]
    except Exception:
        # Fallback to direct message content
        messages = state.get("messages", [])
        if messages:
            query = messages[-1].content if hasattr(messages[-1], 'content') else str(messages[-1])
        else:
            query = state.get("query", "Please provide a research query.")
    
    # Extract dependencies from state
    deps = BiomedicalResearchDeps(
        user_context=state.get("user_context"),
        research_focus=state.get("research_focus"),
        time_range=state.get("time_range"),
        preferred_databases=state.get("preferred_databases")
    )
    
    # Prepare template variables for the agent
    template_vars = {
        "research_focus": state.get("research_focus", ""),
        "user_context": state.get("user_context", ""),
        "time_range": state.get("time_range", ""),
        "preferred_databases": str(state.get("preferred_databases", [])) if state.get("preferred_databases") else "",
    }
    
    # Run the biomedical research
    async with BiomedicalResearcherWrapper(template_vars) as researcher:
        result = await researcher.run_research(query, deps)
    
    # Return updated state
    return {
        "biomedical_research_result": result,
        "messages": state.get("messages", []) + [
            f"Biomedical Research Summary: {result.summary}"
        ]
    }


# Function for streaming biomedical research (for real-time updates)
async def biomedical_researcher_streaming_node(state: Dict[str, Any], writer):
    """
    LangGraph streaming node function for biomedical research.
    """
    from ..prompts import apply_prompt_template
    
    # Apply prompt template to get the processed query
    try:
        prompt_messages = apply_prompt_template("biomedical_researcher", state)
        query = prompt_messages[-1]["content"] if prompt_messages else state.get("messages", [""])[-1]
    except Exception:
        # Fallback to direct message content
        messages = state.get("messages", [])
        if messages:
            query = messages[-1].content if hasattr(messages[-1], 'content') else str(messages[-1])
        else:
            query = state.get("query", "Please provide a research query.")
    
    # Extract dependencies from state
    deps = BiomedicalResearchDeps(
        user_context=state.get("user_context"),
        research_focus=state.get("research_focus"),
        time_range=state.get("time_range"),
        preferred_databases=state.get("preferred_databases")
    )
    
    # Prepare template variables for the agent
    template_vars = {
        "research_focus": state.get("research_focus", ""),
        "user_context": state.get("user_context", ""),
        "time_range": state.get("time_range", ""),
        "preferred_databases": str(state.get("preferred_databases", [])) if state.get("preferred_databases") else "",
    }
    
    # Stream the biomedical research
    async with BiomedicalResearcherWrapper(template_vars) as researcher:
        async for chunk in researcher.run_research_stream(query, deps):
            writer(chunk)
    
    return {
        "messages": state.get("messages", []) + [
            "Biomedical research completed with streaming output."
        ]
    } 