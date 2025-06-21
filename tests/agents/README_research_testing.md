# Research Agent Testing Guide

After modifying the crawling framework, use these scripts to test the `research_agent` individually and understand its behavior and performance.

## Test Scripts

### 1. Quick Test (`quick_research_test.py`)
**Use this for rapid testing during development**

```bash
# Run with default query
python tests/agents/quick_research_test.py

# Run with custom query
python tests/agents/quick_research_test.py "What are the latest trends in web scraping?"

# Test crawling specifically
python tests/agents/quick_research_test.py "Search for information about Python requests library and crawl the official documentation"
```

**Features:**
- Fast single query testing
- Basic response analysis
- Quick feedback on crawling integration

### 2. Comprehensive Demo (`demo_research_agent.py`)
**Use this for thorough testing and analysis**

```bash
# Run full test suite
python tests/agents/demo_research_agent.py

# Run with interactive mode
python tests/agents/demo_research_agent.py --interactive
```

**Features:**
- Individual tool testing (Tavily, crawl_tool, crawl_many_tool)
- Basic research queries
- Crawling-focused tests
- Error handling tests
- Configuration testing
- Interactive mode for custom queries

## Test Categories

### 1. Individual Tools Testing
- Tests each tool (`tavily_tool`, `crawl_tool`, `crawl_many_tool`) separately
- Verifies your crawling framework changes work at the tool level

### 2. Basic Research Queries
- Tests standard research workflows
- Validates prompt templates and response formatting
- Measures response times and quality

### 3. Crawling-Focused Tests
- Specifically tests queries that should trigger crawling
- Analyzes crawling behavior and content extraction
- Validates crawl tool integration

### 4. Error Handling
- Tests agent behavior with invalid queries
- Validates graceful error handling
- Tests edge cases (empty queries, very long queries)

### 5. Configuration Testing
- Tests different agent configurations
- Validates state management
- Tests integration with other components

## What to Look For

### ✅ Successful Crawling Integration
- URLs appear in responses
- "Crawled Content" sections in output
- Content length metrics show extracted data
- Proper markdown formatting

### ⚠️ Potential Issues
- No URLs in responses when expected
- Empty or minimal crawled content
- Errors during tool execution
- Long response times

### 🔍 Key Metrics
- Response times (should be reasonable)
- Content length (indicates successful extraction)  
- Tool usage patterns (search → crawl workflow)
- Error handling behavior

## Environment Setup

Ensure you have the required API keys:
- `OPENAI_API_KEY` or `LLM_API_KEY` or `ANTHROPIC_API_KEY` (for LLM)
- `TAVILY_API_KEY` (for search)

```bash
export OPENAI_API_KEY="your-key-here"
export TAVILY_API_KEY="your-key-here"
```

## Example Usage Workflow

1. **Quick validation** after making changes:
   ```bash
   python tests/agents/quick_research_test.py "Test my crawling changes"
   ```

2. **Comprehensive testing** before committing:
   ```bash
   python tests/agents/demo_research_agent.py
   ```

3. **Interactive testing** for specific scenarios:
   ```bash
   python tests/agents/demo_research_agent.py --interactive
   ```

## Debugging Tips

### If crawling isn't working:
1. Run individual tool tests first
2. Check the crawl tool configuration in `src/tools/crawl.py`
3. Verify the crawler backend settings
4. Test with simple URLs like `https://example.com`

### If responses are empty:
1. Check API key configuration
2. Verify network connectivity
3. Look at the prompt template in `src/prompts/researcher.md`
4. Test with verbose logging

### If performance is slow:
1. Check concurrent crawling settings
2. Monitor memory usage during tests
3. Test with fewer URLs in `crawl_many_tool`
4. Verify backend optimization settings

## Customizing Tests

You can modify the test scripts to:
- Add your own test queries
- Change tool configurations
- Test specific crawling backends
- Add performance benchmarks
- Test with different state configurations

## Output Analysis

The tests provide detailed output including:
- Execution times
- Response analysis
- Tool usage patterns
- Error detection
- Performance metrics

Use this information to validate that your crawling framework changes are working as expected and haven't introduced any regressions. 