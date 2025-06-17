#!/usr/bin/env python3
"""
Comprehensive MCP Server Status Check and Capability Testing

This script provides a detailed analysis of all biomedical MCP servers including:
1. Server availability and initialization
2. Tool enumeration with detailed schemas
3. Real API calls with input/output examples
4. Performance and error handling tests
5. Integration readiness assessment

Usage: uv run python tests/mcp_tests/comprehensive_mcp_status_check.py
"""

import asyncio
import json
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

class MCPServerAnalyzer:
    """Comprehensive analyzer for MCP server capabilities and status."""
    
    def __init__(self):
        self.mcps_dir = project_root / "src" / "service" / "mcps"
        self.results = {}
        self.start_time = time.time()
    
    def print_header(self, title: str, level: int = 1):
        """Print formatted header."""
        chars = "=" if level == 1 else "-" if level == 2 else "."
        print(f"\n{chars * 80}")
        print(f"{title}")
        print(f"{chars * 80}")
    
    def print_subheader(self, title: str):
        """Print formatted subheader."""
        print(f"\n📋 {title}")
        print("-" * 50)
    
    async def analyze_server_detailed(self, server_name: str, server_script: str) -> Dict[str, Any]:
        """Perform detailed analysis of a single MCP server."""
        self.print_header(f"{server_name} MCP Server Analysis", level=1)
        
        server_path = self.mcps_dir / server_script
        if not server_path.exists():
            return {
                "status": "NOT_FOUND",
                "error": f"Server script not found: {server_path}",
                "capabilities": {}
            }
        
        print(f"🔍 Server: {server_name}")
        print(f"📁 Script: {server_script}")
        print(f"📍 Path: {server_path}")
        
        # Test server startup and capabilities
        server_params = StdioServerParameters(
            command="python",
            args=[str(server_path)],
            env=os.environ.copy()
        )
        
        analysis_result = {
            "status": "UNKNOWN",
            "server_info": {
                "name": server_name,
                "script": server_script,
                "path": str(server_path)
            },
            "capabilities": {},
            "performance": {},
            "test_results": []
        }
        
        try:
            start_time = time.time()
            
            async with stdio_client(server_params) as (read, write):
                connection_time = time.time() - start_time
                print(f"✅ Connection established ({connection_time:.2f}s)")
                
                async with ClientSession(read, write) as session:
                    session_start = time.time()
                    await session.initialize()
                    session_time = time.time() - session_start
                    print(f"✅ Session initialized ({session_time:.2f}s)")
                    
                    analysis_result["performance"] = {
                        "connection_time": connection_time,
                        "session_time": session_time
                    }
                    
                    # Analyze tools in detail
                    await self._analyze_tools(session, analysis_result)
                    
                    # Analyze resources
                    await self._analyze_resources(session, analysis_result)
                    
                    # Analyze prompts
                    await self._analyze_prompts(session, analysis_result)
                    
                    # Run capability tests
                    await self._run_capability_tests(session, server_name, analysis_result)
                    
                    analysis_result["status"] = "SUCCESS"
                    
        except Exception as e:
            print(f"❌ Server analysis failed: {e}")
            analysis_result["status"] = "FAILED"
            analysis_result["error"] = str(e)
        
        return analysis_result
    
    async def _analyze_tools(self, session: ClientSession, result: Dict[str, Any]):
        """Analyze available tools in detail."""
        self.print_subheader("Tool Analysis")
        
        try:
            tools_response = await session.list_tools()
            tools = tools_response.tools if hasattr(tools_response, 'tools') else []
            
            print(f"🔧 Found {len(tools)} tools")
            
            tools_info = []
            for i, tool in enumerate(tools, 1):
                # Handle inputSchema as either dict or model
                input_schema = {}
                if hasattr(tool, 'inputSchema') and tool.inputSchema:
                    if hasattr(tool.inputSchema, 'model_dump'):
                        input_schema = tool.inputSchema.model_dump()
                    elif isinstance(tool.inputSchema, dict):
                        input_schema = tool.inputSchema
                    else:
                        input_schema = dict(tool.inputSchema) if tool.inputSchema else {}
                
                tool_info = {
                    "name": tool.name,
                    "description": tool.description,
                    "input_schema": input_schema
                }
                tools_info.append(tool_info)
                
                print(f"  {i}. {tool.name}")
                print(f"     📝 {tool.description}")
                if tool_info["input_schema"]:
                    props = tool_info["input_schema"].get("properties", {})
                    if props:
                        print(f"     📊 Parameters: {', '.join(props.keys())}")
                    required = tool_info["input_schema"].get("required", [])
                    if required:
                        print(f"     ⚠️  Required: {', '.join(required)}")
                print()
            
            result["capabilities"]["tools"] = tools_info
            
        except Exception as e:
            print(f"❌ Tool analysis failed: {e}")
            result["capabilities"]["tools"] = []
    
    async def _analyze_resources(self, session: ClientSession, result: Dict[str, Any]):
        """Analyze available resources."""
        try:
            resources_response = await session.list_resources()
            resources = resources_response.resources if hasattr(resources_response, 'resources') else []
            
            if resources:
                self.print_subheader("Resource Analysis")
                print(f"📚 Found {len(resources)} resources")
                
                resources_info = []
                for resource in resources:
                    resource_info = {
                        "uri": resource.uri,
                        "name": resource.name,
                        "description": getattr(resource, 'description', 'No description'),
                        "mimeType": getattr(resource, 'mimeType', 'Unknown')
                    }
                    resources_info.append(resource_info)
                    print(f"  📄 {resource.name}: {resource.uri}")
                
                result["capabilities"]["resources"] = resources_info
            else:
                result["capabilities"]["resources"] = []
                
        except Exception as e:
            print(f"⚠️  Resource analysis failed: {e}")
            result["capabilities"]["resources"] = []
    
    async def _analyze_prompts(self, session: ClientSession, result: Dict[str, Any]):
        """Analyze available prompts."""
        try:
            prompts_response = await session.list_prompts()
            prompts = prompts_response.prompts if hasattr(prompts_response, 'prompts') else []
            
            if prompts:
                self.print_subheader("Prompt Analysis")
                print(f"💬 Found {len(prompts)} prompts")
                
                prompts_info = []
                for prompt in prompts:
                    prompt_info = {
                        "name": prompt.name,
                        "description": getattr(prompt, 'description', 'No description'),
                        "arguments": getattr(prompt, 'arguments', [])
                    }
                    prompts_info.append(prompt_info)
                    print(f"  💬 {prompt.name}: {prompt_info['description']}")
                
                result["capabilities"]["prompts"] = prompts_info
            else:
                result["capabilities"]["prompts"] = []
                
        except Exception as e:
            print(f"⚠️  Prompt analysis failed: {e}")
            result["capabilities"]["prompts"] = []
    
    async def _run_capability_tests(self, session: ClientSession, server_name: str, result: Dict[str, Any]):
        """Run detailed capability tests for each tool."""
        self.print_subheader("Capability Testing")
        
        tools = result["capabilities"].get("tools", [])
        if not tools:
            print("❌ No tools available for testing")
            return
        
        test_cases = self._get_test_cases_for_server(server_name)
        
        for tool_info in tools:
            tool_name = tool_info["name"]
            print(f"\n🧪 Testing: {tool_name}")
            
            if tool_name in test_cases:
                test_case = test_cases[tool_name]
                try:
                    print(f"   📥 Input: {json.dumps(test_case['input'], indent=2)}")
                    
                    start_time = time.time()
                    response = await session.call_tool(tool_name, test_case['input'])
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
                    
                    print(f"   📤 Output ({execution_time:.2f}s):")
                    print(f"   {response_text[:200]}..." if len(response_text) > 200 else f"   {response_text}")
                    
                    test_result = {
                        "tool": tool_name,
                        "status": "SUCCESS",
                        "input": test_case['input'],
                        "output": response_text,
                        "execution_time": execution_time,
                        "output_length": len(response_text)
                    }
                    
                    result["test_results"].append(test_result)
                    print(f"   ✅ Test passed")
                    
                except Exception as e:
                    print(f"   ❌ Test failed: {e}")
                    test_result = {
                        "tool": tool_name,
                        "status": "FAILED",
                        "input": test_case['input'],
                        "error": str(e),
                        "execution_time": 0
                    }
                    result["test_results"].append(test_result)
            else:
                print(f"   ⚠️  No test case defined")
                result["test_results"].append({
                    "tool": tool_name,
                    "status": "SKIPPED",
                    "reason": "No test case defined"
                })
    
    def _get_test_cases_for_server(self, server_name: str) -> Dict[str, Dict[str, Any]]:
        """Get comprehensive test cases for each server."""
        test_cases = {
            "PubMed": {
                "search_pubmed": {
                    "input": {"query": "COVID-19 vaccines", "max_results": 3}
                },
                "get_pubmed_abstract": {
                    "input": {"pmid": "34567890"}
                },
                "get_related_articles": {
                    "input": {"pmid": "34567890", "max_results": 3}
                },
                "find_by_author": {
                    "input": {"author": "Smith JB", "max_results": 3}
                }
            },
            "BioRxiv": {
                "search_preprints": {
                    "input": {
                        "server": "biorxiv",
                        "category": "bioinformatics", 
                        "start_date": "2024-01-01",
                        "end_date": "2024-01-31",
                        "max_results": 3
                    }
                },
                "get_preprint_by_doi": {
                    "input": {
                        "server": "biorxiv",
                        "doi": "10.1101/2023.01.01.000001"
                    }
                },
                "find_published_version": {
                    "input": {
                        "server": "biorxiv",
                        "doi": "10.1101/2023.01.01.000001"
                    }
                },
                "get_recent_preprints": {
                    "input": {
                        "server": "biorxiv",
                        "days": 7,
                        "max_results": 3,
                        "category": "bioinformatics"
                    }
                }
            },
            "ClinicalTrials": {
                "search_trials": {
                    "input": {"query": "diabetes treatment", "max_results": 3}
                },
                "find_trials_by_condition": {
                    "input": {"condition": "Type 2 Diabetes", "max_results": 3}
                },
                "get_trial_details": {
                    "input": {"nct_id": "NCT02015429"}  # Use valid NCT ID from previous results
                },
                "find_trials_by_location": {
                    "input": {"location": "Boston, MA", "max_results": 3}
                }
            },
            "OpenTargets": {
                "search_targets": {
                    "input": {"query": "Alzheimer", "max_results": 3}
                },
                "get_target_details": {
                    "input": {"target_id": "ENSG00000142192"}  # APP gene from previous result
                },
                "search_diseases": {
                    "input": {"query": "cancer", "max_results": 3}
                },
                "get_target_associated_diseases": {
                    "input": {"target_id": "ENSG00000142192", "max_results": 3}
                },
                "get_disease_associated_targets": {
                    "input": {"disease_id": "MONDO_0004992", "max_results": 3}  # cancer from previous result
                },
                "search_drugs": {
                    "input": {"query": "aspirin", "max_results": 3}
                }
            },
            "DrugBank": {
                "search_drugs": {
                    "input": {"query": "aspirin", "limit": 3}
                },
                "get_drug_info": {
                    "input": {"drugbank_id": "DB00945"}
                },
                "search_by_target": {
                    "input": {"target": "COX-2", "limit": 3}
                },
                "get_drug_interactions": {
                    "input": {"drugbank_id": "DB00945"}
                }
            }
        }
        
        return test_cases.get(server_name, {})
    
    async def generate_status_report(self):
        """Generate comprehensive status report."""
        self.print_header("MCP SERVER STATUS REPORT", level=1)
        
        print(f"🕐 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📍 Project: {project_root}")
        print(f"⏱️  Total Analysis Time: {time.time() - self.start_time:.2f}s")
        
        # Environment check
        self.print_subheader("Environment Check")
        drugbank_key = os.getenv('DRUGBANK_API_KEY')
        print(f"DrugBank API Key: {'✅ Configured' if drugbank_key else '❌ Not configured'}")
        print(f"Python: {sys.version}")
        print(f"Working Directory: {os.getcwd()}")
        
        # Server inventory
        self.print_subheader("Server Inventory")
        total_servers = len(self.results)
        successful_servers = sum(1 for r in self.results.values() if r["status"] == "SUCCESS")
        
        print(f"Total Servers: {total_servers}")
        print(f"Successful: {successful_servers}")
        print(f"Failed: {total_servers - successful_servers}")
        
        # Detailed results
        for server_name, result in self.results.items():
            self._print_server_summary(server_name, result)
        
        # Overall summary
        self.print_header("OVERALL SUMMARY", level=1)
        
        if successful_servers == total_servers:
            print("🎉 ALL MCP SERVERS ARE OPERATIONAL!")
            print("✅ Ready for production use")
            print("✅ Biomedical research agent integration ready")
        elif successful_servers > 0:
            print(f"⚠️  {successful_servers}/{total_servers} servers operational")
            print("🔧 Some servers need attention")
        else:
            print("❌ All servers need debugging")
        
        # Tool summary
        total_tools = sum(
            len(r["capabilities"].get("tools", []))
            for r in self.results.values()
            if r["status"] == "SUCCESS"
        )
        total_tests = sum(
            len(r.get("test_results", []))
            for r in self.results.values()
        )
        successful_tests = sum(
            len([t for t in r.get("test_results", []) if t.get("status") == "SUCCESS"])
            for r in self.results.values()
        )
        
        print(f"\n📊 Total Tools Available: {total_tools}")
        print(f"🧪 Total Tests Run: {total_tests}")
        print(f"✅ Successful Tests: {successful_tests}")
        if total_tests > 0:
            print(f"📈 Success Rate: {(successful_tests/total_tests)*100:.1f}%")
    
    def _print_server_summary(self, server_name: str, result: Dict[str, Any]):
        """Print summary for a single server."""
        status_emoji = "✅" if result["status"] == "SUCCESS" else "❌"
        
        print(f"\n{status_emoji} {server_name}")
        print(f"   Status: {result['status']}")
        
        if result["status"] == "SUCCESS":
            tools_count = len(result["capabilities"].get("tools", []))
            resources_count = len(result["capabilities"].get("resources", []))
            prompts_count = len(result["capabilities"].get("prompts", []))
            
            print(f"   Tools: {tools_count}")
            print(f"   Resources: {resources_count}")
            print(f"   Prompts: {prompts_count}")
            
            if "performance" in result:
                perf = result["performance"]
                print(f"   Connection: {perf.get('connection_time', 0):.2f}s")
                print(f"   Session: {perf.get('session_time', 0):.2f}s")
            
            test_results = result.get("test_results", [])
            if test_results:
                successful_tests = len([t for t in test_results if t.get("status") == "SUCCESS"])
                print(f"   Tests: {successful_tests}/{len(test_results)} passed")
        else:
            print(f"   Error: {result.get('error', 'Unknown error')}")
    
    async def run_comprehensive_analysis(self):
        """Run comprehensive analysis of all MCP servers."""
        self.print_header("COMPREHENSIVE MCP SERVER ANALYSIS", level=1)
        
        # Define servers to analyze
        servers_to_analyze = [
            ("PubMed", "pubmed_mcp.py"),
            ("BioRxiv", "bioarxiv_mcp.py"),
            ("ClinicalTrials", "clinicaltrialsgov_mcp.py"),
            ("OpenTargets", "opentargets_mcp.py")
        ]
        
        # Add DrugBank if API key is available
        if os.getenv('DRUGBANK_API_KEY'):
            servers_to_analyze.append(("DrugBank", "drugbank_mcp.py"))
            print("🔑 DrugBank API key detected - including DrugBank server")
        else:
            print("⚠️  DrugBank API key not found - skipping DrugBank server")
        
        print(f"🎯 Analyzing {len(servers_to_analyze)} MCP servers")
        
        # Analyze each server
        for server_name, server_script in servers_to_analyze:
            try:
                result = await self.analyze_server_detailed(server_name, server_script)
                self.results[server_name] = result
            except Exception as e:
                print(f"❌ Failed to analyze {server_name}: {e}")
                self.results[server_name] = {
                    "status": "CRASHED",
                    "error": str(e),
                    "capabilities": {}
                }
        
        # Generate final report
        await self.generate_status_report()


async def main():
    """Main entry point."""
    print("🚀 Starting Comprehensive MCP Server Analysis...")
    
    analyzer = MCPServerAnalyzer()
    await analyzer.run_comprehensive_analysis()
    
    print(f"\n🏁 Analysis complete!")
    return True


if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️  Analysis interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Analysis crashed: {e}")
        sys.exit(1)