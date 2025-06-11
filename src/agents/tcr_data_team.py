"""
TCR Data Team - Specialized workflow for T-cell receptor analysis.

This extends the existing data team workflow with TCR-specific capabilities.
"""

from typing import Dict, Any
import logging
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import create_react_agent
from functools import partial
from src.agents.data_team import (
    DataTeamState, 
    prepare_data_query_node,
    extract_schema_or_sql_node,
    sql_validator_node,
    sql_executor_node,
    handle_error_node,
    format_final_response_node,
    check_extraction_result,
    decide_after_validation,
    check_for_errors_before_agent,
    check_for_errors_after_execution
)
from src.tools.tcr_analysis import (
    get_vdjdb_schema,
    calculate_tcr_diversity_metrics,
    analyze_cdr3_motifs,
    compare_tcr_repertoires
)
from src.tools.database import execute_sql_query, get_random_subsamples

logger = logging.getLogger(__name__)

def create_tcr_data_team_graph(llm_client: Any):
    """Create TCR data analysis workflow with specialized TCR tools."""
    logger.info("🧬 Creating TCR Data Team Graph with specialized tools...")
    
    workflow = StateGraph(DataTeamState)

    # Create the ReAct agent with TCR-specific tools
    tcr_sql_generating_agent = create_react_agent(
        llm_client, 
        tools=[
            get_vdjdb_schema,           # TCR-specific schema with context
            execute_sql_query,          # Standard SQL execution
            get_random_subsamples,      # Standard sampling
            calculate_tcr_diversity_metrics,  # TCR diversity analysis
            analyze_cdr3_motifs,        # CDR3 sequence analysis
            compare_tcr_repertoires     # TCR repertoire comparison
        ]
    )
    
    # Bind the llm_client to the validation node
    validate_sql_with_llm = partial(sql_validator_node, llm_client=llm_client)

    # Add nodes (reusing most from standard data team)
    workflow.add_node("prepare_query", prepare_data_query_node)
    workflow.add_node("tcr_sql_generating_agent", tcr_sql_generating_agent)
    workflow.add_node("extract_schema_or_sql", extract_schema_or_sql_node)
    workflow.add_node("validate_sql", validate_sql_with_llm)
    workflow.add_node("execute_sql", sql_executor_node)
    workflow.add_node("handle_error", handle_error_node)
    workflow.add_node("format_response", format_final_response_node)

    # Helper node to increment retry counter
    workflow.add_node("increment_retry", lambda state: {
        "sql_generation_retries": state.get("sql_generation_retries", 0) + 1,
        "messages": [],
        "provided_schema_text": None
    })

    # Set entry point
    workflow.set_entry_point("prepare_query")

    # Add edges (same flow as standard data team)
    workflow.add_conditional_edges(
        "prepare_query",
        check_for_errors_before_agent,
        {
            "handle_error": "handle_error",
            "continue_to_agent": "tcr_sql_generating_agent"  # Use TCR agent instead
        }
    )

    workflow.add_edge("tcr_sql_generating_agent", "extract_schema_or_sql")

    workflow.add_conditional_edges(
        "extract_schema_or_sql",
        check_extraction_result,
        {
            "validate_sql": "validate_sql",
            "format_response": "format_response",
            "handle_error": "handle_error"
        }
    )

    workflow.add_conditional_edges(
        "validate_sql",
        decide_after_validation,
        {
            "execute_sql": "execute_sql",
            "retry_sql_generation": "increment_retry",
            "handle_error": "handle_error",
        },
    )

    workflow.add_edge("increment_retry", "prepare_query")

    workflow.add_conditional_edges(
        "execute_sql",
        check_for_errors_after_execution,
        {
            "handle_error": "handle_error",
            "continue_to_format": "format_response"
        }
    )

    workflow.add_edge("handle_error", "format_response")
    workflow.add_edge("format_response", END)

    # Compile the graph
    tcr_data_team_app = workflow.compile()
    tcr_data_team_app.name = "tcr_data_analysis_team"
    logger.info("🧬 TCR DATA TEAM: Compiled TCR data team graph with specialized tools.")
    return tcr_data_team_app 