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
from pydantic_ai.providers.openai import OpenAIProvider

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
    """Get the appropriate PydanticAI model with proper Portkey integration."""
    try:
        from ..config.agents import get_agent_full_config
        config_dict = get_agent_full_config("biomedical_researcher")
        
        # Use the new modular system to create the model
        model = _create_pydantic_ai_model_from_config(config_dict)
        logger.info(f"Created biomedical model successfully: {config_dict['model']} via {config_dict['provider']}")
        return model
        
    except Exception as e:
        logger.error(f"Failed to create biomedical model from config: {e}")
        # Fallback to legacy system
        logger.info("Falling back to legacy model creation")
        return _get_biomedical_model_legacy()


def _create_pydantic_ai_model_from_config(config):
    """Convert provider config to PydanticAI model with proper Portkey support."""
    from pydantic_ai.models.openai import OpenAIModel
    from pydantic_ai.models.anthropic import AnthropicModel
    from pydantic_ai.providers.openai import OpenAIProvider
    from pydantic_ai.providers.anthropic import AnthropicProvider
    from ..config.llm_providers import ProviderType
    
    # Handle both dictionary and object configurations
    if isinstance(config, dict):
        provider_type = config.get('provider')
        model_name = config.get('model')
        api_key = config.get('api_key')
        base_url = config.get('base_url')
        portkey_api_key = config.get('portkey_api_key') or os.getenv('PORTKEY_API_KEY')
        
        # Handle virtual key lookup more carefully
        virtual_key = config.get('virtual_key')
        if not virtual_key and provider_type:
            # Convert provider_type to string if it's an enum
            provider_str = str(provider_type).upper() if hasattr(provider_type, 'upper') else provider_type.value.upper()
            env_var_name = f'PORTKEY_{provider_str.replace("PORTKEY_", "")}_VIRTUAL_KEY'
            virtual_key = os.getenv(env_var_name)
            
        azure_endpoint = config.get('azure_endpoint')
        region = config.get('region', 'us-east-1')
    else:
        # Object-style access for backwards compatibility
        provider_type = config.provider
        model_name = config.model
        api_key = getattr(config, 'api_key', None)
        base_url = getattr(config, 'base_url', None)
        portkey_api_key = getattr(config, 'portkey_api_key', None)
        virtual_key = getattr(config, 'virtual_key', None)
        azure_endpoint = getattr(config, 'azure_endpoint', None)
        region = getattr(config, 'region', 'us-east-1')
    
    if provider_type == ProviderType.OPENAI:
        # Direct OpenAI provider
        logger.info("Creating direct OpenAI provider")
        
        provider_kwargs = {}
        if api_key:
            provider_kwargs['api_key'] = api_key
        if base_url:
            provider_kwargs['base_url'] = base_url
            
        provider = OpenAIProvider(**provider_kwargs)
        return OpenAIModel(model_name, provider=provider)
    
    elif provider_type == ProviderType.ANTHROPIC:
        # Direct Anthropic
        provider_kwargs = {}
        if api_key:
            provider_kwargs['api_key'] = api_key
            
        provider = AnthropicProvider(**provider_kwargs)
        return AnthropicModel(model_name, provider=provider)
    
    elif provider_type in [ProviderType.PORTKEY_OPENAI, ProviderType.PORTKEY_ANTHROPIC, 
                           ProviderType.PORTKEY_BEDROCK, ProviderType.PORTKEY_AZURE]:
        # FIXED: Use Portkey client directly as OpenAI client 
        try:
            from portkey_ai import Portkey
            
            logger.info(f"Creating Portkey client provider for {provider_type}")
            
            # Create Portkey configuration
            portkey_config = {
                "api_key": api_key or os.getenv("OPENAI_API_KEY"),  # Fallback to OpenAI key
            }
            
            # Determine the provider for Portkey config
            if provider_type == ProviderType.PORTKEY_OPENAI:
                portkey_config["provider"] = "openai"
            elif provider_type == ProviderType.PORTKEY_ANTHROPIC:
                portkey_config["provider"] = "anthropic"  
            elif provider_type == ProviderType.PORTKEY_BEDROCK:
                portkey_config["provider"] = "bedrock"
            elif provider_type == ProviderType.PORTKEY_AZURE:
                portkey_config["provider"] = "azure"
            
            # Add virtual key if available
            if virtual_key:
                portkey_config["virtual_key"] = virtual_key
                logger.info(f"Using Portkey virtual key: {virtual_key}")
            
            # Add model override
            portkey_config["override_params"] = {
                "model": model_name
            }
            
            # Add metadata for observability
            metadata = {
                "env": os.getenv("ENVIRONMENT", "development"),
                "_agent": "biomedical_researcher",
                "_model": model_name
            }
            
            # Create Portkey client
            portkey_client = Portkey(
                api_key=portkey_api_key,
                config=portkey_config,
                metadata=metadata
            )
            
            # Use Portkey client as the OpenAI client
            provider = OpenAIProvider(openai_client=portkey_client)
            
            logger.info(f"Successfully created Portkey client provider")
            return OpenAIModel(model_name, provider=provider)
            
        except ImportError as e:
            logger.error(f"Portkey import failed: {e}. Falling back to direct OpenAI")
            # Fallback to direct OpenAI if Portkey is not available
            provider = OpenAIProvider(
                api_key=os.getenv("OPENAI_API_KEY"),
                base_url="https://api.openai.com/v1"
            )
            return OpenAIModel(model_name, provider=provider)
        except Exception as e:
            logger.error(f"Portkey client setup failed: {e}. Falling back to direct OpenAI")
            # Fallback to direct OpenAI if Portkey setup fails
            provider = OpenAIProvider(
                api_key=os.getenv("OPENAI_API_KEY"),
                base_url="https://api.openai.com/v1"
            )
            return OpenAIModel(model_name, provider=provider)
    
    elif provider_type == ProviderType.DEEPSEEK:
        # DeepSeek using OpenAI-compatible interface
        provider = OpenAIProvider(
            api_key=api_key,
            base_url=base_url or "https://api.deepseek.com"
        )
        return OpenAIModel(model_name, provider=provider)
    
    elif provider_type == ProviderType.AZURE:
        # Azure OpenAI
        provider = OpenAIProvider(
            api_key=api_key,
            base_url=f"{azure_endpoint}/openai/deployments/{model_name}",
        )
        return OpenAIModel(model_name, provider=provider)
    
    elif provider_type == ProviderType.BEDROCK:
        # AWS Bedrock
        try:
            from pydantic_ai.models.bedrock import BedrockModel
            
            return BedrockModel(model_name, region=region)
            
        except ImportError:
            logger.error("AWS Bedrock dependencies not installed")
            raise RuntimeError("Bedrock provider requires additional dependencies")
    
    else:
        raise ValueError(f"Unsupported provider type for PydanticAI: {provider_type}")


def _get_biomedical_model_legacy():
    """Legacy biomedical model creation (fallback for backward compatibility)."""
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
    
    # TEMPORARY FIX: Use direct OpenAI for MCP compatibility
    # The Portkey integration works, but MCP servers have serialization issues with Portkey clients
    # TODO: Remove this fallback once PydanticAI fixes NotGiven serialization in MCP context
    logger.info("Using direct OpenAI model for MCP compatibility (avoiding NotGiven serialization)")
    
    from pydantic_ai.models.openai import OpenAIModel
    from pydantic_ai.providers.openai import OpenAIProvider
    
    # Use direct OpenAI to avoid MCP serialization issues
    direct_model = OpenAIModel(
        "gpt-4o-mini",
        provider=OpenAIProvider(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url="https://api.openai.com/v1"
        )
    )
    
    return Agent(
        direct_model,  # Use direct model instead of get_biomedical_model()
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
    
    def research(self, query: str, deps: Optional[BiomedicalResearchDeps] = None) -> BiomedicalResearchOutput:
        """Synchronous wrapper for biomedical research."""
        import asyncio
        
        async def _run():
            async with self:
                return await self.run_research(query, deps)
        
        try:
            # Try to get the current event loop
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If there's already a running loop, we need to run in a new thread
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, _run())
                    return future.result()
            else:
                # No running loop, safe to use asyncio.run
                return asyncio.run(_run())
        except Exception as e:
            logger.error(f"Error in synchronous biomedical research: {e}")
            # Return a structured error response
            return BiomedicalResearchOutput(
                summary=f"Error occurred during biomedical research: {str(e)}",
                key_findings=[],
                sources=[],
                recommendations=["Please check the configuration and try again"],
                confidence_level=0.0
            )
    
    async def run_research(self, query: str, deps: Optional[BiomedicalResearchDeps] = None) -> BiomedicalResearchOutput:
        """Run biomedical research with the given query and dependencies."""
        if deps is None:
            deps = BiomedicalResearchDeps()
        
        self._ensure_agent()
        
        try:
            result = await self.agent.run(query, deps=deps)
            return result.output
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