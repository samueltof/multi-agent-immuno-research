#!/usr/bin/env python3
"""
Test script to verify the plot injection logic in python_repl.py
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.tools.python_repl import inject_plot_saving_code

def test_no_injection_when_explicit_save():
    """Test that no automatic injection occurs when explicit plt.savefig() is present"""
    
    code_with_explicit_save = """
import matplotlib.pyplot as plt
import pandas as pd

# Some plotting code
plt.figure(figsize=(10,6))
plt.plot([1,2,3,4], [1,4,2,3], marker='o')
plt.title('Test Plot')
plt.savefig('/path/to/my/custom/plot.png')
plt.show()
"""
    
    result = inject_plot_saving_code(code_with_explicit_save)
    
    print("=== TEST 1: Code with explicit plt.savefig() ===")
    print("Should NOT inject automatic saving")
    print(f"Contains 'PLOT_SAVED:': {'PLOT_SAVED:' in result}")
    print(f"Contains original savefig: {'/path/to/my/custom/plot.png' in result}")
    print(f"Number of plt.savefig calls: {result.count('plt.savefig(')}")
    
    assert 'PLOT_SAVED:' not in result, "Should not inject automatic saving when explicit saving exists"
    assert '/path/to/my/custom/plot.png' in result, "Should preserve original explicit saving"
    assert result.count('plt.savefig(') == 1, "Should have exactly one plt.savefig call (the original)"
    
    print("✅ Test 1 PASSED\n")

def test_injection_when_no_explicit_save():
    """Test that automatic injection occurs when no explicit plt.savefig() is present"""
    
    code_without_explicit_save = """
import matplotlib.pyplot as plt
import pandas as pd

# Some plotting code
plt.figure(figsize=(10,6))
plt.plot([1,2,3,4], [1,4,2,3], marker='o')
plt.title('Test Plot')
plt.show()
"""
    
    result = inject_plot_saving_code(code_without_explicit_save)
    
    print("=== TEST 2: Code without explicit plt.savefig() ===")
    print("Should inject automatic saving")
    print(f"Contains 'PLOT_SAVED:': {'PLOT_SAVED:' in result}")
    print(f"Number of plt.savefig calls: {result.count('plt.savefig(')}")
    print(f"Contains backend setup: {'matplotlib.use(' in result}")
    
    assert 'PLOT_SAVED:' in result, "Should inject automatic saving when no explicit saving exists"
    assert result.count('plt.savefig(') == 1, "Should have exactly one plt.savefig call (the injected one)"
    assert 'matplotlib.use(' in result, "Should inject backend setup"
    
    print("✅ Test 2 PASSED\n")

def test_no_injection_when_no_plots():
    """Test that no injection occurs when there are no plotting commands"""
    
    code_without_plots = """
import pandas as pd
import numpy as np

# Some data processing
df = pd.DataFrame({'a': [1,2,3], 'b': [4,5,6]})
result = df.sum()
print(result)
"""
    
    result = inject_plot_saving_code(code_without_plots)
    
    print("=== TEST 3: Code without plotting commands ===")
    print("Should NOT inject anything")
    print(f"Contains 'PLOT_SAVED:': {'PLOT_SAVED:' in result}")
    print(f"Code unchanged: {result == code_without_plots}")
    
    assert 'PLOT_SAVED:' not in result, "Should not inject anything when no plots"
    assert result == code_without_plots, "Code should remain unchanged"
    
    print("✅ Test 3 PASSED\n")

if __name__ == "__main__":
    print("Testing plot injection logic...\n")
    
    test_no_injection_when_explicit_save()
    test_injection_when_no_explicit_save() 
    test_no_injection_when_no_plots()
    
    print("🎉 All tests passed! The plot injection logic is working correctly.")
    print("\nSummary:")
    print("- ✅ No double-saving when explicit plt.savefig() exists")
    print("- ✅ Automatic saving when no explicit saving")
    print("- ✅ No injection when no plotting commands") 