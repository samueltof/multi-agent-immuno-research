import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from langchain_core.messages import HumanMessage
from langgraph.types import Command

from src.graph.nodes import planner_node


class TestPlannerNode:
    """Test suite for the planner_node function."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_state = {
            "messages": [HumanMessage(content="What can you tell me about cancer immunogenomics")]
        }

    def test_valid_json_response(self):
        """Test planner node with valid JSON response."""
        valid_json = {
            "thought": "The user is asking about cancer immunogenomics, which is a complex topic.",
            "title": "Cancer Immunogenomics Research Plan",
            "steps": [
                {
                    "agent_name": "researcher",
                    "title": "Research cancer immunogenomics basics",
                    "description": "Search for recent literature on cancer immunogenomics"
                }
            ]
        }
        valid_json_str = json.dumps(valid_json)

        with patch('src.graph.nodes.apply_prompt_template') as mock_template, \
             patch('src.graph.nodes.get_llm_by_type') as mock_llm_getter:
            
            mock_template.return_value = [HumanMessage(content="test")]
            mock_llm = Mock()
            mock_llm.stream.return_value = [Mock(content=valid_json_str)]
            mock_llm_getter.return_value = mock_llm

            result = planner_node(self.mock_state)

            assert isinstance(result, Command)
            assert result.goto == "supervisor"
            assert result.update["messages"][0].content == valid_json_str
            assert result.update["full_plan"] == valid_json_str

    def test_json_wrapped_in_code_blocks(self):
        """Test planner node with JSON wrapped in code blocks."""
        valid_json = {
            "thought": "Test thought",
            "title": "Test Plan",
            "steps": []
        }
        wrapped_json = f"```json\n{json.dumps(valid_json)}\n```"

        with patch('src.graph.nodes.apply_prompt_template') as mock_template, \
             patch('src.graph.nodes.get_llm_by_type') as mock_llm_getter:
            
            mock_template.return_value = [HumanMessage(content="test")]
            mock_llm = Mock()
            mock_llm.stream.return_value = [Mock(content=wrapped_json)]
            mock_llm_getter.return_value = mock_llm

            result = planner_node(self.mock_state)

            assert isinstance(result, Command)
            assert result.goto == "supervisor"
            # Should have code block markers removed
            expected_content = json.dumps(valid_json)
            assert result.update["messages"][0].content == expected_content

    def test_invalid_json_response(self):
        """Test planner node with invalid JSON response."""
        invalid_json = "This is not valid JSON at all"

        with patch('src.graph.nodes.apply_prompt_template') as mock_template, \
             patch('src.graph.nodes.get_llm_by_type') as mock_llm_getter:
            
            mock_template.return_value = [HumanMessage(content="test")]
            mock_llm = Mock()
            mock_llm.stream.return_value = [Mock(content=invalid_json)]
            mock_llm_getter.return_value = mock_llm

            result = planner_node(self.mock_state)

            assert isinstance(result, Command)
            assert result.goto == "__end__"
            assert result.update["messages"][0].content == invalid_json
            assert result.update["full_plan"] == invalid_json

    def test_malformed_json_with_code_blocks(self):
        """Test planner node with malformed JSON in code blocks."""
        malformed_json = "```json\n{\"thought\": \"test\", \"incomplete\": \n```"

        with patch('src.graph.nodes.apply_prompt_template') as mock_template, \
             patch('src.graph.nodes.get_llm_by_type') as mock_llm_getter:
            
            mock_template.return_value = [HumanMessage(content="test")]
            mock_llm = Mock()
            mock_llm.stream.return_value = [Mock(content=malformed_json)]
            mock_llm_getter.return_value = mock_llm

            result = planner_node(self.mock_state)

            assert isinstance(result, Command)
            assert result.goto == "__end__"

    def test_empty_response(self):
        """Test planner node with empty response."""
        with patch('src.graph.nodes.apply_prompt_template') as mock_template, \
             patch('src.graph.nodes.get_llm_by_type') as mock_llm_getter:
            
            mock_template.return_value = [HumanMessage(content="test")]
            mock_llm = Mock()
            mock_llm.stream.return_value = [Mock(content="")]
            mock_llm_getter.return_value = mock_llm

            result = planner_node(self.mock_state)

            assert isinstance(result, Command)
            assert result.goto == "__end__"

    def test_deep_thinking_mode(self):
        """Test planner node with deep thinking mode enabled."""
        state_with_deep_thinking = {
            **self.mock_state,
            "deep_thinking_mode": True
        }
        
        valid_json = {"thought": "test", "title": "test", "steps": []}
        
        with patch('src.graph.nodes.apply_prompt_template') as mock_template, \
             patch('src.graph.nodes.get_llm_by_type') as mock_llm_getter:
            
            mock_template.return_value = [HumanMessage(content="test")]
            mock_reasoning_llm = Mock()
            mock_basic_llm = Mock()
            mock_reasoning_llm.stream.return_value = [Mock(content=json.dumps(valid_json))]
            
            def llm_selector(llm_type):
                if llm_type == "reasoning":
                    return mock_reasoning_llm
                return mock_basic_llm
            
            mock_llm_getter.side_effect = llm_selector

            result = planner_node(state_with_deep_thinking)

            # Should use reasoning LLM
            mock_llm_getter.assert_called_with("reasoning")
            assert result.goto == "supervisor"

    def test_search_before_planning(self):
        """Test planner node with search before planning enabled."""
        state_with_search = {
            **self.mock_state,
            "search_before_planning": True
        }
        
        valid_json = {"thought": "test", "title": "test", "steps": []}
        
        with patch('src.graph.nodes.apply_prompt_template') as mock_template, \
             patch('src.graph.nodes.get_llm_by_type') as mock_llm_getter, \
             patch('src.graph.nodes.tavily_tool') as mock_tavily:
            
            mock_template.return_value = [HumanMessage(content="test content")]
            mock_llm = Mock()
            mock_llm.stream.return_value = [Mock(content=json.dumps(valid_json))]
            mock_llm_getter.return_value = mock_llm
            
            # Mock search results
            mock_tavily.invoke.return_value = [
                {"title": "Test Article", "content": "Test content"}
            ]

            result = planner_node(state_with_search)

            # Should have called search
            mock_tavily.invoke.assert_called_once()
            assert result.goto == "supervisor"

    def test_streamed_response_chunks(self):
        """Test planner node with streamed response in multiple chunks."""
        valid_json = {"thought": "test", "title": "test", "steps": []}
        json_str = json.dumps(valid_json)
        
        # Split JSON into chunks
        chunk1 = json_str[:len(json_str)//2]
        chunk2 = json_str[len(json_str)//2:]

        with patch('src.graph.nodes.apply_prompt_template') as mock_template, \
             patch('src.graph.nodes.get_llm_by_type') as mock_llm_getter:
            
            mock_template.return_value = [HumanMessage(content="test")]
            mock_llm = Mock()
            mock_llm.stream.return_value = [
                Mock(content=chunk1),
                Mock(content=chunk2)
            ]
            mock_llm_getter.return_value = mock_llm

            result = planner_node(self.mock_state)

            assert isinstance(result, Command)
            assert result.goto == "supervisor"
            assert result.update["messages"][0].content == json_str


class TestPlannerNodeEdgeCases:
    """Test edge cases and error conditions for planner_node."""

    def test_json_with_newlines_and_whitespace(self):
        """Test JSON with extra newlines and whitespace."""
        valid_json = {
            "thought": "test",
            "title": "test", 
            "steps": []
        }
        # JSON with extra whitespace
        json_with_whitespace = f"\n\n  {json.dumps(valid_json, indent=2)}  \n\n"
        
        with patch('src.graph.nodes.apply_prompt_template') as mock_template, \
             patch('src.graph.nodes.get_llm_by_type') as mock_llm_getter:
            
            mock_template.return_value = [HumanMessage(content="test")]
            mock_llm = Mock()
            mock_llm.stream.return_value = [Mock(content=json_with_whitespace)]
            mock_llm_getter.return_value = mock_llm

            state = {"messages": [HumanMessage(content="test")]}
            result = planner_node(state)

            # Should still parse successfully
            assert result.goto == "supervisor"

    def test_partial_code_block_markers(self):
        """Test handling of partial or mismatched code block markers."""
        valid_json = {"thought": "test", "title": "test", "steps": []}
        # Only opening marker
        json_with_partial_markers = f"```json\n{json.dumps(valid_json)}"
        
        with patch('src.graph.nodes.apply_prompt_template') as mock_template, \
             patch('src.graph.nodes.get_llm_by_type') as mock_llm_getter:
            
            mock_template.return_value = [HumanMessage(content="test")]
            mock_llm = Mock()
            mock_llm.stream.return_value = [Mock(content=json_with_partial_markers)]
            mock_llm_getter.return_value = mock_llm

            state = {"messages": [HumanMessage(content="test")]}
            result = planner_node(state)

            # Should remove the opening marker and still parse
            assert result.goto == "supervisor"

    @patch('src.graph.nodes.logger')
    def test_logging_behavior(self, mock_logger):
        """Test that appropriate logging occurs."""
        invalid_json = "not valid json"
        
        with patch('src.graph.nodes.apply_prompt_template') as mock_template, \
             patch('src.graph.nodes.get_llm_by_type') as mock_llm_getter:
            
            mock_template.return_value = [HumanMessage(content="test")]
            mock_llm = Mock()
            mock_llm.stream.return_value = [Mock(content=invalid_json)]
            mock_llm_getter.return_value = mock_llm

            state = {"messages": [HumanMessage(content="test")]}
            result = planner_node(state)

            # Should log warning for invalid JSON (check that warning was called with a message about invalid JSON)
            mock_logger.warning.assert_called()
            warning_call_args = mock_logger.warning.call_args[0][0]
            assert "Planner response is not valid JSON" in warning_call_args
            assert result.goto == "__end__"


if __name__ == "__main__":
    pytest.main([__file__]) 