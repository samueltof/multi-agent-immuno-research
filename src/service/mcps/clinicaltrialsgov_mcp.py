from typing import Any, List, Optional
import requests
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server with working directory
mcp = FastMCP("clinicaltrials-mcp", working_dir="/Users/samueltorres/Documents/Repos/apps/langmanus/src/service/mcps")

# Constants
API_BASE_URL = "https://clinicaltrials.gov/api/v2"
TOOL_NAME = "clinicaltrials-mcp"

def make_api_request(endpoint: str, params: dict) -> Any:
    """Make a request to the ClinicalTrials.gov API with proper error handling."""
    url = f"{API_BASE_URL}/{endpoint}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "application/json"
    }
    
    try:
        print(url)
        print(params)
        print(headers)
        response = requests.get(url, params=params, headers=headers, timeout=30.0)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def search_trials(query: str, max_results: int = 10) -> str:
    """Search ClinicalTrials.gov for studies matching the query.
    
    Args:
        query: Search query (e.g., "diabetes treatment", "COVID-19 vaccine", "cancer immunotherapy")
        max_results: Maximum number of results to return (default: 10, max: 50)
    
    Returns:
        List of clinical trials with title, NCT ID, status, and phase.
        Results are ranked by relevance to the query.
        
    Output format:
        Title: [Study title]
        ID: [NCT identifier]
        Status: [Current study status]
        Phase: [Clinical trial phase]
        
    Examples:
        - query="diabetes treatment" → Diabetes-related clinical trials
        - query="Alzheimer drug" → Alzheimer's disease treatments
        - query="pediatric cancer" → Cancer trials for children
        
    Notes:
        - Performance: ~0.07s typical response time
        - Searches across title, conditions, interventions
        - Use specific terms for better results
    """
    search_params = {
        "query.term": query,
        "pageSize": max_results,
        "format": "json"
    }
    
    search_results = make_api_request("studies", search_params)
    
    if isinstance(search_results, dict) and "error" in search_results:
        return f"Error searching ClinicalTrials.gov: {search_results['error']}"
    
    studies = search_results.get("studies", [])
    if not studies:
        return "No results found for your query."
    
    formatted_results = []
    
    for study in studies:
        protocol_section = study.get("protocolSection", {})
        identification = protocol_section.get("identificationModule", {})
        status = protocol_section.get("statusModule", {})
        
        nct_id = identification.get("nctId", "Unknown ID")
        title = identification.get("briefTitle", "No title")
        status_text = status.get("overallStatus", "Unknown status")
        phase = protocol_section.get("phaseModule", {}).get("phase", "Unknown phase")
        
        formatted_results.append(
            f"Title: {title}\n"
            f"ID: {nct_id}\n"
            f"Status: {status_text}\n"
            f"Phase: {phase}"
        )
    
    if not formatted_results:
        return "No study details could be retrieved."
        
    return "\n\n---\n\n".join(formatted_results)

@mcp.tool()
def get_trial_details(nct_id: str) -> str:
    """Get detailed information about a specific clinical trial by its NCT ID.
    
    Args:
        nct_id: The NCT identifier for the trial (format: "NCT########", e.g., "NCT02015429")
    
    Returns:
        Comprehensive trial details including title, status, sponsor, conditions, and description.
        All available metadata from the ClinicalTrials.gov registry.
        
    Output format:
        NCT ID: [Trial identifier]
        Brief Title: [Short title]
        Official Title: [Full official title]
        Status: [Current study status]
        Phase: [Clinical trial phase]
        Sponsor: [Lead sponsor organization]
        Study Type: [Type of study]
        Primary Purpose: [Main study purpose]
        Conditions: [Medical conditions studied]
        Detailed Description: [Full study description]
        
    Examples:
        - nct_id="NCT02015429" → Full details of nutrition study
        - nct_id="NCT03000000" → Complete trial information
        - Use NCT IDs from search_trials results
        
    Notes:
        - Performance: ~0.06s typical response time
        - Returns comprehensive metadata when available
        - Use valid NCT IDs from trial searches
    """
    study_params = {"format": "json"}
    
    study_details = make_api_request(f"studies/{nct_id}", study_params)
    
    if isinstance(study_details, dict) and "error" in study_details:
        return f"Error retrieving trial details: {study_details['error']}"
    
    protocol_section = study_details.get("protocolSection", {})
    
    # Extract main sections
    identification = protocol_section.get("identificationModule", {})
    status = protocol_section.get("statusModule", {})
    sponsor = protocol_section.get("sponsorCollaboratorsModule", {})
    design = protocol_section.get("designModule", {})
    conditions = protocol_section.get("conditionsModule", {})
    description = protocol_section.get("descriptionModule", {})
    
    # Format the details
    title = identification.get("briefTitle", "No title")
    official_title = identification.get("officialTitle", "No official title")
    status_text = status.get("overallStatus", "Unknown status")
    phase = protocol_section.get("phaseModule", {}).get("phase", "Unknown phase")
    
    primary_sponsor = sponsor.get("leadSponsor", {}).get("name", "Unknown sponsor")
    
    study_type = design.get("studyType", "Unknown type")
    primary_purpose = design.get("primaryPurpose", "Unknown purpose")
    
    condition_list = conditions.get("conditions", [])
    conditions_text = ", ".join(condition_list) if condition_list else "None specified"
    
    detailed_description = description.get("detailedDescription", "No detailed description available")
    
    formatted_details = (
        f"NCT ID: {nct_id}\n\n"
        f"Brief Title: {title}\n\n"
        f"Official Title: {official_title}\n\n"
        f"Status: {status_text}\n\n"
        f"Phase: {phase}\n\n"
        f"Sponsor: {primary_sponsor}\n\n"
        f"Study Type: {study_type}\n\n"
        f"Primary Purpose: {primary_purpose}\n\n"
        f"Conditions: {conditions_text}\n\n"
        f"Detailed Description: {detailed_description}"
    )
    
    return formatted_details

@mcp.tool()
def find_trials_by_condition(condition: str, max_results: int = 10) -> str:
    """Search for clinical trials related to a specific medical condition.
    
    Args:
        condition: Medical condition or disease (e.g., "Type 2 Diabetes", "Alzheimer Disease", "Breast Cancer")
        max_results: Maximum number of results to return (default: 10, max: 50)
    
    Returns:
        List of clinical trials specifically targeting the medical condition.
        Filtered to condition-relevant studies only.
        
    Output format:
        Title: [Study title]
        ID: [NCT identifier]
        Status: [Current study status]
        Phase: [Clinical trial phase]
        
    Examples:
        - condition="Type 2 Diabetes" → Diabetes-specific clinical trials
        - condition="Alzheimer Disease" → Alzheimer's treatment studies
        - condition="Breast Cancer" → Breast cancer research trials
        
    Notes:
        - Performance: ~0.06s typical response time
        - More targeted than general search_trials
        - Use standard medical condition names for best results
        - Searches the conditions field specifically
    """
    search_params = {
        "query.cond": condition,
        "pageSize": max_results,
        "format": "json"
    }
    
    search_results = make_api_request("studies", search_params)
    
    if isinstance(search_results, dict) and "error" in search_results:
        return f"Error searching by condition: {search_results['error']}"
    
    return format_search_results(search_results)

@mcp.tool()
def find_trials_by_location(location: str, max_results: int = 10) -> str:
    """Search for clinical trials in a specific location.
    
    Args:
        location: Location (city, state, country) (e.g., "Boston, MA", "New York", "California", "United States")
        max_results: Maximum number of results to return (default: 10, max: 50)
    
    Returns:
        List of clinical trials recruiting or conducted in the specified location.
        Includes trials with study sites in the area.
        
    Output format:
        Title: [Study title]
        ID: [NCT identifier]
        Status: [Current study status]
        Phase: [Clinical trial phase]
        
    Examples:
        - location="Boston, MA" → Trials with Boston study sites
        - location="California" → Trials across California
        - location="Mayo Clinic" → Trials at Mayo Clinic locations
        
    Notes:
        - Performance: ~0.07s typical response time
        - Searches study sites and recruitment locations
        - Useful for finding local trial opportunities
        - Can use institution names, cities, states, or countries
    """
    search_params = {
        "query.locn": location,
        "pageSize": max_results,
        "format": "json"
    }
    
    search_results = make_api_request("studies", search_params)
    
    if isinstance(search_results, dict) and "error" in search_results:
        return f"Error searching by location: {search_results['error']}"
    
    return format_search_results(search_results)

def format_search_results(search_results: dict) -> str:
    """Helper function to format search results."""
    studies = search_results.get("studies", [])
    if not studies:
        return "No results found for your query."
    
    formatted_results = []
    
    for study in studies:
        protocol_section = study.get("protocolSection", {})
        identification = protocol_section.get("identificationModule", {})
        status = protocol_section.get("statusModule", {})
        
        nct_id = identification.get("nctId", "Unknown ID")
        title = identification.get("briefTitle", "No title")
        status_text = status.get("overallStatus", "Unknown status")
        phase = protocol_section.get("phaseModule", {}).get("phase", "Unknown phase")
        
        formatted_results.append(
            f"Title: {title}\n"
            f"ID: {nct_id}\n"
            f"Status: {status_text}\n"
            f"Phase: {phase}"
        )
    
    if not formatted_results:
        return "No study details could be retrieved."
        
    return "\n\n---\n\n".join(formatted_results)

if __name__ == "__main__":
    mcp.run(transport='stdio')
