"""
Evaluation runner for the Data Analyst agent.

This module orchestrates the evaluation process by:
1. Running the data analyst agent on test cases
2. Collecting responses and SQL queries
3. Evaluating responses using OpenEvals LLM-as-a-judge
4. Generating comprehensive reports and visualizations
"""

import asyncio
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import traceback
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from evals.agents.data_analyst.evaluators import DataAnalystAgentEvaluator
from evals.agents.data_analyst.test_dataset import ALL_DATA_ANALYST_TEST_CASES, DataAnalystTestCase, get_dataset_summary
from src.agents.agents import data_analyst_agent


class DataAnalystEvaluationRunner:
    """Main evaluation runner for the Data Analyst agent."""
    
    def __init__(
        self,
        output_dir: str = "evals/outputs/data_analyst",
        evaluator_model: str = "openai:gpt-4o-mini"
    ):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize evaluator
        self.evaluator = DataAnalystAgentEvaluator(model=evaluator_model)
        
        # Setup logging
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging for the evaluation runner."""
        log_file = self.output_dir / f"data_analyst_evaluation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def run_agent_on_test_case(self, test_case: DataAnalystTestCase) -> Dict[str, Any]:
        """Run the data analyst agent on a single test case."""
        try:
            self.logger.info(f"Running data analyst agent on test case: {test_case.id}")
            
            # Prepare the state for the data analyst agent
            state = {
                "messages": [
                    {
                        "role": "user",
                        "content": test_case.natural_language_query
                    }
                ],
                "TEAM_MEMBERS": ["data_analyst"],
                "next": "",
                "full_plan": "",
                "deep_thinking_mode": False,
                "search_before_planning": False,
            }
            
            # Run the data analyst agent
            response = data_analyst_agent(state)
            
            # Extract the final response message
            if "messages" in response and response["messages"]:
                # Get the last message which should be the final response
                last_message = response["messages"][-1]
                if hasattr(last_message, 'content'):
                    agent_output = last_message.content
                elif isinstance(last_message, dict):
                    agent_output = last_message.get("content", str(last_message))
                else:
                    agent_output = str(last_message)
            else:
                agent_output = str(response)
            
            # Extract workflow information from the data team state
            workflow_info = {
                "natural_language_query": response.get("natural_language_query"),
                "generated_sql": response.get("generated_sql"),
                "validation_status": response.get("validation_status"),
                "validation_feedback": response.get("validation_feedback"),
                "execution_result": response.get("execution_result"),
                "error_message": response.get("error_message"),
                "sql_generation_retries": response.get("sql_generation_retries", 0),
                "provided_schema_text": response.get("provided_schema_text"),
                "schema": response.get("schema")
            }
            
            self.logger.info(f"Data analyst agent completed test case: {test_case.id}")
            self.logger.info(f"Generated SQL: {workflow_info['generated_sql']}")
            self.logger.info(f"Validation status: {workflow_info['validation_status']}")
            
            return {
                "agent_response": agent_output,
                "workflow_info": workflow_info,
                "full_state": response,
                "task_id": test_case.id,
                "query_type": test_case.query_type,
                "difficulty": test_case.difficulty
            }
            
        except Exception as e:
            self.logger.error(f"Error running data analyst agent on test case {test_case.id}: {e}")
            self.logger.error(traceback.format_exc())
            return {
                "error": str(e),
                "task_id": test_case.id,
                "query_type": test_case.query_type,
                "difficulty": test_case.difficulty
            }
    
    def evaluate_response(
        self,
        test_case: DataAnalystTestCase,
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
            
            # Run the evaluation with workflow information
            evaluation_result = self.evaluator.evaluate_response(
                natural_language_query=test_case.natural_language_query,
                agent_response=agent_result["agent_response"],
                test_case=test_case,
                workflow_info=agent_result.get("workflow_info", {})
            )
            
            # Extract results
            overall_score = evaluation_result["overall_score"]
            evaluations = evaluation_result["evaluations"]
            
            # Compile results
            result = {
                "test_case_id": test_case.id,
                "query_type": test_case.query_type,
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
                "natural_language_query": test_case.natural_language_query,
                "expected_sql_pattern": test_case.expected_sql_pattern,
                "expected_tables": test_case.expected_tables,
                "expected_columns": test_case.expected_columns,
                "success_criteria": test_case.success_criteria,
                "domain_context": test_case.domain_context,
                # Add workflow information to results
                "generated_sql": evaluation_result.get("generated_sql", ""),
                "execution_results": evaluation_result.get("execution_results", ""),
                "validation_status": evaluation_result.get("validation_status", ""),
                "validation_feedback": evaluation_result.get("validation_feedback", ""),
                "error_message": evaluation_result.get("error_message", ""),
                "sql_retries": evaluation_result.get("sql_retries", 0),
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
    
    def run_single_evaluation(self, test_case: DataAnalystTestCase) -> Dict[str, Any]:
        """Run evaluation on a single test case."""
        # Run agent
        agent_result = self.run_agent_on_test_case(test_case)
        
        # Evaluate response
        evaluation_result = self.evaluate_response(test_case, agent_result)
        
        return evaluation_result
    
    async def run_evaluation_suite(
        self,
        test_cases: Optional[List[DataAnalystTestCase]] = None
    ) -> Dict[str, Any]:
        """Run the complete evaluation suite."""
        if test_cases is None:
            test_cases = ALL_DATA_ANALYST_TEST_CASES
        
        self.logger.info(f"Starting evaluation suite with {len(test_cases)} test cases")
        
        results = []
        for test_case in test_cases:
            result = self.run_single_evaluation(test_case)
            results.append(result)
        
        successful_results = [r for r in results if "error" not in r]
        failed_results = [r for r in results if "error" in r]
        
        summary = self.generate_evaluation_summary(successful_results, failed_results)
        
        final_results = {
            "timestamp": datetime.now().isoformat(),
            "test_cases_count": len(test_cases),
            "successful_evaluations": len(successful_results),
            "failed_evaluations": len(failed_results),
            "summary": summary,
            "detailed_results": successful_results,
            "failures": failed_results,
            "dataset_info": get_dataset_summary()
        }
        
        # Save results
        self.save_results(final_results)
        
        # Print summary
        self.print_summary(final_results)
        
        return final_results
    
    def generate_evaluation_summary(
        self,
        successful_results: List[Dict[str, Any]],
        failed_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate comprehensive summary statistics from evaluation results."""
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
        overall_scores = [r["overall_score"] for r in successful_results]
        avg_overall_score = sum(overall_scores) / len(overall_scores)
        
        # Score distribution
        sorted_scores = sorted(overall_scores)
        score_distribution = {
            "min": min(overall_scores),
            "max": max(overall_scores),
            "median": sorted_scores[len(sorted_scores)//2],
            "std_dev": (sum((x - avg_overall_score) ** 2 for x in overall_scores) / len(overall_scores)) ** 0.5
        }
        
        # Calculate average scores by metric
        metric_scores = {}
        for result in successful_results:
            for metric, score_data in result["individual_scores"].items():
                if metric not in metric_scores:
                    metric_scores[metric] = []
                metric_scores[metric].append(score_data["score"])
        
        avg_metric_scores = {
            metric: sum(scores) / len(scores)
            for metric, scores in metric_scores.items()
        }
        
        # Performance by difficulty
        difficulty_performance = {}
        for result in successful_results:
            difficulty = result["difficulty"]
            if difficulty not in difficulty_performance:
                difficulty_performance[difficulty] = []
            difficulty_performance[difficulty].append(result["overall_score"])
        
        avg_difficulty_performance = {
            diff: sum(scores) / len(scores)
            for diff, scores in difficulty_performance.items()
        }
        
        # Performance by query type
        query_type_performance = {}
        for result in successful_results:
            query_type = result["query_type"]
            if query_type not in query_type_performance:
                query_type_performance[query_type] = []
            query_type_performance[query_type].append(result["overall_score"])
        
        avg_query_type_performance = {
            qtype: sum(scores) / len(scores)
            for qtype, scores in query_type_performance.items()
        }
        
        # SQL execution success rate
        sql_execution_success = sum(1 for r in successful_results if r.get("validation_status") == "valid")
        sql_success_rate = sql_execution_success / len(successful_results) if successful_results else 0
        
        # Workflow completeness analysis
        workflow_scores = metric_scores.get("workflow_completeness", [])
        perfect_workflows = sum(1 for score in workflow_scores if score >= 0.95)
        
        return {
            "total_cases": len(successful_results) + len(failed_results),
            "successful_cases": len(successful_results),
            "failed_cases": len(failed_results),
            "success_rate": len(successful_results) / (len(successful_results) + len(failed_results)),
            "average_score": avg_overall_score,
            "score_distribution": score_distribution,
            "by_metric": avg_metric_scores,
            "by_difficulty": avg_difficulty_performance,
            "by_query_type": avg_query_type_performance,
            "sql_execution_success_rate": sql_success_rate,
            "perfect_workflows": perfect_workflows,
            "sql_generation_retries": sum(r.get("sql_retries", 0) for r in successful_results),
            "dataset_coverage": {
                "unique_difficulties": list(avg_difficulty_performance.keys()),
                "unique_query_types": list(avg_query_type_performance.keys()),
                "total_test_categories": len(set(r["query_type"] for r in successful_results))
            }
        }
    
    def save_results(self, results: Dict[str, Any]):
        """Save evaluation results to JSON files."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save full results as JSON
        results_file = self.output_dir / f"data_analyst_evaluation_results_{timestamp}.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        # Save summary as a separate file
        summary_file = self.output_dir / f"data_analyst_evaluation_summary_{timestamp}.json"
        with open(summary_file, 'w') as f:
            json.dump(results["summary"], f, indent=2, default=str)
        
        self.logger.info(f"Full results saved to {results_file}")
        self.logger.info(f"Summary saved to {summary_file}")
    
    def print_summary(self, results: Dict[str, Any]):
        """Print comprehensive evaluation summary to console."""
        summary = results["summary"]
        
        print("\n" + "="*70)
        print("DATA ANALYST AGENT EVALUATION SUMMARY")
        print("="*70)
        
        # Basic statistics
        print(f"Total test cases: {summary['total_cases']}")
        print(f"Successful evaluations: {summary['successful_cases']}")
        print(f"Failed evaluations: {summary['failed_cases']}")
        print(f"Success rate: {summary['success_rate']:.1%}")
        print(f"Average overall score: {summary['average_score']:.3f}")
        
        # Score distribution
        if "score_distribution" in summary:
            dist = summary["score_distribution"]
            print(f"Score distribution: min={dist['min']:.3f}, median={dist['median']:.3f}, max={dist['max']:.3f}")
            print(f"Standard deviation: {dist['std_dev']:.3f}")
        
        # SQL-specific metrics
        print(f"\nSQL Generation & Execution:")
        print(f"  SQL execution success rate: {summary.get('sql_execution_success_rate', 0):.1%}")
        print(f"  Perfect workflows (≥95%): {summary.get('perfect_workflows', 0)}")
        print(f"  Total SQL generation retries: {summary.get('sql_generation_retries', 0)}")
        
        # Performance by metric
        print(f"\nPerformance by Evaluation Metric:")
        for metric, avg_score in summary.get("by_metric", {}).items():
            metric_display = metric.replace('_', ' ').title()
            print(f"  {metric_display}: {avg_score:.3f}")
        
        # Performance by difficulty
        print(f"\nPerformance by Difficulty Level:")
        for difficulty, avg_score in summary.get("by_difficulty", {}).items():
            print(f"  {difficulty.capitalize()}: {avg_score:.3f}")
        
        # Performance by query type
        print(f"\nPerformance by Query Type:")
        for query_type, avg_score in summary.get("by_query_type", {}).items():
            query_display = query_type.replace('_', ' ').title()
            print(f"  {query_display}: {avg_score:.3f}")
        
        # Dataset coverage
        if "dataset_coverage" in summary:
            coverage = summary["dataset_coverage"]
            print(f"\nDataset Coverage:")
            print(f"  Difficulty levels tested: {', '.join(coverage['unique_difficulties'])}")
            print(f"  Query types tested: {', '.join(coverage['unique_query_types'])}")
            print(f"  Total test categories: {coverage['total_test_categories']}")
        
        print("="*70)


async def run_quick_evaluation(
    test_case_ids: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Run a quick evaluation on selected test cases."""
    runner = DataAnalystEvaluationRunner()
    
    if test_case_ids:
        test_cases = [tc for tc in ALL_DATA_ANALYST_TEST_CASES if tc.id in test_case_ids]
    else:
        # Run first 3 test cases by default
        test_cases = ALL_DATA_ANALYST_TEST_CASES[:3]
    
    return await runner.run_evaluation_suite(test_cases)


if __name__ == "__main__":
    async def main():
        # Run a quick evaluation on a few test cases
        print("Running quick evaluation...")
        results = await run_quick_evaluation(["simple_001", "join_001"])
        print("Quick evaluation completed!")
    
    asyncio.run(main()) 