"""
Test for data team agent schema extraction fix.

This test verifies that the data team agent correctly identifies when a user
is asking for database schema information vs actual SQL queries, preventing
the validation loop issue.
"""

import pytest
from unittest.mock import Mock, patch
from langchain_core.messages import HumanMessage, AIMessage

from src.agents.data_team import DataTeamState, extract_schema_or_sql_node


class TestDataTeamSchemaExtraction:
    """Test cases for data team schema extraction logic."""

    def test_schema_request_with_structure_keywords(self):
        """Test that schema requests with 'structure' keywords are correctly identified."""
        # Mock state with schema request
        state = DataTeamState(
            messages=[
                HumanMessage(content="What is the structure of the database?"),
                AIMessage(content="""Here's the structure of the two tables in the database:

1. Table: complexes  
   Description: One row per T-cell receptor complex (paired α+β chain clone), with shared metadata about MHC alleles, epitope target, assay details, and additional metadata.  
   Columns:  
   • complex_id          – integer (PK)  
   • mhc_a               – text, not null  
   • mhc_b               – text, not null  
   • mhc_class           – text, not null  
   • antigen_epitope     – text, not null  

2. Table: chains  
   Description: One row per individual TCR chain (α or β) linked to its parent complex.  
   Columns:  
   • chain_id            – integer (PK)  
   • complex_id          – integer, not null, FK → complexes(complex_id)  
   • gene                – text, not null ("TRA" or "TRB")  
   • cdr3                – text, not null  
""")
            ],
            natural_language_query="What is the structure of the database?",
            TEAM_MEMBERS=["data_analyst"],
            next="",
            full_plan="",
            deep_thinking_mode=False,
            search_before_planning=False
        )

        result = extract_schema_or_sql_node(state)
        
        # Should identify as schema, not SQL
        assert "provided_schema_text" in result
        assert result["provided_schema_text"] is not None
        assert "generated_sql" not in result or result["generated_sql"] is None
        assert "error_message" not in result

    def test_schema_request_despite_sql_keywords_in_description(self):
        """Test that schema descriptions with SQL keywords are still identified as schema."""
        state = DataTeamState(
            messages=[
                HumanMessage(content="Describe the database schema"),
                AIMessage(content="""Database Schema:

Table: users
- Contains SELECT statements for user queries
- Used for INSERT operations on new users
- Columns: id, name, email

This table is designed to handle all CREATE, READ, UPDATE, DELETE operations efficiently.
""")
            ],
            natural_language_query="Describe the database schema",
            TEAM_MEMBERS=["data_analyst"],
            next="",
            full_plan="",
            deep_thinking_mode=False,
            search_before_planning=False
        )

        result = extract_schema_or_sql_node(state)
        
        # Should identify as schema despite SQL keywords in description
        assert "provided_schema_text" in result
        assert result["provided_schema_text"] is not None
        assert "generated_sql" not in result or result["generated_sql"] is None

    def test_actual_sql_query_detection(self):
        """Test that actual SQL queries are correctly identified."""
        state = DataTeamState(
            messages=[
                HumanMessage(content="Get all users from the database"),
                AIMessage(content="""SELECT id, name, email 
FROM users 
WHERE active = 1 
ORDER BY name;""")
            ],
            natural_language_query="Get all users from the database",
            TEAM_MEMBERS=["data_analyst"],
            next="",
            full_plan="",
            deep_thinking_mode=False,
            search_before_planning=False
        )

        result = extract_schema_or_sql_node(state)
        
        # Should identify as SQL query
        assert "generated_sql" in result
        assert result["generated_sql"] is not None
        assert "provided_schema_text" not in result or result["provided_schema_text"] is None

    def test_sql_in_markdown_block(self):
        """Test that SQL in markdown blocks is correctly extracted."""
        state = DataTeamState(
            messages=[
                HumanMessage(content="Show me the query to get user data"),
                AIMessage(content="""Here's the SQL query you need:

```sql
SELECT u.id, u.name, u.email, p.phone
FROM users u
LEFT JOIN profiles p ON u.id = p.user_id
WHERE u.active = 1;
```

This query joins users with their profiles and filters for active users only.""")
            ],
            natural_language_query="Show me the query to get user data",
            TEAM_MEMBERS=["data_analyst"],
            next="",
            full_plan="",
            deep_thinking_mode=False,
            search_before_planning=False
        )

        result = extract_schema_or_sql_node(state)
        
        # Should extract SQL from markdown block
        assert "generated_sql" in result
        assert result["generated_sql"] is not None
        assert "SELECT u.id, u.name, u.email, p.phone" in result["generated_sql"]
        assert "provided_schema_text" not in result or result["provided_schema_text"] is None

    def test_ambiguous_content_with_schema_request(self):
        """Test that ambiguous content defaults to schema when user asks for schema."""
        state = DataTeamState(
            messages=[
                HumanMessage(content="What tables do we have?"),
                AIMessage(content="We have several tables including users, orders, and products with various relationships.")
            ],
            natural_language_query="What tables do we have?",
            TEAM_MEMBERS=["data_analyst"],
            next="",
            full_plan="",
            deep_thinking_mode=False,
            search_before_planning=False
        )

        result = extract_schema_or_sql_node(state)
        
        # Should default to schema since user asked "what tables"
        assert "provided_schema_text" in result
        assert result["provided_schema_text"] is not None
        assert "generated_sql" not in result or result["generated_sql"] is None

    def test_multiple_table_descriptions(self):
        """Test that content with multiple table descriptions is identified as schema."""
        state = DataTeamState(
            messages=[
                HumanMessage(content="Show me the database structure"),
                AIMessage(content="""Database contains the following tables:

Table: users
- Primary key: id
- Contains user information

Table: orders  
- Primary key: order_id
- Foreign key: user_id references users(id)

Table: products
- Primary key: product_id
- Contains product catalog
""")
            ],
            natural_language_query="Show me the database structure",
            TEAM_MEMBERS=["data_analyst"],
            next="",
            full_plan="",
            deep_thinking_mode=False,
            search_before_planning=False
        )

        result = extract_schema_or_sql_node(state)
        
        # Should identify as schema due to multiple "Table:" patterns
        assert "provided_schema_text" in result
        assert result["provided_schema_text"] is not None
        assert "generated_sql" not in result or result["generated_sql"] is None


def test_integration_schema_request():
    """Integration test for schema request flow."""
    from src.agents.data_team import create_data_team_graph
    
    # Create a minimal test state
    initial_state = DataTeamState(
        messages=[HumanMessage(content="What is the structure of the database?")],
        TEAM_MEMBERS=["data_analyst"],
        next="",
        full_plan="",
        deep_thinking_mode=False,
        search_before_planning=False
    )
    
    # Mock the database schema tool to avoid actual database calls
    with patch('src.agents.data_team.get_database_schema') as mock_schema:
        mock_schema.invoke.return_value = "Mocked schema response"
        
        # Create the graph
        graph = create_data_team_graph()
        
        # The graph should be created without errors
        assert graph is not None
        assert graph.name == "data_analysis_team"


if __name__ == "__main__":
    # Run a quick test
    test = TestDataTeamSchemaExtraction()
    test.test_schema_request_with_structure_keywords()
    test.test_schema_request_despite_sql_keywords_in_description()
    test.test_actual_sql_query_detection()
    test.test_sql_in_markdown_block()
    test.test_ambiguous_content_with_schema_request()
    test.test_multiple_table_descriptions()
    
    print("✅ All schema extraction tests passed!")
    
    # Run integration test
    test_integration_schema_request()
    print("✅ Integration test passed!") 