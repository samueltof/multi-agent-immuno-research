from langchain_core.tools import tool
import pandas as pd
from typing import Optional, List, Dict, Any
import logging
import os
import uuid
from datetime import datetime

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
def execute_sql_query_and_save(query: str, description: str = "") -> str:
    """Executes a SQL query and saves the full results to a CSV file for downstream processing.
    
    This tool provides a hybrid approach: shows meaningful summary and preview in the message
    while saving complete data to file for detailed analysis by specialized agents.
    
    Args:
        query: The SQL query string to be executed.
        description: Optional description of what the query does (for file naming).
        
    Returns:
        A string containing summary, key insights, preview, and file path information.
    """
    try:
        logger.info(f"🛠️ Executing SQL query and saving results: {query[:100]}...")
        
        # Get database manager
        db_manager = get_database_manager()
        
        # Execute query and get results as DataFrame
        result_df = db_manager.execute_query_df(query)
        
        if result_df.empty:
            return "Query executed successfully but returned no results."
        
        # Create outputs directory if it doesn't exist
        outputs_dir = "outputs"
        os.makedirs(outputs_dir, exist_ok=True)
        
        # Generate a unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        query_id = str(uuid.uuid4())[:8]
        
        # Clean description for filename
        if description:
            clean_desc = "".join(c for c in description if c.isalnum() or c in (' ', '_', '-')).rstrip()
            clean_desc = clean_desc.replace(' ', '_')[:50]  # Max 50 chars
            filename = f"query_results_{clean_desc}_{timestamp}_{query_id}.csv"
        else:
            filename = f"query_results_{timestamp}_{query_id}.csv"
        
        file_path = os.path.join(outputs_dir, filename)
        
        # Save the DataFrame to CSV
        result_df.to_csv(file_path, index=False)
        
        # Generate meaningful summary and insights
        total_rows = len(result_df)
        total_cols = len(result_df.columns)
        
        # Provide intelligent preview based on dataset size
        if total_rows <= 20:
            # Small dataset: show all rows
            preview_rows = total_rows
            preview_note = "(complete dataset)"
            preview = result_df.to_string(index=False)
        elif total_rows <= 100:
            # Medium dataset: show first 20 rows
            preview_rows = 20
            preview_note = f"(showing first {preview_rows} rows)"
            preview = result_df.head(preview_rows).to_string(index=False)
        else:
            # Large dataset: show first 15 rows + summary statistics
            preview_rows = 15
            preview_note = f"(showing first {preview_rows} rows)"
            preview = result_df.head(preview_rows).to_string(index=False)
        
        # Generate key insights for numeric columns
        insights = []
        numeric_cols = result_df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            insights.append("\n📊 **Key Insights:**")
            for col in numeric_cols[:3]:  # Limit to first 3 numeric columns
                col_stats = result_df[col].describe()
                insights.append(f"- {col}: Mean={col_stats['mean']:.2f}, Std={col_stats['std']:.2f}, Range=[{col_stats['min']:.2f}, {col_stats['max']:.2f}]")
        
        # Check for categorical patterns
        categorical_cols = result_df.select_dtypes(include=['object']).columns
        if len(categorical_cols) > 0 and len(categorical_cols) <= 3:
            insights.append("\n📈 **Data Distribution:**")
            for col in categorical_cols:
                unique_count = result_df[col].nunique()
                if unique_count <= 10:  # Only show for columns with reasonable number of categories
                    top_values = result_df[col].value_counts().head(3)
                    insights.append(f"- {col}: {unique_count} unique values, top: {dict(top_values)}")
        
        insights_text = "\n".join(insights) if insights else ""
        
        # Create comprehensive result string
        result_str = f"""Query executed successfully and results saved to file.

📋 **Summary:**
- Total rows: {total_rows:,}
- Total columns: {total_cols}
- Columns: {', '.join(result_df.columns.tolist())}

🗂️ **DATASET FILE #{query_id}**: `{file_path}`
📁 **FULL PATH**: {os.path.abspath(file_path)}
🏷️ **FILE ID**: {query_id}
📝 **DESCRIPTION**: {description if description else 'Data analysis results'}{insights_text}

📄 **Data Preview** {preview_note}:
{preview}

💾 **For Detailed Analysis:**
The complete dataset ({total_rows:,} rows) has been saved to '{file_path}' and can be loaded by specialized analysis agents using file loading tools.

🔧 **Next Steps for Analysis Agents:**
- Use `read_csv_file('{file_path}')` to inspect the dataset structure
- Use `load_csv_as_dataframe('{file_path}')` to get loading code for the complete dataset
- Reference this dataset as "File #{query_id}" in subsequent analysis"""
        
        if total_rows > 100:
            result_str += f"\n\n⚠️  **Note**: This message shows a preview for context. The complete dataset with all {total_rows:,} rows is available in the saved file for comprehensive analysis."
        
        logger.info(f"🔘 SQL query executed successfully, {len(result_df)} rows saved to {file_path}")
        return result_str
        
    except Exception as e:
        error_msg = f"Error executing SQL query and saving results: {str(e)}"
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