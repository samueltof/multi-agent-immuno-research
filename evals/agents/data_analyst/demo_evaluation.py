"""
Demo script for Data Analyst Agent Evaluation.

This script demonstrates the evaluation capabilities and shows how to run
different types of evaluations on the data analyst agent.
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path

from .evaluation_runner import DataAnalystEvaluationRunner, run_quick_evaluation
from .test_dataset import (
    ALL_DATA_ANALYST_TEST_CASES, 
    get_test_case_by_id,
    get_test_cases_by_difficulty,
    get_test_cases_by_type,
    get_dataset_summary
)


def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def print_test_case_info(test_case):
    """Print information about a test case."""
    print(f"\n📋 Test Case: {test_case.id}")
    print(f"   Type: {test_case.query_type}")
    print(f"   Difficulty: {test_case.difficulty}")
    print(f"   Query: {test_case.natural_language_query}")
    print(f"   Expected Tables: {', '.join(test_case.expected_tables)}")
    print(f"   Domain Context: {test_case.domain_context}")


async def demo_dataset_overview():
    """Demonstrate the test dataset overview."""
    print_section("DATA ANALYST EVALUATION DATASET OVERVIEW")
    
    summary = get_dataset_summary()
    
    print(f"📊 Total Test Cases: {summary['total_test_cases']}")
    print(f"📈 Schema Coverage: {summary['schema_coverage']['coverage_percentage']:.1f}% "
          f"({summary['schema_coverage']['covered_tables']}/{summary['schema_coverage']['total_tables']} tables)")
    
    print("\n🎯 Test Cases by Difficulty:")
    for difficulty, count in summary['difficulty_distribution'].items():
        print(f"   {difficulty.capitalize()}: {count} cases")
    
    print("\n🔍 Test Cases by Query Type:")
    for query_type, count in summary['query_type_distribution'].items():
        print(f"   {query_type.replace('_', ' ').title()}: {count} cases")
    
    print(f"\n🗄️ Database Tables Covered:")
    for table in summary['tables_covered']:
        print(f"   - {table}")


async def demo_individual_test_cases():
    """Demonstrate individual test case examples."""
    print_section("SAMPLE TEST CASES")
    
    # Show examples from different categories
    example_cases = [
        "simple_001",    # Simple query
        "join_001",      # Join query  
        "agg_002",       # Complex aggregation
        "immuno_001",    # Immunological domain
    ]
    
    for case_id in example_cases:
        try:
            test_case = get_test_case_by_id(case_id)
            print_test_case_info(test_case)
            
            if test_case.expected_sql_pattern:
                print(f"   Expected SQL Pattern: {test_case.expected_sql_pattern}")
            
            print(f"   Success Criteria:")
            for criterion in test_case.success_criteria:
                print(f"     ✓ {criterion}")
                
        except ValueError:
            print(f"   ❌ Test case {case_id} not found")


async def demo_quick_evaluation():
    """Demonstrate a quick evaluation run."""
    print_section("QUICK EVALUATION DEMO")
    
    print("🚀 Running quick evaluation on 3 test cases...")
    print("This will test the data analyst agent on:")
    print("  - Simple epitope counting")
    print("  - Basic epitope listing") 
    print("  - Multi-table join query")
    
    # Run quick evaluation
    try:
        results = await run_quick_evaluation(["simple_001", "simple_002", "join_001"])
        
        print(f"\n✅ Evaluation completed!")
        print(f"   Successful: {results['successful_evaluations']}")
        print(f"   Failed: {results['failed_evaluations']}")
        
        if results['successful_evaluations'] > 0:
            avg_score = results['summary']['overall_average_score']
            print(f"   Average Score: {avg_score:.3f}")
            
            print(f"\n📊 Individual Results:")
            for result in results['detailed_results'][:3]:  # Show first 3
                score = result['overall_score']
                case_id = result['test_case_id']
                print(f"   {case_id}: {score:.3f}")
        
        # Save demo results
        demo_output_dir = Path("evals/outputs/data_analyst/demo")
        demo_output_dir.mkdir(parents=True, exist_ok=True)
        
        demo_file = demo_output_dir / f"demo_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(demo_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\n💾 Demo results saved to: {demo_file}")
        
    except Exception as e:
        print(f"\n❌ Evaluation failed: {e}")


async def demo_filtered_evaluations():
    """Demonstrate filtered evaluation runs."""
    print_section("FILTERED EVALUATION EXAMPLES")
    
    print("🎯 Available filtering options:")
    
    # Show difficulty-based filtering
    print("\n📈 By Difficulty:")
    for difficulty in ["easy", "medium", "hard"]:
        cases = get_test_cases_by_difficulty(difficulty)
        print(f"   {difficulty.capitalize()}: {len(cases)} cases")
        if cases:
            case_ids = [case.id for case in cases[:3]]  # Show first 3
            print(f"     Examples: {', '.join(case_ids)}")
    
    # Show type-based filtering
    print("\n🔍 By Query Type:")
    query_types = ["simple", "join", "aggregation", "immunological"]
    for query_type in query_types:
        cases = get_test_cases_by_type(query_type)
        print(f"   {query_type.replace('_', ' ').title()}: {len(cases)} cases")
        if cases:
            case_ids = [case.id for case in cases[:2]]  # Show first 2
            print(f"     Examples: {', '.join(case_ids)}")


async def demo_evaluation_configuration():
    """Demonstrate different evaluation configurations."""
    print_section("EVALUATION CONFIGURATION OPTIONS")
    
    print("⚙️ Available Configuration Options:")
    
    print("\n🤖 LLM Models:")
    models = ["openai:gpt-4o-mini", "openai:gpt-4o", "anthropic:claude-3-sonnet"]
    for model in models:
        print(f"   - {model}")
    
    print("\n📁 Output Directories:")
    print("   - Default: evals/outputs/data_analyst")
    print("   - Custom: evals/outputs/data_analyst/custom_run")
    print("   - Timestamped: evals/outputs/data_analyst/YYYYMMDD_HHMMSS")
    
    print("\n📊 Evaluation Metrics:")
    metrics = [
        ("SQL Correctness", "25%"),
        ("Schema Understanding", "20%"),
        ("Query Execution", "20%"),
        ("Result Interpretation", "15%"),
        ("Domain Knowledge", "10%"),
        ("Workflow Completeness", "10%")
    ]
    
    for metric, weight in metrics:
        print(f"   - {metric}: {weight}")


async def demo_expected_performance():
    """Show expected performance benchmarks."""
    print_section("EXPECTED PERFORMANCE BENCHMARKS")
    
    print("🎯 Performance Expectations:")
    
    print("\n📊 By Metric:")
    benchmarks = {
        "SQL Correctness": "0.80-0.95",
        "Schema Understanding": "0.85-0.95",
        "Query Execution": "0.75-0.90",
        "Result Interpretation": "0.80-0.90",
        "Domain Knowledge": "0.70-0.85",
        "Overall Score": "0.78-0.88"
    }
    
    for metric, range_str in benchmarks.items():
        print(f"   {metric}: {range_str}")
    
    print("\n📈 By Difficulty:")
    difficulty_benchmarks = {
        "Easy": ">0.90",
        "Medium": "0.80-0.90", 
        "Hard": "0.70-0.85"
    }
    
    for difficulty, range_str in difficulty_benchmarks.items():
        print(f"   {difficulty}: {range_str}")


async def main():
    """Run the complete demo."""
    print_section("DATA ANALYST AGENT EVALUATION DEMO")
    print("This demo showcases the comprehensive evaluation framework")
    print("for the Data Analyst agent using the VDJdb augmented database.")
    
    # Run all demo sections
    await demo_dataset_overview()
    await demo_individual_test_cases()
    await demo_filtered_evaluations()
    await demo_evaluation_configuration()
    await demo_expected_performance()
    
    # Ask user if they want to run actual evaluation
    print_section("INTERACTIVE EVALUATION")
    print("Would you like to run a quick evaluation? (This will test the actual agent)")
    print("Note: This requires database access and may take a few minutes.")
    
    # For demo purposes, we'll skip the interactive part
    # In a real scenario, you could add user input here
    print("\n🔄 Skipping interactive evaluation for demo...")
    print("To run actual evaluations, use:")
    print("  python run_evaluation.py")
    print("  # or")
    print("  python -c 'import asyncio; from demo_evaluation import demo_quick_evaluation; asyncio.run(demo_quick_evaluation())'")
    
    print_section("DEMO COMPLETE")
    print("✅ Demo completed successfully!")
    print("📚 See README.md for detailed usage instructions")
    print("🚀 Ready to evaluate your data analyst agent!")


if __name__ == "__main__":
    asyncio.run(main()) 