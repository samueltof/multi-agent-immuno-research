"""
LangSmith integration using the evaluate function approach.

This module demonstrates how to use LangSmith's evaluate function with 
the existing biomedical researcher evaluation framework.
"""

import asyncio
from typing import Dict, Any, List
from pathlib import Path
from dotenv import load_dotenv
from langsmith import Client

from .evaluators import BiomedicalResearcherEvaluator
from .test_dataset import BIOMEDICAL_TEST_CASES
from src.agents.biomedical_researcher import BiomedicalResearcherWrapper
from src.agents.biomedical_researcher import BiomedicalResearchDeps

# Load environment variables
load_dotenv()

class LangSmithEvaluationRunner:
    """Runner for LangSmith evaluate function integration."""
    
    def __init__(self, output_dir: str = "evals/outputs/biomedical_researcher"):
        self.client = Client()
        self.evaluators = BiomedicalResearcherEvaluator()
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Add feedback keys for LangSmith tracking
        self.evaluators.factual_correctness_evaluator._feedback_key = "factual_correctness"
        self.evaluators.relevance_evaluator._feedback_key = "relevance"
        self.evaluators.source_quality_evaluator._feedback_key = "source_quality"
        self.evaluators.confidence_alignment_evaluator._feedback_key = "confidence_alignment"
    
    async def biomedical_research_target(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Target function that runs the biomedical researcher agent."""
        deps = BiomedicalResearchDeps()
        agent = BiomedicalResearcherWrapper(deps)
        
        result = await agent.run_research(inputs["query"])
        
        return {
            "response": result.response,
            "key_findings": result.key_findings,
            "sources": result.sources
        }
    
    def create_wrapped_evaluator(self, evaluator_name: str):
        """Create a wrapped evaluator for LangSmith evaluate function."""
        
        async def wrapped_evaluator(
            inputs: Dict[str, Any],
            outputs: Dict[str, Any], 
            reference_outputs: Dict[str, Any] = None
        ):
            """Wrapped evaluator compatible with LangSmith evaluate function."""
            
            # Extract test case information
            domain = inputs.get("domain", "cancer_immunogenomics")
            expected_concepts = reference_outputs.get("expected_concepts", []) if reference_outputs else []
            
            # Run comprehensive evaluation
            eval_results = await self.evaluators.evaluate_comprehensive(
                query=inputs["query"],
                response=outputs["response"],
                key_findings=outputs["key_findings"],
                sources=outputs["sources"],
                expected_concepts=expected_concepts,
                domain=domain
            )
            
            if evaluator_name == "comprehensive":
                return {
                    "key": "comprehensive_score",
                    "score": eval_results["overall_score"],
                    "comment": f"Overall evaluation score across all metrics",
                    "metadata": {
                        "factual_correctness": eval_results["factual_correctness"],
                        "relevance": eval_results["relevance"],
                        "source_quality": eval_results["source_quality"],
                        "confidence_alignment": eval_results["confidence_alignment"]
                    }
                }
            else:
                return {
                    "key": evaluator_name,
                    "score": eval_results.get(evaluator_name, 0.0),
                    "comment": f"Evaluation for {evaluator_name}",
                    "metadata": eval_results
                }
        
        return wrapped_evaluator
    
    def create_dataset_from_test_cases(self, dataset_name: str = "cancer_immunogenomics_eval"):
        """Create or update a LangSmith dataset from test cases."""
        
        # Prepare dataset entries
        dataset_entries = []
        for test_case in BIOMEDICAL_TEST_CASES:
            entry = {
                "inputs": {
                    "query": test_case.prompt,
                    "domain": test_case.domain,
                    "difficulty": test_case.difficulty,
                    "test_case_id": test_case.id
                },
                "outputs": None,  # Will be filled by target function
                "reference_outputs": {
                    "reference_info": test_case.reference_info,
                    "expected_concepts": test_case.key_concepts,
                    "expected_sources": test_case.expected_sources
                }
            }
            dataset_entries.append(entry)
        
        # Create dataset
        try:
            dataset = self.client.create_dataset(
                dataset_name=dataset_name,
                description="Cancer immunogenomics evaluation dataset with specialized test cases"
            )
            print(f"Created dataset: {dataset_name}")
        except Exception:
            # Dataset might already exist
            dataset = self.client.read_dataset(dataset_name=dataset_name)
            print(f"Using existing dataset: {dataset_name}")
        
        # Add examples to dataset
        for entry in dataset_entries:
            try:
                self.client.create_example(
                    dataset_id=dataset.id,
                    inputs=entry["inputs"],
                    outputs=entry["outputs"],
                    metadata={
                        "domain": entry["inputs"]["domain"],
                        "difficulty": entry["inputs"]["difficulty"],
                        "test_case_id": entry["inputs"]["test_case_id"]
                    }
                )
            except Exception as e:
                print(f"Example may already exist: {e}")
        
        return dataset_name
    
    async def run_evaluation(self, dataset_name: str = None):
        """Run evaluation using LangSmith evaluate function."""
        
        if not dataset_name:
            dataset_name = self.create_dataset_from_test_cases()
        
        # Create wrapped evaluators
        comprehensive_evaluator = self.create_wrapped_evaluator("comprehensive")
        factual_evaluator = self.create_wrapped_evaluator("factual_correctness")
        relevance_evaluator = self.create_wrapped_evaluator("relevance")
        source_evaluator = self.create_wrapped_evaluator("source_quality")
        
        # Run evaluation
        experiment_results = await self.client.aevaluate(
            self.biomedical_research_target,
            data=dataset_name,
            evaluators=[
                comprehensive_evaluator,
                factual_evaluator, 
                relevance_evaluator,
                source_evaluator
            ],
            experiment_prefix=f"cancer_immunogenomics_eval",
            description="Comprehensive evaluation of cancer immunogenomics biomedical researcher agent",
            metadata={
                "model": "o3-mini",
                "evaluation_version": "1.0",
                "focus": "cancer_immunogenomics"
            }
        )
        
        return experiment_results

# Convenience functions for quick runs
async def run_langsmith_evaluation():
    """Run a complete LangSmith evaluation."""
    runner = LangSmithEvaluationRunner()
    
    print("Creating dataset from test cases...")
    dataset_name = runner.create_dataset_from_test_cases()
    
    print(f"Running evaluation on dataset: {dataset_name}")
    results = await runner.run_evaluation(dataset_name)
    
    print("Evaluation completed!")
    print(f"Experiment ID: {results.experiment_id}")
    print(f"Results URL: {results.experiment_url}")
    
    return results

async def run_subset_evaluation(test_case_ids: List[str]):
    """Run evaluation on a subset of test cases."""
    runner = LangSmithEvaluationRunner()
    
    # Filter test cases
    filtered_cases = [case for case in BIOMEDICAL_TEST_CASES if case.id in test_case_ids]
    
    # Temporarily replace the test cases
    original_cases = BIOMEDICAL_TEST_CASES.copy()
    BIOMEDICAL_TEST_CASES.clear()
    BIOMEDICAL_TEST_CASES.extend(filtered_cases)
    
    try:
        dataset_name = f"cancer_immunogenomics_subset_{len(test_case_ids)}"
        runner.create_dataset_from_test_cases(dataset_name)
        results = await runner.run_evaluation(dataset_name)
        return results
    finally:
        # Restore original test cases
        BIOMEDICAL_TEST_CASES.clear()
        BIOMEDICAL_TEST_CASES.extend(original_cases)

# Example usage
if __name__ == "__main__":
    # Run full evaluation
    results = asyncio.run(run_langsmith_evaluation())
    
    # Or run subset evaluation
    # subset_results = asyncio.run(run_subset_evaluation(["tcr_001", "neoantigen_001", "tme_001"])) 