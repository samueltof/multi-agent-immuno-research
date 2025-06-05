#!/usr/bin/env python3
"""
Comprehensive MCP Server Isolation Tests

This script tests each biomedical MCP server individually using official MCP testing methods:
1. Direct stdio client connections
2. Tool enumeration and testing
3. Individual server validation

Based on official MCP documentation patterns.
"""

import asyncio
import os
import sys
import subprocess
from pathlib import Path
from typing import List, Dict, Any

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

class MCPServerTester:
    """Test individual MCP servers in isolation."""
    
    def __init__(self, mcps_dir: Path):
        self.mcps_dir = mcps_dir
        self.results = {}
    
    async def test_server_initialization(self, server_name: str, server_script: str) -> Dict[str, Any]:
        """Test if a server can initialize and respond to basic requests."""
        print(f"\n{'='*60}")
        print(f"Testing {server_name} Server Initialization")
        print(f"{'='*60}")
        
        server_path = self.mcps_dir / server_script
        if not server_path.exists():
            return {
                "status": "FAIL",
                "error": f"Server script not found: {server_path}",
                "tools": [],
                "resources": [],
                "prompts": []
            }
        
        # Test server startup and basic functionality
        server_params = StdioServerParameters(
            command="python",
            args=[str(server_path)],
            env=os.environ.copy()
        )
        
        try:
            print(f"📡 Connecting to {server_name} server...")
            
            async with stdio_client(server_params) as (read, write):
                print(f"✓ Connection established")
                
                async with ClientSession(read, write) as session:
                    print(f"✓ Session created")
                    
                    # Initialize the connection
                    await session.initialize()
                    print(f"✓ Session initialized")
                    
                    # Test listing tools
                    try:
                        tools_response = await session.list_tools()
                        tools = tools_response.tools if hasattr(tools_response, 'tools') else []
                        print(f"✓ Found {len(tools)} tools")
                        for tool in tools[:3]:  # Show first 3
                            print(f"  - {tool.name}: {tool.description[:60]}...")
                        if len(tools) > 3:
                            print(f"  ... and {len(tools) - 3} more tools")
                    except Exception as e:
                        print(f"⚠ Tool listing failed: {e}")
                        tools = []
                    
                    # Test listing resources  
                    try:
                        resources_response = await session.list_resources()
                        resources = resources_response.resources if hasattr(resources_response, 'resources') else []
                        print(f"✓ Found {len(resources)} resources")
                    except Exception as e:
                        print(f"⚠ Resource listing failed: {e}")
                        resources = []
                    
                    # Test listing prompts
                    try:
                        prompts_response = await session.list_prompts()
                        prompts = prompts_response.prompts if hasattr(prompts_response, 'prompts') else []
                        print(f"✓ Found {len(prompts)} prompts")
                    except Exception as e:
                        print(f"⚠ Prompt listing failed: {e}")
                        prompts = []
                    
                    # Test a simple tool call if tools are available
                    tool_test_result = None
                    if tools:
                        try:
                            # Try the first available tool with minimal parameters
                            first_tool = tools[0]
                            print(f"🔧 Testing tool: {first_tool.name}")
                            
                            # Prepare minimal arguments based on common patterns
                            test_args = self._get_test_args_for_tool(first_tool.name, server_name)
                            
                            if test_args is not None:
                                result = await session.call_tool(first_tool.name, test_args)
                                tool_test_result = f"SUCCESS: {str(result.content)[:100]}..."
                                print(f"✓ Tool test successful: {tool_test_result}")
                            else:
                                tool_test_result = "SKIPPED: No suitable test arguments"
                                print(f"⚠ Tool test skipped: complex arguments required")
                        except Exception as e:
                            tool_test_result = f"FAILED: {str(e)}"
                            print(f"✗ Tool test failed: {e}")
                    
                    return {
                        "status": "SUCCESS",
                        "tools": [{"name": t.name, "description": t.description} for t in tools],
                        "resources": [{"uri": r.uri, "name": r.name} for r in resources] if resources else [],
                        "prompts": [{"name": p.name, "description": p.description} for p in prompts] if prompts else [],
                        "tool_test": tool_test_result,
                        "server_responsive": True
                    }
                    
        except Exception as e:
            print(f"✗ Server test failed: {e}")
            return {
                "status": "FAIL",
                "error": str(e),
                "tools": [],
                "resources": [],
                "prompts": [],
                "server_responsive": False
            }
    
    def _get_test_args_for_tool(self, tool_name: str, server_name: str) -> Dict[str, Any] | None:
        """Get appropriate test arguments for common biomedical tools."""
        tool_name_lower = tool_name.lower()
        
        # PubMed tools
        if 'pubmed' in tool_name_lower and 'search' in tool_name_lower:
            return {"query": "COVID-19", "max_results": 3}
        elif 'pubmed' in tool_name_lower and 'abstract' in tool_name_lower:
            return {"pmid": "34567890"}  # Example PMID
        
        # BioRxiv tools
        elif 'biorxiv' in tool_name_lower or 'preprint' in tool_name_lower:
            if 'search' in tool_name_lower:
                return {"query": "gene therapy", "max_results": 3}
            elif 'doi' in tool_name_lower:
                return {"doi": "10.1101/2023.01.01.000000"}  # Example DOI
        
        # ClinicalTrials tools
        elif 'clinical' in tool_name_lower:
            if 'search' in tool_name_lower:
                return {"query": "cancer", "max_results": 3}
            elif 'condition' in tool_name_lower:
                return {"condition": "diabetes"}
        
        # OpenTargets tools
        elif 'target' in tool_name_lower or 'opentargets' in tool_name_lower:
            if 'search' in tool_name_lower:
                return {"query": "Alzheimer", "size": 3}
            elif 'disease' in tool_name_lower:
                return {"disease_id": "EFO_0000249"}  # Alzheimer's disease
        
        # Generic search patterns
        elif 'search' in tool_name_lower:
            return {"query": "test", "max_results": 3}
        elif 'get' in tool_name_lower or 'fetch' in tool_name_lower:
            return {"id": "test"}
        
        # Return None for complex tools that need specific parameters
        return None
    
    async def test_all_servers(self) -> Dict[str, Dict[str, Any]]:
        """Test all biomedical MCP servers."""
        print("Biomedical MCP Servers - Isolation Testing")
        print("=" * 50)
        print("Testing each server individually using official MCP client patterns")
        print()
        
        # Define servers to test (excluding DrugBank which needs API key)
        servers_to_test = [
            ("PubMed", "pubmed_mcp.py"),
            ("BioRxiv", "bioarxiv_mcp.py"), 
            ("ClinicalTrials", "clinicaltrialsgov_mcp.py"),
            ("OpenTargets", "opentargets_mcp.py")
        ]
        
        # Add DrugBank if API key is available
        if os.getenv('DRUGBANK_API_KEY'):
            servers_to_test.append(("DrugBank", "drugbank_mcp.py"))
            print("🔑 DrugBank API key found - including DrugBank server in tests")
        else:
            print("⚠️  DrugBank API key not found - skipping DrugBank tests")
        
        print(f"\nTesting {len(servers_to_test)} servers...\n")
        
        results = {}
        for server_name, server_script in servers_to_test:
            try:
                result = await self.test_server_initialization(server_name, server_script)
                results[server_name] = result
                
                # Brief pause between tests
                await asyncio.sleep(1)
                
            except Exception as e:
                print(f"✗ Unexpected error testing {server_name}: {e}")
                results[server_name] = {
                    "status": "FAIL",
                    "error": f"Unexpected error: {str(e)}",
                    "tools": [],
                    "resources": [],
                    "prompts": []
                }
        
        return results

async def test_mcp_dev_mode():
    """Test using the official mcp dev command (if available)."""
    print("\n" + "="*60)
    print("Testing MCP Dev Mode (Official Method)")
    print("="*60)
    
    mcps_dir = Path("src/service/mcps")
    
    # Test if mcp command is available
    try:
        result = subprocess.run(["mcp", "--help"], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✓ MCP CLI available")
            
            # Try to test one server with mcp dev
            pubmed_path = mcps_dir / "pubmed_mcp.py"
            if pubmed_path.exists():
                print(f"🧪 Testing PubMed server with 'mcp dev'...")
                print("   (This would normally open MCP Inspector)")
                print(f"   Command would be: mcp dev {pubmed_path}")
                print("   Manual test: Run this command in a separate terminal to test with Inspector")
                return True
        else:
            print("⚠ MCP CLI not available or not working")
            return False
            
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"⚠ MCP CLI not available: {e}")
        return False

def generate_test_report(results: Dict[str, Dict[str, Any]]):
    """Generate a comprehensive test report."""
    print("\n" + "="*60)
    print("MCP SERVERS ISOLATION TEST REPORT")
    print("="*60)
    
    total_servers = len(results)
    successful_servers = sum(1 for r in results.values() if r["status"] == "SUCCESS")
    
    print(f"Total servers tested: {total_servers}")
    print(f"Successfully initialized: {successful_servers}")
    print(f"Failed initialization: {total_servers - successful_servers}")
    print()
    
    # Detailed results
    for server_name, result in results.items():
        status_symbol = "✓" if result["status"] == "SUCCESS" else "✗"
        print(f"{status_symbol} {server_name:.<30} {result['status']}")
        
        if result["status"] == "SUCCESS":
            print(f"   Tools: {len(result['tools'])}")
            print(f"   Resources: {len(result['resources'])}")
            print(f"   Prompts: {len(result['prompts'])}")
            if result.get("tool_test"):
                print(f"   Tool Test: {result['tool_test'][:50]}...")
        else:
            print(f"   Error: {result.get('error', 'Unknown error')}")
        print()
    
    # Summary and recommendations
    print("="*60)
    print("SUMMARY & RECOMMENDATIONS")
    print("="*60)
    
    if successful_servers == total_servers:
        print("🎉 All MCP servers are working correctly!")
        print("✓ Servers can initialize and respond to requests")
        print("✓ Tools are properly exposed")
        print("✓ Basic client connections work")
        print("\nNext steps:")
        print("• Test with MCP Inspector: `npx @modelcontextprotocol/inspector`")
        print("• Integration test with your biomedical researcher agent")
        print("• Consider adding more comprehensive tool tests")
        
    elif successful_servers > 0:
        print(f"✅ {successful_servers}/{total_servers} servers working correctly")
        failed_servers = [name for name, result in results.items() if result["status"] == "FAIL"]
        print(f"⚠️  Failed servers: {', '.join(failed_servers)}")
        print("\nRecommendations:")
        print("• Check failed server configurations")
        print("• Verify dependencies are installed")
        print("• Check server scripts for syntax errors")
        print("• Test failed servers manually with MCP Inspector")
        
    else:
        print("❌ No servers working correctly")
        print("Recommendations:")
        print("• Check MCP Python SDK installation: `uv add mcp`")
        print("• Verify server scripts exist and are executable")
        print("• Check Python environment and dependencies")
        print("• Test with a simple MCP server first")
    
    # Tool statistics
    total_tools = sum(len(r.get("tools", [])) for r in results.values())
    if total_tools > 0:
        print(f"\n📊 Total biomedical tools available: {total_tools}")
        print("Your biomedical researcher agent has access to:")
        for server_name, result in results.items():
            if result["status"] == "SUCCESS" and result.get("tools"):
                print(f"• {server_name}: {len(result['tools'])} tools")

async def main():
    """Main test execution."""
    mcps_dir = Path("src/service/mcps")
    
    if not mcps_dir.exists():
        print(f"❌ MCP servers directory not found: {mcps_dir}")
        print("Make sure you're running this from the project root directory")
        return False
    
    # Initialize tester
    tester = MCPServerTester(mcps_dir)
    
    # Run isolation tests
    results = await tester.test_all_servers()
    
    # Test official MCP dev mode (informational)
    await test_mcp_dev_mode()
    
    # Generate comprehensive report
    generate_test_report(results)
    
    # Return success status
    return all(r["status"] == "SUCCESS" for r in results.values())

if __name__ == "__main__":
    success = asyncio.run(main())
    
    print("\n" + "="*60)
    print("MCP TESTING COMMANDS FOR MANUAL VERIFICATION")
    print("="*60)
    print("To test individual servers manually:")
    print()
    print("1. Using MCP Inspector (Visual Testing):")
    print("   npx @modelcontextprotocol/inspector python src/service/mcps/pubmed_mcp.py")
    print()
    print("2. Using MCP CLI (Command Line Testing):")
    print("   npx @modelcontextprotocol/inspector --cli python src/service/mcps/pubmed_mcp.py --method tools/list")
    print()
    print("3. Using mcp dev (Development Mode):")
    print("   mcp dev src/service/mcps/pubmed_mcp.py")
    print()
    print("4. Test with environment variables:")
    print("   DRUGBANK_API_KEY=your_key npx @modelcontextprotocol/inspector python src/service/mcps/drugbank_mcp.py")
    
    sys.exit(0 if success else 1) 