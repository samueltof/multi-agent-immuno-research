"""
Simple test to verify the schema extraction fix works.
This replicates the exact scenario from the original issue.
"""

from langchain_core.messages import HumanMessage, AIMessage
from src.agents.data_team import DataTeamState, extract_schema_or_sql_node


def test_original_issue_scenario():
    """Test the exact scenario from the original issue."""
    
    # This is the exact content from the original issue that was being misidentified as SQL
    schema_content = """Here's the structure of the two tables in the database:

1. Table: complexes  
   Description: One row per T-cell receptor complex (paired α+β chain clone), with shared metadata about MHC alleles, epitope target, assay details, and additional metadata.  
   Columns:  
   • complex_id          – integer (PK)  
   • mhc_a               – text, not null  
   • mhc_b               – text, not null  
   • mhc_class           – text, not null  
   • antigen_epitope     – text, not null  
   • antigen_gene        – text, not null  
   • antigen_species     – text, not null  
   • reference_id        – text, not null  
   • method              – json, not null  
   • meta                – json, not null  

2. Table: chains  
   Description: One row per individual TCR chain (α or β) linked to its parent complex, including sequence, V/J calls, fix annotations, internal flags, and confidence score.  
   Columns:  
   • chain_id            – integer (PK)  
   • complex_id          – integer, not null, FK → complexes(complex_id)  
   • gene                – text, not null ("TRA" or "TRB")  
   • cdr3                – text, not null  
   • v_segm              – text, not null  
   • j_segm              – text, not null  
   • species             – text, not null  
   • cdr3fix             – json, not null  
   • web_method          – text, not null  
   • web_method_seq      – text, not null  
   • web_cdr3fix_nc      – text, not null  
   • web_cdr3fix_unmp    – text, not null  
   • vdjdb_score         – integer, not null"""

    # The original query that triggered the issue
    original_query = '{"thought": "The user wants to understand the structure of a specific dataset.", "title": "Dataset Structure Analysis Plan", "steps": [{"agent_name": "data_analyst", "title": "Analyze dataset structure", "description": "Examine the dataset to identify its structure, including the types of data it contains, the number of records, and the relationships between different data points."}]}'
    
    # Create state that replicates the original issue
    state = DataTeamState(
        messages=[
            HumanMessage(content="What is the structure of these dataset?"),
            AIMessage(content=schema_content)
        ],
        natural_language_query=original_query,
        TEAM_MEMBERS=["data_analyst"],
        next="",
        full_plan="",
        deep_thinking_mode=False,
        search_before_planning=False
    )

    # Test the extraction logic
    result = extract_schema_or_sql_node(state)
    
    print(f"🔍 Testing original issue scenario...")
    print(f"📝 Query: {original_query[:100]}...")
    print(f"📄 Content: {schema_content[:200]}...")
    
    # Verify the fix works
    assert "provided_schema_text" in result, "Should identify as schema text"
    assert result["provided_schema_text"] is not None, "Schema text should not be None"
    assert result.get("generated_sql") is None, "Should not identify as SQL"
    assert "error_message" not in result, "Should not have error"
    
    print("✅ FIXED: Schema content is now correctly identified as schema, not SQL!")
    print(f"✅ Result: provided_schema_text = {result['provided_schema_text'][:100]}...")
    return True


def test_structure_query_variations():
    """Test various ways users might ask for database structure."""
    
    test_cases = [
        ("What is the structure of the database?", "Database structure request"),
        ("Describe the database schema", "Schema description request"),
        ("What tables do we have?", "Table listing request"),
        ("Show me the database structure", "Structure display request"),
        ("What is the structure of these dataset?", "Dataset structure request (original)"),
    ]
    
    schema_response = """Database Schema:

Table: users
- id (integer, primary key)
- name (text, not null)
- email (text, unique)

Table: orders
- order_id (integer, primary key)
- user_id (integer, foreign key to users.id)
- amount (decimal)"""

    for query, description in test_cases:
        print(f"\n🧪 Testing: {description}")
        print(f"   Query: '{query}'")
        
        state = DataTeamState(
            messages=[
                HumanMessage(content=query),
                AIMessage(content=schema_response)
            ],
            natural_language_query=query,
            TEAM_MEMBERS=["data_analyst"],
            next="",
            full_plan="",
            deep_thinking_mode=False,
            search_before_planning=False
        )

        result = extract_schema_or_sql_node(state)
        
        # All should be identified as schema
        assert "provided_schema_text" in result, f"Failed for: {query}"
        assert result["provided_schema_text"] is not None, f"Schema text None for: {query}"
        assert result.get("generated_sql") is None, f"Incorrectly identified as SQL for: {query}"
        
        print(f"   ✅ Correctly identified as schema")
    
    print(f"\n✅ All {len(test_cases)} structure query variations work correctly!")
    return True


def test_sql_vs_schema_edge_cases():
    """Test edge cases where SQL keywords appear in schema descriptions."""
    
    # Schema description that mentions SQL operations
    tricky_schema = """Database Schema for User Management:

Table: user_queries
- Contains SELECT statements and query logs
- Used for INSERT, UPDATE, DELETE operations tracking
- Columns: id, query_text, operation_type

This table stores all CREATE TABLE statements and ALTER operations
for audit purposes. The system handles JOIN operations between
user_queries and user_sessions tables."""

    # Test with schema-asking query
    state_schema = DataTeamState(
        messages=[
            HumanMessage(content="What is the database schema?"),
            AIMessage(content=tricky_schema)
        ],
        natural_language_query="What is the database schema?",
        TEAM_MEMBERS=["data_analyst"],
        next="",
        full_plan="",
        deep_thinking_mode=False,
        search_before_planning=False
    )

    result_schema = extract_schema_or_sql_node(state_schema)
    
    # Should be identified as schema despite SQL keywords
    assert "provided_schema_text" in result_schema
    assert result_schema["provided_schema_text"] is not None
    assert result_schema.get("generated_sql") is None
    
    print("✅ Edge case: Schema with SQL keywords correctly identified as schema")
    
    # Actual SQL query
    actual_sql = """SELECT u.id, u.name, COUNT(o.order_id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.active = 1
GROUP BY u.id, u.name
ORDER BY order_count DESC;"""

    state_sql = DataTeamState(
        messages=[
            HumanMessage(content="Get user order counts"),
            AIMessage(content=actual_sql)
        ],
        natural_language_query="Get user order counts",
        TEAM_MEMBERS=["data_analyst"],
        next="",
        full_plan="",
        deep_thinking_mode=False,
        search_before_planning=False
    )

    result_sql = extract_schema_or_sql_node(state_sql)
    
    # Should be identified as SQL
    assert "generated_sql" in result_sql
    assert result_sql["generated_sql"] is not None
    assert result_sql.get("provided_schema_text") is None
    
    print("✅ Edge case: Actual SQL correctly identified as SQL")
    return True


if __name__ == "__main__":
    print("🧪 Testing schema extraction fix...")
    print("=" * 60)
    
    # Test the original issue scenario
    test_original_issue_scenario()
    
    # Test various structure query formats
    test_structure_query_variations()
    
    # Test edge cases
    test_sql_vs_schema_edge_cases()
    
    print("\n" + "=" * 60)
    print("🎉 ALL TESTS PASSED! The schema extraction fix is working correctly.")
    print("🚀 Schema requests will no longer get stuck in validation loops!") 