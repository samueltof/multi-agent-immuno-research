#!/usr/bin/env python3
"""
Show detailed MCP server outputs for user testing
"""

import asyncio
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

async def test_detailed_pubmed():
    print('🧬 DETAILED PubMed MCP Server Test')
    print('='*50)
    
    server_params = StdioServerParameters(
        command='python',
        args=['src/service/mcps/pubmed_mcp.py']
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print('📋 Available Tools:')
            tools = await session.list_tools()
            for tool in tools.tools:
                print(f'  • {tool.name}: {tool.description[:60]}...')
            
            print('\n🔍 Testing search_pubmed with COVID-19 query...')
            result = await session.call_tool('search_pubmed', {
                'query': 'COVID-19 vaccines effectiveness', 
                'max_results': 2
            })
            
            print('📊 RESULTS:')
            print('='*50)
            for content in result.content:
                print(content.text)
                print('-'*50)

async def test_detailed_clinicaltrials():
    print('\n🏥 DETAILED ClinicalTrials MCP Server Test')
    print('='*50)
    
    server_params = StdioServerParameters(
        command='python',
        args=['src/service/mcps/clinicaltrialsgov_mcp.py']
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print('📋 Available Tools:')
            tools = await session.list_tools()
            for tool in tools.tools:
                print(f'  • {tool.name}: {tool.description[:60]}...')
            
            print('\n🔍 Testing search_trials with cancer query...')
            result = await session.call_tool('search_trials', {
                'query': 'breast cancer treatment', 
                'max_results': 2
            })
            
            print('📊 RESULTS:')
            print('='*50)
            for content in result.content:
                print(content.text)
                print('-'*50)

async def test_detailed_biorxiv():
    print('\n📚 DETAILED BioRxiv MCP Server Test')
    print('='*50)
    
    server_params = StdioServerParameters(
        command='python',
        args=['src/service/mcps/bioarxiv_mcp.py']
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print('📋 Available Tools:')
            tools = await session.list_tools()
            for tool in tools.tools:
                print(f'  • {tool.name}: {tool.description[:60]}...')
            
            print('\n🔍 Testing search_preprints...')
            result = await session.call_tool('search_preprints', {
                'query': 'machine learning genomics', 
                'category': 'bioinformatics',
                'max_results': 2
            })
            
            print('📊 RESULTS:')
            print('='*50)
            for content in result.content:
                print(content.text)
                print('-'*50)

async def main():
    print('🧬 COMPREHENSIVE MCP SERVER OUTPUT DEMONSTRATION')
    print('='*60)
    print('This shows detailed outputs from each biomedical MCP server')
    print()
    
    try:
        await test_detailed_pubmed()
        await asyncio.sleep(2)
        
        await test_detailed_clinicaltrials()
        await asyncio.sleep(2)
        
        await test_detailed_biorxiv()
        
        print('\n✅ All detailed MCP tests completed!')
        print('You can see real database responses, API calls, and structured data.')
        
    except Exception as e:
        print(f'❌ Error: {e}')

if __name__ == '__main__':
    asyncio.run(main()) 