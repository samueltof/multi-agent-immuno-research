import pytest
import json
import logging
from unittest.mock import Mock, patch
from langchain_core.messages import HumanMessage

from src.graph.nodes import planner_node


class TestPlannerDebug:
    """Debug test suite to analyze planner output issues."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_state = {
            "messages": [HumanMessage(content="What can you tell me about cancer immunogenomics")]
        }

    def test_debug_common_invalid_responses(self):
        """Test various common invalid response patterns to understand failure modes."""
        
        # Common problematic responses that might come from LLM
        truly_problematic_responses = [
            # Plain text response
            "I'll help you research cancer immunogenomics. Let me create a plan.",
            
            # Partial JSON
            '{"thought": "This is about cancer research", "title": "Research Plan"',
            
            # Multiple JSON objects
            '{"thought": "test"}\n{"title": "test", "steps": []}',
            
            # JSON with comments (invalid JSON)
            '{\n  // This is a plan\n  "thought": "test",\n  "title": "test",\n  "steps": []\n}',
            
            # Malformed JSON
            '{"thought": "test", "title": "test", "steps": [}',
            
            # Empty object
            '{}',
            
            # Wrong structure
            '{"plan": {"thought": "test", "title": "test", "steps": []}}',
            
            # Missing required fields
            '{"thought": "test", "steps": []}',
            
            # Steps not a list
            '{"thought": "test", "title": "test", "steps": "not a list"}',
            
            # Steps with missing fields
            '{"thought": "test", "title": "test", "steps": [{"title": "missing agent_name"}]}',
        ]

        # Responses that should now work thanks to JSON extraction
        now_working_responses = [
            # JSON with extra text (should now work)
            'Here is the plan:\n{"thought": "test", "title": "test", "steps": []}',
        ]

        for i, response in enumerate(truly_problematic_responses):
            with patch('src.graph.nodes.apply_prompt_template') as mock_template, \
                 patch('src.graph.nodes.get_llm_by_type') as mock_llm_getter:
                
                mock_template.return_value = [HumanMessage(content="test")]
                mock_llm = Mock()
                mock_llm.stream.return_value = [Mock(content=response)]
                mock_llm_getter.return_value = mock_llm

                result = planner_node(self.mock_state)
                
                print(f"\nTruly problematic case {i}: {response[:50]}...")
                print(f"Result: goto={result.goto}")
                
                # Should go to __end__ for all invalid responses
                assert result.goto == "__end__", f"Test case {i} should fail but went to {result.goto}"

        for i, response in enumerate(now_working_responses):
            with patch('src.graph.nodes.apply_prompt_template') as mock_template, \
                 patch('src.graph.nodes.get_llm_by_type') as mock_llm_getter:
                
                mock_template.return_value = [HumanMessage(content="test")]
                mock_llm = Mock()
                mock_llm.stream.return_value = [Mock(content=response)]
                mock_llm_getter.return_value = mock_llm

                result = planner_node(self.mock_state)
                
                print(f"\nNow working case {i}: {response[:50]}...")
                print(f"Result: goto={result.goto}")
                
                # Should now work thanks to JSON extraction
                assert result.goto == "supervisor", f"Test case {i} should now work but went to {result.goto}"

    def test_debug_valid_minimal_plan(self):
        """Test minimal valid plan structure."""
        minimal_valid_plan = {
            "thought": "User wants information about cancer immunogenomics",
            "title": "Cancer Immunogenomics Research",
            "steps": [
                {
                    "agent_name": "researcher",
                    "title": "Research cancer immunogenomics",
                    "description": "Search for information about cancer immunogenomics"
                }
            ]
        }
        
        with patch('src.graph.nodes.apply_prompt_template') as mock_template, \
             patch('src.graph.nodes.get_llm_by_type') as mock_llm_getter:
            
            mock_template.return_value = [HumanMessage(content="test")]
            mock_llm = Mock()
            mock_llm.stream.return_value = [Mock(content=json.dumps(minimal_valid_plan))]
            mock_llm_getter.return_value = mock_llm

            result = planner_node(self.mock_state)
            
            assert result.goto == "supervisor"
            assert json.loads(result.update["messages"][0].content) == minimal_valid_plan

    def test_debug_response_with_reasoning_text(self):
        """Test response that includes reasoning text before JSON - should now work."""
        reasoning_with_json = """
        Let me analyze this request about cancer immunogenomics and create a comprehensive research plan.

        Cancer immunogenomics is a complex field that combines cancer biology with immunology and genomics.

        {"thought": "The user is asking about cancer immunogenomics, which requires a multi-faceted research approach", "title": "Cancer Immunogenomics Research Plan", "steps": [{"agent_name": "researcher", "title": "Research basics", "description": "Find fundamental information"}]}
        """
        
        with patch('src.graph.nodes.apply_prompt_template') as mock_template, \
             patch('src.graph.nodes.get_llm_by_type') as mock_llm_getter:
            
            mock_template.return_value = [HumanMessage(content="test")]
            mock_llm = Mock()
            mock_llm.stream.return_value = [Mock(content=reasoning_with_json)]
            mock_llm_getter.return_value = mock_llm

            result = planner_node(self.mock_state)
            
            # This should now work because JSON extraction can find the JSON within the text
            assert result.goto == "supervisor"
            
            # Verify the extracted JSON is valid
            extracted_plan = json.loads(result.update["messages"][0].content)
            assert "thought" in extracted_plan
            assert "title" in extracted_plan
            assert "steps" in extracted_plan

    @pytest.mark.parametrize("agent_name", ["researcher", "coder", "browser", "reporter", "data_analyst", "biomedical_researcher"])
    def test_debug_valid_agent_names(self, agent_name):
        """Test that all valid agent names are accepted."""
        valid_plan = {
            "thought": f"Use {agent_name} for this task",
            "title": f"Plan using {agent_name}",
            "steps": [
                {
                    "agent_name": agent_name,
                    "title": f"{agent_name} task",
                    "description": f"Task for {agent_name}"
                }
            ]
        }
        
        with patch('src.graph.nodes.apply_prompt_template') as mock_template, \
             patch('src.graph.nodes.get_llm_by_type') as mock_llm_getter:
            
            mock_template.return_value = [HumanMessage(content="test")]
            mock_llm = Mock()
            mock_llm.stream.return_value = [Mock(content=json.dumps(valid_plan))]
            mock_llm_getter.return_value = mock_llm

            result = planner_node(self.mock_state)
            
            assert result.goto == "supervisor"

    def test_debug_capture_actual_llm_response(self):
        """This test can be used to capture and analyze actual LLM responses."""
        # This is a utility test that can be run manually to see what
        # the actual LLM is producing
        pass


if __name__ == "__main__":
    # Enable debug logging
    logging.basicConfig(level=logging.DEBUG)
    pytest.main([__file__, "-v", "-s"]) 