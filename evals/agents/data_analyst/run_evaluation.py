"""
Simple script to run data analyst agent evaluations.
"""

import asyncio
from evaluation_runner import run_quick_evaluation, DataAnalystEvaluationRunner
from test_dataset import ALL_DATA_ANALYST_TEST_CASES


async def main():
    """Run data analyst evaluations."""
    print("Starting Data Analyst Agent Evaluation")
    print("="*50)
    
    # Option 1: Quick evaluation with specific test cases (commented out)
    # print("Running quick evaluation to test enhanced summary format...")
    # quick_results = await run_quick_evaluation(["simple_001", "simple_002", "simple_003"])
    
    # Option 2: Full evaluation - run all test cases
    print("Running full evaluation with all 30 test cases...")
    runner = DataAnalystEvaluationRunner()
    full_results = await runner.run_evaluation_suite()
    
    print("Evaluation completed!")


if __name__ == "__main__":
    asyncio.run(main()) 