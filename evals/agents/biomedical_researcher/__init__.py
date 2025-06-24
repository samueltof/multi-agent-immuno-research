"""
Biomedical Researcher Agent Evaluation Package

This package provides comprehensive evaluation tools for the biomedical researcher agent
using LLM-as-a-judge methodology.
"""

from .evaluators import (
    BiomedicalResearcherEvaluator,
    create_biomedical_factual_correctness_evaluator,
    create_biomedical_relevance_evaluator,
    create_biomedical_source_quality_evaluator,
    create_biomedical_confidence_alignment_evaluator,
)

from .test_dataset import (
    BIOMEDICAL_TEST_CASES,
    BiomedicalTestCase,
    get_test_case_by_id,
    get_test_cases_by_domain,
    get_test_cases_by_difficulty,
    get_test_dataset_summary,
)

from .evaluation_runner import (
    EvaluationRunner,
    run_quick_evaluation,
    run_full_evaluation,
)

__all__ = [
    # Evaluators
    "BiomedicalResearcherEvaluator",
    "create_biomedical_factual_correctness_evaluator",
    "create_biomedical_relevance_evaluator", 
    "create_biomedical_source_quality_evaluator",
    "create_biomedical_confidence_alignment_evaluator",
    
    # Test Dataset
    "BIOMEDICAL_TEST_CASES",
    "BiomedicalTestCase",
    "get_test_case_by_id",
    "get_test_cases_by_domain",
    "get_test_cases_by_difficulty",
    "get_test_dataset_summary",
    
    # Evaluation Runner
    "EvaluationRunner",
    "run_quick_evaluation",
    "run_full_evaluation",
] 