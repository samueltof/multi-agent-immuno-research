#!/usr/bin/env python3
"""
Run homogeneous difficulty evaluation for the Coder agent.

This script runs evaluations using the homogeneous test dataset where all
test cases have consistent medium-level difficulty for fair comparison.

Usage:
    python run_homogeneous_evaluation.py --quick      # Run quick evaluation
    python run_homogeneous_evaluation.py --full       # Run full homogeneous evaluation
    python run_homogeneous_evaluation.py --case <id>  # Run specific test case
    python run_homogeneous_evaluation.py --type <type> # Run specific task type
"""

import asyncio
import argparse
import sys
from pathlib import Path
from typing import List, Optional

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from evals.agents.coder.test_dataset_homogeneous import (
    ALL_HOMOGENEOUS_TEST_CASES, 
    get_homogeneous_summary,
    DATA_ANALYSIS_CASES,
    VISUALIZATION_CASES,
    DATA_PROCESSING_CASES,
    ALGORITHM_CASES,
    DEBUGGING_CASES,
    STATISTICAL_TESTING_CASES
)
from evals.agents.coder.evaluation_runner import CoderEvaluationRunner


def get_test_cases_by_type(task_type: str):
    """Get test cases by task type."""
    type_mapping = {
        "data_analysis": DATA_ANALYSIS_CASES,
        "visualization": VISUALIZATION_CASES,
        "data_processing": DATA_PROCESSING_CASES,
        "algorithm": ALGORITHM_CASES,
        "debugging": DEBUGGING_CASES,
        "statistical_testing": STATISTICAL_TESTING_CASES
    }
    return type_mapping.get(task_type, [])


def get_test_case_by_id(case_id: str):
    """Get a specific test case by ID."""
    for test_case in ALL_HOMOGENEOUS_TEST_CASES:
        if test_case.id == case_id:
            return test_case
    return None


async def run_homogeneous_evaluation(
    test_cases: Optional[List] = None,
    output_dir: str = "evals/outputs/coder/homogeneous"
):
    """Run evaluation using homogeneous test cases."""
    if test_cases is None:
        test_cases = ALL_HOMOGENEOUS_TEST_CASES
    
    # Initialize evaluation runner
    runner = CoderEvaluationRunner(
        output_dir=output_dir,
        evaluator_model="openai:o4-mini",
        max_concurrent=1
    )
    
    # Run evaluation
    results = await runner.run_evaluation_suite(test_cases=test_cases)
    
    # Save results with homogeneous dataset info
    results['dataset_info'] = {
        'dataset_type': 'homogeneous',
        'difficulty_level': 'medium',
        'total_cases': len(test_cases),
        'summary': get_homogeneous_summary()
    }
    
    runner.save_results(results)
    runner.print_summary(results)
    
    return results


async def main():
    parser = argparse.ArgumentParser(description="Run Coder agent homogeneous evaluation")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--quick", action="store_true", 
                      help="Run quick evaluation (first 2 cases from each type)")
    group.add_argument("--full", action="store_true", 
                      help="Run full homogeneous evaluation on all cases")
    group.add_argument("--case", type=str, 
                      help="Run evaluation on specific test case ID")
    group.add_argument("--type", type=str, 
                      help="Run evaluation on specific task type (data_analysis, visualization, etc.)")
    
    parser.add_argument("--output-dir", type=str, default="evals/outputs/coder/homogeneous", 
                       help="Output directory for results")
    
    args = parser.parse_args()
    
    try:
        if args.quick:
            print("🚀 Running quick homogeneous coder evaluation...")
            # Take first 2 cases from each type for quick eval
            quick_cases = []
            for task_type in ["data_analysis", "visualization", "data_processing", 
                            "algorithm", "debugging", "statistical_testing"]:
                type_cases = get_test_cases_by_type(task_type)
                quick_cases.extend(type_cases[:2])  # Take first 2 from each type
            
            print(f"📊 Running {len(quick_cases)} test cases (2 from each type)")
            results = await run_homogeneous_evaluation(
                test_cases=quick_cases,
                output_dir=args.output_dir
            )
            
        elif args.full:
            print("🚀 Running full homogeneous coder evaluation...")
            print(f"📊 Running {len(ALL_HOMOGENEOUS_TEST_CASES)} test cases")
            results = await run_homogeneous_evaluation(output_dir=args.output_dir)
            
        elif args.case:
            test_case = get_test_case_by_id(args.case)
            if not test_case:
                print(f"❌ Test case '{args.case}' not found")
                print(f"Available test cases: {[tc.id for tc in ALL_HOMOGENEOUS_TEST_CASES]}")
                return 1
                
            print(f"🚀 Running evaluation for test case: {args.case}")
            results = await run_homogeneous_evaluation(
                test_cases=[test_case], 
                output_dir=args.output_dir
            )
            
        elif args.type:
            type_cases = get_test_cases_by_type(args.type)
            if not type_cases:
                print(f"❌ Task type '{args.type}' not found")
                print("Available types: data_analysis, visualization, data_processing, algorithm, debugging, statistical_testing")
                return 1
                
            print(f"🚀 Running evaluation for task type: {args.type}")
            print(f"📊 Running {len(type_cases)} test cases")
            results = await run_homogeneous_evaluation(
                test_cases=type_cases,
                output_dir=args.output_dir
            )
        
        print(f"\n✅ Homogeneous evaluation completed successfully!")
        print(f"📊 Results saved to: {args.output_dir}")
        print(f"🎯 Dataset: Homogeneous difficulty (all medium-level)")
        
        return 0
        
    except Exception as e:
        print(f"❌ Evaluation failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    # Print dataset summary first
    print("📋 Homogeneous Test Dataset Summary:")
    summary = get_homogeneous_summary()
    for key, value in summary.items():
        print(f"   {key}: {value}")
    print()
    
    exit_code = asyncio.run(main())
    sys.exit(exit_code) 