import os
import re
import json
from datetime import datetime
from typing import Dict, Any, Optional

from langchain_core.prompts import PromptTemplate
from langgraph.prebuilt.chat_agent_executor import AgentState


def get_prompt_template(prompt_name: str) -> str:
    template = open(os.path.join(os.path.dirname(__file__), f"{prompt_name}.md")).read()
    # Escape curly braces using backslash
    template = template.replace("{", "{{").replace("}", "}}")
    # Replace `<<VAR>>` with `{VAR}`
    template = re.sub(r"<<([^>>]+)>>", r"{\1}", template)
    return template


def get_processed_prompt(prompt_name: str, template_vars: Dict[str, Any] = None) -> str:
    """Get processed prompt text for use in PydanticAI agents."""
    if template_vars is None:
        template_vars = {}
    
    # Add common template variables
    full_template_vars = {
        "CURRENT_TIME": datetime.now().strftime("%a %b %d %Y %H:%M:%S %z"),
        "research_focus": "",
        "user_context": "",
        "time_range": "",
        "preferred_databases": "",
        **template_vars
    }
    
    # Handle empty values by replacing with empty string
    for key, value in full_template_vars.items():
        if value is None or (isinstance(value, str) and value.strip() == ""):
            full_template_vars[key] = ""
    
    template = get_prompt_template(prompt_name)
    prompt = PromptTemplate(
        input_variables=list(full_template_vars.keys()),
        template=template,
    ).format(**full_template_vars)
    
    return prompt


def get_workflow_prompt_template(agent_name: str, workflow_step: str) -> str:
    """Load workflow-specific prompts from agent subdirectories."""
    template_path = os.path.join(
        os.path.dirname(__file__), 
        agent_name, 
        f"{workflow_step}.md"
    )
    
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Workflow prompt template not found: {template_path}")
    
    template = open(template_path).read()
    # Escape curly braces using backslash
    template = template.replace("{", "{{").replace("}", "}}")
    # Replace `<<VAR>>` with `{VAR}`
    template = re.sub(r"<<([^>>]+)>>", r"{\1}", template)
    return template


def apply_workflow_prompt_template(
    agent_name: str, 
    workflow_step: str, 
    template_vars: Dict[str, Any]
) -> str:
    """Apply workflow-specific prompt template with custom variables."""
    # Add common template variables
    full_template_vars = {
        "CURRENT_TIME": datetime.now().strftime("%a %b %d %Y %H:%M:%S %z"),
        **template_vars
    }
    
    # Handle empty values by replacing with empty string
    for key, value in full_template_vars.items():
        if value is None or (isinstance(value, str) and value.strip() == ""):
            full_template_vars[key] = ""
    
    try:
        template = get_workflow_prompt_template(agent_name, workflow_step)
        prompt = PromptTemplate(
            input_variables=list(full_template_vars.keys()),
            template=template,
        ).format(**full_template_vars)
        return prompt
    except Exception as e:
        raise RuntimeError(f"Failed to apply workflow prompt template for {agent_name}/{workflow_step}: {str(e)}")


def apply_prompt_template(prompt_name: str, state: AgentState) -> list:
    # Prepare template variables
    template_vars = {
        "CURRENT_TIME": datetime.now().strftime("%a %b %d %Y %H:%M:%S %z"),
        **state
    }
    
    # Special handling for reporter to include biomedical research results
    if prompt_name == "reporter":
        biomedical_result = state.get("biomedical_research_result")
        if biomedical_result:
            # Simply indicate that biomedical research data is available
            # The biomedical researcher should handle all formatting in its response
            template_vars["biomedical_research_result"] = "Biomedical research data is available and has been provided by the biomedical researcher with complete citations and sources."
        else:
            template_vars["biomedical_research_result"] = "No biomedical research results available."
    
    # For other agents, ensure the field exists but is empty
    if "biomedical_research_result" not in template_vars:
        template_vars["biomedical_research_result"] = ""
    
    system_prompt = PromptTemplate(
        input_variables=list(template_vars.keys()),
        template=get_prompt_template(prompt_name),
    ).format(**template_vars)
    
    return [{"role": "system", "content": system_prompt}] + state["messages"]
