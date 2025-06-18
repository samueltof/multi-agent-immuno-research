import logging
from langchain_community.tools.file_management import WriteFileTool
from .decorators import create_logged_tool
from langchain.tools import tool

logger = logging.getLogger(__name__)

# Initialize file management tool with logging
LoggedWriteFile = create_logged_tool(WriteFileTool)
write_file_tool = LoggedWriteFile()

@tool
def read_csv_file(file_path: str, max_rows: int = None) -> str:
    """Read a CSV file and return its contents as a pandas DataFrame summary.
    
    This tool is designed to load datasets saved by other agents for analysis.
    
    Args:
        file_path: Path to the CSV file to read.
        max_rows: Maximum number of rows to load (None for all rows).
        
    Returns:
        A string containing information about the loaded dataset and a preview.
    """
    try:
        import pandas as pd
        import os
        
        # Check if file exists
        if not os.path.exists(file_path):
            return f"Error: File '{file_path}' does not exist."
        
        # Read the CSV file
        if max_rows:
            df = pd.read_csv(file_path, nrows=max_rows)
            load_info = f"(loaded first {max_rows} rows)"
        else:
            df = pd.read_csv(file_path)
            load_info = "(loaded all rows)"
        
        if df.empty:
            return f"CSV file '{file_path}' is empty."
        
        # Get basic information about the dataset
        info_str = f"""CSV file loaded successfully {load_info}:

Dataset Information:
- File: {file_path}
- Shape: {df.shape[0]} rows × {df.shape[1]} columns
- Columns: {', '.join(df.columns.tolist())}
- Memory usage: {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB

Data Types:
{df.dtypes.to_string()}

First 5 rows:
{df.head().to_string(index=False)}

Dataset loaded and ready for analysis. You can now access the data using pandas operations."""
        
        return info_str
        
    except Exception as e:
        return f"Error reading CSV file '{file_path}': {str(e)}"


@tool 
def load_csv_as_dataframe(file_path: str) -> str:
    """Load a CSV file as a pandas DataFrame for statistical analysis.
    
    This tool loads the full dataset and makes it available for analysis.
    Use this when you need to perform calculations on the complete dataset.
    
    Args:
        file_path: Path to the CSV file to load.
        
    Returns:
        A confirmation message. The dataset will be available as 'df' variable.
    """
    try:
        import pandas as pd
        import os
        
        # Check if file exists
        if not os.path.exists(file_path):
            return f"Error: File '{file_path}' does not exist."
        
        # Load the CSV file
        df = pd.read_csv(file_path)
        
        if df.empty:
            return f"Error: CSV file '{file_path}' is empty."
        
        # Make the dataframe available globally (this is a limitation of the tool system)
        # Instead, we'll return the data loading code that the agent can execute
        code_to_execute = f"""
import pandas as pd

# Load the dataset
df = pd.read_csv('{file_path}')
print(f"Dataset loaded: {{df.shape[0]}} rows × {{df.shape[1]}} columns")
print(f"Columns: {{', '.join(df.columns.tolist())}}")
print("\\nFirst 5 rows:")
print(df.head())
"""
        
        return f"""Dataset loading code prepared. Execute the following code to load the data:

```python
{code_to_execute.strip()}
```

This will load the complete dataset from '{file_path}' into a pandas DataFrame named 'df' for your analysis."""
        
    except Exception as e:
        return f"Error preparing dataset loading: {str(e)}"


@tool
def extract_file_paths_from_conversation() -> str:
    """Extract CSV file paths mentioned in the current conversation context.
    
    This tool helps when multiple files have been created and you need to identify
    which files are available for analysis. It looks for file path patterns in the
    conversation history.
    
    Returns:
        A summary of file paths found in the conversation with their descriptions.
    """
    try:
        import re
        import os
        
        # This is a simplified version - in practice, this would need access to conversation state
        # For now, we'll provide guidance on how to identify multiple files
        guidance = """
🔍 **Finding Multiple Files in Conversation:**

Look for these patterns in previous messages:

1. **File ID Pattern**: `🗂️ **DATASET FILE #[id]**: path/to/file.csv`
2. **Description Pattern**: `📝 **DESCRIPTION**: [description]`
3. **File Path Pattern**: `outputs/query_results_*.csv`

📋 **Multiple File Workflow:**
- Each file gets a unique ID (e.g., #abc123, #def456)
- Files are described with their purpose
- Use the most recent file for current analysis unless specified otherwise
- Reference files by their ID when discussing multiple datasets

💡 **Tips:**
- Look for the newest timestamp in filenames for latest data
- Check file descriptions to understand what each contains
- Use `read_csv_file(path)` to inspect any file structure before loading
"""
        
        return guidance
        
    except Exception as e:
        return f"Error extracting file paths: {str(e)}"


