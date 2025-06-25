"""
Coder Agent Evaluation Module

This module provides comprehensive evaluation capabilities for the Coder agent using OpenEvals.

Key Components:
- CoderAgentEvaluator: Main evaluator class using LLM-as-judge
- CoderTestCase: Test case data structure
- CoderEvaluationRunner: Orchestrates evaluation process

Usage:
    from evals.agents.coder import run_quick_evaluation, run_full_evaluation
    
    # Run quick evaluation on subset
    results = await run_quick_evaluation()
    
    # Run full evaluation on all test cases  
    results = await run_full_evaluation()
"""

from .evaluators import (
    CoderAgentEvaluator,
    create_code_correctness_evaluator,
    create_code_execution_evaluator,
    create_data_analysis_quality_evaluator,
    create_visualization_quality_evaluator,
    create_code_style_evaluator,
    create_task_completion_evaluator,
    extract_code_from_output,
    extract_plots_from_output
)

from .test_dataset import (
    CoderTestCase,
    ALL_CODER_TEST_CASES,
    get_test_cases_by_type,
    get_test_cases_by_difficulty,
    get_test_case_by_id,
    get_dataset_summary
)

from .evaluation_runner import (
    CoderEvaluationRunner,
    run_quick_evaluation,
    run_full_evaluation
)

__all__ = [
    # Evaluators
    'CoderAgentEvaluator',
    'create_code_correctness_evaluator',
    'create_code_execution_evaluator', 
    'create_data_analysis_quality_evaluator',
    'create_visualization_quality_evaluator',
    'create_code_style_evaluator',
    'create_task_completion_evaluator',
    'extract_code_from_output',
    'extract_plots_from_output',
    
    # Test Dataset
    'CoderTestCase',
    'ALL_CODER_TEST_CASES',
    'get_test_cases_by_type',
    'get_test_cases_by_difficulty',
    'get_test_case_by_id',
    'get_dataset_summary',
    
    # Evaluation Runner
    'CoderEvaluationRunner',
    'run_quick_evaluation',
    'run_full_evaluation'
] 