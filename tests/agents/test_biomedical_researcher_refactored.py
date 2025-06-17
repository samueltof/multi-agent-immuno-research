"""
Test for the refactored biomedical researcher agent.
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock

from src.agents.biomedical_researcher import (
    BiomedicalResearcherWrapper,
    BiomedicalResearchDeps,
    BiomedicalResearchOutput,
    create_biomedical_researcher_agent
)


class TestBiomedicalResearcherRefactored:
    """Test the refactored biomedical researcher agent."""

    def test_prompt_integration(self):
        """Test that the agent properly integrates with the centralized prompt system."""
        template_vars = {
            "research_focus": "cancer immunotherapy",
            "user_context": "medical researcher",
            "time_range": "last 2 years",
            "preferred_databases": "PubMed, ClinicalTrials"
        }
        
        # This should not raise an exception
        agent = create_biomedical_researcher_agent(template_vars)
        assert agent is not None
        assert hasattr(agent, 'system_prompt')
        
        # Get the system prompt content (it's a method)
        prompt_content = agent.system_prompt()
        assert "cancer immunotherapy" in prompt_content
        assert "medical researcher" in prompt_content
    
    def test_wrapper_initialization(self):
        """Test that the wrapper initializes correctly."""
        template_vars = {"research_focus": "drug discovery"}
        wrapper = BiomedicalResearcherWrapper(template_vars)
        
        assert wrapper.template_vars == template_vars
        assert wrapper.agent is None  # Lazy initialization
    
    def test_template_vars_update(self):
        """Test that template variables can be updated."""
        wrapper = BiomedicalResearcherWrapper({"research_focus": "initial"})
        wrapper.update_template_vars({"research_focus": "updated", "user_context": "new"})
        
        expected = {"research_focus": "updated", "user_context": "new"}
        assert wrapper.template_vars == expected
        
    @pytest.mark.asyncio
    async def test_error_handling(self):
        """Test error handling in the refactored system."""
        with patch('src.agents.biomedical_researcher.create_biomedical_researcher_agent') as mock_create:
            # Mock an agent that raises an exception
            mock_agent = AsyncMock()
            mock_agent.run.side_effect = Exception("Test error")
            
            # Create a proper async context manager mock
            mock_mcp_context = AsyncMock()
            mock_mcp_context.__aenter__ = AsyncMock(return_value=mock_mcp_context)
            mock_mcp_context.__aexit__ = AsyncMock(return_value=None)
            mock_agent.run_mcp_servers.return_value = mock_mcp_context
            
            mock_create.return_value = mock_agent
            
            wrapper = BiomedicalResearcherWrapper()
            
            async with wrapper:
                result = await wrapper.run_research("test query")
                
                # Should return structured error response
                assert isinstance(result, BiomedicalResearchOutput)
                assert "Test error" in result.summary
                assert result.confidence_level == 0.0
                assert result.key_findings == []
                assert result.sources == []
                assert len(result.recommendations) > 0


if __name__ == "__main__":
    pytest.main([__file__]) 