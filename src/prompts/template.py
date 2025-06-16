import os
import re
import json
from datetime import datetime

from langchain_core.prompts import PromptTemplate
from langgraph.prebuilt.chat_agent_executor import AgentState


def get_prompt_template(prompt_name: str) -> str:
    template = open(os.path.join(os.path.dirname(__file__), f"{prompt_name}.md")).read()
    # Escape curly braces using backslash
    template = template.replace("{", "{{").replace("}", "}}")
    # Replace `<<VAR>>` with `{VAR}`
    template = re.sub(r"<<([^>>]+)>>", r"{\1}", template)
    return template


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
