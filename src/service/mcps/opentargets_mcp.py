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
        query: Search query for target names or symbols (e.g., "Alzheimer", "BRAF", "kinase", "p53")
        max_results: Maximum number of results to return (default: 10, max: 50)
    
    Returns:
        List of gene targets with symbols and Ensembl IDs.
        Targets are filtered from general search results.
        
    Output format:
        Symbol: [Gene symbol]
        Target ID: [Ensembl gene ID]
        
    Examples:
        - query="Alzheimer" → Returns APP, MAPT, PSEN1 and related targets
        - query="BRAF" → Returns BRAF gene target
        - query="kinase" → Returns various kinase targets
        
    Notes:
        - Performance: ~0.19s typical response time
        - Uses GraphQL search across gene annotations
        - Returns Ensembl gene IDs for further queries
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
        target_id: Open Targets ID for the target (Ensembl gene ID, e.g., "ENSG00000142192")
    
    Returns:
        Comprehensive target information including gene symbol, name, function, location, and tractability.
        All available metadata from Open Targets database.
        
    Output format:
        Symbol: [Gene symbol]
        Name: [Full gene name]
        Target ID: [Ensembl ID]
        Biotype: [Gene biotype]
        Chromosome: [Chromosome location]
        Gene Function: [Functional descriptions]
        Tractability: [Drug development tractability scores]
        
    Examples:
        - target_id="ENSG00000142192" → Detailed APP gene information
        - target_id="ENSG00000157764" → Detailed BRAF gene information
        - Use target IDs from search_targets results
        
    Notes:
        - Performance: ~0.17s typical response time
        - Provides comprehensive gene annotations
        - Includes tractability assessments for drug development
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
        query: Search query for disease names (e.g., "cancer", "diabetes", "Alzheimer", "heart disease")
        max_results: Maximum number of results to return (default: 10, max: 50)
    
    Returns:
        List of diseases with names and ontology IDs.
        Diseases are filtered from general search results.
        
    Output format:
        Disease: [Disease name]
        Disease ID: [Ontology ID (MONDO, EFO, etc.)]
        
    Examples:
        - query="cancer" → Returns various cancer types and related diseases
        - query="diabetes" → Returns diabetes types and metabolic disorders
        - query="Alzheimer" → Returns Alzheimer's disease and related conditions
        
    Notes:
        - Performance: ~0.13s typical response time
        - Uses disease ontologies (MONDO, EFO, Orphanet)
        - Returns disease IDs for association queries
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
        target_id: Open Targets ID for the target (Ensembl gene ID, e.g., "ENSG00000142192")
        max_results: Maximum number of results to return (default: 10, max: 50)
    
    Returns:
        List of diseases associated with the gene target, ranked by association score.
        Returns error message if GraphQL query fails (handled gracefully).
        
    Output format:
        Disease: [Disease name]
        Disease ID: [Disease ontology ID]
        Association Score: [Numerical association strength]
        
    Examples:
        - target_id="ENSG00000142192" → Diseases associated with APP gene
        - target_id="ENSG00000157764" → Diseases associated with BRAF gene
        - Use target IDs from search_targets results
        
    Notes:
        - Performance: ~0.14s typical response time
        - May return GraphQL 400 errors (handled gracefully)
        - Association scores indicate strength of target-disease relationship
        - Returns "No diseases associated" if none found
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
        disease_id: Open Targets disease ID (ontology ID, e.g., "MONDO_0004992", "EFO_0000249")
        max_results: Maximum number of results to return (default: 10, max: 50)
    
    Returns:
        List of gene targets associated with the disease, ranked by association score.
        Returns error message if GraphQL query fails (handled gracefully).
        
    Output format:
        Symbol: [Gene symbol]
        Name: [Full gene name]
        Target ID: [Ensembl gene ID]
        Association Score: [Numerical association strength]
        
    Examples:
        - disease_id="MONDO_0004992" → Targets associated with cancer
        - disease_id="EFO_0000249" → Targets associated with Alzheimer's disease
        - Use disease IDs from search_diseases results
        
    Notes:
        - Performance: ~0.14s typical response time
        - May return GraphQL 400 errors (handled gracefully)
        - Association scores indicate strength of disease-target relationship
        - Returns "No targets associated" if none found
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
        query: Search query for drug names (e.g., "aspirin", "ibuprofen", "metformin", "chemotherapy")
        max_results: Maximum number of results to return (default: 10, max: 50)
    
    Returns:
        List of drugs with names and ChEMBL IDs.
        Drugs are filtered from general search results.
        
    Output format:
        Drug: [Drug name]
        Drug ID: [ChEMBL identifier]
        
    Examples:
        - query="aspirin" → Returns ASPIRIN with ChEMBL ID
        - query="metformin" → Returns metformin drug information
        - query="antibody" → Returns various antibody drugs
        
    Notes:
        - Performance: ~0.14s typical response time
        - Uses ChEMBL database integration
        - Returns ChEMBL IDs for drug-target interaction queries
        - Covers approved drugs and experimental compounds
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