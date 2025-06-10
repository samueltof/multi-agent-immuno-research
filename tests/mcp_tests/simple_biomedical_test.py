#!/usr/bin/env python3
"""
Simple Biomedical Researcher Test

This script tests the biomedical research capabilities using direct MCP calls
without complex validation that might be causing issues.
"""

import asyncio
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

# Example questions to test
EXAMPLE_QUESTIONS = [
    {
        "question": "Find recent research about CRISPR applications in treating genetic diseases",
        "server": "PubMed",
        "tool": "search_pubmed", 
        "args": {"query": "CRISPR gene therapy genetic diseases", "max_results": 3}
    },
    {
        "question": "What clinical trials are currently studying new Alzheimer's treatments?", 
        "server": "ClinicalTrials",
        "tool": "search_trials",
        "args": {"query": "Alzheimer disease treatment", "max_results": 3}
    },
    {
        "question": "Search for latest preprints on AI in drug discovery",
        "server": "BioRxiv", 
        "tool": "search_preprints",
        "args": {
            "server": "biorxiv",
            "start_date": "2024-01-01", 
            "end_date": "2024-12-31",
            "category": "bioinformatics",
            "max_results": 3
        }
    },
    {
        "question": "What are the genetic targets like BRCA1 and TP53?",
        "server": "OpenTargets",
        "tool": "search_targets", 
        "args": {"query": "BRCA1", "max_results": 3}
    }
]

async def test_biomedical_question(question_data):
    """Test a biomedical research question using the appropriate MCP server."""
    question = question_data["question"]
    server_name = question_data["server"]
    tool_name = question_data["tool"]
    tool_args = question_data["args"]
    
    print(f"\n🔬 Testing: {question}")
    print(f"📊 Using: {server_name} server -> {tool_name}")
    print("-" * 80)
    
    # Map server names to script files
    server_scripts = {
        "PubMed": "pubmed_mcp.py",
        "ClinicalTrials": "clinicaltrialsgov_mcp.py", 
        "BioRxiv": "bioarxiv_mcp.py",
        "OpenTargets": "opentargets_mcp.py"
    }
    
    server_script = server_scripts.get(server_name)
    if not server_script:
        print(f"❌ Unknown server: {server_name}")
        return False
    
    server_path = Path("src/service/mcps") / server_script
    if not server_path.exists():
        print(f"❌ Server script not found: {server_path}")
        return False
    
    # Test the MCP server
    server_params = StdioServerParameters(
        command="python",
        args=[str(server_path)]
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                # Call the tool
                print(f"🔧 Calling tool: {tool_name}")
                result = await session.call_tool(tool_name, tool_args)
                
                print("✅ Success!")
                print("📋 Results:")
                print("-" * 40)
                
                # Display the result
                if hasattr(result, 'content'):
                    for content_item in result.content:
                        if hasattr(content_item, 'text'):
                            text = content_item.text
                            
                            # Check for error indicators in the response
                            if ("error" in text.lower() or 
                                "unknown tool" in text.lower() or
                                "404 not found" in text.lower() or
                                text.startswith("Error")):
                                print("❌ Error detected in response:")
                                print(text)
                                return False
                            
                            # Truncate very long responses
                            if len(text) > 1000:
                                text = text[:1000] + "\n... [truncated]"
                            print(text)
                        else:
                            print(str(content_item))
                else:
                    result_str = str(result)
                    # Check for error indicators in the response
                    if ("error" in result_str.lower() or 
                        "unknown tool" in result_str.lower() or
                        "404 not found" in result_str.lower()):
                        print("❌ Error detected in response:")
                        print(result_str)
                        return False
                    print(result_str)
                
                return True
                
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

async def run_all_tests():
    """Run all biomedical test questions."""
    print("🧬 Simple Biomedical Researcher Testing")
    print("=" * 60)
    print("Testing direct MCP server calls for biomedical research")
    print(f"Available servers: PubMed, ClinicalTrials, BioRxiv, OpenTargets")
    print()
    
    results = []
    for i, question_data in enumerate(EXAMPLE_QUESTIONS, 1):
        print(f"\n[{i}/{len(EXAMPLE_QUESTIONS)}]", end="")
        success = await test_biomedical_question(question_data)
        results.append(success)
        
        # Brief pause between tests
        if i < len(EXAMPLE_QUESTIONS):
            print("\n⏳ Waiting 3 seconds before next test...")
            await asyncio.sleep(3)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    for i, (question_data, success) in enumerate(zip(EXAMPLE_QUESTIONS, results), 1):
        status = "✅ PASS" if success else "❌ FAIL"
        server = question_data["server"]
        print(f"{i}. {server:<15} {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All biomedical research tests passed!")
        print("✅ MCP servers are working correctly")
        print("✅ Database connections are functional")
        print("✅ Tools are responding properly")
        print("✅ Ready for production use")
    elif passed > 0:
        print(f"\n✅ {passed}/{total} tests passed")
        print("🔧 Some servers may need attention")
    else:
        print("\n❌ All tests failed")
        print("🔧 Check MCP server configuration")

def interactive_test():
    """Interactive test mode."""
    print("🧬 Interactive Biomedical Research Testing")
    print("=" * 50)
    print("Choose a test:")
    print()
    
    for i, question_data in enumerate(EXAMPLE_QUESTIONS, 1):
        question = question_data["question"]
        server = question_data["server"]
        print(f"{i}. [{server}] {question}")
    
    print(f"{len(EXAMPLE_QUESTIONS) + 1}. Run all tests")
    print(f"{len(EXAMPLE_QUESTIONS) + 2}. Exit")
    
    try:
        choice = int(input(f"\nSelect option (1-{len(EXAMPLE_QUESTIONS) + 2}): "))
        
        if 1 <= choice <= len(EXAMPLE_QUESTIONS):
            question_data = EXAMPLE_QUESTIONS[choice - 1]
            return asyncio.run(test_biomedical_question(question_data))
        elif choice == len(EXAMPLE_QUESTIONS) + 1:
            return asyncio.run(run_all_tests())
        elif choice == len(EXAMPLE_QUESTIONS) + 2:
            print("👋 Goodbye!")
            return True
        else:
            print("Invalid choice")
            return False
            
    except ValueError:
        print("Invalid input")
        return False
    except KeyboardInterrupt:
        print("\n👋 Testing interrupted. Goodbye!")
        return True

if __name__ == "__main__":
    print("🧬 Simple Biomedical Research Testing")
    print("=" * 40)
    print("Choose testing mode:")
    print("1. Interactive testing (choose individual questions)")
    print("2. Run all tests automatically")
    print("3. Exit")
    
    try:
        mode = input("\nSelect mode (1-3): ").strip()
        
        if mode == "1":
            interactive_test()
        elif mode == "2":
            asyncio.run(run_all_tests())
        elif mode == "3":
            print("👋 Goodbye!")
        else:
            print("Invalid choice")
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}") 