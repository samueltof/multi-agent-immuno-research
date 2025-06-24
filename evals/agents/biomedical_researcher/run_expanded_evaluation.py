#!/usr/bin/env python3
"""
Run evaluations using the expanded cancer immunogenomics dataset.

This script provides multiple options for running evaluations:
1. Full evaluation (all 33 cases)
2. High-priority cases only (18 cases)
3. Balanced subset (configurable size)
4. Specific test cases by ID
5. Domain-specific evaluations

Run from project root: python evals/agents/biomedical_researcher/run_expanded_evaluation.py
"""

import asyncio
import argparse
import sys
from pathlib import Path
from typing import List, Optional

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from evals.agents.biomedical_researcher.test_dataset_expanded import (
    BIOMEDICAL_TEST_CASES_EXPANDED,
    get_high_priority_cases,
    get_balanced_subset,
    get_expanded_test_cases_by_domain,
    get_expanded_test_cases_by_difficulty,
    get_all_expanded_domains,
    get_expanded_dataset_summary
)
from evals.agents.biomedical_researcher.evaluation_runner import EvaluationRunner


def print_dataset_info():
    """Print information about the expanded dataset."""
    summary = get_expanded_dataset_summary()
    domains = get_all_expanded_domains()
    
    print("=== EXPANDED CANCER IMMUNOGENOMICS EVALUATION DATASET ===")
    print(f"Total cases: {summary['total_cases']}")
    print(f"Domains: {summary['domain_count']}")
    print(f"Average cases per domain: {summary['avg_cases_per_domain']:.1f}")
    print()
    
    print("Domain distribution:")
    for domain, count in summary['domains'].items():
        print(f"  {domain}: {count} cases")
    print()
    
    print("Difficulty distribution:")
    for difficulty, count in summary['difficulties'].items():
        print(f"  {difficulty}: {count} cases")
    print()
    
    print("Priority distribution:")
    for priority, count in summary['priorities'].items():
        print(f"  {priority}: {count} cases")
    print()


async def run_full_evaluation():
    """Run evaluation on all 33 test cases."""
    print("🔬 Running FULL evaluation (33 cases)")
    print("This will take approximately 45-60 minutes...")
    
    runner = EvaluationRunner(
        output_dir="evals/outputs/biomedical_researcher/full_expanded",
        evaluator_model="openai:gpt-4o"
    )
    
    results = await runner.run_evaluation_suite(
        test_cases=BIOMEDICAL_TEST_CASES_EXPANDED,
        max_concurrent=1  # Sequential to avoid MCP conflicts
    )
    
    return results


async def run_high_priority_evaluation():
    """Run evaluation on high-priority cases only (18 cases)."""
    high_priority_cases = get_high_priority_cases()
    print(f"⭐ Running HIGH-PRIORITY evaluation ({len(high_priority_cases)} cases)")
    print("These are the most important cases for conference presentation...")
    
    runner = EvaluationRunner(
        output_dir="evals/outputs/biomedical_researcher/high_priority_expanded",
        evaluator_model="openai:gpt-4o"
    )
    
    results = await runner.run_evaluation_suite(
        test_cases=high_priority_cases,
        max_concurrent=1
    )
    
    return results


async def run_balanced_subset_evaluation(n_cases: int = 15):
    """Run evaluation on a balanced subset."""
    subset_cases = get_balanced_subset(n_cases)
    print(f"⚖️ Running BALANCED SUBSET evaluation ({len(subset_cases)} cases)")
    print("Balanced across difficulty levels...")
    
    runner = EvaluationRunner(
        output_dir=f"evals/outputs/biomedical_researcher/balanced_{n_cases}_expanded",
        evaluator_model="openai:gpt-4o"
    )
    
    results = await runner.run_evaluation_suite(
        test_cases=subset_cases,
        max_concurrent=1
    )
    
    return results


async def run_domain_evaluation(domain: str):
    """Run evaluation on a specific domain."""
    domain_cases = get_expanded_test_cases_by_domain(domain)
    if not domain_cases:
        print(f"❌ No cases found for domain: {domain}")
        print(f"Available domains: {', '.join(get_all_expanded_domains())}")
        return None
    
    print(f"🎯 Running DOMAIN-SPECIFIC evaluation: {domain} ({len(domain_cases)} cases)")
    
    runner = EvaluationRunner(
        output_dir=f"evals/outputs/biomedical_researcher/domain_{domain}_expanded",
        evaluator_model="openai:o4-mini"
    )
    
    results = await runner.run_evaluation_suite(
        test_cases=domain_cases,
        max_concurrent=1
    )
    
    return results


async def run_specific_cases_evaluation(case_ids: List[str]):
    """Run evaluation on specific test case IDs."""
    specific_cases = [case for case in BIOMEDICAL_TEST_CASES_EXPANDED if case.id in case_ids]
    
    if not specific_cases:
        print(f"❌ No cases found for IDs: {case_ids}")
        return None
    
    if len(specific_cases) != len(case_ids):
        found_ids = [case.id for case in specific_cases]
        missing_ids = [id for id in case_ids if id not in found_ids]
        print(f"⚠️ Warning: Some case IDs not found: {missing_ids}")
    
    print(f"🔍 Running SPECIFIC CASES evaluation ({len(specific_cases)} cases)")
    print(f"Cases: {[case.id for case in specific_cases]}")
    
    runner = EvaluationRunner(
        output_dir="evals/outputs/biomedical_researcher/specific_cases_expanded",
        evaluator_model="openai:o4-mini"
    )
    
    results = await runner.run_evaluation_suite(
        test_cases=specific_cases,
        max_concurrent=1
    )
    
    return results


async def run_quick_test():
    """Quick test with a single case using gpt-3.5-turbo for faster testing."""
    test_case = BIOMEDICAL_TEST_CASES_EXPANDED[0]  # First case
    print(f"🧪 Running QUICK TEST with case: {test_case.id}")
    print("Using gpt-3.5-turbo for faster testing...")
    
    runner = EvaluationRunner(
        output_dir="evals/outputs/biomedical_researcher/quick_test",
        evaluator_model="openai:gpt-3.5-turbo"
    )
    
    results = await runner.run_evaluation_suite(
        test_cases=[test_case],
        max_concurrent=1
    )
    
    return results


async def main():
    parser = argparse.ArgumentParser(
        description="Run biomedical researcher evaluations using expanded dataset",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_expanded_evaluation.py --info                    # Show dataset info
  python run_expanded_evaluation.py --full                    # Run all 33 cases
  python run_expanded_evaluation.py --high-priority           # Run 18 high-priority cases
  python run_expanded_evaluation.py --balanced 10             # Run balanced subset of 10 cases
  python run_expanded_evaluation.py --domain tcr_analysis     # Run TCR analysis domain
  python run_expanded_evaluation.py --cases tcr_001 tcr_002   # Run specific cases
        """
    )
    
    parser.add_argument("--info", action="store_true", help="Show dataset information and exit")
    parser.add_argument("--full", action="store_true", help="Run full evaluation (33 cases)")
    parser.add_argument("--high-priority", action="store_true", help="Run high-priority cases (18 cases)")
    parser.add_argument("--balanced", type=int, metavar="N", help="Run balanced subset of N cases")
    parser.add_argument("--domain", type=str, help="Run evaluation for specific domain")
    parser.add_argument("--cases", nargs="+", metavar="ID", help="Run specific test case IDs")
    parser.add_argument('--quick-test', action='store_true',
                        help='Run quick test with single case using gpt-3.5-turbo')
    
    args = parser.parse_args()
    
    # Show dataset info if requested
    if args.info:
        print_dataset_info()
        return
    
    if args.quick_test:
        results = await run_quick_test()
    elif args.full:
        results = await run_full_evaluation()
    elif args.high_priority:
        results = await run_high_priority_evaluation()
    elif args.balanced:
        results = await run_balanced_subset_evaluation(args.balanced)
    elif args.domain:
        results = await run_domain_evaluation(args.domain)
    elif args.cases:
        results = await run_specific_cases_evaluation(args.cases)
    else:
        print("❌ Please specify an evaluation type. Use --help for options.")
        return
    
    try:
        if results:
            print("\n✅ Evaluation completed successfully!")
            print(f"📊 Results saved to: {results.get('output_files', {}).get('results_file', 'output directory')}")
            
            # Print quick summary
            if 'summary' in results:
                summary = results['summary']
                print(f"\n📈 Quick Summary:")
                print(f"   Success rate: {summary['success_rate']:.1%}")
                print(f"   Average score: {summary['average_score']:.3f}")
                print(f"   Score range: {summary['min_score']:.3f} - {summary['max_score']:.3f}")
        
    except KeyboardInterrupt:
        print("\n⚠️ Evaluation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Evaluation failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main()) 