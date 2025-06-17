import pytest
import asyncio
from pathlib import Path
from src.tools.python_sandbox import python_sandbox_tool

class TestPythonSandbox:
    
    def test_basic_execution(self):
        """Test basic Python code execution in sandbox"""
        code = "print('Hello from sandbox!')\nresult = 2 + 3\nprint(f'Result: {result}')"
        
        result = python_sandbox_tool.invoke(code)
        
        assert "Hello from sandbox!" in result
        assert "Result: 5" in result
        assert "Successfully executed:" in result
    
    def test_data_analysis(self):
        """Test data analysis capabilities"""
        code = """
import pandas as pd
import numpy as np

# Create sample data
data = {'A': [1, 2, 3, 4, 5], 'B': [10, 20, 30, 40, 50]}
df = pd.DataFrame(data)

print("DataFrame:")
print(df)
print(f"Sum of column A: {df['A'].sum()}")
print(f"Mean of column B: {df['B'].mean()}")
"""
        
        result = python_sandbox_tool.invoke(code)
        
        assert "DataFrame:" in result
        assert "Sum of column A: 15" in result
        assert "Mean of column B: 30.0" in result
    
    def test_matplotlib_plotting(self):
        """Test matplotlib plotting with automatic saving"""
        code = """
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2*np.pi, 100)
y = np.sin(x)

plt.figure(figsize=(8, 6))
plt.plot(x, y)
plt.title('Sine Wave')
plt.xlabel('x')
plt.ylabel('sin(x)')
plt.show()
"""
        
        result = python_sandbox_tool.invoke(code)
        
        assert "Successfully executed:" in result
        assert "Plots generated:" in result or "PLOT_SAVED:" in result
    
    def test_error_handling(self):
        """Test error handling for invalid code"""
        code = "invalid_function_that_doesnt_exist()"
        
        result = python_sandbox_tool.invoke(code)
        
        assert "Failed to execute in sandbox" in result or "Error" in result
    
    def test_stateful_execution(self):
        """Test that variables persist between executions"""
        # First execution - define a variable
        code1 = "x = 42\nprint(f'x = {x}')"
        result1 = python_sandbox_tool.invoke(code1)
        
        assert "x = 42" in result1
        
        # Second execution - use the previously defined variable
        code2 = "y = x * 2\nprint(f'y = {y}')"
        result2 = python_sandbox_tool.invoke(code2)
        
        assert "y = 84" in result2 