"""
Demo script for the Web Researcher agent evaluation system.

This script demonstrates how to:
1. Run evaluations on individual test cases
2. Analyze evaluation results
3. Compare different evaluation metrics
4. Understand RAG-specific evaluation components
"""

import asyncio
import json
from pathlib import Path
from typing import Dict, Any

from .evaluation_runner import EvaluationRunner
from .test_dataset import RESEARCHER_TEST_CASES, get_test_case_by_id
from .evaluators import ResearcherEvaluator


async def demo_single_evaluation():
    """Demo evaluation on a single test case."""
    print("="*80)
    print("DEMO: Single Test Case Evaluation")
    print("="*80)
    
    # Select a test case
    test_case = get_test_case_by_id("tech_001")
    print(f"Test Case: {test_case.id}")
    print(f"Domain: {test_case.domain}")
    print(f"Difficulty: {test_case.difficulty}")
    print(f"Query: {test_case.prompt}")
    print()
    
    # Initialize evaluation runner
    runner = EvaluationRunner(
        output_dir="evals/outputs/researcher/demo",
        evaluator_model="openai:o4-mini"
    )
    
    # Run evaluation
    print("Running evaluation...")
    result = runner.run_single_evaluation(test_case)
    
    # Display results
    print("\nEvaluation Results:")
    print(f"Overall Score: {result.get('overall_score', 'Error'):.2f}")
    
    if 'individual_scores' in result:
        print("\nDetailed Scores:")
        for metric, score_info in result['individual_scores'].items():
            print(f"  {metric}: {score_info['score']:.2f}")
            print(f"    Comment: {score_info['comment'][:100]}...")
    
    return result


async def demo_domain_evaluation():
    """Demo evaluation on all test cases from a specific domain."""
    print("\n" + "="*80)
    print("DEMO: Domain-Specific Evaluation (Technology)")
    print("="*80)
    
    from .test_dataset import get_test_cases_by_domain
    
    # Get technology test cases
    tech_cases = get_test_cases_by_domain("technology")
    print(f"Found {len(tech_cases)} technology test cases")
    
    # Run evaluation
    runner = EvaluationRunner(output_dir="evals/outputs/researcher/demo")
    
    results = []
    for test_case in tech_cases[:2]:  # Limit to 2 for demo
        print(f"\nEvaluating: {test_case.id}")
        result = runner.run_single_evaluation(test_case)
        results.append(result)
    
    # Analyze results
    print("\nDomain Analysis:")
    scores = [r.get('overall_score', 0) for r in results if 'overall_score' in r]
    if scores:
        print(f"Average Score: {sum(scores)/len(scores):.2f}")
        print(f"Best Score: {max(scores):.2f}")
        print(f"Worst Score: {min(scores):.2f}")
    
    return results


def demo_rag_evaluation():
    """Demo RAG-specific evaluation components."""
    print("\n" + "="*80)
    print("DEMO: RAG-Specific Evaluation")
    print("="*80)
    
    # Create evaluator
    evaluator = ResearcherEvaluator()
    
    # Sample RAG components
    prompt = "What are the latest developments in quantum computing?"
    retrieved_content = """
    Recent advances in quantum computing include:
    - IBM's 1000-qubit processor
    - Google's quantum error correction breakthroughs
    - Quantum networking developments
    """
    generated_response = """
    Quantum computing has seen significant advances in 2024, including IBM's release of 
    their 1000-qubit Condor processor and Google's breakthrough in quantum error correction...
    """
    
    print("Evaluating RAG components:")
    print(f"Prompt: {prompt}")
    print(f"Retrieved content: {retrieved_content[:100]}...")
    print(f"Generated response: {generated_response[:100]}...")
    
    # Create mock response for evaluation
    mock_response = {
        "content": generated_response,
        "sources": ["https://example.com/quantum-news"],
        "search_info": "Searched for quantum computing developments 2024",
        "crawled_content": retrieved_content
    }
    
    # Create mock test case info
    test_case_info = {
        "expected_sources": ["quantum computing news"],
        "search_keywords": ["quantum computing", "2024", "developments"],
        "key_concepts": ["quantum processor", "error correction", "networking"]
    }
    
    # Run comprehensive RAG evaluation using the main evaluate_response method
    rag_results = evaluator.evaluate_response(
        prompt=prompt,
        response=mock_response,
        test_case_info=test_case_info
    )
    
    print("\nCore RAG Evaluation Results:")
    # Focus on core RAG-specific metrics
    core_rag_metrics = ["faithfulness", "context_precision", "context_recall", "rag_effectiveness"]
    for metric in core_rag_metrics:
        if metric in rag_results:
            result = rag_results[metric]
            if isinstance(result, dict) and "score" in result:
                print(f"  {metric}: {result.get('score', 'Error'):.2f}")
                print(f"    {result.get('comment', 'No comment')[:80]}...")
            else:
                print(f"  {metric}: Error - {result}")
    
    print("\nAdvanced Enhancement Metrics:")
    # Show new enhancement metrics
    enhancement_metrics = ["temporal_accuracy", "bias_assessment", "factual_verification"]
    for metric in enhancement_metrics:
        if metric in rag_results:
            result = rag_results[metric]
            if isinstance(result, dict) and "score" in result:
                print(f"  {metric}: {result.get('score', 'Error'):.2f}")
                print(f"    {result.get('comment', 'No comment')[:80]}...")
            else:
                print(f"  {metric}: Error - {result}")
    
    # Also show other metrics for context
    print("\nCore Web Research Metrics:")
    other_metrics = ["search_quality", "information_synthesis", "source_quality"]
    for metric in other_metrics:
        if metric in rag_results:
            result = rag_results[metric]
            if isinstance(result, dict) and "score" in result:
                print(f"  {metric}: {result.get('score', 'Error'):.2f}")
            else:
                print(f"  {metric}: Error - {result}")
    
    # Calculate and show overall score
    overall_score = evaluator.calculate_overall_score(rag_results)
    print(f"\nOverall Weighted Score: {overall_score:.3f}")
    print("(Based on enhanced weighting system with new metrics)")
    
    print("\n" + "="*80)


async def demo_comparative_analysis():
    """Demo comparing evaluation results across different metrics."""
    print("\n" + "="*80)
    print("DEMO: Comparative Analysis Across Metrics")
    print("="*80)
    
    # Run evaluation on a few test cases
    runner = EvaluationRunner(output_dir="evals/outputs/researcher/demo")
    
    test_case_ids = ["tech_001", "science_001", "business_001"]
    results = []
    
    for test_id in test_case_ids:
        test_case = get_test_case_by_id(test_id)
        result = runner.run_single_evaluation(test_case)
        results.append(result)
    
    # Analyze metric performance
    metrics = ["search_quality", "crawling_quality", "information_synthesis", 
               "source_quality", "research_completeness"]
    
    print("Metric Performance Analysis:")
    for metric in metrics:
        scores = []
        for result in results:
            if 'individual_scores' in result and metric in result['individual_scores']:
                scores.append(result['individual_scores'][metric]['score'])
        
        if scores:
            avg_score = sum(scores) / len(scores)
            print(f"{metric}: {avg_score:.2f} (avg across {len(scores)} cases)")


def save_demo_results(results: Dict[str, Any]):
    """Save demo results for analysis."""
    output_dir = Path("evals/outputs/researcher/demo")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_dir / "demo_results.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\nDemo results saved to: {output_dir / 'demo_results.json'}")


async def main():
    """Run all demo evaluations."""
    print("Web Researcher Agent Evaluation Demo")
    print("This demo shows the evaluation capabilities for the web research agent.")
    print("The agent uses web search and crawling to gather information and answer queries.")
    
    all_results = {}
    
    # Demo 1: Single evaluation
    result1 = await demo_single_evaluation()
    all_results['single_evaluation'] = result1
    
    # Demo 2: Domain evaluation
    result2 = await demo_domain_evaluation()
    all_results['domain_evaluation'] = result2
    
    # Demo 3: RAG evaluation
    demo_rag_evaluation()
    
    # Demo 4: Comparative analysis
    await demo_comparative_analysis()
    
    # Save results
    save_demo_results(all_results)
    
    print("\n" + "="*80)
    print("DEMO COMPLETED")
    print("="*80)
    print("Key features demonstrated:")
    print("- Individual test case evaluation")
    print("- Domain-specific evaluation")
    print("- RAG component evaluation")
    print("- Comparative metric analysis")
    print("- Comprehensive scoring system")


if __name__ == "__main__":
    asyncio.run(main()) 