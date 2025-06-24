"""
Evaluation runner for the Web Researcher agent.

This module orchestrates the evaluation process by:
1. Running the web researcher agent on test cases
2. Collecting responses and metadata (search results, crawled content)
3. Evaluating responses using LLM-as-a-judge for multiple criteria
4. Generating comprehensive reports with RAG-specific metrics
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

from .evaluators import ResearcherEvaluator
from .test_dataset import RESEARCHER_TEST_CASES, ResearcherTestCase, get_test_dataset_summary
from src.agents.agents import research_agent


class EvaluationRunner:
    """Main evaluation runner for the Web Researcher agent."""
    
    def __init__(
        self,
        output_dir: str = "evals/outputs/researcher",
        evaluator_model: str = "openai:o4-mini",
        agent_config: Optional[Dict[str, Any]] = None
    ):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize evaluator
        self.evaluator = ResearcherEvaluator(model=evaluator_model)
        
        # Agent configuration
        self.agent_config = agent_config or {}
        
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
    
    def run_agent_on_test_case(self, test_case: ResearcherTestCase) -> Dict[str, Any]:
        """Run the web researcher agent on a single test case."""
        try:
            self.logger.info(f"Running agent on test case: {test_case.id}")
            
            # Prepare the state for the research agent
            state = {
                "messages": [{"role": "user", "content": test_case.prompt}],
                "domain": test_case.domain,
                "difficulty": test_case.difficulty,
                "requires_recent_info": test_case.requires_recent_info
            }
            
            # Run the research agent
            result = research_agent.invoke(state)
            
            # Extract information from the result
            messages = result.get("messages", [])
            last_message = messages[-1] if messages else {}
            response_content = last_message.get("content", "") if isinstance(last_message, dict) else str(last_message)
            
            # Try to extract additional metadata if available
            search_info = ""
            crawled_content = ""
            sources_used = []
            
            # Look for tool calls and results in the messages
            for message in messages:
                if isinstance(message, dict):
                    # Check for tool calls
                    tool_calls = message.get("tool_calls", [])
                    for tool_call in tool_calls:
                        if tool_call.get("name") == "tavily_tool":
                            search_info += f"Search: {tool_call.get('args', {})}\n"
                        elif tool_call.get("name") in ["crawl_tool", "crawl_many_tool"]:
                            crawled_content += f"Crawled: {tool_call.get('args', {})}\n"
                    
                    # Check for tool results
                    if "tool_call_id" in message:
                        content = message.get("content", "")
                        if "http" in content:  # Likely contains URLs
                            sources_used.extend([line.strip() for line in content.split("\n") if line.strip().startswith("http")])
            
            # Create structured response
            response = {
                "content": response_content,
                "sources": sources_used,
                "search_info": search_info,
                "crawled_content": crawled_content,
                "query": test_case.prompt,
                "domain": test_case.domain,
                "difficulty": test_case.difficulty,
                "raw_result": result
            }
            
            self.logger.info(f"Agent completed test case: {test_case.id}")
            return response
            
        except Exception as e:
            self.logger.error(f"Error running agent on test case {test_case.id}: {e}")
            self.logger.error(traceback.format_exc())
            return {
                "error": str(e),
                "query": test_case.prompt,
                "domain": test_case.domain,
                "difficulty": test_case.difficulty
            }
    
    def evaluate_response(
        self,
        test_case: ResearcherTestCase,
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
            
            # Prepare test case information for evaluators
            test_case_info = {
                "expected_sources": test_case.expected_sources,
                "search_keywords": test_case.search_keywords,
                "key_concepts": test_case.key_concepts,
                "requires_recent_info": test_case.requires_recent_info
            }
            
            # Run the comprehensive evaluation
            evaluations = self.evaluator.evaluate_response(
                prompt=test_case.prompt,
                response=agent_response,
                test_case_info=test_case_info
            )
            
            # Calculate overall score
            overall_score = self.evaluator.calculate_overall_score(evaluations)
            
            # Compile results
            result = {
                "test_case_id": test_case.id,
                "domain": test_case.domain,
                "difficulty": test_case.difficulty,
                "requires_recent_info": test_case.requires_recent_info,
                "overall_score": overall_score,
                "individual_scores": {
                    metric: {
                        "score": eval_result.get("score", 0.0) if isinstance(eval_result, dict) and "error" not in eval_result else 0.0,
                        "comment": eval_result.get("comment", "") if isinstance(eval_result, dict) and "error" not in eval_result else f"Error: {eval_result.get('error', 'Unknown error')}"
                    }
                    for metric, eval_result in evaluations.items()
                },
                "agent_response": agent_response,
                "expected_concepts": test_case.key_concepts,
                "expected_sources": test_case.expected_sources,
                "expected_keywords": test_case.search_keywords
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
    
    def run_single_evaluation(self, test_case: ResearcherTestCase) -> Dict[str, Any]:
        """Run evaluation on a single test case."""
        # Run agent
        agent_response = self.run_agent_on_test_case(test_case)
        
        # Evaluate response
        evaluation_result = self.evaluate_response(test_case, agent_response)
        
        return evaluation_result
    
    async def run_evaluation_suite(
        self,
        test_cases: Optional[List[ResearcherTestCase]] = None,
        max_concurrent: int = 1
    ) -> Dict[str, Any]:
        """Run the complete evaluation suite."""
        if test_cases is None:
            test_cases = RESEARCHER_TEST_CASES
        
        self.logger.info(f"Starting evaluation suite with {len(test_cases)} test cases")
        
        # For now, run synchronously since the research agent may not be async-safe
        results = []
        for test_case in test_cases:
            try:
                result = self.run_single_evaluation(test_case)
                results.append(result)
            except Exception as e:
                self.logger.error(f"Failed to evaluate test case {test_case.id}: {e}")
                results.append({
                    "error": str(e),
                    "test_case_id": test_case.id
                })
        
        # Separate successful and failed results
        successful_results = [r for r in results if not isinstance(r, Exception) and "error" not in r]
        failed_results = [r for r in results if isinstance(r, Exception) or "error" in r]
        
        # Generate summary
        summary = self.generate_evaluation_summary(successful_results, failed_results)
        
        # Compile final results
        final_results = {
            "summary": summary,
            "successful_evaluations": successful_results,
            "failed_evaluations": failed_results,
            "test_dataset_info": get_test_dataset_summary(),
            "evaluation_config": {
                "evaluator_model": self.evaluator.model,
                "total_test_cases": len(test_cases),
                "max_concurrent": max_concurrent
            },
            "timestamp": datetime.now().isoformat()
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
        """Generate a summary of evaluation results."""
        if not successful_results:
            return {
                "total_cases": len(successful_results) + len(failed_results),
                "successful_cases": 0,
                "failed_cases": len(failed_results),
                "overall_success_rate": 0.0,
                "average_score": 0.0
            }
        
        # Calculate overall statistics
        scores = [r["overall_score"] for r in successful_results if "overall_score" in r]
        average_score = sum(scores) / len(scores) if scores else 0.0
        
        # Calculate scores by domain
        domain_stats = {}
        for result in successful_results:
            domain = result.get("domain", "unknown")
            if domain not in domain_stats:
                domain_stats[domain] = {"scores": [], "count": 0}
            domain_stats[domain]["scores"].append(result.get("overall_score", 0.0))
            domain_stats[domain]["count"] += 1
        
        # Calculate average scores by domain
        for domain, stats in domain_stats.items():
            stats["average_score"] = sum(stats["scores"]) / len(stats["scores"])
            del stats["scores"]  # Remove individual scores to save space
        
        # Calculate scores by difficulty
        difficulty_stats = {}
        for result in successful_results:
            difficulty = result.get("difficulty", "unknown")
            if difficulty not in difficulty_stats:
                difficulty_stats[difficulty] = {"scores": [], "count": 0}
            difficulty_stats[difficulty]["scores"].append(result.get("overall_score", 0.0))
            difficulty_stats[difficulty]["count"] += 1
        
        # Calculate average scores by difficulty
        for difficulty, stats in difficulty_stats.items():
            stats["average_score"] = sum(stats["scores"]) / len(stats["scores"])
            del stats["scores"]  # Remove individual scores to save space
        
        # Calculate individual metric averages
        metric_averages = {}
        for result in successful_results:
            individual_scores = result.get("individual_scores", {})
            for metric, score_info in individual_scores.items():
                if isinstance(score_info, dict) and "score" in score_info:
                    if metric not in metric_averages:
                        metric_averages[metric] = []
                    metric_averages[metric].append(score_info["score"])
        
        # Calculate final metric averages
        for metric, scores in metric_averages.items():
            metric_averages[metric] = sum(scores) / len(scores) if scores else 0.0
        
        # Recent info analysis
        recent_info_cases = [r for r in successful_results if r.get("requires_recent_info", False)]
        recent_info_avg_score = sum(r["overall_score"] for r in recent_info_cases) / len(recent_info_cases) if recent_info_cases else 0.0
        
        return {
            "total_cases": len(successful_results) + len(failed_results),
            "successful_cases": len(successful_results),
            "failed_cases": len(failed_results),
            "overall_success_rate": len(successful_results) / (len(successful_results) + len(failed_results)),
            "average_score": average_score,
            "domain_performance": domain_stats,
            "difficulty_performance": difficulty_stats,
            "metric_averages": metric_averages,
            "recent_info_performance": {
                "cases_requiring_recent_info": len(recent_info_cases),
                "average_score": recent_info_avg_score
            }
        }
    
    def save_results(self, results: Dict[str, Any]):
        """Save evaluation results to files."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save full results as JSON
        results_file = self.output_dir / f"evaluation_results_{timestamp}.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        # Save summary as separate file
        summary_file = self.output_dir / f"evaluation_summary_{timestamp}.json"
        with open(summary_file, 'w') as f:
            json.dump(results["summary"], f, indent=2, default=str)
        
        # Save visualization data
        viz_data = self.prepare_visualization_data(results)
        viz_file = self.output_dir / f"visualization_data_{timestamp}.json"
        with open(viz_file, 'w') as f:
            json.dump(viz_data, f, indent=2, default=str)
        
        self.logger.info(f"Results saved to {results_file}")
        self.logger.info(f"Summary saved to {summary_file}")
        self.logger.info(f"Visualization data saved to {viz_file}")
    
    def prepare_visualization_data(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare data for visualization."""
        successful_results = results.get("successful_evaluations", [])
        
        if not successful_results:
            return {"error": "No successful results to visualize"}
        
        # Prepare data for different chart types
        viz_data = {
            "overall_scores": {
                "test_cases": [r["test_case_id"] for r in successful_results],
                "scores": [r["overall_score"] for r in successful_results],
                "domains": [r.get("domain", "unknown") for r in successful_results],
                "difficulties": [r.get("difficulty", "unknown") for r in successful_results]
            },
            "metric_breakdown": {},
            "domain_comparison": {},
            "difficulty_comparison": {},
            "recent_info_analysis": {}
        }
        
        # Metric breakdown data
        metrics = set()
        for result in successful_results:
            metrics.update(result.get("individual_scores", {}).keys())
        
        for metric in metrics:
            viz_data["metric_breakdown"][metric] = {
                "test_cases": [],
                "scores": []
            }
            for result in successful_results:
                individual_scores = result.get("individual_scores", {})
                if metric in individual_scores:
                    viz_data["metric_breakdown"][metric]["test_cases"].append(result["test_case_id"])
                    viz_data["metric_breakdown"][metric]["scores"].append(individual_scores[metric].get("score", 0.0))
        
        # Domain comparison data
        domains = set(r.get("domain", "unknown") for r in successful_results)
        for domain in domains:
            domain_results = [r for r in successful_results if r.get("domain") == domain]
            viz_data["domain_comparison"][domain] = {
                "count": len(domain_results),
                "average_score": sum(r["overall_score"] for r in domain_results) / len(domain_results),
                "scores": [r["overall_score"] for r in domain_results]
            }
        
        # Difficulty comparison data
        difficulties = set(r.get("difficulty", "unknown") for r in successful_results)
        for difficulty in difficulties:
            difficulty_results = [r for r in successful_results if r.get("difficulty") == difficulty]
            viz_data["difficulty_comparison"][difficulty] = {
                "count": len(difficulty_results),
                "average_score": sum(r["overall_score"] for r in difficulty_results) / len(difficulty_results),
                "scores": [r["overall_score"] for r in difficulty_results]
            }
        
        # Recent info analysis
        recent_info_results = [r for r in successful_results if r.get("requires_recent_info", False)]
        non_recent_results = [r for r in successful_results if not r.get("requires_recent_info", False)]
        
        viz_data["recent_info_analysis"] = {
            "recent_info_required": {
                "count": len(recent_info_results),
                "average_score": sum(r["overall_score"] for r in recent_info_results) / len(recent_info_results) if recent_info_results else 0.0,
                "scores": [r["overall_score"] for r in recent_info_results]
            },
            "no_recent_info": {
                "count": len(non_recent_results),
                "average_score": sum(r["overall_score"] for r in non_recent_results) / len(non_recent_results) if non_recent_results else 0.0,
                "scores": [r["overall_score"] for r in non_recent_results]
            }
        }
        
        return viz_data
    
    def print_summary(self, results: Dict[str, Any]):
        """Print a summary of evaluation results."""
        summary = results.get("summary", {})
        
        print("\n" + "="*80)
        print("WEB RESEARCHER AGENT EVALUATION SUMMARY")
        print("="*80)
        
        print(f"\nOverall Results:")
        print(f"  Total test cases: {summary.get('total_cases', 0)}")
        print(f"  Successful evaluations: {summary.get('successful_cases', 0)}")
        print(f"  Failed evaluations: {summary.get('failed_cases', 0)}")
        print(f"  Success rate: {summary.get('overall_success_rate', 0.0):.1%}")
        print(f"  Average score: {summary.get('average_score', 0.0):.3f}")
        
        # Domain performance
        domain_perf = summary.get("domain_performance", {})
        if domain_perf:
            print(f"\nPerformance by Domain:")
            for domain, stats in domain_perf.items():
                print(f"  {domain}: {stats.get('average_score', 0.0):.3f} (n={stats.get('count', 0)})")
        
        # Difficulty performance  
        difficulty_perf = summary.get("difficulty_performance", {})
        if difficulty_perf:
            print(f"\nPerformance by Difficulty:")
            for difficulty, stats in difficulty_perf.items():
                print(f"  {difficulty}: {stats.get('average_score', 0.0):.3f} (n={stats.get('count', 0)})")
        
        # Metric averages
        metric_avgs = summary.get("metric_averages", {})
        if metric_avgs:
            print(f"\nAverage Scores by Metric:")
            for metric, avg_score in metric_avgs.items():
                print(f"  {metric}: {avg_score:.3f}")
        
        # Recent info performance
        recent_info_perf = summary.get("recent_info_performance", {})
        if recent_info_perf:
            print(f"\nRecent Information Requirements:")
            print(f"  Cases requiring recent info: {recent_info_perf.get('cases_requiring_recent_info', 0)}")
            print(f"  Average score: {recent_info_perf.get('average_score', 0.0):.3f}")
        
        print("\n" + "="*80)


async def run_quick_evaluation(
    test_case_ids: Optional[List[str]] = None,
    output_dir: str = "evals/outputs/researcher"
) -> Dict[str, Any]:
    """Run a quick evaluation on a subset of test cases."""
    if test_case_ids is None:
        # Select a few representative test cases
        test_case_ids = ["basic_001", "tech_001", "health_001", "current_001"]
    
    # Get test cases
    test_cases = []
    for case_id in test_case_ids:
        try:
            from .test_dataset import get_test_case_by_id
            test_cases.append(get_test_case_by_id(case_id))
        except ValueError:
            print(f"Warning: Test case {case_id} not found")
    
    # Run evaluation
    runner = EvaluationRunner(output_dir=output_dir)
    return await runner.run_evaluation_suite(test_cases=test_cases)


async def run_full_evaluation(output_dir: str = "evals/outputs/researcher") -> Dict[str, Any]:
    """Run the complete evaluation suite on all test cases."""
    runner = EvaluationRunner(output_dir=output_dir)
    return await runner.run_evaluation_suite()


if __name__ == "__main__":
    async def main():
        # Run a quick evaluation
        print("Running quick evaluation...")
        results = await run_quick_evaluation()
        print(f"Quick evaluation completed. Results saved to {results.get('output_dir', 'unknown')}")
    
    asyncio.run(main()) 