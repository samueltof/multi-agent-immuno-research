from langchain_core.tools import tool
import pandas as pd
from typing import Optional, List, Dict, Any
import logging

from src.config.database import DatabaseSettings
from src.service.database import DatabaseManager

logger = logging.getLogger(__name__)

# Global database manager instance for tools
_db_manager: Optional[DatabaseManager] = None

def get_database_manager() -> DatabaseManager:
    """Get or create the global database manager instance."""
    global _db_manager
    if _db_manager is None:
        settings = DatabaseSettings()
        _db_manager = DatabaseManager(settings)
    return _db_manager


@tool
def execute_sql_query(query: str) -> str:
    """Executes a given SQL query against the database and returns the result.
    
    Args:
        query: The SQL query string to be executed.
        
    Returns:
        A string representation of the query result (dataframe) or an error message.
    """
    try:
        logger.info(f"🛠️ Executing SQL query: {query[:100]}...")
        
        # Get database manager
        db_manager = get_database_manager()
        
        # Execute query and get results as DataFrame for better formatting
        result_df = db_manager.execute_query_df(query)
        
        if result_df.empty:
            return "Query executed successfully but returned no results."
        
        # Format the results as a readable string
        result_str = f"Query executed successfully. Results ({len(result_df)} rows):\n\n"
        result_str += result_df.to_string(index=False, max_rows=100)
        
        if len(result_df) > 100:
            result_str += f"\n\n... (showing first 100 rows of {len(result_df)} total rows)"
        
        logger.info(f"🔘 SQL query executed successfully, returned {len(result_df)} rows")
        return result_str
        
    except Exception as e:
        error_msg = f"Error executing SQL query: {str(e)}"
        logger.error(f"❌ {error_msg}")
        return error_msg


@tool
def get_database_schema() -> str:
    """Returns the schema description of the database.
    
    Returns:
        A string containing the database schema description.
    """
    try:
        logger.info("🛠️ Fetching database schema...")
        
        # Get database manager
        db_manager = get_database_manager()
        
        # Load schema description
        schema_description = db_manager.load_schema_description()
        
        logger.info("🔘 Database schema fetched successfully")
        return schema_description
        
    except Exception as e:
        error_msg = f"Error fetching database schema: {str(e)}"
        logger.error(f"❌ {error_msg}")
        return error_msg


@tool
def get_random_subsamples(tables: List[Dict[str, Any]], sample_size: int = 5) -> str:
    """Retrieve random data samples from specified database tables.
    
    Args:
        tables: List of tables with their columns to sample.
                Format: [{"table_name": "table1", "noun_columns": ["col1", "col2"]}, ...]
        sample_size: Number of random rows to retrieve per table (default: 5).
    
    Returns:
        A string containing the sample data or an error message.
    """
    try:
        logger.info(f"🛠️ Getting random subsamples from {len(tables)} tables, {sample_size} rows each")
        
        # Get database manager
        db_manager = get_database_manager()
        db_settings = DatabaseSettings()
        
        # Helper function to get database-specific random function
        def get_random_function() -> str:
            SQL_RANDOM_FUNCTIONS = {
                "sqlite": "RANDOM()",
                "athena": "rand()",
                "postgres": "RANDOM()",
                "mysql": "RAND()",
                "mssql": "NEWID()",
            }
            db_type = db_settings.database_type.value.lower()
            return SQL_RANDOM_FUNCTIONS.get(db_type, "RANDOM()")
        
        # Helper function to get database-specific limit syntax
        def get_limit_syntax() -> Dict[str, str]:
            db_type = db_settings.database_type.value.lower()
            if db_type == "mssql":
                return {"select_prefix": f"TOP {sample_size}", "limit_suffix": ""}
            else:
                return {"select_prefix": "", "limit_suffix": f"LIMIT {sample_size}"}
        
        samples = {}
        limit_syntax = get_limit_syntax()
        random_func = get_random_function()
        
        for table in tables:
            table_name = table["table_name"]
            noun_columns = table["noun_columns"]
            
            query = f"""
                SELECT {limit_syntax['select_prefix']} {", ".join(noun_columns)}
                FROM {table_name} 
                ORDER BY {random_func}
                {limit_syntax['limit_suffix']}
            """
            
            try:
                # Execute query and get results as DataFrame
                result_df = db_manager.execute_query_df(query.strip())
                
                if not result_df.empty:
                    # Convert DataFrame to list of dictionaries
                    samples[table_name] = result_df.to_dict('records')
                else:
                    samples[table_name] = []
                    
            except Exception as e:
                logger.error(f"Error sampling table {table_name}: {str(e)}")
                samples[table_name] = []
        
        # Format results as a readable string
        if not samples or all(not sample_list for sample_list in samples.values()):
            return "No sample data could be retrieved from any of the specified tables."
        
        result_str = "Random sample data retrieved:\n\n"
        
        for table_name, sample_list in samples.items():
            result_str += f"**{table_name}** ({len(sample_list)} rows):\n"
            
            if sample_list:
                # Create a DataFrame for better formatting
                sample_df = pd.DataFrame(sample_list)
                result_str += sample_df.to_string(index=False)
            else:
                result_str += "  No data available or error occurred"
            
            result_str += "\n\n"
        
        logger.info(f"🔘 Random subsamples retrieved successfully from {len(samples)} tables")
        return result_str
        
    except Exception as e:
        error_msg = f"Error retrieving random samples: {str(e)}"
        logger.error(f"❌ {error_msg}")
        return error_msg


# Additional helper function that can be used by the data team workflow
def validate_sql_syntax(sql_query: str) -> dict:
    """Basic SQL syntax validation.
    
    Args:
        sql_query: The SQL query to validate
        
    Returns:
        Dict with 'valid' boolean and 'errors' list
    """
    errors = []
    sql_upper = sql_query.upper().strip()
    
    # Basic validation checks
    if not sql_upper:
        errors.append("Query is empty")
    
    if "SELECT *" in sql_upper:
        errors.append("Use of SELECT * is not allowed - specify exact columns")
    
    # Check for basic SQL structure
    sql_keywords = ["SELECT", "INSERT", "UPDATE", "DELETE", "CREATE", "DROP", "ALTER"]
    if not any(keyword in sql_upper for keyword in sql_keywords):
        errors.append("No valid SQL keyword found")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors
    } 