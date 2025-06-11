"""
Tests for the Biomedical Researcher Agent.

This module tests the PydanticAI + MCP integration for biomedical research,
including both unit tests and integration tests.
"""

import pytest
import asyncio
import os
from unittest.mock import Mock, patch, AsyncMock
from dataclasses import dataclass
from typing import Dict, Any

# Import the biomedical researcher components
from src.agents.biomedical_researcher import (
    BiomedicalResearchDeps,
    BiomedicalResearchOutput,
    biomedical_researcher_agent,
    biomedical_researcher_wrapper,
    biomedical_researcher_node,
    create_biomedical_mcp_servers,
    get_biomedical_model
)


class TestBiomedicalResearchDeps:
    """Test the BiomedicalResearchDeps dataclass."""
    
    def test_deps_creation_with_defaults(self):
        """Test creating deps with default values."""
        deps = BiomedicalResearchDeps()
        assert deps.user_context is None
        assert deps.research_focus is None
        assert deps.time_range is None
        assert deps.preferred_databases is None
    
    def test_deps_creation_with_values(self):
        """Test creating deps with specific values."""
        deps = BiomedicalResearchDeps(
            user_context="PhD researcher in oncology",
            research_focus="cancer immunotherapy",
            time_range="last 2 years",
            preferred_databases=["pubmed", "clinicaltrials"]
        )
        assert deps.user_context == "PhD researcher in oncology"
        assert deps.research_focus == "cancer immunotherapy"
        assert deps.time_range == "last 2 years"
        assert deps.preferred_databases == ["pubmed", "clinicaltrials"]


class TestBiomedicalResearchOutput:
    """Test the BiomedicalResearchOutput model."""
    
    def test_output_creation_valid(self):
        """Test creating a valid research output."""
        output = BiomedicalResearchOutput(
            summary="Test summary",
            key_findings=["Finding 1", "Finding 2"],
            sources=[{"title": "Test Paper", "pmid": "12345"}],
            recommendations=["Recommendation 1"],
            confidence_level=0.8
        )
        assert output.summary == "Test summary"
        assert len(output.key_findings) == 2
        assert len(output.sources) == 1
        assert output.confidence_level == 0.8
    
    def test_output_confidence_validation(self):
        """Test confidence level validation."""
        # Valid confidence levels
        output1 = BiomedicalResearchOutput(
            summary="Test",
            key_findings=[],
            sources=[],
            recommendations=[],
            confidence_level=0.0
        )
        assert output1.confidence_level == 0.0
        
        output2 = BiomedicalResearchOutput(
            summary="Test",
            key_findings=[],
            sources=[],
            recommendations=[],
            confidence_level=1.0
        )
        assert output2.confidence_level == 1.0
        
        # Invalid confidence level should raise validation error
        with pytest.raises(ValueError):
            BiomedicalResearchOutput(
                summary="Test",
                key_findings=[],
                sources=[],
                recommendations=[],
                confidence_level=1.5
            )


class TestMCPServerCreation:
    """Test MCP server creation functionality."""
    
    @patch('os.path.exists')
    def test_create_biomedical_mcp_servers(self, mock_exists):
        """Test creation of biomedical MCP servers."""
        # Mock that MCP files exist
        mock_exists.return_value = True
        
        servers = create_biomedical_mcp_servers()
        
        # Should create at least 4 servers (PubMed, BioRxiv, ClinicalTrials, OpenTargets)
        assert len(servers) >= 4
        
        # Check that prefixes are set correctly
        server_prefixes = []
        for server in servers:
            if hasattr(server, 'tool_prefix'):
                server_prefixes.append(server.tool_prefix)
        
        expected_prefixes = ['pubmed', 'biorxiv', 'clinicaltrials', 'opentargets']
        for prefix in expected_prefixes:
            assert prefix in server_prefixes
    
    @patch.dict(os.environ, {'DRUGBANK_API_KEY': 'test-key'})
    @patch('os.path.exists')
    def test_create_biomedical_mcp_servers_with_drugbank(self, mock_exists):
        """Test MCP server creation includes DrugBank when API key is available."""
        mock_exists.return_value = True
        
        servers = create_biomedical_mcp_servers()
        
        # Should include DrugBank server when API key is present
        drugbank_found = False
        for server in servers:
            if hasattr(server, 'tool_prefix') and server.tool_prefix == 'drugbank':
                drugbank_found = True
                break
        
        assert drugbank_found, "DrugBank server should be included when API key is available"


class TestBiomedicalModel:
    """Test biomedical model configuration."""
    
    @patch('src.agents.biomedical_researcher.get_llm_by_type')
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_get_biomedical_model_openai(self, mock_get_llm):
        """Test getting OpenAI model for biomedical research."""
        mock_llm = Mock()
        mock_llm.model_name = "gpt-4o"
        mock_get_llm.return_value = mock_llm
        
        model = get_biomedical_model()
        
        # Should return an OpenAI-compatible model
        assert model is not None
        mock_get_llm.assert_called_once()
    
    @patch('src.agents.biomedical_researcher.get_llm_by_type')
    @patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'})
    def test_get_biomedical_model_claude(self, mock_get_llm):
        """Test getting Claude model for biomedical research."""
        mock_llm = Mock()
        mock_llm.model_name = "claude-3-sonnet"
        mock_get_llm.return_value = mock_llm
        
        model = get_biomedical_model()
        
        assert model is not None
        mock_get_llm.assert_called_once()


class TestBiomedicalResearcherWrapper:
    """Test the BiomedicalResearcherWrapper class."""
    
    def test_wrapper_initialization(self):
        """Test wrapper initialization."""
        wrapper = biomedical_researcher_wrapper
        assert wrapper.agent is not None
        assert wrapper._mcp_context is None
    
    @pytest.mark.asyncio
    async def test_wrapper_context_management(self):
        """Test wrapper async context management."""
        with patch.object(biomedical_researcher_agent, 'run_mcp_servers') as mock_run_mcp:
            mock_context = AsyncMock()
            mock_run_mcp.return_value = mock_context
            
            async with biomedical_researcher_wrapper as wrapper:
                assert wrapper is not None
                mock_context.__aenter__.assert_called_once()
            
            mock_context.__aexit__.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_run_research_success(self):
        """Test successful research execution."""
        with patch.object(biomedical_researcher_agent, 'run') as mock_run:
            mock_result = Mock()
            mock_result.data = BiomedicalResearchOutput(
                summary="Test research results",
                key_findings=["Finding 1"],
                sources=[{"title": "Test Paper"}],
                recommendations=["Test recommendation"],
                confidence_level=0.9
            )
            mock_run.return_value = mock_result
            
            with patch.object(biomedical_researcher_wrapper, '_mcp_context', None):
                result = await biomedical_researcher_wrapper.run_research("test query")
            
            assert isinstance(result, BiomedicalResearchOutput)
            assert result.summary == "Test research results"
            assert result.confidence_level == 0.9
    
    @pytest.mark.asyncio
    async def test_run_research_error_handling(self):
        """Test error handling during research."""
        with patch.object(biomedical_researcher_agent, 'run', side_effect=Exception("Test error")):
            with patch.object(biomedical_researcher_wrapper, '_mcp_context', None):
                result = await biomedical_researcher_wrapper.run_research("test query")
            
            assert isinstance(result, BiomedicalResearchOutput)
            assert "Error occurred during research" in result.summary
            assert result.confidence_level == 0.0


class TestLangGraphIntegration:
    """Test LangGraph integration functionality."""
    
    @pytest.mark.asyncio
    async def test_biomedical_researcher_node_basic(self):
        """Test basic biomedical researcher node functionality."""
        state = {
            "messages": ["Research CRISPR gene therapy"],
            "user_context": "Medical researcher",
            "research_focus": "gene therapy"
        }
        
        with patch('src.agents.biomedical_researcher.biomedical_researcher_wrapper') as mock_wrapper:
            mock_wrapper_instance = AsyncMock()
            mock_wrapper.__aenter__ = AsyncMock(return_value=mock_wrapper_instance)
            mock_wrapper.__aexit__ = AsyncMock()
            
            mock_result = BiomedicalResearchOutput(
                summary="CRISPR research summary",
                key_findings=["CRISPR is promising"],
                sources=[{"title": "CRISPR Study"}],
                recommendations=["Continue research"],
                confidence_level=0.8
            )
            mock_wrapper_instance.run_research.return_value = mock_result
            
            result_state = await biomedical_researcher_node(state)
            
            assert "biomedical_research_result" in result_state
            assert "messages" in result_state
            assert len(result_state["messages"]) > len(state["messages"])
    
    @pytest.mark.asyncio
    async def test_biomedical_researcher_node_with_prompt_template(self):
        """Test node with prompt template application."""
        state = {
            "messages": ["What are the latest developments in Alzheimer's treatment?"],
        }
        
        with patch('src.agents.biomedical_researcher.apply_prompt_template') as mock_prompt:
            mock_prompt.return_value = [Mock(content="Processed query")]
            
            with patch('src.agents.biomedical_researcher.biomedical_researcher_wrapper') as mock_wrapper:
                mock_wrapper_instance = AsyncMock()
                mock_wrapper.__aenter__ = AsyncMock(return_value=mock_wrapper_instance)
                mock_wrapper.__aexit__ = AsyncMock()
                
                mock_result = BiomedicalResearchOutput(
                    summary="Alzheimer's research summary",
                    key_findings=["New treatments emerging"],
                    sources=[],
                    recommendations=[],
                    confidence_level=0.7
                )
                mock_wrapper_instance.run_research.return_value = mock_result
                
                result_state = await biomedical_researcher_node(state)
                
                assert result_state is not None
                mock_prompt.assert_called_once()
    
    def test_state_processing(self):
        """Test state processing for dependencies."""
        state = {
            "user_context": "Clinical researcher",
            "research_focus": "COVID-19 treatments",
            "time_range": "last 6 months",
            "preferred_databases": ["pubmed", "clinicaltrials"]
        }
        
        # This would normally be done inside the node function
        deps = BiomedicalResearchDeps(
            user_context=state.get("user_context"),
            research_focus=state.get("research_focus"),
            time_range=state.get("time_range"),
            preferred_databases=state.get("preferred_databases")
        )
        
        assert deps.user_context == "Clinical researcher"
        assert deps.research_focus == "COVID-19 treatments"
        assert deps.time_range == "last 6 months"
        assert deps.preferred_databases == ["pubmed", "clinicaltrials"]


class TestIntegrationScenarios:
    """Test real-world integration scenarios."""
    
    @pytest.mark.asyncio
    async def test_end_to_end_research_flow(self):
        """Test a complete research workflow."""
        # This is a more comprehensive integration test
        query = "Find recent research on mRNA vaccine effectiveness"
        
        state = {
            "messages": [query],
            "user_context": "Public health researcher",
            "research_focus": "vaccine effectiveness",
            "time_range": "last 12 months"
        }
        
        # Mock the entire flow
        with patch('src.agents.biomedical_researcher.biomedical_researcher_wrapper') as mock_wrapper:
            mock_wrapper_instance = AsyncMock()
            mock_wrapper.__aenter__ = AsyncMock(return_value=mock_wrapper_instance)
            mock_wrapper.__aexit__ = AsyncMock()
            
            expected_result = BiomedicalResearchOutput(
                summary="mRNA vaccines show sustained effectiveness against COVID-19",
                key_findings=[
                    "95% effectiveness in preventing severe disease",
                    "Effectiveness decreases over time",
                    "Boosters restore high protection levels"
                ],
                sources=[
                    {"title": "mRNA Vaccine Effectiveness Study", "pmid": "12345"},
                    {"title": "Real-world Vaccine Data", "journal": "NEJM"}
                ],
                recommendations=[
                    "Consider booster recommendations",
                    "Monitor waning immunity",
                    "Study variant-specific effectiveness"
                ],
                confidence_level=0.85
            )
            mock_wrapper_instance.run_research.return_value = expected_result
            
            result_state = await biomedical_researcher_node(state)
            
            # Verify the result structure
            assert "biomedical_research_result" in result_state
            research_result = result_state["biomedical_research_result"]
            
            assert research_result.summary.startswith("mRNA vaccines")
            assert len(research_result.key_findings) == 3
            assert len(research_result.sources) == 2
            assert research_result.confidence_level == 0.85
            
            # Verify state updates
            assert "messages" in result_state
            assert len(result_state["messages"]) > 0


@pytest.fixture
def sample_state():
    """Fixture providing a sample state for testing."""
    return {
        "messages": ["Research the latest developments in cancer immunotherapy"],
        "user_context": "Oncology researcher",
        "research_focus": "immunotherapy",
        "time_range": "last 2 years",
        "preferred_databases": ["pubmed", "clinicaltrials", "biorxiv"]
    }


@pytest.fixture
def sample_deps():
    """Fixture providing sample dependencies for testing."""
    return BiomedicalResearchDeps(
        user_context="Medical researcher",
        research_focus="gene therapy",
        time_range="last year",
        preferred_databases=["pubmed", "biorxiv"]
    )


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"]) 