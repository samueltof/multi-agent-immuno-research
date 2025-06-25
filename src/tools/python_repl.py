import logging
import os
import re
from pathlib import Path
from typing import Annotated
from langchain_core.tools import tool
from langchain_experimental.utilities import PythonREPL
from .decorators import log_io

# Initialize REPL and logger
repl = PythonREPL()
logger = logging.getLogger(__name__)

# Create plots directory
PLOTS_DIR = Path("outputs/plots")
PLOTS_DIR.mkdir(parents=True, exist_ok=True)

def inject_plot_saving_code(code: str) -> str:
    """Inject plot saving code into Python code that uses matplotlib"""
    # Check if the code contains matplotlib plotting commands
    plot_commands = ['plt.show()', 'plt.plot(', 'plt.bar(', 'plt.scatter(', 'plt.hist(', 'plt.barh(']
    
    if any(cmd in code for cmd in plot_commands):
        # Check if the code already contains explicit plt.savefig() calls
        if 'plt.savefig(' in code:
            # Code already has explicit saving, don't inject automatic saving
            # Just ensure proper backend setup if needed
            if 'matplotlib.pyplot' in code or 'import matplotlib' in code:
                if 'matplotlib.use(' not in code:
                    backend_code = '''
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
'''
                    # Add backend setting at the beginning if not already present
                    code = backend_code + code
            return code
        
        # No explicit saving found, proceed with automatic injection
        # Generate a unique filename
        import uuid
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plot_filename = f"plot_{timestamp}_{uuid.uuid4().hex[:8]}.png"
        plot_path = PLOTS_DIR / plot_filename
        
        # Replace plt.show() with plt.savefig() and add import if needed
        modified_code = code
        
        # Add matplotlib import if not present
        if 'import matplotlib.pyplot as plt' not in modified_code and 'plt.' in modified_code:
            modified_code = 'import matplotlib.pyplot as plt\n' + modified_code
        
        # Add backend setting for headless environment
        if 'matplotlib.pyplot' in modified_code or 'import matplotlib' in modified_code:
            backend_code = '''
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
'''
            modified_code = backend_code + modified_code
        
        # Replace plt.show() with plt.savefig()
        if 'plt.show()' in modified_code:
            modified_code = modified_code.replace(
                'plt.show()', 
                f'plt.savefig("{plot_path}", dpi=300, bbox_inches="tight")\nprint(f"PLOT_SAVED: {plot_path}")'
            )
        else:
            # If no plt.show(), add savefig at the end
            modified_code += f'\nplt.savefig("{plot_path}", dpi=300, bbox_inches="tight")\nprint(f"PLOT_SAVED: {plot_path}")'
        
        return modified_code
    
    return code

def extract_plot_paths(output: str) -> list:
    """Extract plot file paths from the execution output"""
    plot_paths = []
    for line in output.split('\n'):
        if line.startswith('PLOT_SAVED: '):
            plot_path = line.replace('PLOT_SAVED: ', '').strip()
            if os.path.exists(plot_path):
                plot_paths.append(plot_path)
    return plot_paths

@tool
@log_io
def python_repl_tool(
    code: Annotated[
        str, "The python code to execute to do further analysis or calculation."
    ],
):
    """Use this to execute python code and do data analysis or calculation. If you want to see the output of a value,
    you should print it out with `print(...)`. This is visible to the user. Plots will be automatically saved and displayed."""
    logger.info("Executing Python code")
    
    # Inject plot saving code
    modified_code = inject_plot_saving_code(code)
    
    try:
        result = repl.run(modified_code)
        logger.info("Code execution successful")
        
        # Extract plot paths from output
        plot_paths = extract_plot_paths(result)
        
        # Format result with plot information
        result_str = f"Successfully executed:\n```python\n{code}\n```\nStdout: {result}"
        
        if plot_paths:
            result_str += f"\n\nPlots generated:\n"
            for plot_path in plot_paths:
                result_str += f"PLOT_SAVED: {plot_path}\n"
        
        return result_str
        
    except BaseException as e:
        error_msg = f"Failed to execute. Error: {repr(e)}"
        logger.error(error_msg)
        return error_msg
