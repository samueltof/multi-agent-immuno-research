"""
Evaluation module for the Web Researcher agent.

This module provides comprehensive evaluation capabilities for the general web researcher agent,
including evaluation of web search quality, content crawling effectiveness, information synthesis,
and overall research quality.

The researcher agent differs from the biomedical researcher by having:
- Broader information access through web search
- Web crawling capabilities for content extraction
- General domain knowledge rather than specialized biomedical focus
- RAG-based approach using web content as knowledge base

Key evaluation components:
- Search Quality: Effectiveness of web search strategies and results
- Crawling Quality: Accuracy and relevance of crawled content
- Information Synthesis: Quality of combining multiple web sources
- Research Completeness: Coverage of the research topic
- Source Quality: Credibility and reliability of web sources used
"""

from .test_dataset import (
    RESEARCHER_TEST_CASES,
    ResearcherTestCase,
    get_test_cases_by_domain,
    get_test_cases_by_difficulty,
    get_test_case_by_id,
    get_all_domains,
    get_test_dataset_summary,
)

from .evaluators import (
    ResearcherEvaluator,
    create_search_quality_evaluator,
    create_crawling_quality_evaluator,
    create_information_synthesis_evaluator,
    create_source_quality_evaluator,
    create_research_completeness_evaluator,
    create_faithfulness_evaluator,
    create_context_precision_evaluator,
    create_context_recall_evaluator,
    create_temporal_accuracy_evaluator,
    create_bias_assessment_evaluator,
    create_factual_verification_evaluator,
)

from .evaluation_runner import (
    EvaluationRunner,
    run_quick_evaluation,
    run_full_evaluation,
)

__all__ = [
    # Test dataset
    "RESEARCHER_TEST_CASES",
    "ResearcherTestCase", 
    "get_test_cases_by_domain",
    "get_test_cases_by_difficulty",
    "get_test_case_by_id",
    "get_all_domains",
    "get_test_dataset_summary",
    
    # Evaluators
    "ResearcherEvaluator",
    "create_search_quality_evaluator",
    "create_crawling_quality_evaluator", 
    "create_information_synthesis_evaluator",
    "create_source_quality_evaluator",
    "create_research_completeness_evaluator",
    "create_faithfulness_evaluator",
    "create_context_precision_evaluator",
    "create_context_recall_evaluator",
    "create_temporal_accuracy_evaluator",
    "create_bias_assessment_evaluator",
    "create_factual_verification_evaluator",
    
    # Evaluation runner
    "EvaluationRunner",
    "run_quick_evaluation",
    "run_full_evaluation",
] 