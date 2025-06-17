#!/usr/bin/env python3
"""
MCP Test Runner - Run all MCP tests and status checks

This script provides an easy way to run all MCP-related tests and checks:
1. Existing isolation tests
2. Direct validation tests 
3. Comprehensive status check
4. Output display tests

Usage: uv run python tests/mcp_tests/run_all_mcp_tests.py [--quick]
"""

import asyncio
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import List, Tuple

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

class MCPTestRunner:
    """Run all MCP tests in sequence with detailed reporting."""
    
    def __init__(self, quick_mode: bool = False):
        self.quick_mode = quick_mode
        self.tests_dir = Path(__file__).parent
        self.results = {}
        self.start_time = time.time()
    
    def print_header(self, title: str):
        """Print formatted header."""
        print(f"\n{'='*80}")
        print(f"🧪 {title}")
        print(f"{'='*80}")
    
    def print_test_result(self, test_name: str, success: bool, duration: float = 0, details: str = ""):
        """Print test result."""
        status = "✅ PASS" if success else "❌ FAIL"
        duration_str = f"({duration:.1f}s)" if duration > 0 else ""
        details_str = f" - {details}" if details else ""
        print(f"{status} {test_name} {duration_str}{details_str}")
    
    async def run_python_test(self, test_name: str, script_path: Path, timeout: int = 300) -> Tuple[bool, str, float]:
        """Run a Python test script and return success status, output, and duration."""
        start_time = time.time()
        
        try:
            # Run the test script
            result = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=project_root
            )
            
            duration = time.time() - start_time
            
            if result.returncode == 0:
                return True, result.stdout, duration
            else:
                return False, result.stderr or result.stdout, duration
                
        except subprocess.TimeoutExpired:
            duration = time.time() - start_time
            return False, f"Test timed out after {timeout}s", duration
        except Exception as e:
            duration = time.time() - start_time
            return False, f"Test failed with exception: {e}", duration
    
    async def run_mcp_isolation_test(self):
        """Run MCP isolation tests."""
        print("\n🔍 Running MCP Isolation Tests...")
        script_path = self.tests_dir / "test_mcp_isolation.py"
        
        if not script_path.exists():
            self.print_test_result("MCP Isolation Test", False, 0, "Script not found")
            return False
        
        success, output, duration = await self.run_python_test("MCP Isolation Test", script_path)
        self.print_test_result("MCP Isolation Test", success, duration)
        
        if not success:
            print(f"❌ Error output:\n{output[:500]}...")
        
        self.results["isolation"] = {
            "success": success,
            "duration": duration,
            "output": output
        }
        
        return success
    
    async def run_mcp_validation_test(self):
        """Run MCP direct validation tests."""
        print("\n🔍 Running MCP Direct Validation Tests...")
        script_path = self.tests_dir / "validate_mcp_direct.py"
        
        if not script_path.exists():
            self.print_test_result("MCP Validation Test", False, 0, "Script not found")
            return False
        
        success, output, duration = await self.run_python_test("MCP Validation Test", script_path)
        self.print_test_result("MCP Validation Test", success, duration)
        
        if not success:
            print(f"❌ Error output:\n{output[:500]}...")
        
        self.results["validation"] = {
            "success": success,
            "duration": duration,
            "output": output
        }
        
        return success
    
    async def run_mcp_comprehensive_check(self):
        """Run comprehensive MCP status check."""
        print("\n🔍 Running Comprehensive MCP Status Check...")
        script_path = self.tests_dir / "comprehensive_mcp_status_check.py"
        
        if not script_path.exists():
            self.print_test_result("Comprehensive Status Check", False, 0, "Script not found")
            return False
        
        success, output, duration = await self.run_python_test("Comprehensive Status Check", script_path, timeout=600)
        self.print_test_result("Comprehensive Status Check", success, duration)
        
        if not success:
            print(f"❌ Error output:\n{output[:500]}...")
        else:
            # Show some of the output for successful comprehensive checks
            print("📊 Status Check Results:")
            lines = output.split('\n')
            for line in lines[-20:]:  # Show last 20 lines
                if line.strip():
                    print(f"   {line}")
        
        self.results["comprehensive"] = {
            "success": success,
            "duration": duration,
            "output": output
        }
        
        return success
    
    async def run_mcp_output_display(self):
        """Run MCP output display tests."""
        if self.quick_mode:
            print("\n⏩ Skipping output display tests (quick mode)")
            return True
        
        print("\n🔍 Running MCP Output Display Tests...")
        script_path = self.tests_dir / "show_mcp_outputs.py"
        
        if not script_path.exists():
            self.print_test_result("Output Display Test", False, 0, "Script not found")
            return False
        
        success, output, duration = await self.run_python_test("Output Display Test", script_path)
        self.print_test_result("Output Display Test", success, duration)
        
        if not success:
            print(f"❌ Error output:\n{output[:500]}...")
        
        self.results["output_display"] = {
            "success": success,
            "duration": duration,
            "output": output
        }
        
        return success
    
    async def run_biomedical_integration_test(self):
        """Run biomedical researcher integration test."""
        if self.quick_mode:
            print("\n⏩ Skipping biomedical integration tests (quick mode)")
            return True
        
        print("\n🔍 Running Biomedical Researcher Integration Test...")
        script_path = self.tests_dir / "test_biomedical_researcher.py"
        
        if not script_path.exists():
            self.print_test_result("Biomedical Integration Test", False, 0, "Script not found")
            return False
        
        success, output, duration = await self.run_python_test("Biomedical Integration Test", script_path)
        self.print_test_result("Biomedical Integration Test", success, duration)
        
        if not success:
            print(f"❌ Error output:\n{output[:500]}...")
        
        self.results["biomedical_integration"] = {
            "success": success,
            "duration": duration,
            "output": output
        }
        
        return success
    
    def check_environment(self):
        """Check the testing environment."""
        self.print_header("Environment Check")
        
        # Check Python version
        python_version = sys.version
        print(f"🐍 Python: {python_version}")
        
        # Check working directory
        print(f"📁 Working Directory: {os.getcwd()}")
        
        # Check project root
        print(f"📍 Project Root: {project_root}")
        
        # Check MCP servers directory
        mcps_dir = project_root / "src" / "service" / "mcps"
        print(f"🗂️  MCPs Directory: {mcps_dir}")
        print(f"   Exists: {'✅' if mcps_dir.exists() else '❌'}")
        
        # Check individual MCP servers
        mcp_servers = [
            "pubmed_mcp.py",
            "bioarxiv_mcp.py", 
            "clinicaltrialsgov_mcp.py",
            "opentargets_mcp.py",
            "drugbank_mcp.py"
        ]
        
        print(f"\n🔧 MCP Server Files:")
        for server in mcp_servers:
            server_path = mcps_dir / server
            exists = server_path.exists()
            print(f"   {server}: {'✅' if exists else '❌'}")
        
        # Check environment variables
        print(f"\n🔐 Environment Variables:")
        drugbank_key = os.getenv('DRUGBANK_API_KEY')
        print(f"   DRUGBANK_API_KEY: {'✅ Set' if drugbank_key else '❌ Not set'}")
        
        # Check dependencies
        print(f"\n📦 Dependencies:")
        try:
            import mcp
            print(f"   mcp: ✅ Available")
        except ImportError:
            print(f"   mcp: ❌ Missing")
        
        try:
            from pydantic_ai import Agent
            print(f"   pydantic_ai: ✅ Available")
        except ImportError:
            print(f"   pydantic_ai: ❌ Missing")
    
    def generate_summary_report(self):
        """Generate a summary report of all test results."""
        self.print_header("MCP Test Summary Report")
        
        total_time = time.time() - self.start_time
        print(f"🕐 Total Execution Time: {total_time:.1f}s")
        print(f"🧪 Tests Run: {len(self.results)}")
        
        successful_tests = sum(1 for r in self.results.values() if r["success"])
        failed_tests = len(self.results) - successful_tests
        
        print(f"✅ Successful: {successful_tests}")
        print(f"❌ Failed: {failed_tests}")
        
        if failed_tests == 0:
            print(f"\n🎉 ALL TESTS PASSED!")
            print("✅ All MCP servers are operational")
            print("✅ Integration tests successful")
            print("✅ Ready for production use")
        elif successful_tests > 0:
            print(f"\n⚠️  {successful_tests}/{len(self.results)} tests passed")
            print("🔧 Some tests need attention")
        else:
            print(f"\n❌ All tests failed - debugging required")
        
        # Detailed results
        print(f"\n📊 Detailed Results:")
        for test_name, result in self.results.items():
            status = "✅ PASS" if result["success"] else "❌ FAIL"
            duration = result["duration"]
            print(f"   {test_name}: {status} ({duration:.1f}s)")
        
        return failed_tests == 0
    
    async def run_all_tests(self):
        """Run all MCP tests in sequence."""
        self.print_header("MCP Test Suite Runner")
        
        mode_str = "Quick Mode" if self.quick_mode else "Full Mode"
        print(f"🎯 Running in {mode_str}")
        
        # Check environment first
        self.check_environment()
        
        # Define test sequence
        test_sequence = [
            ("MCP Isolation", self.run_mcp_isolation_test),
            ("MCP Validation", self.run_mcp_validation_test),
            ("Comprehensive Check", self.run_mcp_comprehensive_check),
        ]
        
        if not self.quick_mode:
            test_sequence.extend([
                ("Output Display", self.run_mcp_output_display),
                ("Biomedical Integration", self.run_biomedical_integration_test),
            ])
        
        # Run tests
        for test_name, test_func in test_sequence:
            try:
                print(f"\n🚀 Starting {test_name}...")
                await test_func()
            except Exception as e:
                print(f"💥 {test_name} crashed: {e}")
                self.results[test_name.lower().replace(" ", "_")] = {
                    "success": False,
                    "duration": 0,
                    "output": f"Crashed: {e}"
                }
        
        # Generate summary
        return self.generate_summary_report()


async def main():
    """Main entry point."""
    # Check for quick mode
    quick_mode = "--quick" in sys.argv
    
    runner = MCPTestRunner(quick_mode=quick_mode)
    success = await runner.run_all_tests()
    
    return success


if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️  Testing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Test runner crashed: {e}")
        sys.exit(1) 