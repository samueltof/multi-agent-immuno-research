import pytest
import json
from unittest.mock import Mock, patch
from langchain_core.messages import HumanMessage

from src.graph.nodes import planner_node


class TestPlannerIntegration:
    """Integration tests for planner_node with real-world scenarios."""

    def test_cancer_immunogenomics_query(self):
        """Test the specific cancer immunogenomics query that was failing."""
        state = {
            "messages": [
                {"role": "user", "content": "hello"},
                {"role": "assistant", "content": "Hello! I'm DataManus, your AI coordinator for cancer immunogenomics research. How can I assist you today?"},
                {"role": "user", "content": "What can you tell me about cancer immunogenomics"}
            ]
        }

        # Simulate various possible LLM responses that might occur
        potential_responses = [
            # Valid JSON response
            {
                "thought": "The user is asking about cancer immunogenomics, which is a complex field combining cancer biology, immunology, and genomics.",
                "title": "Cancer Immunogenomics Research Plan",
                "steps": [
                    {
                        "agent_name": "researcher",
                        "title": "Research cancer immunogenomics fundamentals",
                        "description": "Search for recent literature on cancer immunogenomics basics, key concepts, and current research trends"
                    },
                    {
                        "agent_name": "researcher",
                        "title": "Investigate TCR datasets and analysis methods",
                        "description": "Find information about T-cell receptor datasets and analysis methodologies in cancer research"
                    },
                    {
                        "agent_name": "reporter",
                        "title": "Compile comprehensive report",
                        "description": "Create a detailed report summarizing the findings about cancer immunogenomics"
                    }
                ]
            },
            
            # Response with explanatory text (should now work)
            """
            I need to create a comprehensive research plan for cancer immunogenomics. This is a rapidly evolving field.
            
            {"thought": "The user wants to understand cancer immunogenomics, which requires a multi-faceted research approach", "title": "Cancer Immunogenomics Research", "steps": [{"agent_name": "researcher", "title": "Literature review", "description": "Research current cancer immunogenomics literature"}]}
            """,
            
            # Response wrapped in code blocks (should work)
            '''```json
            {"thought": "Cancer immunogenomics combines cancer research with immune system genomics", "title": "Cancer Immunogenomics Study", "steps": [{"agent_name": "researcher", "title": "Research basics", "description": "Find fundamental information about cancer immunogenomics"}]}
            ```''',
        ]

        for i, response_content in enumerate(potential_responses):
            with patch('src.graph.nodes.apply_prompt_template') as mock_template, \
                 patch('src.graph.nodes.get_llm_by_type') as mock_llm_getter:
                
                mock_template.return_value = [HumanMessage(content="test")]
                mock_llm = Mock()
                
                if isinstance(response_content, dict):
                    # Convert dict to JSON string
                    response_str = json.dumps(response_content)
                else:
                    # Use string directly
                    response_str = response_content
                    
                mock_llm.stream.return_value = [Mock(content=response_str)]
                mock_llm_getter.return_value = mock_llm

                result = planner_node(state)

                print(f"Test case {i}: {type(response_content).__name__}")
                print(f"Result: goto={result.goto}")

                # All cases should now work
                assert result.goto == "supervisor", f"Test case {i} failed: {result.goto}"
                
                # Verify the plan structure is valid
                plan_content = result.update["messages"][0].content
                parsed_plan = json.loads(plan_content)
                
                assert "thought" in parsed_plan
                assert "title" in parsed_plan
                assert "steps" in parsed_plan
                assert isinstance(parsed_plan["steps"], list)
                
                if parsed_plan["steps"]:
                    for step in parsed_plan["steps"]:
                        assert "agent_name" in step
                        assert "title" in step
                        assert "description" in step

    def test_edge_case_responses(self):
        """Test edge cases that might cause the original error."""
        state = {"messages": [HumanMessage(content="What can you tell me about cancer immunogenomics")]}
        
        # These should fail gracefully
        problematic_responses = [
            "",  # Empty response
            "Sorry, I cannot create a plan for this request.",  # Plain text
            '{"incomplete": "json"',  # Malformed JSON
            '{"wrong": "structure"}',  # Missing required fields
        ]
        
        for response in problematic_responses:
            with patch('src.graph.nodes.apply_prompt_template') as mock_template, \
                 patch('src.graph.nodes.get_llm_by_type') as mock_llm_getter:
                
                mock_template.return_value = [HumanMessage(content="test")]
                mock_llm = Mock()
                mock_llm.stream.return_value = [Mock(content=response)]
                mock_llm_getter.return_value = mock_llm

                result = planner_node(state)
                
                # Should fail gracefully without crashing
                assert result.goto == "__end__"
                assert "messages" in result.update
                assert "full_plan" in result.update

    def test_robust_json_extraction(self):
        """Test that JSON extraction works with various formatting."""
        state = {"messages": [HumanMessage(content="test query")]}
        
        valid_plan = {
            "thought": "Test thought",
            "title": "Test Plan", 
            "steps": [{"agent_name": "researcher", "title": "Test", "description": "Test desc"}]
        }
        
        # Various ways the JSON might be embedded
        embedding_patterns = [
            # Extra whitespace
            f"\n\n\n{json.dumps(valid_plan)}\n\n\n",
            
            # Mixed with text
            f"Here's my analysis:\n\n{json.dumps(valid_plan)}\n\nThis should work.",
            
            # With code blocks
            f"```json\n{json.dumps(valid_plan, indent=2)}\n```",
            
            # Partial code blocks
            f"```json\n{json.dumps(valid_plan)}",
            
            # Just the JSON
            json.dumps(valid_plan),
        ]
        
        for pattern in embedding_patterns:
            with patch('src.graph.nodes.apply_prompt_template') as mock_template, \
                 patch('src.graph.nodes.get_llm_by_type') as mock_llm_getter:
                
                mock_template.return_value = [HumanMessage(content="test")]
                mock_llm = Mock()
                mock_llm.stream.return_value = [Mock(content=pattern)]
                mock_llm_getter.return_value = mock_llm

                result = planner_node(state)
                
                # Should extract and validate the JSON successfully
                assert result.goto == "supervisor"
                
                extracted_plan = json.loads(result.update["messages"][0].content)
                assert extracted_plan == valid_plan


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"]) 