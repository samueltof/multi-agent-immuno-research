#!/usr/bin/env python3
"""
Master TCR Test Runner

Runs all TCR testing scripts in order from basic to complex.
This orchestrates the complete testing suite for the TCR analysis system.
"""

import sys
import os
import subprocess
import time
from pathlib import Path

def print_header(title: str, level: int = 1):
    """Print formatted header"""
    if level == 1:
        print("\n" + "🧬" + "=" * 70)
        print(f"   {title}")
        print("=" * 70)
    else:
        print(f"\n{'  ' * (level-1)}📋 {title}")
        print("  " + "-" * (50 - (level-1)*2))

def run_test_script(script_path: str, description: str) -> bool:
    """Run a test script and return success status"""
    print(f"\n🚀 RUNNING: {description}")
    print(f"   Script: {script_path}")
    print("   " + "-" * 40)
    
    if not os.path.exists(script_path):
        print(f"   ❌ Script not found: {script_path}")
        return False
    
    try:
        start_time = time.time()
        
        # Run the script
        result = subprocess.run([
            sys.executable, script_path
        ], 
        capture_output=True, 
        text=True, 
        cwd=os.getcwd()
        )
        
        execution_time = time.time() - start_time
        
        # Print output
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        # Check result
        if result.returncode == 0:
            print(f"   ✅ PASSED in {execution_time:.2f}s")
            return True
        else:
            print(f"   ❌ FAILED (exit code: {result.returncode})")
            return False
            
    except Exception as e:
        print(f"   ❌ EXECUTION ERROR: {e}")
        return False

def check_prerequisites():
    """Check if all prerequisite files exist"""
    print_header("PREREQUISITE CHECK")
    
    required_files = [
        ("src/tools/tcr_analysis.py", "TCR analysis tools"),
        ("src/agents/tcr_data_team.py", "TCR data team workflow"),
        ("src/config/vdjdb.py", "VDJdb configuration"),
        ("src/agents/agents.py", "Agent definitions"),
    ]
    
    missing_files = []
    
    for file_path, description in required_files:
        if os.path.exists(file_path):
            print(f"   ✅ {description}: {file_path}")
        else:
            print(f"   ❌ {description}: {file_path} - MISSING")
            missing_files.append(file_path)
    
    if missing_files:
        print("\n⚠️  MISSING PREREQUISITES:")
        for file_path in missing_files:
            print(f"   • {file_path}")
        print("\nPlease ensure all TCR components are implemented before testing.")
        return False
    
    print("\n✅ All prerequisites found!")
    return True

def run_all_tests():
    """Run all TCR tests in sequence"""
    print_header("TCR ANALYSIS SYSTEM - COMPLETE TEST SUITE")
    print("Testing the multi-agent framework for cancer immunogenomics")
    print("From basic tool validation to complex interactive demonstrations")
    
    # Check prerequisites
    if not check_prerequisites():
        return False
    
    # Define test sequence
    tests = [
        {
            "script": "tests/test_01_tcr_tools_basic.py",
            "name": "Basic Tool Testing",
            "description": "Test individual TCR analysis tools in isolation",
            "level": "BASIC",
            "required": True
        },
        {
            "script": "tests/test_02_tcr_data_setup.py", 
            "name": "Data Setup & Environment",
            "description": "Validate data infrastructure and environment configuration",
            "level": "INTERMEDIATE",
            "required": True
        },
        {
            "script": "tests/test_03_tcr_agent_integration.py",
            "name": "Agent Integration",
            "description": "Test complete agent integration and workflows",
            "level": "ADVANCED",
            "required": True
        },
        {
            "script": "tests/test_04_interactive_demo.py",
            "name": "Interactive Demo",
            "description": "Manual testing with real agent execution",
            "level": "EXPERT",
            "required": False
        }
    ]
    
    # Track results
    results = []
    
    print_header("TEST EXECUTION SEQUENCE", 2)
    for i, test in enumerate(tests, 1):
        print(f"   {i}. [{test['level']}] {test['name']}")
        print(f"      {test['description']}")
        if not test['required']:
            print("      (Optional - requires API keys)")
    
    print("\n" + "=" * 70)
    
    # Execute tests
    for i, test in enumerate(tests, 1):
        print_header(f"TEST {i}/4: {test['name']} [{test['level']}]")
        
        success = run_test_script(test['script'], test['description'])
        results.append({
            "test": test['name'],
            "level": test['level'],
            "success": success,
            "required": test['required']
        })
        
        # Stop on required test failure
        if not success and test['required']:
            print(f"\n💥 REQUIRED TEST FAILED: {test['name']}")
            print("   Cannot proceed with remaining tests.")
            print("   Please fix the issues and try again.")
            break
        
        # Pause between tests
        if i < len(tests):
            print(f"\n⏳ Preparing for next test...")
            time.sleep(2)
    
    # Print final results
    print_header("FINAL TEST RESULTS")
    
    passed_required = 0
    total_required = 0
    passed_optional = 0
    total_optional = 0
    
    for result in results:
        status = "✅ PASS" if result['success'] else "❌ FAIL"
        req_text = "REQUIRED" if result['required'] else "OPTIONAL"
        
        print(f"   {status} [{result['level']}] {result['test']} ({req_text})")
        
        if result['required']:
            total_required += 1
            if result['success']:
                passed_required += 1
        else:
            total_optional += 1
            if result['success']:
                passed_optional += 1
    
    print("\n" + "=" * 70)
    print(f"📊 SUMMARY:")
    print(f"   Required Tests: {passed_required}/{total_required} passed")
    print(f"   Optional Tests: {passed_optional}/{total_optional} passed")
    
    # Overall assessment
    if passed_required == total_required:
        print("\n🎉 SUCCESS! TCR Analysis System is ready for production!")
        print("\n🔬 CAPABILITIES VALIDATED:")
        print("   ✅ TCR database analysis and querying")
        print("   ✅ Diversity metrics calculation") 
        print("   ✅ CDR3 motif discovery and analysis")
        print("   ✅ Repertoire comparison and biomarker identification")
        print("   ✅ Multi-agent workflow orchestration")
        
        if passed_optional > 0:
            print("   ✅ Interactive demonstration capabilities")
        
        print("\n🎯 READY FOR:")
        print("   • Cancer immunogenomics research")
        print("   • Immunotherapy response prediction")
        print("   • Immune-related adverse events (irAEs) detection")
        print("   • TCR biomarker discovery")
        print("   • Deep research in T-cell receptor datasets")
        
        return True
    else:
        print("\n⚠️  ISSUES DETECTED")
        print("   Some required tests failed. Please review and fix.")
        print("   The system is not ready for production use.")
        return False

def main():
    """Main entry point"""
    # Change to project root if running from tests directory
    if os.path.basename(os.getcwd()) == 'tests':
        os.chdir('..')
    
    # Add src to Python path
    if 'src' not in sys.path:
        sys.path.append('src')
    
    success = run_all_tests()
    
    if success:
        print("\n🚀 You can now use the TCR Analysis System for your research!")
        print("   Try running: python tests/test_04_interactive_demo.py")
    
    exit(0 if success else 1)

if __name__ == "__main__":
    main() 