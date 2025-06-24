"""
Main script to run evaluations for the Web Researcher agent.

This script provides easy entry points to run evaluations with different configurations.
"""

import asyncio
import argparse
from pathlib import Path
from typing import List, Optional

from .evaluation_runner import run_quick_evaluation, run_full_evaluation
from .test_dataset import RESEARCHER_TEST_CASES, get_all_domains


def main():
    """Main CLI interface for running researcher evaluations."""
    parser = argparse.ArgumentParser(description="Run evaluations for the Web Researcher agent")
    
    parser.add_argument(
        "--mode",
        choices=["quick", "full", "custom"],
        default="quick",
        help="Evaluation mode: quick (subset), full (all cases), or custom (specify test cases)"
    )
    
    parser.add_argument(
        "--test-cases",
        nargs="+",
        help="Specific test case IDs to run (for custom mode)"
    )
    
    parser.add_argument(
        "--domain",
        choices=get_all_domains(),
        help="Run evaluations for a specific domain only"
    )
    
    parser.add_argument(
        "--difficulty",
        choices=["basic", "intermediate", "expert"],
        help="Run evaluations for a specific difficulty level only"
    )
    
    parser.add_argument(
        "--output-dir",
        default="evals/outputs/researcher",
        help="Output directory for evaluation results"
    )
    
    parser.add_argument(
        "--max-concurrent",
        type=int,
        default=1,
        help="Maximum number of concurrent evaluations"
    )
    
    parser.add_argument(
        "--evaluator-model",
        default="openai:o4-mini",
        help="Model to use for LLM-as-a-judge evaluation"
    )
    
    args = parser.parse_args()
    
    # Filter test cases based on arguments
    if args.mode == "custom" and args.test_cases:
        test_case_ids = args.test_cases
    elif args.domain or args.difficulty:
        from .test_dataset import get_test_cases_by_domain, get_test_cases_by_difficulty
        
        test_cases = RESEARCHER_TEST_CASES
        if args.domain:
            test_cases = get_test_cases_by_domain(args.domain)
        if args.difficulty:
            filtered_by_difficulty = get_test_cases_by_difficulty(args.difficulty)
            if args.domain:
                # Intersection of domain and difficulty filters
                test_cases = [tc for tc in test_cases if tc in filtered_by_difficulty]
            else:
                test_cases = filtered_by_difficulty
        
        test_case_ids = [tc.id for tc in test_cases]
    else:
        test_case_ids = None
    
    # Run evaluation
    if args.mode == "quick" or (args.mode == "custom" and args.test_cases):
        result = asyncio.run(run_quick_evaluation(
            test_case_ids=test_case_ids,
            output_dir=args.output_dir
        ))
    else:  # full mode
        result = asyncio.run(run_full_evaluation(
            output_dir=args.output_dir
        ))
    
    print("\n" + "="*80)
    print("EVALUATION COMPLETED")
    print("="*80)
    print(f"Total test cases: {result['summary']['total_cases']}")
    print(f"Successful: {result['summary']['successful_cases']}")
    print(f"Failed: {result['summary']['failed_cases']}")
    print(f"Overall score: {result['summary']['average_score']:.3f}")
    print(f"Results saved to: {args.output_dir}")


if __name__ == "__main__":
    main() 