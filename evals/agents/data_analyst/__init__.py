"""
Data Analyst Agent Evaluation Module.

This module provides comprehensive evaluation capabilities for the Data Analyst agent,
including:

- Test datasets with natural language queries for VDJdb database
- LLM-as-a-judge evaluators for SQL correctness and domain knowledge
- Evaluation runners for orchestrating test execution
- Reporting and analysis capabilities

Key Components:
- test_dataset.py: Comprehensive test cases covering various SQL scenarios
- evaluators.py: LLM-as-a-judge evaluators for multi-dimensional assessment
- evaluation_runner.py: Orchestration and execution of evaluation suites
- run_evaluation.py: Simple script for running evaluations

Usage:
    from evals.agents.data_analyst import run_quick_evaluation
    
    # Run quick evaluation
    results = await run_quick_evaluation(["simple_001", "join_001"])
    
    # Run full evaluation
    runner = DataAnalystEvaluationRunner()
    results = await runner.run_evaluation_suite()
"""

from .test_dataset import (
    DataAnalystTestCase,
    ALL_DATA_ANALYST_TEST_CASES,
    get_test_case_by_id,
    get_test_cases_by_difficulty,
    get_test_cases_by_type,
    get_dataset_summary
)

from .evaluators import (
    DataAnalystAgentEvaluator,
    extract_sql_from_output,
    create_sql_correctness_evaluator
)

from .evaluation_runner import (
    DataAnalystEvaluationRunner,
    run_quick_evaluation
)

__all__ = [
    "DataAnalystTestCase",
    "ALL_DATA_ANALYST_TEST_CASES", 
    "get_test_case_by_id",
    "get_test_cases_by_difficulty",
    "get_test_cases_by_type",
    "get_dataset_summary",
    "DataAnalystAgentEvaluator",
    "extract_sql_from_output",
    "create_sql_correctness_evaluator",
    "DataAnalystEvaluationRunner",
    "run_quick_evaluation"
] 