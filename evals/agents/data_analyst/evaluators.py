"""
Custom evaluators for the Data Analyst agent using OpenEvals.

This module provides specialized evaluators for assessing:
- SQL Query Correctness: Validates generated SQL against expected patterns
- Schema Understanding: Evaluates proper use of database schema
- Query Execution Success: Validates that queries execute and return meaningful results
- Result Interpretation: Assesses quality of data analysis and insights
- Domain Knowledge: Evaluates immunological domain understanding
"""

import re
import json
import logging
from typing import Any, Dict, List, Optional, Union
from pathlib import Path

from openevals.llm import create_llm_as_judge
from openevals.types import EvaluatorResult


logger = logging.getLogger(__name__)


# Custom prompts for data analyst evaluation
SQL_CORRECTNESS_PROMPT = """
You are an expert SQL developer evaluating the correctness of SQL queries.

Rate the SQL correctness on a scale of 0-1:
- 1.0: Perfect SQL query that fully addresses the request
- 0.8: Good SQL with minor issues
- 0.6: Adequate SQL but missing some aspects
- 0.4: Basic SQL with significant issues
- 0.2: Poor SQL with major problems
- 0.0: No SQL generated or completely incorrect

**Evaluation Context:**
- For data retrieval questions: SQL should correctly query the data to answer the question
- For schema exploration questions: SQL should appropriately explore database structure (e.g., DESCRIBE, PRAGMA table_info, SELECT column_name)
- Consider SQLite-specific syntax and functions
- Evaluate query efficiency and best practices

<natural_language_request>
{inputs}
</natural_language_request>

<generated_response>
{outputs}
</generated_response>

<generated_sql>
{generated_sql}
</generated_sql>

<validation_status>
{validation_status}
</validation_status>

<validation_feedback>
{validation_feedback}
</validation_feedback>

<expected_sql_pattern>
{expected_sql_pattern}
</expected_sql_pattern>

**Evaluation Guidelines:**
- If no SQL was generated but the question requires SQL, score should be low (0.0-0.2)
- If SQL was generated but inappropriate for the question type, score should be low (0.2-0.4)
- If SQL is syntactically correct but logically flawed, score should be medium (0.4-0.6)
- If SQL is correct but could be optimized, score should be good (0.6-0.8)
- If SQL perfectly addresses the request with good practices, score should be perfect (0.8-1.0)

**Schema Query Examples:**
- "What columns are in table X?" → PRAGMA table_info(X) or DESCRIBE X
- "Show me the structure of table X" → PRAGMA table_info(X)
- "What tables are available?" → SELECT name FROM sqlite_master WHERE type='table'

Provide your evaluation as a score between 0.0 and 1.0, and explain your reasoning.
"""

SCHEMA_UNDERSTANDING_PROMPT = """
You are an expert database analyst evaluating how well a data analyst understands and uses the database schema.

Your task is to assess:
- Whether the correct tables are referenced
- If proper column names are used
- Whether foreign key relationships are handled correctly
- If the response demonstrates understanding of table structures
- Whether the approach is appropriate for the database design
- For schema exploration questions, whether the appropriate method was used (direct schema reference vs SQL queries)

Rate the schema understanding on a scale of 0-1:
- 1.0: Perfect understanding and use of database schema with appropriate method
- 0.8: Good schema usage with minor issues
- 0.6: Adequate schema understanding but some mistakes
- 0.4: Basic schema usage with notable errors
- 0.2: Poor schema understanding with significant mistakes
- 0.0: No evidence of schema understanding

**Important Context:**
- Some schema questions (like "What are the column names in table X?") may legitimately require SQL queries (e.g., DESCRIBE, PRAGMA table_info, SELECT * LIMIT 0)
- Other schema questions can be answered directly from provided schema information
- The evaluation should consider whether the chosen approach (SQL vs direct schema reference) is appropriate for the question type

<natural_language_request>
{inputs}
</natural_language_request>

<generated_response>
{outputs}
</generated_response>

<database_schema_context>
VDJdb Augmented Database Schema:
- epitopes: epitope_id, sequence, length, ic50, source_protein, species
- mhc_alleles: allele_id, allele_name, locus, class, resolution
- donors: donor_id, species, age, sex, health_status
- samples: sample_id, donor_id, tissue, collection_date
- publications: pub_id, reference_id, title, journal, pub_date, authors
- complexes: complex_id, epitope_id, mhc_a_id, mhc_b_id, sample_id, pub_id, method, meta
- chains: chain_id, complex_id, gene, cdr3, v_segm, j_segm, species, vdjdb_score
- assays: assay_id, complex_id, assay_type, lab, date_run
</database_schema_context>

<expected_tables>
{expected_tables}
</expected_tables>

<expected_columns>
{expected_columns}
</expected_columns>

<generated_sql>
{generated_sql}
</generated_sql>

**Evaluation Guidelines:**
- If a SQL query was generated for a schema question, check if it's appropriate (e.g., DESCRIBE table, PRAGMA table_info(table), SELECT column_name FROM table LIMIT 0)
- If no SQL was generated, check if the schema information was correctly extracted and presented
- Consider whether the response demonstrates understanding of table relationships and structure
- Evaluate the accuracy of table and column references

Provide your evaluation as a score between 0.0 and 1.0, and explain your reasoning.
"""

QUERY_EXECUTION_PROMPT = """
You are an expert data analyst evaluating whether a database query executed successfully and produced meaningful results.

Your task is to assess:
- Whether the query executed without errors (if SQL was generated)
- If the results are meaningful and complete
- Whether the output addresses the original request
- If the data returned is appropriate for the query
- Whether any error handling was done properly
- For schema questions, whether the approach taken was appropriate

Rate the query execution success on a scale of 0-1:
- 1.0: Query executed perfectly with meaningful, complete results OR appropriate non-SQL response for schema questions
- 0.8: Query executed successfully with minor issues
- 0.6: Query executed but with some problems or incomplete results
- 0.4: Query executed partially with significant issues
- 0.2: Query executed but failed to produce expected results
- 0.0: Query failed to execute or produced no meaningful output

**Evaluation Context:**
- For data queries: Expect SQL execution with results
- For schema questions: May have SQL execution OR direct schema information presentation
- Consider whether the response method (SQL vs direct answer) is appropriate for the question type

<natural_language_request>
{inputs}
</natural_language_request>

<generated_response>
{outputs}
</generated_response>

<generated_sql>
{generated_sql}
</generated_sql>

<execution_results>
{execution_results}
</execution_results>

**Evaluation Guidelines:**
- If the question requires data retrieval and no SQL was executed, score should be low (0.0-0.2)
- If the question is about schema and can be answered without SQL execution, consider if the response is complete and accurate
- If SQL was generated but not executed when it should have been, score should be low (0.2-0.4)
- If execution failed due to SQL errors, score should be low (0.0-0.4)
- If execution succeeded but results are incomplete or incorrect, score should be medium (0.4-0.6)
- If execution succeeded with good results, score should be high (0.6-1.0)

Provide your evaluation as a score between 0.0 and 1.0, and explain your reasoning.
"""

DATA_PRESENTATION_PROMPT = """
You are an expert data analyst evaluating the quality of data presentation and formatting.

Your task is to assess:
- Whether the results are clearly presented and formatted
- If the data is organized in a readable manner
- Whether the output addresses the original request
- If the presentation is professional and clear
- Whether appropriate formatting is used (tables, headers, etc.)

Note: Do NOT evaluate interpretation or insights - only focus on data presentation quality.

Rate the data presentation quality on a scale of 0-1:
- 1.0: Excellent presentation with clear formatting and organization
- 0.8: Good presentation with minor formatting issues
- 0.6: Adequate presentation but could be clearer
- 0.4: Basic presentation with formatting problems
- 0.2: Poor presentation with significant issues
- 0.0: No clear data presentation

<natural_language_request>
{inputs}
</natural_language_request>

<generated_response>
{outputs}
</generated_response>

<generated_sql>
{generated_sql}
</generated_sql>

<execution_results>
{execution_results}
</execution_results>

Provide your evaluation as a score between 0.0 and 1.0, and explain your reasoning.
"""

# Domain knowledge evaluation removed - data analyst agent focuses on data retrieval and presentation,
# not domain interpretation. Domain knowledge should come from other specialized agents.

WORKFLOW_COMPLETENESS_PROMPT = """
You are evaluating the completeness of a data analysis workflow.

Your task is to assess:
- Whether all steps of the analysis were completed
- If the workflow follows logical progression
- Whether intermediate steps are properly handled
- If error recovery and validation are included
- Whether the final output is comprehensive

Rate the workflow completeness on a scale of 0-1:
- 1.0: Complete workflow with all necessary steps
- 0.8: Mostly complete workflow with minor gaps
- 0.6: Adequate workflow but missing some steps
- 0.4: Basic workflow with significant gaps
- 0.2: Incomplete workflow with major issues
- 0.0: No coherent workflow evident

<natural_language_request>
{inputs}
</natural_language_request>

<generated_response>
{outputs}
</generated_response>

<generated_sql>
{generated_sql}
</generated_sql>

<validation_status>
{validation_status}
</validation_status>

<sql_retries>
{sql_retries}
</sql_retries>

<error_message>
{error_message}
</error_message>

<expected_workflow_steps>
1. Schema understanding/retrieval
2. SQL query generation
3. Query validation
4. Query execution
5. Result interpretation and presentation
</expected_workflow_steps>

Provide your evaluation as a score between 0.0 and 1.0, and explain your reasoning.
"""


def extract_sql_from_output(agent_output: str) -> str:
    """Extract SQL query from the agent's output."""
    # First try to find SQL in code blocks
    sql_match = re.search(r"```sql\s*(.*?)\s*```", agent_output, re.DOTALL | re.IGNORECASE)
    if sql_match:
        return sql_match.group(1).strip()
    
    # Try to find SQL in generic code blocks
    code_match = re.search(r"```\s*(.*?)\s*```", agent_output, re.DOTALL)
    if code_match:
        potential_sql = code_match.group(1).strip()
        if any(keyword.upper() in potential_sql.upper() for keyword in ["SELECT", "INSERT", "UPDATE", "DELETE", "WITH", "DESCRIBE", "SHOW", "PRAGMA"]):
            return potential_sql
    
    # Look for SQL keywords at the start of lines (for plain SQL output)
    sql_keywords = ["SELECT ", "INSERT ", "UPDATE ", "DELETE ", "WITH ", "DESCRIBE ", "SHOW ", "PRAGMA "]
    lines = agent_output.split('\n')
    
    # Try to find a line that starts with SQL keywords
    for line in lines:
        line_stripped = line.strip()
        line_upper = line_stripped.upper()
        if any(line_upper.startswith(keyword.upper()) for keyword in sql_keywords):
            # Check if this looks like a complete SQL statement
            if line_stripped.endswith(';') or any(keyword in line_upper for keyword in ['FROM ', 'WHERE ', 'GROUP BY', 'ORDER BY', 'LIMIT ']):
                return line_stripped
    
    # If no single line matches, try to find multi-line SQL
    sql_start_idx = -1
    for i, line in enumerate(lines):
        line_stripped = line.strip()
        line_upper = line_stripped.upper()
        if any(line_upper.startswith(keyword.upper()) for keyword in sql_keywords):
            sql_start_idx = i
            break
    
    if sql_start_idx >= 0:
        # Collect lines until we find a logical end
        sql_lines = []
        for i in range(sql_start_idx, len(lines)):
            line = lines[i].strip()
            if not line:
                # Empty line might indicate end of SQL
                if sql_lines:
                    break
                continue
            
            sql_lines.append(line)
            
            # Check if this line ends the SQL statement
            if line.endswith(';'):
                break
            
            # Check if we've hit a non-SQL line
            if not any(keyword in line.upper() for keyword in ['SELECT', 'FROM', 'WHERE', 'JOIN', 'GROUP', 'ORDER', 'HAVING', 'LIMIT', 'UNION', 'INSERT', 'UPDATE', 'DELETE', 'WITH', 'DESCRIBE', 'SHOW', 'PRAGMA', 'AND', 'OR', 'ON', 'AS', 'BY', 'ASC', 'DESC']):
                # This might be explanatory text, check if previous lines form complete SQL
                if len(sql_lines) > 1:
                    sql_lines.pop()  # Remove the non-SQL line
                    break
        
        if sql_lines:
            return ' '.join(sql_lines)
    
    return ""


def extract_execution_results(agent_output: str) -> str:
    """Extract execution results from the agent's output."""
    # Look for result patterns
    result_patterns = [
        r"Here are the results.*?:\s*(.*?)(?=\n\n|\Z)",
        r"Results:\s*(.*?)(?=\n\n|\Z)",
        r"Query result:\s*(.*?)(?=\n\n|\Z)",
        r"The query returned:\s*(.*?)(?=\n\n|\Z)"
    ]
    
    for pattern in result_patterns:
        match = re.search(pattern, agent_output, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
    
    # Fallback: look for any structured data (tables, JSON, etc.)
    lines = agent_output.split('\n')
    result_lines = []
    in_result_section = False
    
    for line in lines:
        if any(keyword in line.lower() for keyword in ['result', 'output', 'data', 'rows']):
            in_result_section = True
            continue
        
        if in_result_section and (line.strip().startswith('|') or line.strip().startswith('{')):
            result_lines.append(line)
        elif in_result_section and not line.strip():
            break
    
    return '\n'.join(result_lines) if result_lines else ""


def create_sql_correctness_evaluator(model: str = "openai:gpt-4o-mini"):
    """Create SQL correctness evaluator."""
    llm_judge = create_llm_as_judge(model=model, prompt=SQL_CORRECTNESS_PROMPT)
    
    def wrapped_evaluator(*, inputs: str, outputs: str, expected_sql_pattern: str = "", 
                         generated_sql: str = "", validation_status: str = None, 
                         validation_feedback: str = "", **kwargs) -> EvaluatorResult:
        # Use workflow-provided SQL if available, otherwise extract from text
        sql_to_evaluate = generated_sql if generated_sql else extract_sql_from_output(outputs)
        
        return llm_judge(
            inputs=inputs,
            outputs=outputs,
            generated_sql=sql_to_evaluate or "",
            expected_sql_pattern=expected_sql_pattern or "No specific pattern expected",
            validation_status=validation_status or "unknown",
            validation_feedback=validation_feedback or ""
        )
    
    return wrapped_evaluator


def create_schema_understanding_evaluator(model: str = "openai:gpt-4o-mini"):
    """Create schema understanding evaluator."""
    llm_judge = create_llm_as_judge(model=model, prompt=SCHEMA_UNDERSTANDING_PROMPT)
    
    def wrapped_evaluator(*, inputs: str, outputs: str, expected_tables: List[str] = None, 
                         expected_columns: List[str] = None, generated_sql: str = "", **kwargs) -> EvaluatorResult:
        # Use workflow-provided SQL if available, otherwise extract from text
        sql_to_evaluate = generated_sql if generated_sql else extract_sql_from_output(outputs)
        
        return llm_judge(
            inputs=inputs,
            outputs=outputs,
            expected_tables=", ".join(expected_tables) if expected_tables else "No specific tables expected",
            expected_columns=", ".join(expected_columns) if expected_columns else "No specific columns expected",
            generated_sql=sql_to_evaluate or "No SQL generated"
        )
    
    return wrapped_evaluator


def create_query_execution_evaluator(model: str = "openai:gpt-4o-mini"):
    """Create query execution evaluator."""
    llm_judge = create_llm_as_judge(model=model, prompt=QUERY_EXECUTION_PROMPT)
    
    def wrapped_evaluator(*, inputs: str, outputs: str, execution_results: str = "", 
                         validation_status: str = None, error_message: str = "", generated_sql: str = "", **kwargs) -> EvaluatorResult:
        # Use workflow-provided execution results if available, otherwise extract from text
        results_to_evaluate = execution_results if execution_results else extract_execution_results(outputs)
        sql_to_evaluate = generated_sql if generated_sql else extract_sql_from_output(outputs)
        
        return llm_judge(
            inputs=inputs,
            outputs=outputs,
            generated_sql=sql_to_evaluate or "",
            execution_results=results_to_evaluate or "No execution results available"
        )
    
    return wrapped_evaluator


def create_data_presentation_evaluator(model: str = "openai:gpt-4o-mini"):
    """Create data presentation evaluator."""
    llm_judge = create_llm_as_judge(model=model, prompt=DATA_PRESENTATION_PROMPT)
    
    def wrapped_evaluator(*, inputs: str, outputs: str, execution_results: str = "", generated_sql: str = "", **kwargs) -> EvaluatorResult:
        # Use workflow-provided execution results if available, otherwise extract from text
        results_to_evaluate = execution_results if execution_results else extract_execution_results(outputs)
        sql_to_evaluate = generated_sql if generated_sql else extract_sql_from_output(outputs)
        
        return llm_judge(
            inputs=inputs,
            outputs=outputs,
            generated_sql=sql_to_evaluate or "",
            execution_results=results_to_evaluate or "No execution results available"
        )
    
    return wrapped_evaluator


# Domain knowledge evaluator removed - not needed for data analyst agent


def create_workflow_completeness_evaluator(model: str = "openai:gpt-4o-mini"):
    """Create workflow completeness evaluator."""
    llm_judge = create_llm_as_judge(model=model, prompt=WORKFLOW_COMPLETENESS_PROMPT)
    
    def wrapped_evaluator(*, inputs: str, outputs: str, validation_status: str = None,
                         sql_retries: int = 0, error_message: str = "", generated_sql: str = "", **kwargs) -> EvaluatorResult:
        # Use workflow-provided SQL if available, otherwise extract from text
        sql_to_evaluate = generated_sql if generated_sql else extract_sql_from_output(outputs)
        
        # Ensure all parameters are strings to avoid KeyError in prompt formatting
        return llm_judge(
            inputs=inputs,
            outputs=outputs,
            generated_sql=sql_to_evaluate or "",
            validation_status=validation_status or "unknown",
            sql_retries=str(sql_retries),
            error_message=error_message or "No errors encountered"
        )
    
    return wrapped_evaluator


class DataAnalystAgentEvaluator:
    """Comprehensive evaluator for the Data Analyst agent."""
    
    def __init__(self, model: str = "openai:gpt-4o-mini"):
        self.model = model
        self.evaluators = {
            "sql_correctness": create_sql_correctness_evaluator(model),
            "schema_understanding": create_schema_understanding_evaluator(model),
            "query_execution": create_query_execution_evaluator(model),
            "data_presentation": create_data_presentation_evaluator(model),
            "workflow_completeness": create_workflow_completeness_evaluator(model),
        }
    
    def evaluate_response(
        self,
        natural_language_query: str,
        agent_response: str,
        test_case: Any = None,
        workflow_info: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Evaluate a data analyst response comprehensively.
        
        Args:
            natural_language_query: The original natural language query
            agent_response: The agent's response
            test_case: The test case object with expected values
            workflow_info: Dictionary containing workflow state information
            
        Returns:
            Dictionary containing evaluation results and overall score
        """
        evaluations = {}
        
        # Extract SQL and results - prioritize workflow info over text parsing
        if workflow_info:
            generated_sql = workflow_info.get("generated_sql", "")
            execution_results = workflow_info.get("execution_result", "")
            validation_status = workflow_info.get("validation_status")
            validation_feedback = workflow_info.get("validation_feedback", "")
            error_message = workflow_info.get("error_message", "")
            sql_retries = workflow_info.get("sql_generation_retries", 0)
        else:
            # Fallback to text extraction
            generated_sql = extract_sql_from_output(agent_response)
            execution_results = extract_execution_results(agent_response)
            validation_status = None
            validation_feedback = ""
            error_message = ""
            sql_retries = 0
        
        # Determine if this is a schema question
        is_schema_question = (test_case and hasattr(test_case, 'query_type') and 
                             test_case.query_type == "schema")
        
        # Prepare evaluation parameters with workflow information
        # Ensure all values are strings to avoid KeyError in prompt formatting
        eval_params = {
            "inputs": natural_language_query,
            "outputs": agent_response,
            "generated_sql": generated_sql or "",
            "execution_results": execution_results or "",
            "validation_status": validation_status or "unknown",
            "validation_feedback": validation_feedback or "",
            "error_message": error_message or "",
            "sql_retries": sql_retries or 0,
        }
        
        if test_case:
            eval_params.update({
                "expected_sql_pattern": test_case.expected_sql_pattern or "",
                "expected_tables": test_case.expected_tables or [],
                "expected_columns": test_case.expected_columns or [],
                "domain_context": test_case.domain_context or "",
            })
        
        # Run evaluations - skip SQL correctness for schema questions
        for metric_name, evaluator in self.evaluators.items():
            # Skip SQL correctness evaluation for schema questions
            if metric_name == "sql_correctness" and is_schema_question:
                logger.info(f"Skipping {metric_name} evaluation for schema question")
                continue
                
            try:
                result = evaluator(**eval_params)
                evaluations[metric_name] = result
                logger.info(f"Evaluation {metric_name}: {result.get('score', 0.0):.2f}")
            except Exception as e:
                logger.error(f"Error in {metric_name} evaluation: {e}")
                evaluations[metric_name] = EvaluatorResult(score=0.0, comment=f"Evaluation failed: {str(e)}")
        
        # Calculate overall score
        overall_score = self.calculate_overall_score(evaluations, is_schema_question)
        
        return {
            "evaluations": evaluations,
            "overall_score": overall_score,
            "generated_sql": generated_sql,
            "execution_results": execution_results,
            "validation_status": validation_status,
            "validation_feedback": validation_feedback,
            "error_message": error_message,
            "sql_retries": sql_retries,
            "agent_response": agent_response,
            "is_schema_question": is_schema_question
        }
    
    def calculate_overall_score(self, evaluations: Dict[str, EvaluatorResult], is_schema_question: bool = False) -> float:
        """Calculate weighted overall score."""
        if is_schema_question:
            # For schema questions, redistribute SQL correctness weight to other metrics
            weights = {
                "schema_understanding": 0.40,     # Increased: Most important for schema questions
                "query_execution": 0.25,          # Execution (or appropriate non-execution)
                "data_presentation": 0.20,        # Clear schema presentation
                "workflow_completeness": 0.15,    # Complete workflow execution
                # sql_correctness: 0.0 - Not applicable for schema questions
            }
        else:
            # Standard weights for data queries
            weights = {
                "sql_correctness": 0.30,          # Core responsibility
                "schema_understanding": 0.25,     # Critical for correct queries
                "query_execution": 0.25,          # Must execute correctly
                "data_presentation": 0.10,        # Clear data presentation
                "workflow_completeness": 0.10,    # Complete workflow execution
            }
        
        weighted_sum = 0.0
        total_weight = 0.0
        
        for metric, weight in weights.items():
            if metric in evaluations:
                score = evaluations[metric].get("score", 0.0) if isinstance(evaluations[metric], dict) else evaluations[metric]
                weighted_sum += score * weight
                total_weight += weight
        
        return weighted_sum / total_weight if total_weight > 0 else 0.0
    
    def generate_detailed_report(
        self,
        natural_language_query: str,
        agent_response: str,
        evaluations: Dict[str, EvaluatorResult],
        overall_score: float,
        test_case: Any = None
    ) -> Dict[str, Any]:
        """Generate a detailed evaluation report."""
        
        generated_sql = extract_sql_from_output(agent_response)
        execution_results = extract_execution_results(agent_response)
        
        # Determine if this is a schema question
        is_schema_question = (test_case and hasattr(test_case, 'query_type') and 
                             test_case.query_type == "schema")
        
        report = {
            "query": natural_language_query,
            "overall_score": overall_score,
            "generated_sql": generated_sql,
            "execution_results": execution_results,
            "evaluation_details": {},
            "success_criteria_met": [],
            "recommendations": [],
            "is_schema_question": is_schema_question
        }
        
        # Add evaluation details
        for metric, result in evaluations.items():
            if isinstance(result, dict):
                report["evaluation_details"][metric] = {
                    "score": result.get("score", 0.0),
                    "comment": result.get("comment", ""),
                }
            else:
                report["evaluation_details"][metric] = {
                    "score": result,
                    "comment": "No detailed feedback available"
                }
        
        # Check success criteria if test case provided
        if test_case and hasattr(test_case, 'success_criteria'):
            for criterion in test_case.success_criteria:
                # Simple heuristic check - can be enhanced
                if any(keyword.lower() in agent_response.lower() 
                       for keyword in criterion.split() if len(keyword) > 3):
                    report["success_criteria_met"].append(criterion)
        
        # Generate recommendations based on scores and question type
        if is_schema_question:
            # Schema-specific recommendations
            if report["evaluation_details"].get("schema_understanding", {}).get("score", 0) < 0.7:
                report["recommendations"].append("Improve understanding and presentation of database schema structure")
            
            if report["evaluation_details"].get("data_presentation", {}).get("score", 0) < 0.7:
                report["recommendations"].append("Improve formatting and clarity of schema information presentation")
            
            if report["evaluation_details"].get("query_execution", {}).get("score", 0) < 0.7:
                report["recommendations"].append("Better handle schema exploration approach (SQL vs direct schema reference)")
            
            if report["evaluation_details"].get("workflow_completeness", {}).get("score", 0) < 0.7:
                report["recommendations"].append("Ensure complete schema exploration workflow")
        else:
            # Data query recommendations
            if report["evaluation_details"].get("sql_correctness", {}).get("score", 0) < 0.7:
                report["recommendations"].append("Improve SQL query correctness and syntax")
            
            if report["evaluation_details"].get("schema_understanding", {}).get("score", 0) < 0.7:
                report["recommendations"].append("Better understand and utilize database schema")
            
            if report["evaluation_details"].get("query_execution", {}).get("score", 0) < 0.7:
                report["recommendations"].append("Improve query execution and error handling")
            
            if report["evaluation_details"].get("data_presentation", {}).get("score", 0) < 0.7:
                report["recommendations"].append("Improve data presentation formatting and clarity")
            
            if report["evaluation_details"].get("workflow_completeness", {}).get("score", 0) < 0.7:
                report["recommendations"].append("Ensure complete workflow execution with proper validation")
        
        return report 