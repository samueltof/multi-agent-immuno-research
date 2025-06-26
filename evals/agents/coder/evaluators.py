"""
Custom evaluators for the Coder agent using OpenEvals.

This module provides specialized evaluators for assessing:
- Code Correctness: Using prebuilt LLM-as-judge for code evaluation
- Code Execution: Validates that generated code executes successfully
- Data Analysis Quality: Evaluates the quality of data analysis and insights
- Visualization Quality: Assesses the quality and appropriateness of plots/visualizations
- Code Style: Evaluates code quality, readability, and best practices
- Task Completion: How well the coder completed the requested task
"""

import re
import json
import logging
from typing import Any, Dict, List, Optional, Union
from pathlib import Path

from openevals.llm import create_llm_as_judge
from openevals.code.llm import create_code_llm_as_judge, CODE_CORRECTNESS_PROMPT
from openevals.types import EvaluatorResult


logger = logging.getLogger(__name__)


# Custom prompts for coder evaluation
CODE_EXECUTION_SUCCESS_PROMPT = """
You are an expert Python developer evaluating whether code executed successfully and produced meaningful results.

Your task is to assess:
- Whether the code ran without errors
- If any plots were generated successfully
- Whether the output is meaningful and complete
- If the execution matches the expected task

Rate the execution success on a scale of 0-1:
- 1.0: Code executed perfectly with meaningful output
- 0.8: Code executed successfully with minor issues
- 0.6: Code executed but with some problems or incomplete output
- 0.4: Code executed partially with significant issues
- 0.2: Code executed but failed to produce expected results
- 0.0: Code failed to execute or produced no meaningful output

<task_description>
{inputs}
</task_description>

<generated_code>
{code}
</generated_code>

<execution_output>
{outputs}
</execution_output>

Provide your evaluation as a score between 0.0 and 1.0, and explain your reasoning.
"""

DATA_ANALYSIS_QUALITY_PROMPT = """
You are an expert data scientist evaluating the quality of data analysis performed by code.

Your task is to assess:
- Appropriateness of analytical methods used
- Quality of statistical analysis and calculations
- Insights extracted from the data
- Handling of data preprocessing and cleaning
- Completeness of the analysis

Rate the data analysis quality on a scale of 0-1:
- 1.0: Excellent analysis with appropriate methods and valuable insights
- 0.8: Good analysis with minor methodological issues
- 0.6: Adequate analysis but missing some key aspects
- 0.4: Basic analysis with significant methodological concerns
- 0.2: Poor analysis with major flaws
- 0.0: No meaningful analysis performed

<task_description>
{inputs}
</task_description>

<generated_code>
{code}
</generated_code>

<analysis_output>
{outputs}
</analysis_output>

<reference_dataset_info>
{reference_outputs}
</reference_dataset_info>

Provide your evaluation as a score between 0.0 and 1.0, and explain your reasoning.
"""

VISUALIZATION_QUALITY_PROMPT = """
You are an expert in data visualization evaluating the quality and appropriateness of generated plots and charts.

Your task is to assess:
- Appropriateness of visualization type for the data
- Quality of plot aesthetics (labels, titles, legends)
- Clarity and readability of the visualization
- Whether the plot effectively communicates insights
- Technical correctness of the visualization code

Rate the visualization quality on a scale of 0-1:
- 1.0: Excellent visualization that effectively communicates insights
- 0.8: Good visualization with minor aesthetic or clarity issues
- 0.6: Adequate visualization but could be improved
- 0.4: Basic visualization with significant issues
- 0.2: Poor visualization that's hard to interpret
- 0.0: No visualization or completely inappropriate plot

<task_description>
{inputs}
</task_description>

<generated_code>
{code}
</generated_code>

<plot_output>
{outputs}
</plot_output>

Provide your evaluation as a score between 0.0 and 1.0, and explain your reasoning.
"""

CODE_STYLE_PROMPT = """
You are an expert Python developer evaluating code style, readability, and best practices.

Your task is to assess:
- Code readability and structure
- Adherence to Python best practices
- Appropriate use of libraries and functions
- Code comments and documentation
- Error handling and robustness

Rate the code style on a scale of 0-1:
- 1.0: Excellent code style following all best practices
- 0.8: Good code style with minor issues
- 0.6: Adequate code style but room for improvement
- 0.4: Basic code style with notable issues
- 0.2: Poor code style with significant problems
- 0.0: Very poor code style, hard to read/maintain

<task_description>
{inputs}
</task_description>

<generated_code>
{code}
</generated_code>

Provide your evaluation as a score between 0.0 and 1.0, and explain your reasoning.
"""

TASK_COMPLETION_PROMPT = """
You are evaluating how well the generated code completed the requested task.

Your task is to assess:
- Whether all requirements were addressed
- Completeness of the solution
- Accuracy in following instructions
- Appropriateness of the approach taken

Rate the task completion on a scale of 0-1:
- 1.0: Task completed perfectly with all requirements met
- 0.8: Task mostly completed with minor gaps
- 0.6: Task adequately completed but missing some aspects
- 0.4: Task partially completed with significant gaps
- 0.2: Task minimally completed with major gaps
- 0.0: Task not completed or completely off-track

<task_description>
{inputs}
</task_description>

<generated_code>
{code}
</generated_code>

<execution_output>
{outputs}
</execution_output>

<expected_deliverables>
{reference_outputs}
</expected_deliverables>

Provide your evaluation as a score between 0.0 and 1.0, and explain your reasoning.
"""


def extract_code_from_output(agent_output: str) -> str:
    """Extract Python code from the agent's output."""
    # Look for code blocks after "Successfully executed:" pattern (primary format)
    execution_matches = re.findall(r'Successfully executed:\n```python\n(.*?)\n```', agent_output, re.DOTALL)
    if execution_matches:
        return '\n\n'.join(execution_matches)
    
    # Look for standalone code blocks in the output
    code_blocks = re.findall(r'```python\n(.*?)\n```', agent_output, re.DOTALL)
    if code_blocks:
        return '\n\n'.join(code_blocks)
    
    # If no code blocks found, return empty string (no code to evaluate)
    return ""


def extract_plots_from_output(agent_output: str) -> List[str]:
    """Extract plot file paths from the agent's output."""
    plot_matches = re.findall(r'PLOT_SAVED: (.+?)(?:\n|$)', agent_output)
    return plot_matches


def create_code_correctness_evaluator(model: str = "openai:o4-mini"):
    """Create an evaluator for code correctness using custom LLM-as-judge."""
    def wrapped_evaluator(*, inputs: str, outputs: str, code: str = "", **kwargs) -> EvaluatorResult:
        # If code is not provided, extract it from outputs
        if not code:
            code = extract_code_from_output(outputs)
        
        evaluator = create_llm_as_judge(
            prompt=CODE_CORRECTNESS_PROMPT,
            model=model,
            choices=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
            feedback_key="code_correctness"
        )
        
        return evaluator(inputs=inputs, outputs=outputs, code=code)
    
    return wrapped_evaluator


def create_code_execution_evaluator(model: str = "openai:o4-mini"):
    """Create an evaluator for successful code execution."""
    def wrapped_evaluator(*, inputs: str, outputs: str, code: str = "", **kwargs) -> EvaluatorResult:
        # If code is not provided, extract it from outputs
        if not code:
            code = extract_code_from_output(outputs)
        
        evaluator = create_llm_as_judge(
            prompt=CODE_EXECUTION_SUCCESS_PROMPT,
            model=model,
            choices=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
            feedback_key="code_execution_success"
        )
        
        return evaluator(inputs=inputs, outputs=outputs, code=code)
    
    return wrapped_evaluator


def create_data_analysis_quality_evaluator(model: str = "openai:o4-mini"):
    """Create an evaluator for data analysis quality."""
    def wrapped_evaluator(*, inputs: str, outputs: str, code: str = "", reference_outputs: str = "", **kwargs) -> EvaluatorResult:
        # If code is not provided, extract it from outputs
        if not code:
            code = extract_code_from_output(outputs)
        
        evaluator = create_llm_as_judge(
            prompt=DATA_ANALYSIS_QUALITY_PROMPT,
            model=model,
            choices=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
            feedback_key="data_analysis_quality"
        )
        
        return evaluator(inputs=inputs, outputs=outputs, code=code, reference_outputs=reference_outputs)
    
    return wrapped_evaluator


def create_visualization_quality_evaluator(model: str = "openai:o4-mini"):
    """Create an evaluator for visualization quality."""
    def wrapped_evaluator(*, inputs: str, outputs: str, code: str = "", **kwargs) -> EvaluatorResult:
        # If code is not provided, extract it from outputs
        if not code:
            code = extract_code_from_output(outputs)
        
        evaluator = create_llm_as_judge(
            prompt=VISUALIZATION_QUALITY_PROMPT,
            model=model,
            choices=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
            feedback_key="visualization_quality"
        )
        
        return evaluator(inputs=inputs, outputs=outputs, code=code)
    
    return wrapped_evaluator


def create_code_style_evaluator(model: str = "openai:o4-mini"):
    """Create an evaluator for code style and best practices."""
    def wrapped_evaluator(*, inputs: str, outputs: str, code: str = "", **kwargs) -> EvaluatorResult:
        # If code is not provided, extract it from outputs
        if not code:
            code = extract_code_from_output(outputs)
        
        evaluator = create_llm_as_judge(
            prompt=CODE_STYLE_PROMPT,
            model=model,
            choices=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
            feedback_key="code_style"
        )
        
        return evaluator(inputs=inputs, outputs=outputs, code=code)
    
    return wrapped_evaluator


def create_task_completion_evaluator(model: str = "openai:o4-mini"):
    """Create an evaluator for task completion."""
    def wrapped_evaluator(*, inputs: str, outputs: str, code: str = "", reference_outputs: str = "", **kwargs) -> EvaluatorResult:
        # If code is not provided, extract it from outputs
        if not code:
            code = extract_code_from_output(outputs)
        
        evaluator = create_llm_as_judge(
            prompt=TASK_COMPLETION_PROMPT,
            model=model,
            choices=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
            feedback_key="task_completion"
        )
        
        return evaluator(inputs=inputs, outputs=outputs, code=code, reference_outputs=reference_outputs)
    
    return wrapped_evaluator


class CoderAgentEvaluator:
    """Comprehensive evaluator for the Coder agent."""
    
    def __init__(self, model: str = "openai:o4-mini"):
        self.model = model
        
        # Initialize all evaluators
        self.code_correctness_evaluator = create_code_correctness_evaluator(model)
        self.code_execution_evaluator = create_code_execution_evaluator(model)
        self.data_analysis_evaluator = create_data_analysis_quality_evaluator(model)
        self.visualization_evaluator = create_visualization_quality_evaluator(model)
        self.code_style_evaluator = create_code_style_evaluator(model)
        self.task_completion_evaluator = create_task_completion_evaluator(model)
    
    def evaluate_response(
        self,
        task_description: str,
        agent_response: str,
        reference_outputs: Optional[str] = None,
        expected_deliverables: Optional[str] = None
    ) -> Dict[str, EvaluatorResult]:
        """
        Evaluate a coder agent response comprehensively.
        
        Args:
            task_description: The original task/prompt given to the coder
            agent_response: The complete response from the coder agent
            reference_outputs: Optional reference information about expected results
            expected_deliverables: Optional description of what should be delivered
        
        Returns:
            Dictionary of evaluation results for each metric
        """
        logger.info("Starting comprehensive evaluation of coder response")
        
        # Extract code from the agent response
        extracted_code = extract_code_from_output(agent_response)
        
        evaluations = {}
        
        try:
            # 1. Code Correctness (using OpenEvals prebuilt)
            logger.info("Evaluating code correctness")
            evaluations["code_correctness"] = self.code_correctness_evaluator(
                inputs=task_description,
                outputs=extracted_code if extracted_code else agent_response
            )
        except Exception as e:
            logger.error(f"Error in code correctness evaluation: {e}")
            evaluations["code_correctness"] = {"score": 0.0, "comment": f"Evaluation error: {e}"}
        
        try:
            # 2. Code Execution Success
            logger.info("Evaluating code execution success")
            evaluations["code_execution"] = self.code_execution_evaluator(
                inputs=task_description,
                outputs=agent_response,
                code=extracted_code
            )
        except Exception as e:
            logger.error(f"Error in code execution evaluation: {e}")
            evaluations["code_execution"] = {"score": 0.0, "comment": f"Evaluation error: {e}"}
        
        try:
            # 3. Data Analysis Quality (if applicable)
            logger.info("Evaluating data analysis quality")
            evaluations["data_analysis"] = self.data_analysis_evaluator(
                inputs=task_description,
                outputs=agent_response,
                code=extracted_code,
                reference_outputs=reference_outputs or ""
            )
        except Exception as e:
            logger.error(f"Error in data analysis evaluation: {e}")
            evaluations["data_analysis"] = {"score": 0.0, "comment": f"Evaluation error: {e}"}
        
        try:
            # 4. Visualization Quality (if plots were created)
            plot_paths = extract_plots_from_output(agent_response)
            if plot_paths or "plt." in extracted_code or "plot" in task_description.lower():
                logger.info("Evaluating visualization quality")
                evaluations["visualization"] = self.visualization_evaluator(
                    inputs=task_description,
                    outputs=agent_response,
                    code=extracted_code
                )
            else:
                evaluations["visualization"] = {"score": 1.0, "comment": "No visualization required for this task"}
        except Exception as e:
            logger.error(f"Error in visualization evaluation: {e}")
            evaluations["visualization"] = {"score": 0.0, "comment": f"Evaluation error: {e}"}
        
        try:
            # 5. Code Style
            logger.info("Evaluating code style")
            evaluations["code_style"] = self.code_style_evaluator(
                inputs=task_description,
                outputs=agent_response,
                code=extracted_code
            )
        except Exception as e:
            logger.error(f"Error in code style evaluation: {e}")
            evaluations["code_style"] = {"score": 0.0, "comment": f"Evaluation error: {e}"}
        
        try:
            # 6. Task Completion
            logger.info("Evaluating task completion")
            evaluations["task_completion"] = self.task_completion_evaluator(
                inputs=task_description,
                outputs=agent_response,
                code=extracted_code,
                reference_outputs=expected_deliverables or reference_outputs or ""
            )
        except Exception as e:
            logger.error(f"Error in task completion evaluation: {e}")
            evaluations["task_completion"] = {"score": 0.0, "comment": f"Evaluation error: {e}"}
        
        logger.info("Comprehensive evaluation completed")
        
        # Calculate overall score
        overall_score = self.calculate_overall_score(evaluations)
        
        # Add overall score to results
        result = {
            "overall_score": overall_score,
            "metric_scores": {k: v.get("score", 0.0) if isinstance(v, dict) else 0.0 for k, v in evaluations.items()},
            "evaluations": evaluations
        }
        
        return result
    
    def calculate_overall_score(self, evaluations: Dict[str, EvaluatorResult]) -> float:
        """
        Calculate an overall score from individual evaluations.
        
        Weights:
        - Task Completion: 30%
        - Code Correctness: 25%
        - Code Execution: 20%
        - Data Analysis: 15%
        - Visualization: 5%
        - Code Style: 5%
        """
        weights = {
            "task_completion": 0.30,
            "code_correctness": 0.25,
            "code_execution": 0.20,
            "data_analysis": 0.15,
            "visualization": 0.05,
            "code_style": 0.05
        }
        
        total_score = 0.0
        total_weight = 0.0
        
        for metric, weight in weights.items():
            if metric in evaluations:
                eval_result = evaluations[metric]
                score = eval_result.get("score", 0.0) if isinstance(eval_result, dict) else 0.0
                total_score += score * weight
                total_weight += weight
        
        # Normalize by actual weights used (in case some evaluations failed)
        return total_score / total_weight if total_weight > 0 else 0.0
    
    def generate_detailed_report(
        self,
        task_description: str,
        agent_response: str,
        evaluations: Dict[str, EvaluatorResult],
        overall_score: float
    ) -> Dict[str, Any]:
        """Generate a detailed evaluation report."""
        
        # Extract key information
        extracted_code = extract_code_from_output(agent_response)
        plot_paths = extract_plots_from_output(agent_response)
        
        return {
            "overall_score": overall_score,
            "task_description": task_description,
            "extracted_code": extracted_code,
            "plots_generated": plot_paths,
            "evaluation_details": evaluations,
            "summary": {
                "code_quality": {
                    "correctness": evaluations.get("code_correctness", {}).get("score", 0.0),
                    "style": evaluations.get("code_style", {}).get("score", 0.0),
                    "execution": evaluations.get("code_execution", {}).get("score", 0.0)
                },
                "analysis_quality": {
                    "data_analysis": evaluations.get("data_analysis", {}).get("score", 0.0),
                    "visualization": evaluations.get("visualization", {}).get("score", 0.0)
                },
                "task_completion": evaluations.get("task_completion", {}).get("score", 0.0)
            }
        }
