import asyncio
import logging
import os
import uuid
from pathlib import Path
from typing import Annotated
from datetime import datetime
from langchain_core.tools import tool
from langchain_sandbox import PyodideSandbox
from langchain_experimental.utilities import PythonREPL
from .decorators import log_io

logger = logging.getLogger(__name__)

# Create plots directory
PLOTS_DIR = Path("outputs/plots")
PLOTS_DIR.mkdir(parents=True, exist_ok=True)

def inject_plot_saving_code(code: str) -> str:
    """Inject plot saving code into Python code that uses matplotlib"""
    # Check if the code contains matplotlib plotting commands
    plot_commands = ['plt.show()', 'plt.plot(', 'plt.bar(', 'plt.scatter(', 'plt.hist(', 'plt.barh(']
    
    if any(cmd in code for cmd in plot_commands):
        # Generate a unique filename
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

# Global execution instances (lazy-loaded)
_sandbox = None
_repl_fallback = None
_use_fallback = False

def get_executor():
    """Get or create the code execution instance (sandbox preferred, REPL fallback)"""
    global _sandbox, _repl_fallback, _use_fallback
    
    if _use_fallback:
        # Use REPL fallback
        if _repl_fallback is None:
            _repl_fallback = PythonREPL()
            logger.info("Using PythonREPL fallback for code execution")
        return _repl_fallback
    
    if _sandbox is None:
        try:
            # Ensure Deno is in PATH by adding common Deno installation paths
            import subprocess
            import os
            
            # Check current PATH
            current_path = os.environ.get('PATH', '')
            logger.info(f"Current PATH: {current_path}")
            
            # Common Deno installation paths
            deno_paths = [
                os.path.expanduser('~/.deno/bin'),
                '/usr/local/bin',
                '/opt/homebrew/bin',
            ]
            
            # Add Deno paths to PATH if not already present
            path_parts = current_path.split(':')
            for deno_path in deno_paths:
                if deno_path not in path_parts and os.path.exists(deno_path):
                    os.environ['PATH'] = f"{deno_path}:{current_path}"
                    logger.info(f"Added {deno_path} to PATH")
                    break
            
            # Try to find deno executable
            try:
                result = subprocess.run(['which', 'deno'], capture_output=True, text=True, check=True)
                deno_path = result.stdout.strip()
                logger.info(f"Found deno at: {deno_path}")
            except subprocess.CalledProcessError:
                logger.warning("Could not find deno with 'which' command")
            
            _sandbox = PyodideSandbox(
                # Allow network access for package installation
                allow_net=True,
                # Make it stateful to persist variables between executions
                stateful=True
            )
            logger.info("Successfully created PyodideSandbox instance")
        except Exception as e:
            logger.warning(f"Failed to create PyodideSandbox: {e}")
            logger.info("Falling back to PythonREPL for code execution")
            _use_fallback = True
            if _repl_fallback is None:
                _repl_fallback = PythonREPL()
            return _repl_fallback
    
    return _sandbox

@tool
@log_io
def python_sandbox_tool(
    code: Annotated[
        str, "The python code to execute to do further analysis or calculation."
    ],
):
    """Use this to execute python code in a secure sandbox environment for data analysis or calculation. 
    If you want to see the output of a value, you should print it out with `print(...)`. This is visible to the user. 
    Plots will be automatically saved and displayed. Variables persist between executions."""
    logger.info("Executing Python code in secure sandbox")
    
    # Inject plot saving code
    modified_code = inject_plot_saving_code(code)
    
    async def execute_code():
        try:
            # Get the executor instance (sandbox or REPL fallback)
            executor = get_executor()
            
            # Execute based on executor type
            if isinstance(executor, PythonREPL):
                # Use REPL fallback (synchronous)
                result_output = executor.run(modified_code)
                logger.info("Code execution successful using REPL fallback")
                
                # Extract plot paths from output
                plot_paths = extract_plot_paths(result_output)
                
                # Format result with plot information
                result_str = f"Successfully executed:\n```python\n{code}\n```\nOutput: {result_output}"
                
                if plot_paths:
                    result_str += f"\n\nPlots generated:\n"
                    for plot_path in plot_paths:
                        result_str += f"- {plot_path}\n"
                
                return result_str
            else:
                # Use PyodideSandbox (async)
                result = await executor.execute(modified_code)
            logger.info("Sandbox code execution successful")
            
            # Extract the result content according to the CodeExecutionResult structure
            output = ""
            if result.stdout:
                output += result.stdout
            if result.stderr:
                output += f"\nSTDERR: {result.stderr}"
            if result.result is not None:
                output += f"\nResult: {result.result}"
            
            # Check execution status
            if result.status != 'success':
                return f"Execution failed with status: {result.status}\nOutput: {output}"
            
            # Extract plot paths from output
            plot_paths = extract_plot_paths(output)
            
            # Format result with plot information
            result_str = f"Successfully executed:\n```python\n{code}\n```\nOutput: {output}"
            
            if plot_paths:
                result_str += f"\n\nPlots generated:\n"
                for plot_path in plot_paths:
                    result_str += f"- {plot_path}\n"
            
            return result_str
            
        except Exception as e:
            error_msg = f"Failed to execute in sandbox. Error: {repr(e)}"
            logger.error(error_msg)
            return error_msg
    
    # Run the async function
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(execute_code()) 