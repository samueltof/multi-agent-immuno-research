"""
Test script for the Web Researcher agent evaluation system.

This script performs basic tests to ensure all components are working correctly.
"""

import asyncio
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from evals.agents.researcher import (
    RESEARCHER_TEST_CASES,
    ResearcherEvaluator,
    EvaluationRunner,
    get_test_case_by_id,
    get_all_domains,
    get_test_dataset_summary,
)


def test_dataset_integrity():
    """Test that the test dataset is properly structured."""
    print("Testing dataset integrity...")
    
    # Check that we have test cases
    assert len(RESEARCHER_TEST_CASES) > 0, "No test cases found"
    print(f"✓ Found {len(RESEARCHER_TEST_CASES)} test cases")
    
    # Check test case structure
    for test_case in RESEARCHER_TEST_CASES[:3]:  # Test first 3
        assert test_case.id, f"Test case missing ID: {test_case}"
        assert test_case.prompt, f"Test case missing prompt: {test_case.id}"
        assert test_case.domain, f"Test case missing domain: {test_case.id}"
        assert test_case.difficulty in ["basic", "intermediate", "expert"], f"Invalid difficulty: {test_case.id}"
        assert test_case.expected_sources, f"Test case missing expected sources: {test_case.id}"
        assert test_case.key_concepts, f"Test case missing key concepts: {test_case.id}"
        assert test_case.search_keywords, f"Test case missing search keywords: {test_case.id}"
    
    print("✓ Test case structure validation passed")
    
    # Test utility functions
    domains = get_all_domains()
    assert len(domains) > 0, "No domains found"
    print(f"✓ Found domains: {domains}")
    
    # Test getting test case by ID
    first_case = get_test_case_by_id(RESEARCHER_TEST_CASES[0].id)
    assert first_case is not None, "Failed to get test case by ID"
    print(f"✓ Test case retrieval by ID works")
    
    # Test dataset summary
    summary = get_test_dataset_summary()
    assert "total_test_cases" in summary, "Invalid dataset summary"
    print(f"✓ Dataset summary: {summary['total_test_cases']} total cases")


def test_evaluator_initialization():
    """Test that evaluators can be initialized properly."""
    print("\nTesting evaluator initialization...")
    
    try:
        evaluator = ResearcherEvaluator(model="openai:o3-mini")
        print("✓ ResearcherEvaluator initialized successfully")
        
        # Test that all evaluators are accessible
        assert hasattr(evaluator, 'search_quality_evaluator'), "Missing search quality evaluator"
        assert hasattr(evaluator, 'crawling_quality_evaluator'), "Missing crawling quality evaluator"
        assert hasattr(evaluator, 'information_synthesis_evaluator'), "Missing synthesis evaluator"
        assert hasattr(evaluator, 'source_quality_evaluator'), "Missing source quality evaluator"
        assert hasattr(evaluator, 'research_completeness_evaluator'), "Missing completeness evaluator"
        
        print("✓ All individual evaluators are accessible")
        
    except Exception as e:
        print(f"✗ Failed to initialize evaluator: {e}")
        raise


def test_evaluation_runner_initialization():
    """Test that the evaluation runner can be initialized."""
    print("\nTesting evaluation runner initialization...")
    
    try:
        runner = EvaluationRunner(
            output_dir="evals/outputs/researcher/test",
            evaluator_model="openai:o3-mini"
        )
        print("✓ EvaluationRunner initialized successfully")
        
        # Check that output directory was created
        assert runner.output_dir.exists(), "Output directory not created"
        print(f"✓ Output directory created: {runner.output_dir}")
        
    except Exception as e:
        print(f"✗ Failed to initialize evaluation runner: {e}")
        raise


def test_mock_evaluation():
    """Test evaluation with mock data (no actual agent call)."""
    print("\nTesting mock evaluation...")
    
    try:
        evaluator = ResearcherEvaluator(model="openai:o3-mini")
        
        # Create mock response data
        mock_response = {
            "content": "Quantum computing is a revolutionary technology that uses quantum mechanical phenomena...",
            "sources": ["https://example.com/quantum1", "https://example.com/quantum2"],
            "search_info": "Search: quantum computing 2024",
            "crawled_content": "Quantum computers use qubits...",
            "query": "What are the latest developments in quantum computing?",
            "domain": "technology",
            "difficulty": "intermediate"
        }
        
        # Test case info
        test_case_info = {
            "expected_sources": ["academic", "tech_companies"],
            "search_keywords": ["quantum computing", "qubits", "quantum supremacy"],
            "key_concepts": ["quantum computing", "qubits", "quantum algorithms"],
            "requires_recent_info": True
        }
        
        print("✓ Mock data prepared")
        print("✓ Mock evaluation setup complete (actual LLM calls would happen here)")
        
        # Note: We don't actually run the evaluation to avoid API costs
        # In a real test, you would uncomment the following:
        # evaluations = evaluator.evaluate_response(
        #     prompt="What are the latest developments in quantum computing?",
        #     response=mock_response,
        #     test_case_info=test_case_info
        # )
        
    except Exception as e:
        print(f"✗ Failed mock evaluation setup: {e}")
        raise


async def test_single_evaluation_flow():
    """Test the single evaluation flow (without actual agent execution)."""
    print("\nTesting single evaluation flow...")
    
    try:
        runner = EvaluationRunner(
            output_dir="evals/outputs/researcher/test",
            evaluator_model="openai:o3-mini"
        )
        
        # Get a test case
        test_case = get_test_case_by_id("tech_001")
        assert test_case is not None, "Test case not found"
        print(f"✓ Test case loaded: {test_case.id}")
        
        print("✓ Single evaluation flow setup complete")
        print("  (Actual agent execution and evaluation would happen here)")
        
        # Note: We don't actually run the evaluation to avoid API costs and agent execution
        # In a real test with proper API keys and setup, you would uncomment:
        # result = runner.run_single_evaluation(test_case)
        # assert 'overall_score' in result or 'error' in result, "Invalid evaluation result"
        
    except Exception as e:
        print(f"✗ Failed single evaluation flow: {e}")
        raise


def test_import_structure():
    """Test that all imports work correctly."""
    print("\nTesting import structure...")
    
    try:
        from evals.agents.researcher.evaluators import (
            create_search_quality_evaluator,
            create_crawling_quality_evaluator,
            create_information_synthesis_evaluator,
            create_source_quality_evaluator,
            create_research_completeness_evaluator,
        )
        print("✓ Individual evaluator creators imported successfully")
        
        from evals.agents.researcher.test_dataset import (
            get_test_cases_by_domain,
            get_test_cases_by_difficulty,
        )
        print("✓ Dataset utility functions imported successfully")
        
        from evals.agents.researcher.evaluation_runner import (
            run_quick_evaluation,
            run_full_evaluation,
        )
        print("✓ Evaluation runner functions imported successfully")
        
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        raise


def run_all_tests():
    """Run all tests."""
    print("="*60)
    print("WEB RESEARCHER EVALUATION SYSTEM - TEST SUITE")
    print("="*60)
    
    try:
        # Test 1: Dataset integrity
        test_dataset_integrity()
        
        # Test 2: Import structure
        test_import_structure()
        
        # Test 3: Evaluator initialization
        test_evaluator_initialization()
        
        # Test 4: Evaluation runner initialization
        test_evaluation_runner_initialization()
        
        # Test 5: Mock evaluation
        test_mock_evaluation()
        
        # Test 6: Single evaluation flow
        asyncio.run(test_single_evaluation_flow())
        
        print("\n" + "="*60)
        print("ALL TESTS PASSED! ✓")
        print("="*60)
        print("\nThe evaluation system is ready to use.")
        print("To run actual evaluations:")
        print("1. Set up your API keys (OPENAI_API_KEY, TAVILY_API_KEY)")
        print("2. Run: python run_evaluation.py --mode quick")
        print("3. Or run: python demo_evaluation.py")
        
        return True
        
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"TEST FAILED! ✗")
        print(f"{'='*60}")
        print(f"Error: {e}")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 