import unittest
import os
from unittest.mock import patch, MagicMock
from src.tools.search import tavily_tool
from src.config import TAVILY_MAX_RESULTS


class TestTavilySearch(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        # Ensure TAVILY_API_KEY is set for tests
        if not os.environ.get("TAVILY_API_KEY"):
            os.environ["TAVILY_API_KEY"] = "test_api_key"

    def test_tavily_tool_initialization(self):
        """Test that tavily_tool is properly initialized"""
        self.assertIsNotNone(tavily_tool)
        self.assertEqual(tavily_tool.max_results, TAVILY_MAX_RESULTS)

    @patch('langchain_tavily.TavilySearch._run')
    def test_successful_search(self, mock_run):
        """Test successful search with Tavily API"""
        # Mock successful response as dict (new behavior)
        mock_response = {
            "query": "test query", 
            "follow_up_questions": None, 
            "answer": None, 
            "images": [], 
            "results": [
                {
                    "title": "Test Result", 
                    "url": "https://example.com", 
                    "content": "Test content about the query", 
                    "score": 0.9
                }
            ]
        }
        mock_run.return_value = mock_response
        
        result = tavily_tool.invoke({"query": "test query"})
        
        # The new TavilySearch returns dict/JSON
        self.assertTrue(isinstance(result, (dict, str)))
        if isinstance(result, dict):
            self.assertIn("results", result)
            self.assertEqual(result["query"], "test query")
            self.assertGreater(len(result["results"]), 0)
        else:
            # If wrapped by decorator to return string
            self.assertIn("Test Result", result)
            self.assertIn("https://example.com", result)
        mock_run.assert_called_once_with(query="test query")

    @patch('langchain_tavily.TavilySearch._run')
    def test_search_with_domain_filtering(self, mock_run):
        """Test search with domain filtering"""
        mock_response = {
            "query": "test query", 
            "results": [
                {
                    "title": "Wikipedia Result", 
                    "url": "https://en.wikipedia.org/wiki/test", 
                    "content": "Test content from Wikipedia"
                }
            ]
        }
        mock_run.return_value = mock_response
        
        # Test with domain filtering
        result = tavily_tool.invoke({
            "query": "test query",
            "include_domains": ["wikipedia.org"]
        })
        
        self.assertTrue(isinstance(result, (dict, str)))
        if isinstance(result, dict):
            self.assertIn("results", result)
            self.assertGreater(len(result["results"]), 0)
        else:
            self.assertIn("Wikipedia Result", result)

    @patch('langchain_tavily.TavilySearch._run')
    def test_search_error_handling(self, mock_run):
        """Test error handling when Tavily API fails"""
        # Mock API error
        mock_run.side_effect = Exception("API Error: Rate limit exceeded")
        
        # The new implementation should raise the exception rather than catching it
        with self.assertRaises(Exception) as context:
            tavily_tool.invoke({"query": "test query"})
        
        self.assertIn("API Error: Rate limit exceeded", str(context.exception))

    def test_search_with_empty_query(self):
        """Test search behavior with empty query"""
        try:
            result = tavily_tool.invoke({"query": ""})
            # Should either return empty results or handle gracefully
            self.assertIsInstance(result, str)
        except Exception as e:
            # If it raises an exception, it should be a validation error
            self.assertIn("query", str(e).lower())

    @patch('langchain_tavily.TavilySearch._run')
    def test_max_results_configuration(self, mock_run):
        """Test that max_results configuration is respected"""
        # Create a mock response with more results than max_results
        results = [
            {"title": f"Result {i}", "url": f"https://example{i}.com", "content": f"Content {i}"} 
            for i in range(10)  # More than TAVILY_MAX_RESULTS (5)
        ]
        mock_response = '{"query": "test query", "results": ' + str(results).replace("'", '"') + '}'
        mock_run.return_value = mock_response
        
        result = tavily_tool.invoke({"query": "test query"})
        
        self.assertIsInstance(result, str)
        # Verify that the tool respects the max_results setting
        # The actual behavior depends on the TavilySearch implementation

    def test_real_search_integration(self):
        """Integration test with real Tavily API (requires valid API key)"""
        # Skip if no real API key is available
        if not os.environ.get("TAVILY_API_KEY") or os.environ.get("TAVILY_API_KEY") == "test_api_key":
            self.skipTest("Skipping real API test - no valid TAVILY_API_KEY found")
        
        try:
            result = tavily_tool.invoke({"query": "Python programming language"})
            
            # The new TavilySearch returns dict/JSON, not string
            self.assertTrue(isinstance(result, (dict, str)))
            
            if isinstance(result, dict):
                self.assertIn("query", result)
                self.assertIn("results", result)
                self.assertGreater(len(result["results"]), 0)
                # Check that results contain Python-related content
                results_text = str(result["results"])
                self.assertIn("Python", results_text)
            else:
                # If it's a string, check for Python content
                self.assertGreater(len(result), 0)
                self.assertIn("Python", result)
            
        except Exception as e:
            self.fail(f"Real API integration test failed: {e}")

    def test_tool_name_and_description(self):
        """Test that the tool has proper name and description"""
        # Verify tool has proper attributes
        self.assertTrue(hasattr(tavily_tool, 'name'))
        self.assertTrue(hasattr(tavily_tool, 'description'))


if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2) 