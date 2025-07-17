"""
Test LangGraph MCP integration with Portkey to determine if NotGiven serialization 
issues are specific to PydanticAI or affect MCP more broadly.

This test creates a LangGraph agent using LangChain MCP adapters to connect to our
biomedical MCP servers, and tests it with both direct OpenAI and Portkey integration.
"""

import asyncio
import os
import logging
from typing import Dict, Any
import pytest

# LangGraph and LangChain imports
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI

# MCP adapters
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools

# Portkey integration
try:
    from portkey_ai import Portkey
    PORTKEY_AVAILABLE = True
except ImportError:
    PORTKEY_AVAILABLE = False

logger = logging.getLogger(__name__)


class LangGraphMCPTester:
    """Test class for LangGraph MCP integration with Portkey."""
    
    def __init__(self):
        self.mcp_client = None
        self.tools = []
        self.agent_direct = None
        self.agent_portkey = None
        
    async def setup_mcp_servers(self):
        """Set up MCP servers using our biomedical servers."""
        # Get the absolute path to the MCP servers
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        mcps_dir = os.path.join(project_root, "src", "service", "mcps")
        
        # Configure MCP client with our biomedical servers
        self.mcp_client = MultiServerMCPClient({
            "pubmed": {
                "command": "python",
                "args": [os.path.join(mcps_dir, "pubmed_mcp.py")],
                "transport": "stdio",
            },
            "biorxiv": {
                "command": "python", 
                "args": [os.path.join(mcps_dir, "bioarxiv_mcp.py")],
                "transport": "stdio",
            },
            # Only add DrugBank if API key is available
            **({
                "drugbank": {
                    "command": "python",
                    "args": [os.path.join(mcps_dir, "drugbank_mcp.py")],
                    "transport": "stdio",
                    "env": {"DRUGBANK_API_KEY": os.getenv('DRUGBANK_API_KEY')}
                }
            } if os.getenv('DRUGBANK_API_KEY') else {}),
            "opentargets": {
                "command": "python",
                "args": [os.path.join(mcps_dir, "opentargets_mcp.py")], 
                "transport": "stdio",
            }
        })
        
        logger.info("MCP client configured with biomedical servers")
        
    async def load_tools(self):
        """Load tools from MCP servers."""
        try:
            self.tools = await self.mcp_client.get_tools()
            logger.info(f"Loaded {len(self.tools)} tools from MCP servers")
            for tool in self.tools:
                logger.info(f"  - {tool.name}: {tool.description}")
            return True
        except Exception as e:
            logger.error(f"Failed to load MCP tools: {e}")
            return False
    
    def create_direct_openai_agent(self):
        """Create LangGraph agent with direct OpenAI."""
        try:
            # Use direct OpenAI
            model = ChatOpenAI(
                model="gpt-4o-mini",
                api_key=os.getenv("OPENAI_API_KEY"),
                base_url="https://api.openai.com/v1"
            )
            
            self.agent_direct = create_react_agent(
                model=model,
                tools=self.tools,
                prompt="You are a biomedical research assistant. Use the available biomedical database tools to find information."
            )
            
            logger.info("✅ Direct OpenAI LangGraph agent created successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to create direct OpenAI agent: {e}")
            return False
    
    def create_portkey_agent(self):
        """Create LangGraph agent with Portkey integration."""
        if not PORTKEY_AVAILABLE:
            logger.warning("❌ Portkey not available - skipping Portkey agent creation")
            return False
            
        try:
            # Create ChatOpenAI with Portkey configuration using headers approach
            model = ChatOpenAI(
                model="gpt-4o-mini",
                openai_api_key=os.getenv("PORTKEY_API_KEY"),  # Use Portkey API key
                openai_api_base="https://api.portkey.ai/v1",  # Use Portkey base URL
                default_headers={
                    "x-portkey-api-key": os.getenv("PORTKEY_API_KEY"),
                    "x-portkey-virtual-key": os.getenv("PORTKEY_OPENAI_VIRTUAL_KEY", "@openai"),
                    "x-portkey-metadata": '{"env": "test", "_agent": "langgraph_mcp_test", "_model": "gpt-4o-mini"}'
                }
            )
            
            self.agent_portkey = create_react_agent(
                model=model,
                tools=self.tools,
                prompt="You are a biomedical research assistant. Use the available biomedical database tools to find information."
            )
            
            logger.info("✅ Portkey LangGraph agent created successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to create Portkey agent: {e}")
            return False
    
    async def test_direct_agent(self, query: str = "Search for recent papers on immunotherapy"):
        """Test the direct OpenAI agent."""
        if not self.agent_direct:
            logger.error("❌ Direct agent not available")
            return False
            
        try:
            logger.info(f"🧪 Testing direct OpenAI agent with query: {query}")
            
            result = await self.agent_direct.ainvoke({
                "messages": [{"role": "user", "content": query}]
            })
            
            logger.info("✅ Direct OpenAI agent test successful")
            logger.info(f"Response: {result['messages'][-1].content[:200]}...")
            return True
            
        except Exception as e:
            logger.error(f"❌ Direct OpenAI agent test failed: {e}")
            return False
    
    async def test_portkey_agent(self, query: str = "Search for recent papers on immunotherapy"):
        """Test the Portkey agent."""
        if not self.agent_portkey:
            logger.error("❌ Portkey agent not available")
            return False
            
        try:
            logger.info(f"🧪 Testing Portkey agent with query: {query}")
            
            result = await self.agent_portkey.ainvoke({
                "messages": [{"role": "user", "content": query}]
            })
            
            logger.info("✅ Portkey agent test successful")
            logger.info(f"Response: {result['messages'][-1].content[:200]}...")
            return True
            
        except Exception as e:
            logger.error(f"❌ Portkey agent test failed: {e}")
            logger.error(f"Error type: {type(e).__name__}")
            logger.error(f"Error details: {str(e)}")
            
            # Check for NotGiven serialization error specifically
            if "NotGiven" in str(e) or "JSON serializable" in str(e):
                logger.error("🚨 DETECTED: NotGiven serialization error in LangGraph MCP!")
                logger.error("This indicates the issue is NOT specific to PydanticAI")
            
            return False
    
    async def run_comprehensive_test(self):
        """Run comprehensive test comparing direct OpenAI vs Portkey with MCP."""
        logger.info("🚀 Starting LangGraph MCP + Portkey Integration Test")
        logger.info("=" * 80)
        
        # Setup phase
        logger.info("📋 Phase 1: Setup MCP servers")
        await self.setup_mcp_servers()
        
        logger.info("📋 Phase 2: Load MCP tools")
        tools_loaded = await self.load_tools()
        if not tools_loaded:
            logger.error("❌ Failed to load MCP tools - aborting test")
            return False
        
        # Agent creation phase
        logger.info("📋 Phase 3: Create agents")
        direct_created = self.create_direct_openai_agent()
        portkey_created = self.create_portkey_agent()
        
        # Testing phase
        logger.info("📋 Phase 4: Test agents")
        test_results = {}
        
        if direct_created:
            test_results["direct_openai"] = await self.test_direct_agent()
        else:
            test_results["direct_openai"] = False
            
        if portkey_created:
            test_results["portkey"] = await self.test_portkey_agent()
        else:
            test_results["portkey"] = False
        
        # Results summary
        logger.info("=" * 80)
        logger.info("📊 TEST RESULTS SUMMARY")
        logger.info("=" * 80)
        
        logger.info(f"✅ MCP Tools Loaded: {tools_loaded} ({len(self.tools)} tools)")
        logger.info(f"✅ Direct OpenAI Agent: {test_results.get('direct_openai', False)}")
        logger.info(f"✅ Portkey Agent: {test_results.get('portkey', False)}")
        
        # Analysis
        if test_results.get("direct_openai", False) and not test_results.get("portkey", False):
            logger.warning("🔍 ANALYSIS: Direct OpenAI works but Portkey fails")
            logger.warning("This suggests Portkey has issues with MCP integration (not just PydanticAI)")
        elif test_results.get("direct_openai", False) and test_results.get("portkey", False):
            logger.info("🎉 ANALYSIS: Both Direct OpenAI and Portkey work!")
            logger.info("The issue might be specific to PydanticAI's MCP integration")
        elif not test_results.get("direct_openai", False):
            logger.error("🚨 ANALYSIS: Even direct OpenAI fails - MCP setup issue")
        
        return test_results


async def main():
    """Main test function."""
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Environment check
    logger.info("🔍 Environment Check")
    logger.info(f"OPENAI_API_KEY: {'✅ Set' if os.getenv('OPENAI_API_KEY') else '❌ Missing'}")
    logger.info(f"PORTKEY_API_KEY: {'✅ Set' if os.getenv('PORTKEY_API_KEY') else '❌ Missing'}")
    logger.info(f"DRUGBANK_API_KEY: {'✅ Set' if os.getenv('DRUGBANK_API_KEY') else '⚠️ Optional'}")
    logger.info(f"Portkey Available: {'✅ Yes' if PORTKEY_AVAILABLE else '❌ No'}")
    
    # Run the test
    tester = LangGraphMCPTester()
    results = await tester.run_comprehensive_test()
    
    return results


if __name__ == "__main__":
    asyncio.run(main()) 