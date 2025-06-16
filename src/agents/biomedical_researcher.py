"""
Biomedical Researcher Agent - A PydanticAI agent integrated with biomedical MCP servers.

This agent combines PydanticAI's powerful agent capabilities with Model Context Protocol (MCP)
servers for accessing biomedical databases like PubMed, BioRxiv, ClinicalTrials.gov, etc.
It's designed to work within the LangGraph orchestration framework.
"""

from dataclasses import dataclass
from contextlib import AsyncExitStack
from typing import Dict, List, Any, Optional
import asyncio
import os
import logging

from pydantic import BaseModel, Field

from ..config.agents import AGENT_LLM_MAP
from ..agents.llm import get_llm_by_type
from ..config import (
    REASONING_API_KEY,
    REASONING_BASE_URL,
    BASIC_API_KEY,
    BASIC_BASE_URL,
)

logger = logging.getLogger(__name__)

# Use try/except to handle import issues with pydantic-ai and OpenAI compatibility
try:
    from pydantic_ai import Agent, RunContext
    from pydantic_ai.mcp import MCPServerStdio
    from pydantic_ai.models.openai import OpenAIModel
    from pydantic_ai.models.anthropic import AnthropicModel
    PYDANTIC_AI_AVAILABLE = True
except ImportError as e:
    logger.warning(f"PydanticAI import failed: {e}. Biomedical researcher will use fallback mode.")
    PYDANTIC_AI_AVAILABLE = False
    # Define dummy classes for type hints
    Agent = None
    RunContext = None
    MCPServerStdio = None
    OpenAIModel = None
    AnthropicModel = None


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
    """Get the appropriate model for the biomedical researcher agent."""
    if not PYDANTIC_AI_AVAILABLE:
        logger.warning("PydanticAI not available, returning None for biomedical model")
        return None
        
    # Use the reasoning model type for biomedical research
    base_llm = get_llm_by_type(AGENT_LLM_MAP["biomedical_researcher"])
    
    # Convert the base LLM to PydanticAI compatible model
    # Extract model name from the LangChain LLM
    if hasattr(base_llm, 'model_name'):
        model_name = base_llm.model_name
    elif hasattr(base_llm, 'model'):
        model_name = base_llm.model
    else:
        model_name = "gpt-4o"  # fallback
    
    # Use the same API configuration as the rest of the application
    # Since biomedical_researcher is mapped to "reasoning" type, use REASONING_* configs
    agent_type = AGENT_LLM_MAP["biomedical_researcher"]
    if agent_type == "reasoning":
        api_key = REASONING_API_KEY
        base_url = REASONING_BASE_URL
    else:
        api_key = BASIC_API_KEY
        base_url = BASIC_BASE_URL
    
    # Fallback to environment variables if config is not set
    if not api_key:
        api_key = os.getenv('OPENAI_API_KEY') or os.getenv('LLM_API_KEY', 'no-api-key-provided')
    if not base_url:
        base_url = os.getenv('BASE_URL', 'https://api.openai.com/v1')
    
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


# Create MCP servers for biomedical databases
def create_biomedical_mcp_servers():
    """Create MCP servers for biomedical databases."""
    if not PYDANTIC_AI_AVAILABLE:
        logger.warning("PydanticAI not available, returning empty MCP servers list")
        return []
        
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


# Create the biomedical researcher agent
def create_biomedical_researcher_agent():
    """Create the biomedical researcher agent, with fallback if PydanticAI is not available."""
    if not PYDANTIC_AI_AVAILABLE:
        logger.warning("PydanticAI not available, biomedical researcher agent will use fallback mode")
        return None
        
    return Agent(
        get_biomedical_model(),
        deps_type=BiomedicalResearchDeps,
        output_type=BiomedicalResearchOutput,
        mcp_servers=create_biomedical_mcp_servers(),
        retries=3,  # Add retry configuration
        system_prompt="""You are an expert biomedical researcher AI assistant specializing in comprehensive literature review, 
        clinical research analysis, and drug discovery research. You have access to multiple biomedical databases through 
        specialized tools.

        Your capabilities include:
        - Searching and analyzing PubMed literature with pubmed_* tools
        - Finding preprints and recent research via biorxiv_* tools  
        - Investigating clinical trials using clinicaltrials_* tools
        - Researching drug information with drugbank_* tools (if DRUGBANK_API_KEY is configured)
        - Exploring disease-target associations via opentargets_* tools

        When conducting research:
        1. Always start by understanding the research question and context
        2. Use multiple databases for comprehensive coverage
        3. Cross-reference findings across different sources
        4. Provide evidence-based conclusions with proper citations
        5. Highlight any limitations or gaps in the available data
        6. Suggest follow-up research directions when appropriate

        IMPORTANT: Your summary should be a COMPLETE, SELF-CONTAINED report that includes:
        - A clear summary of the research findings
        - Specific key findings from the literature
        - Complete bibliographic citations formatted as: "Author et al. (Year). Title. Journal. PMID: XXXXX"
        - Actionable recommendations
        - Your confidence assessment

        The reporter agent will use your summary directly, so ensure it includes all necessary information including properly formatted citations. Do NOT rely on separate citation formatting - include everything in your summary.

        IMPORTANT CITATION FORMATTING:
        When you find research articles through the MCP tools, extract the complete citation information:
        - From PubMed results: Extract title, authors, journal, publication date, and PMID
        - From BioRxiv results: Extract title, authors, DOI, and submission date
        - From Clinical Trials: Extract study title, NCT number, phase, and status
        - From other databases: Extract available identifiers and metadata
        
        Format sources as detailed objects with ALL available information:
        - title: Full article/study title
        - authors: Author list or "Authors et al." format
        - journal: Journal name or database source
        - year: Publication year
        - pmid: PubMed ID (when available)
        - doi: DOI (when available)
        - url: URL or database identifier
        - database: Source database name

        IMPORTANT: Always respond with valid JSON structure containing:
        - summary: A COMPLETE, SELF-CONTAINED research report with embedded citations
        - key_findings: A list of strings with key insights
        - sources: A list of objects with COMPLETE source information as detailed above
        - recommendations: A list of strings with actionable recommendations
        - confidence_level: A float between 0.0 and 1.0 indicating confidence

        Example response format:
        {
            "summary": "Recent research on cancer immunogenomics has shown significant advances. Smith et al. (2024) demonstrated improved CAR-T cell efficacy (PMID: 12345678), while Johnson et al. (2024) reported novel biomarkers for patient selection (PMID: 87654321). These findings suggest...",
            "key_findings": ["Finding 1", "Finding 2"],
            "sources": [
                {
                    "title": "Full article title here",
                    "authors": "Smith JA, Johnson B, et al.",
                    "journal": "Nature Medicine",
                    "year": "2024",
                    "pmid": "12345678",
                    "database": "PubMed"
                }
            ],
            "recommendations": ["Recommendation 1"],
            "confidence_level": 0.8
        }
        
        CRITICAL: 
        1. When using MCP tools, carefully parse the returned information to extract ALL citation details
        2. Include complete citations WITHIN your summary text, not just in the sources array
        3. Your summary should be comprehensive enough to be used directly by the reporter
        4. Do not use placeholder citations - use the actual data returned by the tools
        """,
        instructions="""Focus on providing comprehensive, evidence-based biomedical research insights. 
        Use the available biomedical database tools to gather information from multiple sources. 
        Always cite your sources and provide confidence assessments for your findings.
        Ensure your response follows the exact JSON structure required."""
    )

# Initialize the agent
biomedical_researcher_agent = create_biomedical_researcher_agent()


# Define tools only if PydanticAI is available
if PYDANTIC_AI_AVAILABLE and biomedical_researcher_agent:
    @biomedical_researcher_agent.tool
    async def search_recent_literature(ctx: RunContext[BiomedicalResearchDeps], topic: str, days: int = 30) -> str:
        """Search for recent literature on a topic across multiple databases."""
        # This is a meta-tool that coordinates searches across multiple databases
        # The actual database searches will be handled by the MCP servers
        return f"Initiating comprehensive literature search for '{topic}' in the last {days} days across PubMed, BioRxiv, and other databases."

    @biomedical_researcher_agent.tool  
    async def analyze_research_trends(ctx: RunContext[BiomedicalResearchDeps], topic: str, time_period: str = "1 year") -> str:
        """Analyze research trends for a given topic over a specified time period."""
        return f"Analyzing research trends for '{topic}' over the last {time_period} using multiple biomedical databases."

    @biomedical_researcher_agent.tool
    async def find_clinical_evidence(ctx: RunContext[BiomedicalResearchDeps], condition: str, intervention: str) -> str:
        """Find clinical evidence for a specific condition and intervention."""
        return f"Searching for clinical evidence on '{intervention}' for '{condition}' across clinical trials and published literature."


# LangGraph integration wrapper
class BiomedicalResearcherWrapper:
    """Wrapper class to integrate the PydanticAI biomedical researcher with LangGraph."""
    
    def __init__(self):
        self.agent = biomedical_researcher_agent
        self._mcp_context = None
        self.fallback_mode = not PYDANTIC_AI_AVAILABLE or self.agent is None
    
    async def __aenter__(self):
        """Start MCP servers when entering async context."""
        if self.fallback_mode:
            logger.warning("Biomedical researcher in fallback mode - PydanticAI not available")
            return self
            
        self._mcp_context = self.agent.run_mcp_servers()
        await self._mcp_context.__aenter__()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Stop MCP servers when exiting async context."""
        if self._mcp_context:
            await self._mcp_context.__aexit__(exc_type, exc_val, exc_tb)
    
    async def run_research(self, query: str, deps: Optional[BiomedicalResearchDeps] = None) -> BiomedicalResearchOutput:
        """Run biomedical research with the given query and dependencies."""
        if deps is None:
            deps = BiomedicalResearchDeps()
        
        # Fallback mode - use basic LLM instead of PydanticAI
        if self.fallback_mode:
            logger.warning("Using fallback mode for biomedical research")
            base_llm = get_llm_by_type(AGENT_LLM_MAP["biomedical_researcher"])
            
            # Create a simple research prompt
            prompt = f"""You are a biomedical researcher. Please research the following query:
            
            Query: {query}
            
            Please provide:
            1. A summary of the topic
            2. Key findings
            3. Relevant sources (if known)
            4. Recommendations for further research
            
            Note: This is running in fallback mode without access to specialized biomedical databases."""
            
            try:
                response = await base_llm.ainvoke(prompt)
                content = response.content if hasattr(response, 'content') else str(response)
                
                return BiomedicalResearchOutput(
                    summary=content[:500] + "..." if len(content) > 500 else content,
                    key_findings=["Fallback mode - limited biomedical database access"],
                    sources=[{"title": "Fallback Response", "url": "N/A"}],
                    recommendations=["Install pydantic-ai for full biomedical research capabilities"],
                    confidence_level=0.3
                )
            except Exception as e:
                logger.error(f"Error in fallback biomedical research: {e}")
                return BiomedicalResearchOutput(
                    summary=f"Error in fallback mode: {str(e)}",
                    key_findings=[],
                    sources=[],
                    recommendations=["Check configuration and try again"],
                    confidence_level=0.0
                )
        
        # Normal PydanticAI mode
        try:
            result = await self.agent.run(query, deps=deps)
            return result.data
        except Exception as e:
            logger.error(f"Error in biomedical research: {e}")
            
            # If it's a validation error, try to extract useful information from the error
            if "result validation" in str(e).lower() or "exceeded maximum retries" in str(e).lower():
                logger.warning("PydanticAI validation failed, falling back to basic LLM")
                # Fall back to basic LLM approach
                base_llm = get_llm_by_type(AGENT_LLM_MAP["biomedical_researcher"])
                
                prompt = f"""You are a biomedical researcher. Research the following query and provide structured information:

Query: {query}

Please respond with a JSON structure containing:
- summary: A clear summary of the research topic
- key_findings: A list of key insights (even if limited)
- sources: A list of relevant sources you know about
- recommendations: A list of research recommendations
- confidence_level: A number between 0 and 1

Example response:
{{
    "summary": "Your research summary here",
    "key_findings": ["Finding 1", "Finding 2"],
    "sources": [{{"title": "Source Title", "url": "N/A"}}],
    "recommendations": ["Recommendation 1"],
    "confidence_level": 0.5
}}"""
                
                try:
                    response = await base_llm.ainvoke(prompt)
                    content = response.content if hasattr(response, 'content') else str(response)
                    
                    # Try to parse the JSON response
                    import json
                    try:
                        parsed_data = json.loads(content)
                        return BiomedicalResearchOutput(**parsed_data)
                    except (json.JSONDecodeError, TypeError):
                        # If JSON parsing fails, create a basic response
                        return BiomedicalResearchOutput(
                            summary=content[:500] + "..." if len(content) > 500 else content,
                            key_findings=["Validation error occurred - using fallback response"],
                            sources=[{"title": "Fallback Response", "url": "N/A"}],
                            recommendations=["Check PydanticAI configuration and try again"],
                            confidence_level=0.3
                        )
                except Exception as fallback_error:
                    logger.error(f"Error in fallback biomedical research: {fallback_error}")
                    return BiomedicalResearchOutput(
                        summary=f"Multiple errors occurred: {str(e)} | Fallback error: {str(fallback_error)}",
                        key_findings=[],
                        sources=[],
                        recommendations=["Check configuration and try again"],
                        confidence_level=0.0
                    )
            
            # Return a fallback response for other errors
            return BiomedicalResearchOutput(
                summary=f"Error occurred during research: {str(e)}",
                key_findings=[],
                sources=[],
                recommendations=["Please try again or contact support"],
                confidence_level=0.0
            )
    
    async def run_research_stream(self, query: str, deps: Optional[BiomedicalResearchDeps] = None):
        """Run biomedical research with streaming output."""
        if deps is None:
            deps = BiomedicalResearchDeps()
        
        # Fallback mode
        if self.fallback_mode:
            yield "Using fallback mode for biomedical research...\n"
            result = await self.run_research(query, deps)
            yield f"Research Summary: {result.summary}\n"
            return
        
        # Normal streaming mode
        async with self.agent.run_stream(query, deps=deps) as result:
            async for chunk in result.stream_text(delta=True):
                yield chunk


# Create the wrapper instance
biomedical_researcher_wrapper = BiomedicalResearcherWrapper()


# Function to be used by LangGraph nodes
async def biomedical_researcher_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    LangGraph node function for biomedical research.
    
    This function integrates the PydanticAI biomedical researcher agent
    into the LangGraph workflow.
    """
    from ..prompts import apply_prompt_template
    
    # Apply prompt template if available
    try:
        prompt_messages = apply_prompt_template("biomedical_researcher", state)
        query = prompt_messages[-1].content if prompt_messages else state.get("messages", [""])[-1]
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
    
    # Run the biomedical research
    async with biomedical_researcher_wrapper as researcher:
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
    
    # Apply prompt template if available
    try:
        prompt_messages = apply_prompt_template("biomedical_researcher", state)
        query = prompt_messages[-1].content if prompt_messages else state.get("messages", [""])[-1]
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
    
    # Stream the biomedical research
    async with biomedical_researcher_wrapper as researcher:
        async for chunk in researcher.run_research_stream(query, deps):
            writer(chunk)
    
    return {
        "messages": state.get("messages", []) + [
            "Biomedical research completed with streaming output."
        ]
    } 