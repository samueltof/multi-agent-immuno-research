# Data Analyst Agent Integration

This document describes the integration of the Data Analyst agent into the LangManus multiagent system.

## Overview

The Data Analyst agent is a sophisticated workflow-based agent that specializes in:
- Converting natural language questions into SQL queries
- Validating SQL queries for correctness
- Executing queries against databases
- Providing insights and analysis from query results
- Handling database schema exploration

## Architecture

### Custom Workflow Agent

Unlike other agents in the system that use the built-in `create_react_agent`, the Data Analyst uses a custom LangGraph workflow (`src/agents/data_team.py`) that provides:

1. **Query Preparation**: Extracts user queries and prepares them for processing
2. **SQL Generation**: Uses a ReAct agent to generate SQL queries or provide schema information
3. **SQL Validation**: Validates generated SQL using an LLM with structured output
4. **Query Execution**: Executes validated queries against the database
5. **Error Handling**: Provides retry logic and error recovery
6. **Response Formatting**: Formats results for user consumption

### Integration Points

#### 1. Agent Configuration (`src/config/agents.py`)
```python
AGENT_LLM_MAP = {
    # ... other agents
    "data_analyst": "reasoning",  # Uses reasoning LLM for complex analysis
}
```

#### 2. Team Membership (`src/config/__init__.py`)
```python
TEAM_MEMBERS = ["researcher", "coder", "browser", "reporter", "data_analyst"]
```

#### 3. Database Tools (`src/tools/database.py`)
- `execute_sql_query`: Executes SQL queries against the database
- `get_database_schema`: Retrieves database schema information

#### 4. Prompt Template (`src/prompts/data_analyst.md`)
Defines the agent's role, capabilities, and guidelines for SQL generation and data analysis.

#### 5. Graph Integration (`src/graph/`)
- **nodes.py**: Contains `data_analyst_node` function
- **builder.py**: Adds data_analyst node to the workflow graph
- **types.py**: Updated Router type to include data_analyst

## Usage

The Data Analyst agent can handle various types of requests:

### Database Schema Requests
```
"Show me the database schema"
"What tables are available in the database?"
```

### Data Analysis Queries
```
"Find the top 10 customers by revenue"
"Show sales trends over the last 6 months"
"Calculate the average order value by region"
```

### Complex Analysis
```
"Analyze customer churn patterns"
"Compare product performance across categories"
"Generate a sales report with key metrics"
```

## Workflow Details

### State Management
The agent uses an extended state (`DataTeamState`) that includes:
- Standard workflow state (messages, team members, etc.)
- SQL-specific state (generated queries, validation status, execution results)
- Error handling state (error messages, retry counters)

### SQL Generation Process
1. **Input Analysis**: Determines if request is for schema or data query
2. **Schema Retrieval**: Fetches database schema if needed for context
3. **Query Generation**: Creates SQLite-compatible SQL queries
4. **Validation**: Checks syntax and logical correctness
5. **Execution**: Runs validated queries against the database
6. **Retry Logic**: Automatically retries failed queries with corrections

### Error Handling
- Automatic retry for invalid SQL (up to 2 retries)
- Detailed error messages and feedback
- Graceful fallback for database connection issues

## Database Setup

To use the Data Analyst agent with an actual database:

1. **Implement Database Manager**: Update `src/tools/database.py` with your database connection logic
2. **Configure Schema**: Ensure schema description is available
3. **Test Connection**: Verify database connectivity and permissions

### Example Implementation
```python
# In src/tools/database.py
from your_database_module import get_database_manager

@tool
def execute_sql_query(query: str) -> str:
    try:
        db_manager = get_database_manager()
        result_df = db_manager.execute_query_df(query)
        return result_df.to_markdown(index=False)
    except Exception as e:
        return f"Error executing SQL query: {str(e)}"
```

## Supervisor Integration

The supervisor has been updated to understand the Data Analyst's capabilities:

```markdown
- **`data_analyst`**: Specializes in SQL query generation and database analysis. 
  Converts natural language questions into SQL queries, validates them, executes 
  them against databases, and provides insights from the results. Use for any 
  database-related tasks or data analysis requests.
```

## Best Practices

### SQL Query Standards
- Never use `SELECT *` - always specify exact columns
- Include appropriate JOIN conditions
- Use WHERE clauses for filtering
- Handle NULL values appropriately
- Order results meaningfully

### Error Handling
- Provide clear error messages
- Suggest alternative approaches when queries fail
- Include validation feedback in responses

### Performance
- Use the reasoning LLM for complex analysis tasks
- Implement query optimization in the database layer
- Consider caching for frequently requested schema information

## Testing

The integration includes comprehensive testing to verify:
- Module imports work correctly
- Graph building includes the data analyst node
- Data team workflow can be created successfully
- No circular import issues

## Future Enhancements

Potential improvements for the Data Analyst agent:
- Chart generation capabilities
- Advanced analytics functions
- Query optimization suggestions
- Data visualization integration
- Multi-database support
- Query result caching 