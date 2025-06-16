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
            try:
                # Handle both object and dictionary formats
                if hasattr(biomedical_result, 'summary'):
                    # Object format
                    summary = biomedical_result.summary
                    key_findings = biomedical_result.key_findings
                    sources = biomedical_result.sources
                    recommendations = biomedical_result.recommendations
                    confidence_level = biomedical_result.confidence_level
                else:
                    # Dictionary format
                    summary = biomedical_result.get('summary', 'No summary available')
                    key_findings = biomedical_result.get('key_findings', [])
                    sources = biomedical_result.get('sources', [])
                    recommendations = biomedical_result.get('recommendations', [])
                    confidence_level = biomedical_result.get('confidence_level', 0.0)
                
                # Format the biomedical research result for the reporter
                biomedical_data = f"""
**Biomedical Research Results Available:**

**Summary:** {summary}

**Key Findings:**
{chr(10).join(f"• {finding}" for finding in key_findings) if key_findings else "• No key findings available"}

**Sources:**
{chr(10).join(f"• {source}" for source in sources) if sources else "• No sources available"}

**Recommendations:**
{chr(10).join(f"• {rec}" for rec in recommendations) if recommendations else "• No recommendations available"}

**Confidence Level:** {confidence_level:.2f}
"""
                template_vars["biomedical_research_result"] = biomedical_data
            except Exception as e:
                # Fallback if there's an error parsing the biomedical result
                template_vars["biomedical_research_result"] = f"Biomedical research data available but could not be parsed: {str(e)}"
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
