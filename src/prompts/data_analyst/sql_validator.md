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

Consider:
- **SQLite** SQL syntax correctness
- Table and column existence in the schema (if schema is provided). If schema is missing, validate syntax only.
- Appropriateness of the query for the user's request.

## Response Format

Respond with the required structured output format containing:
- `status`: "valid", "invalid", or "error"
- `feedback`: Detailed feedback on the validation, including reasons for invalidity or confirmation of validity 