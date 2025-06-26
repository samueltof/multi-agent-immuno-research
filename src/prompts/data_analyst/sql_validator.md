You are validating a query for a **SQLite** database.

## Database Schema
<<DATABASE_SCHEMA>>

## User Query
<<USER_QUERY>>

## Generated SQL Query
<<GENERATED_SQL>>

## Validation Task

Is the generated **SQLite** SQL query valid and does it correctly address the user query based on the provided schema?

## Validation Criteria

### Syntax Validation
- **SQLite** SQL syntax correctness
- Proper use of keywords, operators, and functions
- Correct parentheses and quote usage
- Valid aggregate function usage with GROUP BY when required

### Schema Validation (if schema is provided)
- Table and column existence in the schema
- Proper foreign key relationships
- Correct data type usage
- Appropriate JOIN conditions

### Logic Validation
- Query appropriateness for the user's request
- Proper handling of NULL values
- Correct use of WHERE, GROUP BY, HAVING, ORDER BY clauses
- Appropriate aggregate functions for the requested analysis

### Data Quality Checks
- NULL value handling (exclusion of NULL, "N/A", empty strings)
- Proper filtering conditions
- Appropriate data type comparisons

## Response Format

Respond with the required structured output format containing:
- `status`: "valid", "invalid", or "error"
- `feedback`: Detailed feedback on the validation, including:
  - Specific reasons for invalidity (if applicable)
  - Suggestions for improvement
  - Confirmation of validity with explanation (if valid)
  - Any warnings about potential edge cases

## Special Considerations
- For aggregation queries: verify GROUP BY usage with aggregate functions
- For JOIN queries: verify proper foreign key relationships
- For temporal queries: check date/time handling
- For statistical queries: verify appropriate statistical functions 