from typing import Any, List, Optional
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server with working directory
mcp = FastMCP("opentargets-mcp", working_dir="/Users/samueltorres/Documents/Repos/apps/langmanus/src/service/mcps")

# Constants - using GraphQL endpoint
API_BASE_URL = "https://api.platform.opentargets.org/api/v4/graphql"
TOOL_NAME = "opentargets-mcp"

async def make_graphql_request(query: str, variables: dict = None) -> Any:
    """Make a GraphQL request to the Open Targets API with proper error handling."""
    async with httpx.AsyncClient() as client:
        try:
            payload = {"query": query}
            if variables:
                payload["variables"] = variables
                
            response = await client.post(API_BASE_URL, json=payload, timeout=30.0)
            response.raise_for_status()
            result = response.json()
            
            if "errors" in result:
                return {"error": f"GraphQL errors: {result['errors']}"}
            
            return result.get("data", {})
        except Exception as e:
            return {"error": str(e)}

@mcp.tool()
async def search_targets(query: str, max_results: int = 10) -> str:
    """Search Open Targets for gene targets matching the query using GraphQL.
    
    Args:
        query: Search query for target names or symbols
        max_results: Maximum number of results to return (default: 10)
    """
    graphql_query = """
    query searchQuery($queryString: String!) {
        search(queryString: $queryString) {
            hits {
                id
                name
                entity
            }
        }
    }
    """
    
    variables = {
        "queryString": query
    }
    
    results = await make_graphql_request(graphql_query, variables)
    
    if isinstance(results, dict) and "error" in results:
        return f"Error searching Open Targets: {results['error']}"
    
    search_results = results.get("search", {})
    all_hits = search_results.get("hits", [])
    
    # Filter for targets only and limit results
    target_hits = [hit for hit in all_hits if hit.get("entity") == "target"][:max_results]
    
    if not target_hits:
        return "No targets found for your query."
    
    formatted_results = []
    for hit in target_hits:
        target_id = hit.get("id", "Unknown ID")
        name = hit.get("name", "No name")
        
        formatted_results.append(
            f"Symbol: {name}\n"
            f"Target ID: {target_id}"
        )
    
    return "\n\n---\n\n".join(formatted_results)

@mcp.tool()
async def get_target_details(target_id: str) -> str:
    """Get detailed information about a specific target by ID using GraphQL.
    
    Args:
        target_id: Open Targets ID for the target (e.g., "ENSG00000157764")
    """
    graphql_query = """
    query targetInfo($ensemblId: String!) {
        target(ensemblId: $ensemblId) {
            id
            approvedSymbol
            approvedName
            biotype
            genomicLocation {
                chromosome
                start
                end
                strand
            }
            functionDescriptions
            tractability {
                label
                modality
                value
            }
        }
    }
    """
    
    variables = {"ensemblId": target_id}
    
    results = await make_graphql_request(graphql_query, variables)
    
    if isinstance(results, dict) and "error" in results:
        return f"Error retrieving target details: {results['error']}"
    
    target = results.get("target")
    if not target:
        return f"No target found with ID: {target_id}"
    
    name = target.get("approvedName", "No name")
    symbol = target.get("approvedSymbol", "Unknown symbol")
    biotype = target.get("biotype", "Unknown biotype")
    functions = target.get("functionDescriptions", [])
    genomic_location = target.get("genomicLocation", {})
    tractability = target.get("tractability", [])
    
    # Format functions
    function_text = "\n  - ".join(functions) if functions else "Not available"
    
    # Format tractability
    tractability_text = ""
    if tractability:
        tractability_text = "\nTractability:\n"
        for tract in tractability[:3]:  # Show first 3
            label = tract.get("label", "Unknown")
            modality = tract.get("modality", "Unknown")
            value = tract.get("value", "Unknown")
            tractability_text += f"  - {label} ({modality}): {value}\n"
    
    formatted_details = (
        f"Symbol: {symbol}\n"
        f"Name: {name}\n"
        f"Target ID: {target_id}\n"
        f"Biotype: {biotype}\n"
        f"Chromosome: {genomic_location.get('chromosome', 'Unknown')}\n"
        f"Gene Function:\n  - {function_text}"
        f"{tractability_text}"
    )
    
    return formatted_details

@mcp.tool()
async def search_diseases(query: str, max_results: int = 10) -> str:
    """Search for diseases in Open Targets using GraphQL.
    
    Args:
        query: Search query for disease names
        max_results: Maximum number of results to return (default: 10)
    """
    graphql_query = """
    query searchQuery($queryString: String!) {
        search(queryString: $queryString) {
            hits {
                id
                name
                entity
            }
        }
    }
    """
    
    variables = {
        "queryString": query
    }
    
    results = await make_graphql_request(graphql_query, variables)
    
    if isinstance(results, dict) and "error" in results:
        return f"Error searching diseases: {results['error']}"
    
    search_results = results.get("search", {})
    all_hits = search_results.get("hits", [])
    
    # Filter for diseases only and limit results
    disease_hits = [hit for hit in all_hits if hit.get("entity") == "disease"][:max_results]
    
    if not disease_hits:
        return "No diseases found for your query."
    
    formatted_results = []
    for hit in disease_hits:
        disease_id = hit.get("id", "Unknown ID")
        name = hit.get("name", "No name")
        
        formatted_results.append(
            f"Disease: {name}\n"
            f"Disease ID: {disease_id}"
        )
    
    return "\n\n---\n\n".join(formatted_results)

@mcp.tool()
async def get_target_associated_diseases(target_id: str, max_results: int = 10) -> str:
    """Get diseases associated with a specific target using GraphQL.
    
    Args:
        target_id: Open Targets ID for the target (e.g., "ENSG00000157764")
        max_results: Maximum number of results to return (default: 10)
    """
    graphql_query = """
    query targetAssociations($ensemblId: String!, $size: Int!) {
        target(ensemblId: $ensemblId) {
            id
            approvedSymbol
            associatedDiseases(first: $size) {
                count
                rows {
                    disease {
                        id
                        name
                    }
                    score
                }
            }
        }
    }
    """
    
    variables = {
        "ensemblId": target_id,
        "size": max_results
    }
    
    results = await make_graphql_request(graphql_query, variables)
    
    if isinstance(results, dict) and "error" in results:
        return f"Error retrieving associated diseases: {results['error']}"
    
    target = results.get("target")
    if not target:
        return f"No target found with ID: {target_id}"
    
    associated_diseases = target.get("associatedDiseases", {})
    rows = associated_diseases.get("rows", [])
    
    if not rows:
        return f"No diseases associated with target ID: {target_id}"
    
    formatted_results = []
    for row in rows:
        disease = row.get("disease", {})
        disease_id = disease.get("id", "Unknown ID")
        name = disease.get("name", "No name")
        score = row.get("score", 0)
        
        formatted_results.append(
            f"Disease: {name}\n"
            f"Disease ID: {disease_id}\n"
            f"Association Score: {score:.3f}"
        )
    
    return "\n\n---\n\n".join(formatted_results)

@mcp.tool()
async def get_disease_associated_targets(disease_id: str, max_results: int = 10) -> str:
    """Get targets associated with a specific disease using GraphQL.
    
    Args:
        disease_id: Open Targets disease ID
        max_results: Maximum number of results to return (default: 10)
    """
    graphql_query = """
    query diseaseAssociations($efoId: String!, $size: Int!) {
        disease(efoId: $efoId) {
            id
            name
            associatedTargets(first: $size) {
                count
                rows {
                    target {
                        id
                        approvedSymbol
                        approvedName
                    }
                    score
                }
            }
        }
    }
    """
    
    variables = {
        "efoId": disease_id,
        "size": max_results
    }
    
    results = await make_graphql_request(graphql_query, variables)
    
    if isinstance(results, dict) and "error" in results:
        return f"Error retrieving associated targets: {results['error']}"
    
    disease = results.get("disease")
    if not disease:
        return f"No disease found with ID: {disease_id}"
    
    associated_targets = disease.get("associatedTargets", {})
    rows = associated_targets.get("rows", [])
    
    if not rows:
        return f"No targets associated with disease ID: {disease_id}"
    
    formatted_results = []
    for row in rows:
        target = row.get("target", {})
        target_id = target.get("id", "Unknown ID")
        symbol = target.get("approvedSymbol", "Unknown symbol")
        name = target.get("approvedName", "No name")
        score = row.get("score", 0)
        
        formatted_results.append(
            f"Symbol: {symbol}\n"
            f"Name: {name}\n"
            f"Target ID: {target_id}\n"
            f"Association Score: {score:.3f}"
        )
    
    return "\n\n---\n\n".join(formatted_results)

@mcp.tool()
async def search_drugs(query: str, max_results: int = 10) -> str:
    """Search for drugs in Open Targets using GraphQL.
    
    Args:
        query: Search query for drug names
        max_results: Maximum number of results to return (default: 10)
    """
    graphql_query = """
    query searchQuery($queryString: String!) {
        search(queryString: $queryString) {
            hits {
                id
                name
                entity
            }
        }
    }
    """
    
    variables = {
        "queryString": query
    }
    
    results = await make_graphql_request(graphql_query, variables)
    
    if isinstance(results, dict) and "error" in results:
        return f"Error searching drugs: {results['error']}"
    
    search_results = results.get("search", {})
    all_hits = search_results.get("hits", [])
    
    # Filter for drugs only and limit results
    drug_hits = [hit for hit in all_hits if hit.get("entity") == "drug"][:max_results]
    
    if not drug_hits:
        return "No drugs found for your query."
    
    formatted_results = []
    for hit in drug_hits:
        drug_id = hit.get("id", "Unknown ID")
        name = hit.get("name", "No name")
        
        formatted_results.append(
            f"Drug: {name}\n"
            f"Drug ID: {drug_id}"
        )
    
    return "\n\n---\n\n".join(formatted_results)

if __name__ == "__main__":
    mcp.run() 