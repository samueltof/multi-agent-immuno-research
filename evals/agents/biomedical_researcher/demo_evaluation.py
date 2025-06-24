"""
Demo script for testing the Biomedical Researcher evaluation framework.

This script demonstrates how to use the evaluation framework with mock data
before integrating with the actual biomedical researcher agent.
"""

import asyncio
import json
from pathlib import Path

from .evaluators import BiomedicalResearcherEvaluator
from .test_dataset import get_test_case_by_id, get_test_dataset_summary


def create_mock_response(test_case_id: str) -> dict:
    """Create mock responses for different test cases."""
    
    mock_responses = {
        "basic_001": {
            "summary": """Type 1 and Type 2 diabetes mellitus are two distinct forms of diabetes with different underlying pathophysiology and treatment approaches. Type 1 diabetes is an autoimmune condition where the immune system attacks and destroys insulin-producing beta cells in the pancreas, leading to absolute insulin deficiency. Type 2 diabetes is characterized by insulin resistance and relative insulin deficiency, often associated with obesity and lifestyle factors.""",
            "key_findings": """Key differences include:
            - Type 1: Autoimmune destruction of beta cells, typically develops in childhood/adolescence, requires insulin therapy
            - Type 2: Insulin resistance and progressive beta cell dysfunction, typically develops in adults, can often be managed with lifestyle changes and oral medications initially
            - Type 1 accounts for 5-10% of diabetes cases, Type 2 accounts for 90-95%
            - Genetic factors differ between the two types""",
            "sources": [
                "PubMed: American Diabetes Association. Classification and Diagnosis of Diabetes. Diabetes Care 2021;44(Supplement 1):S15-S33",
                "PubMed: Atkinson, M.A., et al. Type 1 diabetes. Lancet 2014;383(9911):69-82",
                "PubMed: DeFronzo, R.A., et al. Type 2 diabetes mellitus. Nat Rev Dis Primers 2015;1:15019"
            ],
            "recommendations": "Regular monitoring of blood glucose, appropriate medication management, lifestyle modifications including diet and exercise, and screening for complications are essential for both types of diabetes.",
            "confidence_level": 0.9
        },
        
        "oncology_002": {
            "summary": """Pembrolizumab is a humanized monoclonal antibody that targets the programmed cell death protein 1 (PD-1) receptor on T lymphocytes. It works by blocking the interaction between PD-1 and its ligands (PD-L1 and PD-L2), thereby preventing the inhibition of T-cell immune responses. This mechanism allows the immune system to recognize and attack cancer cells more effectively.""",
            "key_findings": """Mechanism and efficacy in melanoma:
            - Pembrolizumab binds to PD-1 receptor with high specificity and affinity
            - Blocks immune checkpoint pathway that tumors use to evade immune surveillance
            - Shows significant improvement in overall survival and progression-free survival in advanced melanoma
            - Response rates of 30-40% in treatment-naive advanced melanoma patients
            - Durable responses observed, with some patients maintaining response for years
            - Common side effects include fatigue, skin rash, and immune-related adverse events""",
            "sources": [
                "PubMed: Robert, C., et al. Pembrolizumab versus Ipilimumab in Advanced Melanoma. N Engl J Med 2015;372(26):2521-2532",
                "DrugBank: Pembrolizumab Drug Entry DB09037",
                "PubMed: Schachter, J., et al. Pembrolizumab versus ipilimumab for advanced melanoma: final overall survival results. Lancet 2017;390(10105):1853-1862"
            ],
            "recommendations": "Pembrolizumab is recommended as first-line therapy for advanced melanoma patients with good performance status. Regular monitoring for immune-related adverse events is essential.",
            "confidence_level": 0.85
        }
    }
    
    return mock_responses.get(test_case_id, {
        "summary": "Mock summary for test case",
        "key_findings": "Mock key findings",
        "sources": ["Mock source 1", "Mock source 2"],
        "recommendations": "Mock recommendations",
        "confidence_level": 0.7
    })


async def demo_single_evaluation():
    """Demonstrate evaluation of a single test case."""
    print("=== DEMO: Single Test Case Evaluation ===\n")
    
    # Get a test case
    test_case = get_test_case_by_id("basic_001")
    print(f"Test Case: {test_case.id}")
    print(f"Domain: {test_case.domain}")
    print(f"Difficulty: {test_case.difficulty}")
    print(f"Prompt: {test_case.prompt[:100]}...\n")
    
    # Create mock response
    mock_response = create_mock_response(test_case.id)
    print("Mock Agent Response:")
    print(f"Summary: {mock_response['summary'][:100]}...")
    print(f"Confidence: {mock_response['confidence_level']}\n")
    
    # Initialize evaluator
    evaluator = BiomedicalResearcherEvaluator()
    print("Evaluating response...")
    
    # Run evaluation
    evaluations = evaluator.evaluate_response(
        prompt=test_case.prompt,
        response=mock_response,
        reference_outputs=test_case.reference_info
    )
    
    # Calculate overall score
    overall_score = evaluator.calculate_overall_score(evaluations)
    
    # Display results
    print("\n=== EVALUATION RESULTS ===")
    print(f"Overall Score: {overall_score:.3f}")
    print("\nIndividual Metrics:")
    for metric, result in evaluations.items():
        score = result.get('score', 0.0)
        comment = result.get('comment', 'No comment')
        print(f"\n{metric.replace('_', ' ').title()}: {score:.3f}")
        print(f"Comment: {comment[:200]}{'...' if len(comment) > 200 else ''}")


async def demo_multiple_evaluations():
    """Demonstrate evaluation of multiple test cases."""
    print("\n\n=== DEMO: Multiple Test Cases Evaluation ===\n")
    
    # Select test cases
    test_case_ids = ["basic_001", "oncology_002"]
    evaluator = BiomedicalResearcherEvaluator()
    
    all_results = []
    
    for test_id in test_case_ids:
        print(f"Evaluating test case: {test_id}")
        
        # Get test case and mock response
        test_case = get_test_case_by_id(test_id)
        mock_response = create_mock_response(test_id)
        
        # Evaluate
        evaluations = evaluator.evaluate_response(
            prompt=test_case.prompt,
            response=mock_response,
            reference_outputs=test_case.reference_info
        )
        
        overall_score = evaluator.calculate_overall_score(evaluations)
        
        result = {
            "test_case_id": test_id,
            "domain": test_case.domain,
            "difficulty": test_case.difficulty,
            "overall_score": overall_score,
            "individual_scores": {
                metric: result.get('score', 0.0)
                for metric, result in evaluations.items()
            }
        }
        
        all_results.append(result)
        print(f"Score: {overall_score:.3f}\n")
    
    # Summary
    print("=== SUMMARY ===")
    avg_score = sum(r["overall_score"] for r in all_results) / len(all_results)
    print(f"Average Overall Score: {avg_score:.3f}")
    
    # Individual metric averages
    metric_averages = {}
    for result in all_results:
        for metric, score in result["individual_scores"].items():
            if metric not in metric_averages:
                metric_averages[metric] = []
            metric_averages[metric].append(score)
    
    print("\nAverage Scores by Metric:")
    for metric, scores in metric_averages.items():
        avg = sum(scores) / len(scores)
        print(f"  {metric.replace('_', ' ').title()}: {avg:.3f}")


def demo_test_dataset_overview():
    """Show overview of the test dataset."""
    print("\n\n=== DEMO: Test Dataset Overview ===\n")
    
    summary = get_test_dataset_summary()
    
    print(f"Total Test Cases: {summary['total_cases']}")
    print(f"Average Concepts per Case: {summary['average_concepts_per_case']:.1f}")
    
    print("\nCases by Domain:")
    for domain, count in summary['domains'].items():
        print(f"  {domain}: {count}")
    
    print("\nCases by Difficulty:")
    for difficulty, count in summary['difficulties'].items():
        print(f"  {difficulty}: {count}")


def save_demo_results():
    """Save demo results for inspection."""
    print("\n\n=== DEMO: Saving Results ===\n")
    
    # Create sample results
    demo_results = {
        "evaluation_info": {
            "timestamp": "2024-01-15T10:30:00",
            "evaluator_model": "openai:gpt-4o-mini",
            "demo_mode": True
        },
        "test_cases_evaluated": ["basic_001", "oncology_002"],
        "sample_evaluation": {
            "test_case_id": "basic_001",
            "overall_score": 0.825,
            "individual_scores": {
                "factual_correctness": 0.9,
                "relevance": 0.8,
                "source_quality": 0.8,
                "confidence_alignment": 0.8
            }
        }
    }
    
    # Save to file
    output_dir = Path("evals/outputs/biomedical_researcher")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    filepath = output_dir / "demo_evaluation_results.json"
    with open(filepath, 'w') as f:
        json.dump(demo_results, f, indent=2)
    
    print(f"Demo results saved to: {filepath}")


async def run_full_demo():
    """Run the complete demo."""
    print("🧬 BIOMEDICAL RESEARCHER EVALUATION FRAMEWORK DEMO 🧬")
    print("=" * 60)
    
    # Dataset overview
    demo_test_dataset_overview()
    
    # Single evaluation
    await demo_single_evaluation()
    
    # Multiple evaluations
    await demo_multiple_evaluations()
    
    # Save results
    save_demo_results()
    
    print("\n" + "=" * 60)
    print("✅ Demo completed successfully!")
    print("\nNext steps:")
    print("1. Integrate with actual biomedical researcher agent")
    print("2. Run evaluation on full test dataset")
    print("3. Analyze results and improve agent performance")
    print("4. Set up automated evaluation pipeline")


if __name__ == "__main__":
    asyncio.run(run_full_demo()) 