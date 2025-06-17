import pytest
import json
from unittest.mock import Mock, patch
from langchain_core.messages import HumanMessage

from src.graph.nodes import supervisor_node
from src.graph.types import Router


class TestEnhancedSupervisor:
    """Test suite for the enhanced supervisor functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_state = {
            "messages": [
                HumanMessage(content="What can you tell me about TCR sequences in COVID-19 patients?"),
                HumanMessage(
                    content='{"thought": "Research TCR sequences in COVID-19", "title": "COVID-19 TCR Analysis", "steps": [{"agent_name": "data_analyst", "title": "Query VDJdb", "description": "Search for COVID-19 TCR sequences"}, {"agent_name": "biomedical_researcher", "title": "Literature review", "description": "Find papers on COVID-19 TCR analysis"}]}',
                    name="planner"
                ),
            ],
            "TEAM_MEMBERS": ["researcher", "coder", "browser", "reporter", "data_analyst", "biomedical_researcher"],
            "next": "",
            "full_plan": '{"thought": "Research TCR sequences in COVID-19", "title": "COVID-19 TCR Analysis", "steps": [{"agent_name": "data_analyst", "title": "Query VDJdb", "description": "Search for COVID-19 TCR sequences"}]}',
            "deep_thinking_mode": False,
            "search_before_planning": False,
        }

    def test_supervisor_with_reasoning(self):
        """Test supervisor returns decision with reasoning."""
        mock_response = {
            "next": "data_analyst",
            "reasoning": "Starting with VDJdb query as planned to gather initial TCR data"
        }
        
        with patch('src.graph.nodes.apply_prompt_template') as mock_template, \
             patch('src.graph.nodes.get_llm_by_type') as mock_llm_getter:
            
            mock_template.return_value = [{"role": "system", "content": "supervisor prompt"}]
            mock_llm = Mock()
            mock_llm.with_structured_output.return_value.invoke.return_value = mock_response
            mock_llm_getter.return_value = mock_llm

            result = supervisor_node(self.mock_state)

            assert result.goto == "data_analyst"
            assert result.update["next"] == "data_analyst"
            mock_llm.with_structured_output.assert_called_once_with(Router)

    def test_supervisor_handles_missing_reasoning(self):
        """Test supervisor handles response without reasoning field."""
        mock_response = {
            "next": "biomedical_researcher"
            # No reasoning field
        }
        
        with patch('src.graph.nodes.apply_prompt_template') as mock_template, \
             patch('src.graph.nodes.get_llm_by_type') as mock_llm_getter:
            
            mock_template.return_value = [{"role": "system", "content": "supervisor prompt"}]
            mock_llm = Mock()
            mock_llm.with_structured_output.return_value.invoke.return_value = mock_response
            mock_llm_getter.return_value = mock_llm

            result = supervisor_node(self.mock_state)

            assert result.goto == "biomedical_researcher"
            assert result.update["next"] == "biomedical_researcher"

    def test_supervisor_finish_handling(self):
        """Test supervisor properly handles FINISH command."""
        mock_response = {
            "next": "FINISH",
            "reasoning": "Research objectives met with cross-validated findings"
        }
        
        with patch('src.graph.nodes.apply_prompt_template') as mock_template, \
             patch('src.graph.nodes.get_llm_by_type') as mock_llm_getter:
            
            mock_template.return_value = [{"role": "system", "content": "supervisor prompt"}]
            mock_llm = Mock()
            mock_llm.with_structured_output.return_value.invoke.return_value = mock_response
            mock_llm_getter.return_value = mock_llm

            result = supervisor_node(self.mock_state)

            assert result.goto == "__end__"
            assert result.update["next"] == "__end__"

    def test_supervisor_sees_agent_responses(self):
        """Test supervisor has access to previous agent responses for iterative decisions."""
        state_with_responses = {
            **self.mock_state,
            "messages": [
                *self.mock_state["messages"],
                HumanMessage(
                    content="Response from data_analyst:\n\n<response>\nFound 15 TCR sequences associated with COVID-19 response in VDJdb. Notable patterns in CDR3 sequences suggest strong HLA-A*02:01 restriction.\n</response>\n\n*Please execute the next step.*",
                    name="data_analyst"
                ),
            ]
        }
        
        mock_response = {
            "next": "biomedical_researcher",
            "reasoning": "Data analyst found HLA-A*02:01 restricted patterns. Need literature context to validate and explore clinical significance."
        }
        
        with patch('src.graph.nodes.apply_prompt_template') as mock_template, \
             patch('src.graph.nodes.get_llm_by_type') as mock_llm_getter:
            
            mock_template.return_value = [{"role": "system", "content": "supervisor prompt"}] + state_with_responses["messages"]
            mock_llm = Mock()
            mock_llm.with_structured_output.return_value.invoke.return_value = mock_response
            mock_llm_getter.return_value = mock_llm

            result = supervisor_node(state_with_responses)

            # Verify the supervisor has access to all messages including agent responses
            call_args = mock_template.call_args
            assert "supervisor" in call_args[0]
            assert state_with_responses == call_args[0][1]
            
            assert result.goto == "biomedical_researcher" 