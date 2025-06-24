"""
Evaluation runner for the Biomedical Researcher agent.

This module orchestrates the evaluation process by:
1. Running the biomedical researcher agent on test cases
2. Collecting responses
3. Evaluating responses using LLM-as-a-judge
4. Generating comprehensive reports
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import traceback
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from .evaluators import BiomedicalResearcherEvaluator
from .test_dataset import BIOMEDICAL_TEST_CASES, BiomedicalTestCase, get_test_dataset_summary
from src.agents.biomedical_researcher import BiomedicalResearcherWrapper


class EvaluationRunner:
    """Main evaluation runner for the Biomedical Researcher agent."""
    
    def __init__(
        self,
        output_dir: str = "evals/outputs/biomedical_researcher",
        evaluator_model: str = "openai:o3-mini",
        agent_config: Optional[Dict[str, Any]] = None
    ):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize evaluator
        self.evaluator = BiomedicalResearcherEvaluator(model=evaluator_model)
        
        # Initialize agent
        self.agent_config = agent_config or {}
        self.agent = None  # Will be initialized when needed
        
        # Setup logging
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging for the evaluation runner."""
        log_file = self.output_dir / f"evaluation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def initialize_agent(self):
        """Initialize the biomedical researcher agent."""
        try:
            self.agent = BiomedicalResearcherWrapper(**self.agent_config)
            self.logger.info("Biomedical researcher agent initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize agent: {e}")
            raise
    
    async def run_agent_on_test_case(self, test_case: BiomedicalTestCase) -> Dict[str, Any]:
        """Run the biomedical researcher agent on a single test case."""
        try:
            self.logger.info(f"Running agent on test case: {test_case.id}")
            
            # Initialize agent if not already done
            if self.agent is None:
                self.initialize_agent()
            
            # Create dependencies for the research query
            from src.agents.biomedical_researcher import BiomedicalResearchDeps
            deps = BiomedicalResearchDeps(
                research_focus=test_case.domain,
                preferred_databases=test_case.expected_sources
            )
            
            # Run the actual biomedical researcher agent
            async with self.agent as researcher:
                result = await researcher.run_research(test_case.prompt, deps)
                
                # Convert BiomedicalResearchOutput to dict format expected by evaluator
                response = {
                    "summary": result.summary,
                    "key_findings": result.key_findings,
                    "sources": result.sources,
                    "recommendations": result.recommendations,
                    "confidence_level": result.confidence_level,
                    "query": test_case.prompt
                }
            
            self.logger.info(f"Agent completed test case: {test_case.id}")
            return response
            
        except Exception as e:
            self.logger.error(f"Error running agent on test case {test_case.id}: {e}")
            self.logger.error(traceback.format_exc())
            return {
                "error": str(e),
                "query": test_case.prompt
            }
    
    def evaluate_response(
        self,
        test_case: BiomedicalTestCase,
        agent_response: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Evaluate an agent response using LLM-as-a-judge."""
        try:
            self.logger.info(f"Evaluating response for test case: {test_case.id}")
            
            # Skip evaluation if there was an error in the agent response
            if "error" in agent_response:
                return {
                    "error": "Agent response contained error",
                    "agent_error": agent_response["error"]
                }
            
            # Run the comprehensive evaluation
            evaluations = self.evaluator.evaluate_response(
                prompt=test_case.prompt,
                response=agent_response,
                reference_outputs=test_case.reference_info
            )
            
            # Calculate overall score
            overall_score = self.evaluator.calculate_overall_score(evaluations)
            
            # Compile results
            result = {
                "test_case_id": test_case.id,
                "domain": test_case.domain,
                "difficulty": test_case.difficulty,
                "overall_score": overall_score,
                "individual_scores": {
                    metric: {
                        "score": eval_result.get("score", 0.0),
                        "comment": eval_result.get("comment", "")
                    }
                    for metric, eval_result in evaluations.items()
                },
                "agent_response": agent_response,
                "expected_concepts": test_case.key_concepts,
                "expected_sources": test_case.expected_sources
            }
            
            self.logger.info(f"Evaluation completed for test case: {test_case.id}, score: {overall_score:.2f}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error evaluating test case {test_case.id}: {e}")
            self.logger.error(traceback.format_exc())
            return {
                "error": str(e),
                "test_case_id": test_case.id
            }
    
    async def run_single_evaluation(self, test_case: BiomedicalTestCase) -> Dict[str, Any]:
        """Run evaluation on a single test case."""
        # Run agent
        agent_response = await self.run_agent_on_test_case(test_case)
        
        # Evaluate response
        evaluation_result = self.evaluate_response(test_case, agent_response)
        
        return evaluation_result
    
    async def run_evaluation_suite(
        self,
        test_cases: Optional[List[BiomedicalTestCase]] = None,
        max_concurrent: int = 1
    ) -> Dict[str, Any]:
        """Run the complete evaluation suite."""
        if test_cases is None:
            test_cases = BIOMEDICAL_TEST_CASES
        
        self.logger.info(f"Starting evaluation suite with {len(test_cases)} test cases")
        
        # Create semaphore to limit concurrent executions
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def run_with_semaphore(test_case):
            async with semaphore:
                return await self.run_single_evaluation(test_case)
        
        # Run evaluations concurrently
        results = await asyncio.gather(
            *[run_with_semaphore(test_case) for test_case in test_cases],
            return_exceptions=True
        )
        
        # Process results
        successful_results = []
        failed_results = []
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                failed_results.append({
                    "test_case_id": test_cases[i].id,
                    "error": str(result)
                })
            elif isinstance(result, dict) and "error" in result:
                failed_results.append(result)
            elif result is not None:
                successful_results.append(result)
        
        # Compile final results
        final_results = {
            "evaluation_summary": self.generate_evaluation_summary(successful_results, failed_results),
            "successful_evaluations": successful_results,
            "failed_evaluations": failed_results,
            "test_dataset_summary": get_test_dataset_summary(),
            "evaluation_config": {
                "evaluator_model": self.evaluator.model,
                "agent_config": self.agent_config,
                "timestamp": datetime.now().isoformat()
            }
        }
        
        # Save results
        self.save_results(final_results)
        
        self.logger.info(f"Evaluation suite completed. Success: {len(successful_results)}, Failed: {len(failed_results)}")
        
        return final_results
    
    def generate_evaluation_summary(
        self,
        successful_results: List[Dict[str, Any]],
        failed_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate a summary of evaluation results."""
        if not successful_results:
            return {
                "total_cases": len(failed_results),
                "successful_cases": 0,
                "failed_cases": len(failed_results),
                "success_rate": 0.0,
                "average_score": 0.0,
                "scores_by_domain": {},
                "scores_by_difficulty": {},
                "metric_averages": {}
            }
        
        # Calculate overall statistics
        total_cases = len(successful_results) + len(failed_results)
        success_rate = len(successful_results) / total_cases if total_cases > 0 else 0
        
        # Calculate score statistics
        scores = [result["overall_score"] for result in successful_results]
        average_score = sum(scores) / len(scores) if scores else 0
        
        # Calculate scores by domain
        scores_by_domain = {}
        for result in successful_results:
            domain = result["domain"]
            if domain not in scores_by_domain:
                scores_by_domain[domain] = []
            scores_by_domain[domain].append(result["overall_score"])
        
        # Average scores by domain
        for domain in scores_by_domain:
            scores_by_domain[domain] = sum(scores_by_domain[domain]) / len(scores_by_domain[domain])
        
        # Calculate scores by difficulty
        scores_by_difficulty = {}
        for result in successful_results:
            difficulty = result["difficulty"]
            if difficulty not in scores_by_difficulty:
                scores_by_difficulty[difficulty] = []
            scores_by_difficulty[difficulty].append(result["overall_score"])
        
        # Average scores by difficulty
        for difficulty in scores_by_difficulty:
            scores_by_difficulty[difficulty] = sum(scores_by_difficulty[difficulty]) / len(scores_by_difficulty[difficulty])
        
        # Calculate individual metric averages
        metric_averages = {}
        for result in successful_results:
            for metric, score_data in result["individual_scores"].items():
                if metric not in metric_averages:
                    metric_averages[metric] = []
                metric_averages[metric].append(score_data["score"])
        
        # Average individual metrics
        for metric in metric_averages:
            metric_averages[metric] = sum(metric_averages[metric]) / len(metric_averages[metric])
        
        return {
            "total_cases": total_cases,
            "successful_cases": len(successful_results),
            "failed_cases": len(failed_results),
            "success_rate": success_rate,
            "average_score": average_score,
            "min_score": min(scores) if scores else 0,
            "max_score": max(scores) if scores else 0,
            "scores_by_domain": scores_by_domain,
            "scores_by_difficulty": scores_by_difficulty,
            "metric_averages": metric_averages
        }
    
    def save_results(self, results: Dict[str, Any]):
        """Save evaluation results to multiple structured files for analysis and visualization."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        try:
            # 1. Save complete results as JSON
            main_filename = f"biomedical_researcher_evaluation_{timestamp}.json"
            main_filepath = self.output_dir / main_filename
            with open(main_filepath, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            
            # 2. Save structured data for visualization as CSV-friendly JSON
            viz_data = self.prepare_visualization_data(results)
            viz_filename = f"biomedical_researcher_visualization_data_{timestamp}.json"
            viz_filepath = self.output_dir / viz_filename
            with open(viz_filepath, 'w') as f:
                json.dump(viz_data, f, indent=2, default=str)
            
            # 3. Save summary metrics for quick analysis
            summary_filename = f"biomedical_researcher_summary_{timestamp}.json"
            summary_filepath = self.output_dir / summary_filename
            with open(summary_filepath, 'w') as f:
                json.dump(results["evaluation_summary"], f, indent=2, default=str)
            
            self.logger.info(f"Results saved to:")
            self.logger.info(f"  Complete results: {main_filepath}")
            self.logger.info(f"  Visualization data: {viz_filepath}")
            self.logger.info(f"  Summary metrics: {summary_filepath}")
            
        except Exception as e:
            self.logger.error(f"Failed to save results: {e}")
    
    def prepare_visualization_data(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare structured data optimized for visualization and plotting."""
        successful_results = results.get("successful_evaluations", [])
        
        # Flatten individual results for easier plotting
        flattened_results = []
        for result in successful_results:
            flat_result = {
                "test_case_id": result["test_case_id"],
                "domain": result["domain"],
                "difficulty": result["difficulty"],
                "overall_score": result["overall_score"]
            }
            
            # Add individual metric scores
            for metric, score_data in result["individual_scores"].items():
                flat_result[f"{metric}_score"] = score_data["score"]
                flat_result[f"{metric}_comment"] = score_data["comment"]
            
            flattened_results.append(flat_result)
        
        # Create domain-wise analysis
        domain_analysis = {}
        difficulty_analysis = {}
        
        for result in successful_results:
            domain = result["domain"]
            difficulty = result["difficulty"]
            
            # Domain analysis
            if domain not in domain_analysis:
                domain_analysis[domain] = {
                    "count": 0,
                    "total_score": 0,
                    "scores": [],
                    "metrics": {metric: [] for metric in ["factual_correctness", "relevance", "source_quality", "confidence_alignment"]}
                }
            
            domain_analysis[domain]["count"] += 1
            domain_analysis[domain]["total_score"] += result["overall_score"]
            domain_analysis[domain]["scores"].append(result["overall_score"])
            
            for metric, score_data in result["individual_scores"].items():
                domain_analysis[domain]["metrics"][metric].append(score_data["score"])
            
            # Difficulty analysis
            if difficulty not in difficulty_analysis:
                difficulty_analysis[difficulty] = {
                    "count": 0,
                    "total_score": 0,
                    "scores": [],
                    "metrics": {metric: [] for metric in ["factual_correctness", "relevance", "source_quality", "confidence_alignment"]}
                }
            
            difficulty_analysis[difficulty]["count"] += 1
            difficulty_analysis[difficulty]["total_score"] += result["overall_score"]
            difficulty_analysis[difficulty]["scores"].append(result["overall_score"])
            
            for metric, score_data in result["individual_scores"].items():
                difficulty_analysis[difficulty]["metrics"][metric].append(score_data["score"])
        
        # Calculate averages and statistics
        for domain_data in domain_analysis.values():
            if domain_data["count"] > 0:
                domain_data["average_score"] = domain_data["total_score"] / domain_data["count"]
                domain_data["min_score"] = min(domain_data["scores"])
                domain_data["max_score"] = max(domain_data["scores"])
                
                for metric, scores in domain_data["metrics"].items():
                    domain_data["metrics"][metric] = {
                        "average": sum(scores) / len(scores) if scores else 0,
                        "min": min(scores) if scores else 0,
                        "max": max(scores) if scores else 0,
                        "scores": scores
                    }
        
        for difficulty_data in difficulty_analysis.values():
            if difficulty_data["count"] > 0:
                difficulty_data["average_score"] = difficulty_data["total_score"] / difficulty_data["count"]
                difficulty_data["min_score"] = min(difficulty_data["scores"])
                difficulty_data["max_score"] = max(difficulty_data["scores"])
                
                for metric, scores in difficulty_data["metrics"].items():
                    difficulty_data["metrics"][metric] = {
                        "average": sum(scores) / len(scores) if scores else 0,
                        "min": min(scores) if scores else 0,
                        "max": max(scores) if scores else 0,
                        "scores": scores
                    }
        
        return {
            "individual_results": flattened_results,
            "domain_analysis": domain_analysis,
            "difficulty_analysis": difficulty_analysis,
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "evaluator_model": results["evaluation_config"]["evaluator_model"],
                "total_test_cases": len(flattened_results),
                "domains": list(domain_analysis.keys()),
                "difficulties": list(difficulty_analysis.keys()),
                "metrics": ["factual_correctness", "relevance", "source_quality", "confidence_alignment"]
            }
        }
    
    def print_summary(self, results: Dict[str, Any]):
        """Print a formatted summary of evaluation results."""
        summary = results["evaluation_summary"]
        
        print("\n" + "="*60)
        print("BIOMEDICAL RESEARCHER AGENT EVALUATION SUMMARY")
        print("="*60)
        print(f"Total Test Cases: {summary['total_cases']}")
        print(f"Successful: {summary['successful_cases']}")
        print(f"Failed: {summary['failed_cases']}")
        print(f"Success Rate: {summary['success_rate']:.1%}")
        print(f"Average Score: {summary['average_score']:.3f}")
        print(f"Score Range: {summary['min_score']:.3f} - {summary['max_score']:.3f}")
        
        print("\nScores by Domain:")
        for domain, score in summary['scores_by_domain'].items():
            print(f"  {domain}: {score:.3f}")
        
        print("\nScores by Difficulty:")
        for difficulty, score in summary['scores_by_difficulty'].items():
            print(f"  {difficulty}: {score:.3f}")
        
        print("\nIndividual Metric Averages:")
        for metric, score in summary['metric_averages'].items():
            print(f"  {metric}: {score:.3f}")
        
        print("="*60)


# Convenience functions for running evaluations
async def run_quick_evaluation(
    test_case_ids: Optional[List[str]] = None,
    output_dir: str = "evals/outputs/biomedical_researcher"
) -> Dict[str, Any]:
    """Run a quick evaluation on specific test cases."""
    if test_case_ids:
        test_cases = [case for case in BIOMEDICAL_TEST_CASES if case.id in test_case_ids]
    else:
        # Run on a subset for quick testing
        test_cases = BIOMEDICAL_TEST_CASES[:3]
    
    runner = EvaluationRunner(output_dir=output_dir)
    results = await runner.run_evaluation_suite(test_cases)
    runner.print_summary(results)
    
    return results


async def run_full_evaluation(output_dir: str = "evals/outputs/biomedical_researcher") -> Dict[str, Any]:
    """Run the complete evaluation suite."""
    runner = EvaluationRunner(output_dir=output_dir)
    results = await runner.run_evaluation_suite()
    runner.print_summary(results)
    
    return results


if __name__ == "__main__":
    # Example usage
    import asyncio
    
    async def main():
        # Run a quick evaluation
        print("Running quick evaluation...")
        await run_quick_evaluation(test_case_ids=["basic_001", "oncology_002"])
        
        # Uncomment to run full evaluation
        # print("Running full evaluation...")
        # await run_full_evaluation()
    
    asyncio.run(main()) 