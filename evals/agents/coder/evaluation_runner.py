"""
Evaluation runner for the Coder agent.

This module orchestrates the evaluation process by:
1. Running the coder agent on test cases
2. Collecting responses and generated code
3. Evaluating responses using OpenEvals LLM-as-a-judge
4. Generating comprehensive reports and visualizations
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

from evals.agents.coder.evaluators import CoderAgentEvaluator
from evals.agents.coder.test_dataset import ALL_CODER_TEST_CASES, CoderTestCase, get_dataset_summary
from src.agents.agents import coder_agent


class CoderEvaluationRunner:
    """Main evaluation runner for the Coder agent."""
    
    def __init__(
        self,
        output_dir: str = "evals/outputs/coder",
        evaluator_model: str = "openai:o4-mini",
        max_concurrent: int = 1
    ):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.max_concurrent = max_concurrent
        
        # Initialize evaluator
        self.evaluator = CoderAgentEvaluator(model=evaluator_model)
        
        # Setup logging
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging for the evaluation runner."""
        log_file = self.output_dir / f"coder_evaluation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def run_agent_on_test_case(self, test_case: CoderTestCase) -> Dict[str, Any]:
        """Run the coder agent on a single test case."""
        try:
            self.logger.info(f"Running coder agent on test case: {test_case.id}")
            
            # Prepare the state for the coder agent
            # The coder agent expects messages in a specific format
            state = {
                "messages": [
                    {
                        "role": "user",
                        "content": test_case.task_description
                    }
                ]
            }
            
            # If sample data is provided, add it to the context
            if test_case.sample_data:
                state["messages"][0]["content"] += f"\n\nSample data:\n{test_case.sample_data}"
            
            # Run the coder agent
            response = coder_agent.invoke(state)
            
            # Extract the agent's response - combine all message content
            if "messages" in response and response["messages"]:
                full_conversation = ""
                for msg in response["messages"]:
                    if hasattr(msg, 'content') and msg.content:
                        full_conversation += msg.content + "\n\n"
                agent_output = full_conversation.strip()
            else:
                agent_output = str(response)
            
            self.logger.info(f"Coder agent completed test case: {test_case.id}")
            
            return {
                "agent_response": agent_output,
                "full_state": response,
                "task_id": test_case.id,
                "task_type": test_case.task_type,
                "difficulty": test_case.difficulty
            }
            
        except Exception as e:
            self.logger.error(f"Error running coder agent on test case {test_case.id}: {e}")
            self.logger.error(traceback.format_exc())
            return {
                "error": str(e),
                "task_id": test_case.id,
                "task_type": test_case.task_type,
                "difficulty": test_case.difficulty
            }
    
    def evaluate_response(
        self,
        test_case: CoderTestCase,
        agent_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Evaluate an agent response using LLM-as-a-judge."""
        try:
            self.logger.info(f"Evaluating response for test case: {test_case.id}")
            
            # Skip evaluation if there was an error in the agent response
            if "error" in agent_result:
                return {
                    "error": "Agent response contained error",
                    "agent_error": agent_result["error"],
                    "test_case_id": test_case.id
                }
            
            # Run the comprehensive evaluation
            evaluation_result = self.evaluator.evaluate_response(
                task_description=test_case.task_description,
                agent_response=agent_result["agent_response"],
                reference_outputs=test_case.expected_deliverables,
                expected_deliverables=test_case.expected_deliverables
            )
            
            # Extract overall score and evaluations
            overall_score = evaluation_result["overall_score"]
            evaluations = evaluation_result["evaluations"]
            
            # Generate detailed report
            detailed_report = self.evaluator.generate_detailed_report(
                task_description=test_case.task_description,
                agent_response=agent_result["agent_response"],
                evaluations=evaluations,
                overall_score=overall_score
            )
            
            # Compile results
            result = {
                "test_case_id": test_case.id,
                "task_type": test_case.task_type,
                "difficulty": test_case.difficulty,
                "overall_score": overall_score,
                "individual_scores": {
                    metric: {
                        "score": eval_result.get("score", 0.0) if isinstance(eval_result, dict) else eval_result,
                        "comment": eval_result.get("comment", "") if isinstance(eval_result, dict) else ""
                    }
                    for metric, eval_result in evaluations.items()
                },
                "agent_response": agent_result["agent_response"],
                "extracted_code": detailed_report.get("extracted_code", ""),
                "plots_generated": detailed_report.get("plots_generated", []),
                "expected_deliverables": test_case.expected_deliverables,
                "success_criteria": test_case.success_criteria,
                "detailed_report": detailed_report
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
    
    def run_single_evaluation(self, test_case: CoderTestCase) -> Dict[str, Any]:
        """Run evaluation on a single test case."""
        # Run agent
        agent_result = self.run_agent_on_test_case(test_case)
        
        # Evaluate response
        evaluation_result = self.evaluate_response(test_case, agent_result)
        
        return evaluation_result
    
    async def run_evaluation_suite(
        self,
        test_cases: Optional[List[CoderTestCase]] = None,
        max_concurrent: Optional[int] = None
    ) -> Dict[str, Any]:
        """Run the complete evaluation suite."""
        if test_cases is None:
            test_cases = ALL_CODER_TEST_CASES
        
        if max_concurrent is None:
            max_concurrent = self.max_concurrent
        
        self.logger.info(f"Starting coder evaluation suite with {len(test_cases)} test cases")
        
        # Since the coder agent is synchronous, we'll run sequentially for now
        # In the future, this could be made async if the agent supports it
        results = []
        for test_case in test_cases:
            try:
                result = self.run_single_evaluation(test_case)
                results.append(result)
            except Exception as e:
                self.logger.error(f"Failed to evaluate test case {test_case.id}: {e}")
                results.append({
                    "error": str(e),
                    "test_case_id": test_case.id,
                    "task_type": test_case.task_type,
                    "difficulty": test_case.difficulty
                })
        
        # Process results
        successful_results = [r for r in results if "error" not in r]
        failed_results = [r for r in results if "error" in r]
        
        # Generate summary
        summary = self.generate_evaluation_summary(successful_results, failed_results)
        
        # Compile final results
        final_results = {
            "timestamp": datetime.now().isoformat(),
            "summary": summary,
            "successful_evaluations": successful_results,
            "failed_evaluations": failed_results,
            "dataset_info": get_dataset_summary()
        }
        
        # Save results
        self.save_results(final_results)
        
        # Print summary
        self.print_summary(final_results)
        
        self.logger.info("Coder evaluation suite completed")
        return final_results
    
    def generate_evaluation_summary(
        self,
        successful_results: List[Dict[str, Any]],
        failed_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate a summary of evaluation results."""
        if not successful_results:
            return {
                "total_cases": len(successful_results) + len(failed_results),
                "successful_cases": 0,
                "failed_cases": len(failed_results),
                "success_rate": 0.0,
                "average_score": 0.0,
                "message": "No successful evaluations to analyze"
            }
        
        # Calculate overall statistics
        scores = [r["overall_score"] for r in successful_results]
        avg_score = sum(scores) / len(scores)
        
        # Group by task type
        by_task_type = {}
        for result in successful_results:
            task_type = result["task_type"]
            if task_type not in by_task_type:
                by_task_type[task_type] = []
            by_task_type[task_type].append(result["overall_score"])
        
        task_type_averages = {
            task_type: sum(scores) / len(scores)
            for task_type, scores in by_task_type.items()
        }
        
        # Group by difficulty
        by_difficulty = {}
        for result in successful_results:
            difficulty = result["difficulty"]
            if difficulty not in by_difficulty:
                by_difficulty[difficulty] = []
            by_difficulty[difficulty].append(result["overall_score"])
        
        difficulty_averages = {
            difficulty: sum(scores) / len(scores)
            for difficulty, scores in by_difficulty.items()
        }
        
        # Individual metric analysis
        metric_scores = {}
        for result in successful_results:
            for metric, score_info in result["individual_scores"].items():
                if metric not in metric_scores:
                    metric_scores[metric] = []
                metric_scores[metric].append(score_info["score"])
        
        metric_averages = {
            metric: sum(scores) / len(scores)
            for metric, scores in metric_scores.items()
        }
        
        return {
            "total_cases": len(successful_results) + len(failed_results),
            "successful_cases": len(successful_results),
            "failed_cases": len(failed_results),
            "success_rate": len(successful_results) / (len(successful_results) + len(failed_results)),
            "average_score": avg_score,
            "score_distribution": {
                "min": min(scores),
                "max": max(scores),
                "median": sorted(scores)[len(scores)//2]
            },
            "by_task_type": task_type_averages,
            "by_difficulty": difficulty_averages,
            "by_metric": metric_averages
        }
    
    def save_results(self, results: Dict[str, Any]):
        """Save evaluation results to files."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save full results as JSON
        results_file = self.output_dir / f"coder_evaluation_results_{timestamp}.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        # Save summary as a separate file
        summary_file = self.output_dir / f"coder_evaluation_summary_{timestamp}.json"
        with open(summary_file, 'w') as f:
            json.dump(results["summary"], f, indent=2, default=str)
        
        self.logger.info(f"Results saved to {results_file}")
        self.logger.info(f"Summary saved to {summary_file}")
    
    def print_summary(self, results: Dict[str, Any]):
        """Print a formatted summary of the evaluation results."""
        summary = results["summary"]
        
        print("\n" + "="*60)
        print("CODER AGENT EVALUATION SUMMARY")
        print("="*60)
        print(f"Total test cases: {summary['total_cases']}")
        print(f"Successful evaluations: {summary['successful_cases']}")
        print(f"Failed evaluations: {summary['failed_cases']}")
        print(f"Success rate: {summary['success_rate']:.1%}")
        print(f"Average overall score: {summary['average_score']:.2f}")
        
        if "score_distribution" in summary:
            dist = summary["score_distribution"]
            print(f"Score distribution: min={dist['min']:.2f}, median={dist['median']:.2f}, max={dist['max']:.2f}")
        
        print("\nPerformance by Task Type:")
        for task_type, avg_score in summary.get("by_task_type", {}).items():
            print(f"  {task_type}: {avg_score:.2f}")
        
        print("\nPerformance by Difficulty:")
        for difficulty, avg_score in summary.get("by_difficulty", {}).items():
            print(f"  {difficulty}: {avg_score:.2f}")
        
        print("\nPerformance by Metric:")
        for metric, avg_score in summary.get("by_metric", {}).items():
            print(f"  {metric}: {avg_score:.2f}")
        
        print("="*60)


async def run_quick_evaluation(
    test_case_ids: Optional[List[str]] = None,
    output_dir: str = "evals/outputs/coder"
) -> Dict[str, Any]:
    """Run a quick evaluation on a subset of test cases."""
    if test_case_ids is None:
        # Run on first test case from each category
        test_cases = [
            ALL_CODER_TEST_CASES[0],  # First data analysis case
            ALL_CODER_TEST_CASES[2],  # First visualization case  
            ALL_CODER_TEST_CASES[6]   # First debugging case
        ]
    else:
        from evals.agents.coder.test_dataset import get_test_case_by_id
        test_cases = [get_test_case_by_id(tid) for tid in test_case_ids if get_test_case_by_id(tid)]
    
    runner = CoderEvaluationRunner(output_dir=output_dir)
    return await runner.run_evaluation_suite(test_cases)


async def run_full_evaluation(output_dir: str = "evals/outputs/coder") -> Dict[str, Any]:
    """Run the complete evaluation suite on all test cases."""
    runner = CoderEvaluationRunner(output_dir=output_dir)
    return await runner.run_evaluation_suite()


if __name__ == "__main__":
    async def main():
        # Run a quick evaluation on a few test cases
        print("Running quick coder agent evaluation...")
        results = await run_quick_evaluation()
        
        # Optionally run full evaluation
        # print("Running full coder agent evaluation...")
        # results = await run_full_evaluation()
    
    asyncio.run(main()) 