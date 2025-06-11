# TCR Analysis System - Testing Suite

This directory contains a comprehensive testing suite for the **TCR Data Analyst** multi-agent framework designed for cancer immunogenomics research.

## 🧬 Testing Philosophy: Basic to Complex

The testing suite follows a progressive complexity approach:

```
BASIC → INTERMEDIATE → ADVANCED → EXPERT
  ↓         ↓           ↓         ↓
Tools    Environment   Agent   Interactive
Only     + Data      Integration  Demo
```

## 📋 Test Files Overview

### 1. `test_01_tcr_tools_basic.py` - **BASIC LEVEL**
- **Purpose**: Test individual TCR analysis tools in isolation
- **Tests**: Tool functionality without agent integration
- **Coverage**:
  - VDJdb schema retrieval
  - CDR3 motif analysis
  - TCR diversity metrics calculation
  - Repertoire comparison
- **Prerequisites**: None
- **Runtime**: ~30 seconds

### 2. `test_02_tcr_data_setup.py` - **INTERMEDIATE LEVEL**
- **Purpose**: Validate data infrastructure and environment
- **Tests**: Database setup, configuration, connectivity
- **Coverage**:
  - Environment variable configuration
  - Directory structure validation
  - Sample VDJdb database creation
  - Database connectivity testing
  - Tool-database integration
- **Prerequisites**: Basic tools working
- **Runtime**: ~45 seconds

### 3. `test_03_tcr_agent_integration.py` - **ADVANCED LEVEL**
- **Purpose**: Test complete agent integration and workflows
- **Tests**: Full multi-agent system coordination
- **Coverage**:
  - Agent initialization and configuration
  - LangGraph workflow validation
  - Complex scenario handling
  - Multi-step workflow coordination
  - Error handling and edge cases
- **Prerequisites**: Environment and data setup complete
- **Runtime**: ~60 seconds

### 4. `test_04_interactive_demo.py` - **EXPERT LEVEL**
- **Purpose**: Interactive demonstration with real agent execution
- **Tests**: Manual testing with live LLM integration
- **Coverage**:
  - Real agent query processing
  - Interactive scenario execution
  - Custom query handling
  - Session management
- **Prerequisites**: All previous tests + API keys
- **Runtime**: Interactive (user-driven)

## 🚀 Running the Tests

### Option 1: Run All Tests (Recommended)
```bash
python tests/run_all_tcr_tests.py
```

This will:
- Check prerequisites
- Run tests in proper sequence
- Stop on critical failures
- Provide comprehensive results

### Option 2: Run Individual Tests
```bash
# Basic tool testing
python tests/test_01_tcr_tools_basic.py

# Environment setup
python tests/test_02_tcr_data_setup.py

# Agent integration
python tests/test_03_tcr_agent_integration.py

# Interactive demo (requires API keys)
python tests/test_04_interactive_demo.py
```

## 🔧 Prerequisites

### System Requirements
- Python 3.8+
- SQLite3
- All TCR framework components implemented

### Required Files
- `src/tools/tcr_analysis.py` - TCR analysis tools
- `src/agents/tcr_data_team.py` - TCR workflow
- `src/config/vdjdb.py` - Database configuration
- `src/agents/agents.py` - Agent definitions

### Optional Requirements (for interactive demo)
- `.env` file with LLM API keys
- Network connectivity

## 📊 Expected Results

### ✅ Success Criteria
All required tests (1-3) should pass:
- **Basic Tools**: All 4 tool test suites pass
- **Environment**: All 5 setup tests pass  
- **Integration**: All 6 agent tests pass

### ⚠️ Common Issues

1. **Import Errors**: Ensure you're running from project root
2. **Missing Database**: Run test_02 to create sample VDJdb
3. **Agent Configuration**: Check AGENT_LLM_MAP contains tcr_data_analyst
4. **API Key Issues**: Only affects interactive demo (test_04)

## 🎯 What These Tests Validate

### Core Capabilities
- ✅ VDJdb database analysis and querying
- ✅ TCR diversity metrics calculation
- ✅ CDR3 motif discovery and pattern analysis
- ✅ Repertoire comparison between patient groups
- ✅ Multi-agent workflow orchestration

### Research Applications
- ✅ Cancer immunogenomics analysis
- ✅ Immunotherapy response prediction
- ✅ Immune-related adverse events (irAEs) detection
- ✅ TCR biomarker discovery
- ✅ Deep research in T-cell receptor datasets

## 🔬 Framework Validation

These tests validate the implementation described in the research abstract:

> "Multi-Agent Framework for Deep Research in Cancer Immunogenomics via TCR Datasets and Scientific Literature Search"

The framework uses:
- **LangGraph** for multi-agent orchestration
- **PydanticAI** for individual agent implementation
- **VDJdb/TCRdb** for T-cell receptor data analysis
- **MCP servers** for biomedical data integration

## 🎉 Success Outcome

When all tests pass, your system is ready for production cancer immunogenomics research with full capabilities for:

- TCR repertoire analysis
- Biomarker identification
- Treatment response prediction
- Adverse event detection
- Multi-step research workflows

---

*For questions or issues, refer to the main project documentation or examine individual test files for detailed implementation.* 