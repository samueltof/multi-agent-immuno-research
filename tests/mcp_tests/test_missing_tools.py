#!/usr/bin/env python3
"""
Test Missing MCP Tools

This script focuses on testing the tools that were not tested or had parameter issues
in the comprehensive status check. It provides detailed testing for:

1. PubMed: find_by_author
2. BioRxiv: All tools with corrected parameters  
3. ClinicalTrials: get_trial_details (with valid NCT ID), find_trials_by_location
4. OpenTargets: get_target_details, get_target_associated_diseases, get_disease_associated_targets

Usage: uv run python tests/mcp_tests/test_missing_tools.py
"""

import asyncio
import sys
import time
from pathlib import Path
from typing import Dict, Any

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

class MissingToolsTester:
    """Test the tools that were previously untested or had parameter issues."""
    
    def __init__(self):
        self.mcps_dir = project_root / "src" / "service" / "mcps"
        self.results = {}
        self.start_time = time.time()
    
    def print_header(self, title: str):
        """Print formatted header."""
        print(f"\n{'='*80}")
        print(f"🧪 {title}")
        print(f"{'='*80}")
    
    def print_test_header(self, tool_name: str, server_name: str):
        """Print test header for individual tools."""
        print(f"\n🔧 Testing {server_name}: {tool_name}")
        print("-" * 60)
    
    async def test_tool(self, session: ClientSession, tool_name: str, test_input: Dict[str, Any], server_name: str) -> Dict[str, Any]:
        """Test a single tool with the given input."""
        start_time = time.time()
        
        try:
            print(f"📥 Input: {test_input}")
            
            response = await session.call_tool(tool_name, test_input)
            execution_time = time.time() - start_time
            
            # Format response content
            response_content = []
            if hasattr(response, 'content'):
                for content in response.content:
                    if hasattr(content, 'text'):
                        response_content.append(content.text)
                    else:
                        response_content.append(str(content))
            
            response_text = "\n".join(response_content)
            
            print(f"📤 Output ({execution_time:.2f}s):")
            # Show first 300 characters of output
            display_text = response_text[:300] + "..." if len(response_text) > 300 else response_text
            print(f"   {display_text}")
            print(f"✅ SUCCESS")
            
            return {
                "status": "SUCCESS",
                "input": test_input,
                "output": response_text,
                "execution_time": execution_time,
                "output_length": len(response_text)
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            print(f"❌ FAILED: {e}")
            
            return {
                "status": "FAILED", 
                "input": test_input,
                "error": str(e),
                "execution_time": execution_time
            }
    
    async def test_pubmed_missing_tools(self):
        """Test PubMed tools that were not tested."""
        self.print_header("PubMed Missing Tools Test")
        
        server_params = StdioServerParameters(
            command="python",
            args=[str(self.mcps_dir / "pubmed_mcp.py")]
        )
        
        results = []
        
        try:
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    
                    # Test find_by_author
                    self.print_test_header("find_by_author", "PubMed")
                    result = await self.test_tool(
                        session, 
                        "find_by_author",
                        {"author": "Fauci AS", "max_results": 3},
                        "PubMed"
                    )
                    results.append(("find_by_author", result))
                    
        except Exception as e:
            print(f"❌ PubMed server connection failed: {e}")
            results.append(("find_by_author", {"status": "SERVER_ERROR", "error": str(e)}))
        
        self.results["PubMed"] = results
        return results
    
    async def test_biorxiv_missing_tools(self):
        """Test BioRxiv tools with corrected parameters."""
        self.print_header("BioRxiv Missing Tools Test (Corrected Parameters)")
        
        server_params = StdioServerParameters(
            command="python",
            args=[str(self.mcps_dir / "bioarxiv_mcp.py")]
        )
        
        results = []
        
        try:
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    
                    # Test search_preprints with correct parameters
                    self.print_test_header("search_preprints", "BioRxiv")
                    result = await self.test_tool(
                        session,
                        "search_preprints",
                        {
                            "server": "biorxiv",
                            "category": "bioinformatics",
                            "start_date": "2024-01-01", 
                            "end_date": "2024-01-31",
                            "max_results": 3
                        },
                        "BioRxiv"
                    )
                    results.append(("search_preprints", result))
                    
                    # Test get_preprint_by_doi with correct parameters
                    self.print_test_header("get_preprint_by_doi", "BioRxiv")
                    result = await self.test_tool(
                        session,
                        "get_preprint_by_doi",
                        {
                            "server": "biorxiv",
                            "doi": "10.1101/2023.12.01.000001"
                        },
                        "BioRxiv"
                    )
                    results.append(("get_preprint_by_doi", result))
                    
                    # Test find_published_version with correct parameters
                    self.print_test_header("find_published_version", "BioRxiv")
                    result = await self.test_tool(
                        session,
                        "find_published_version",
                        {
                            "server": "biorxiv",
                            "doi": "10.1101/2023.12.01.000001"
                        },
                        "BioRxiv"
                    )
                    results.append(("find_published_version", result))
                    
                    # Test get_recent_preprints
                    self.print_test_header("get_recent_preprints", "BioRxiv")
                    result = await self.test_tool(
                        session,
                        "get_recent_preprints",
                        {
                            "server": "biorxiv",
                            "days": 7,
                            "max_results": 3,
                            "category": "bioinformatics"
                        },
                        "BioRxiv"
                    )
                    results.append(("get_recent_preprints", result))
                    
        except Exception as e:
            print(f"❌ BioRxiv server connection failed: {e}")
            results.append(("all_tools", {"status": "SERVER_ERROR", "error": str(e)}))
        
        self.results["BioRxiv"] = results
        return results
    
    async def test_clinicaltrials_missing_tools(self):
        """Test ClinicalTrials tools that were not tested."""
        self.print_header("ClinicalTrials Missing Tools Test")
        
        server_params = StdioServerParameters(
            command="python",
            args=[str(self.mcps_dir / "clinicaltrialsgov_mcp.py")]
        )
        
        results = []
        
        try:
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    
                    # Test get_trial_details with a valid NCT ID
                    self.print_test_header("get_trial_details", "ClinicalTrials")
                    result = await self.test_tool(
                        session,
                        "get_trial_details",
                        {"nct_id": "NCT02015429"},  # Valid NCT ID from previous results
                        "ClinicalTrials"
                    )
                    results.append(("get_trial_details", result))
                    
                    # Test find_trials_by_location
                    self.print_test_header("find_trials_by_location", "ClinicalTrials")
                    result = await self.test_tool(
                        session,
                        "find_trials_by_location",
                        {"location": "Boston, MA", "max_results": 3},
                        "ClinicalTrials"
                    )
                    results.append(("find_trials_by_location", result))
                    
        except Exception as e:
            print(f"❌ ClinicalTrials server connection failed: {e}")
            results.append(("all_tools", {"status": "SERVER_ERROR", "error": str(e)}))
        
        self.results["ClinicalTrials"] = results
        return results
    
    async def test_opentargets_missing_tools(self):
        """Test OpenTargets tools that were not tested."""
        self.print_header("OpenTargets Missing Tools Test")
        
        server_params = StdioServerParameters(
            command="python",
            args=[str(self.mcps_dir / "opentargets_mcp.py")]
        )
        
        results = []
        
        try:
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    
                    # Test get_target_details
                    self.print_test_header("get_target_details", "OpenTargets")
                    result = await self.test_tool(
                        session,
                        "get_target_details",
                        {"target_id": "ENSG00000142192"},  # APP gene
                        "OpenTargets"
                    )
                    results.append(("get_target_details", result))
                    
                    # Test get_target_associated_diseases
                    self.print_test_header("get_target_associated_diseases", "OpenTargets")
                    result = await self.test_tool(
                        session,
                        "get_target_associated_diseases",
                        {"target_id": "ENSG00000142192", "max_results": 3},
                        "OpenTargets"
                    )
                    results.append(("get_target_associated_diseases", result))
                    
                    # Test get_disease_associated_targets
                    self.print_test_header("get_disease_associated_targets", "OpenTargets")
                    result = await self.test_tool(
                        session,
                        "get_disease_associated_targets",
                        {"disease_id": "MONDO_0004992", "max_results": 3},  # cancer
                        "OpenTargets"
                    )
                    results.append(("get_disease_associated_targets", result))
                    
        except Exception as e:
            print(f"❌ OpenTargets server connection failed: {e}")
            results.append(("all_tools", {"status": "SERVER_ERROR", "error": str(e)}))
        
        self.results["OpenTargets"] = results
        return results
    
    def generate_summary_report(self):
        """Generate a summary report of the missing tools tests."""
        self.print_header("Missing Tools Test Summary Report")
        
        total_time = time.time() - self.start_time
        print(f"🕐 Total Test Time: {total_time:.1f}s")
        
        total_tests = 0
        successful_tests = 0
        
        for server_name, server_results in self.results.items():
            print(f"\n📊 {server_name} Results:")
            
            for tool_name, result in server_results:
                total_tests += 1
                status = result.get("status", "UNKNOWN")
                
                if status == "SUCCESS":
                    successful_tests += 1
                    exec_time = result.get("execution_time", 0)
                    output_len = result.get("output_length", 0)
                    print(f"   ✅ {tool_name}: SUCCESS ({exec_time:.2f}s, {output_len} chars)")
                elif status == "FAILED":
                    error = result.get("error", "Unknown error")
                    print(f"   ❌ {tool_name}: FAILED - {error[:100]}...")
                else:
                    print(f"   ⚠️  {tool_name}: {status}")
        
        print(f"\n🎯 Overall Results:")
        print(f"Total Tests: {total_tests}")
        print(f"Successful: {successful_tests}")
        print(f"Failed: {total_tests - successful_tests}")
        
        if total_tests > 0:
            success_rate = (successful_tests / total_tests) * 100
            print(f"Success Rate: {success_rate:.1f}%")
        
        if successful_tests == total_tests:
            print(f"\n🎉 ALL MISSING TOOLS NOW WORKING!")
            print("✅ Previously untested tools are now verified")
            print("✅ Parameter issues have been resolved")
        elif successful_tests > 0:
            print(f"\n✅ {successful_tests}/{total_tests} missing tools now working")
            print("🔧 Some tools may need further debugging")
        else:
            print(f"\n❌ All missing tools still need attention")
        
        return successful_tests == total_tests
    
    async def run_all_missing_tool_tests(self):
        """Run all missing tool tests."""
        self.print_header("Testing Previously Untested MCP Tools")
        
        print("🎯 Focus: Tools that were not tested or had parameter issues")
        print("📝 Goal: Verify all 18 biomedical tools are working")
        
        # Run tests for each server
        await self.test_pubmed_missing_tools()
        await self.test_biorxiv_missing_tools()
        await self.test_clinicaltrials_missing_tools()
        await self.test_opentargets_missing_tools()
        
        # Generate final summary
        return self.generate_summary_report()


async def main():
    """Main entry point."""
    print("🚀 Starting Missing Tools Test...")
    
    tester = MissingToolsTester()
    success = await tester.run_all_missing_tool_tests()
    
    print(f"\n🏁 Missing tools test complete!")
    return success


if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️  Testing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Testing crashed: {e}")
        sys.exit(1)