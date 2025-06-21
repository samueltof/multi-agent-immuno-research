# Multi-Agent Immunological Research System

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[English](./README.md)

> Advancing Immunological Research Through AI

Multi-Agent Immunological Research System is an AI-powered framework designed for comprehensive analysis of T-cell receptor (TCR) databases and immunological research. Built upon a multi-agent architecture inspired by [LangManus](https://github.com/langmanus/langmanus), this system combines language models with specialized biomedical tools for tasks like literature search, data analysis, and immunological insights generation.

## Table of Contents
- [Multi-Agent Immunological Research System](#multi-agent-immunological-research-system)
  - [Table of Contents](#table-of-contents)
  - [Quick Start](#quick-start)
  - [Architecture](#architecture)
  - [Features](#features)
    - [Core Capabilities](#core-capabilities)
    - [Biomedical Tools and Integrations](#biomedical-tools-and-integrations)
    - [Development Features](#development-features)
    - [Research Workflow Management](#research-workflow-management)
  - [Why This System?](#why-this-system)
  - [Setup](#setup)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Configuration](#configuration)
    - [Configure Pre-commit Hook](#configure-pre-commit-hook)
  - [Usage](#usage)
    - [Basic Execution](#basic-execution)
    - [Advanced Execution Options](#advanced-execution-options)
    - [API Server](#api-server)
    - [Advanced Configuration](#advanced-configuration)
    - [Agent Prompts System](#agent-prompts-system)
      - [Core Agent Roles](#core-agent-roles)
      - [Prompt System Architecture](#prompt-system-architecture)
  - [Web UI](#web-ui)
  - [Development](#development)
    - [Testing](#testing)
    - [Code Quality](#code-quality)
  - [Contributing](#contributing)
  - [License](#license)
  - [Acknowledgments](#acknowledgments)

## Quick Start

```bash
# Clone the repository
git clone https://github.com/samueltof/multi-agent-immuno-research.git
cd multi-agent-immuno-research

# Create and activate virtual environment through uv
uv python install 3.12
uv venv --python 3.12

source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv sync

# Configure environment
cp .env.example .env
# Edit .env with your API keys and database connections

# Run the project
uv run main.py
```

## Architecture

The Multi-Agent Immunological Research System implements a hierarchical multi-agent architecture where specialized agents collaborate to accomplish complex immunological research tasks:

![Multi-Agent Architecture](./assets/architecture.png)

The system consists of the following specialized agents working together:

1. **Coordinator** - Handles initial research queries and routes immunological tasks
2. **Planner** - Analyzes research objectives and creates execution strategies
3. **Supervisor** - Oversees and manages the execution of biomedical research workflows
4. **Biomedical Researcher** - Specialized agent for literature search and biomedical data analysis
5. **Data Analyst** - Handles TCR database queries and statistical analysis
6. **Browser** - Performs web browsing and biomedical information retrieval
7. **Reporter** - Generates research reports and immunological insights summaries

## Features

### Core Capabilities
- 🤖 **LLM Integration**
    - Support for open source models optimized for scientific tasks
    - OpenAI-compatible API interface
    - Multi-tier LLM system for different research complexities

### Biomedical Tools and Integrations
- 🔬 **TCR Database Access**
    - VDJDB integration for T-cell receptor analysis
    - Custom TCR sequence analysis tools
    - Immunological database querying

- 🔍 **Biomedical Search and Retrieval**
    - PubMed literature search via MCP servers
    - BioArxiv preprint analysis
    - ClinicalTrials.gov integration
    - DrugBank pharmaceutical data access
    - OpenTargets therapeutic target information

- 📊 **Data Analysis**
    - SQL database integration (PostgreSQL, MySQL, SQLite, MS SQL, AWS Athena)
    - Statistical analysis for immunological data
    - TCR sequence pattern recognition

### Development Features
- 🐍 **Python Integration**
    - Built-in Python REPL for data analysis
    - Specialized immunological libraries
    - Package management with uv

### Research Workflow Management
- 📊 **Visualization and Control**
    - Research workflow graph visualization
    - Multi-agent orchestration for complex studies
    - Task delegation and progress monitoring

## Why This System?

This project is inspired by [LangManus](https://github.com/langmanus/langmanus) and builds upon the incredible work of the open source community. We believe in advancing immunological research through AI while leveraging established biomedical resources:

- Comprehensive TCR database integration
- Specialized agents for biomedical research tasks
- Multi-modal analysis combining literature, clinical data, and molecular information
- Open source approach to accelerate immunological discoveries

We're committed to advancing scientific research and welcome contributions from immunologists, bioinformaticians, and AI researchers.

## Setup

### Prerequisites

- [uv](https://github.com/astral-sh/uv) package manager
- Database access credentials (for TCR databases)
- Biomedical API keys (PubMed, ClinicalTrials.gov, etc.)

### Installation

The system leverages [uv](https://github.com/astral-sh/uv) as its package manager to streamline dependency management.
Follow the steps below to set up a virtual environment and install the necessary dependencies:

```bash
# Step 1: Create and activate a virtual environment through uv
uv python install 3.12
uv venv --python 3.12

source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Step 2: Install project dependencies
uv sync
```

By completing these steps, you'll ensure your environment is properly configured and ready for immunological research.

### Configuration

The system uses a three-tier LLM system with separate configurations for reasoning, basic tasks, and vision-language tasks. Create a `.env` file in the project root and configure the following environment variables:

```ini
# Reasoning LLM Configuration (for complex immunological reasoning)
REASONING_PROVIDER=openai  # Choose "openai" or "deepseek"
REASONING_MODEL=your_reasoning_model
REASONING_API_KEY=your_reasoning_api_key
REASONING_BASE_URL=your_custom_base_url  # Optional

# Basic LLM Configuration (for simpler tasks)
BASIC_MODEL=your_basic_model
BASIC_API_KEY=your_basic_api_key
BASIC_BASE_URL=your_custom_base_url  # Optional

# Vision-Language LLM Configuration (for tasks involving images/plots)
VL_MODEL=your_vl_model
VL_API_KEY=your_vl_api_key
VL_BASE_URL=your_custom_base_url  # Optional

# Database Configuration
DATABASE_URL=your_database_connection_string
VDJDB_PATH=path_to_vdjdb_database

# Biomedical API Keys
PUBMED_API_KEY=your_pubmed_api_key  # Optional, for higher rate limits
CLINICALTRIALS_API_KEY=your_clinicaltrials_api_key  # Optional
DRUGBANK_API_KEY=your_drugbank_api_key  # Optional

# Tool API Keys
TAVILY_API_KEY=your_tavily_api_key
JINA_API_KEY=your_jina_api_key  # Optional

# Browser Configuration
CHROME_INSTANCE_PATH=/Applications/Google Chrome.app/Contents/MacOS/Google Chrome  # Optional
```

> **Note:**
>
> - The system uses different models for different types of research tasks:
>     - Reasoning LLM for complex immunological analysis and hypothesis generation
>     - Basic LLM for simpler text-based biomedical tasks
>     - Vision-Language LLM for analyzing research plots and molecular diagrams
> - Database configuration is required for TCR analysis functionality
> - Biomedical API keys provide access to specialized databases and higher rate limits
> - All configurations can be customized based on your research requirements

You can copy the `.env.example` file as a template to get started:

```bash
cp .env.example .env
```

### Configure Pre-commit Hook
The system includes a pre-commit hook that runs linting and formatting checks before each commit. To set it up:

1. Make the pre-commit script executable:
```bash
chmod +x pre-commit
```

2. Install the pre-commit hook:
```bash
ln -s ../../pre-commit .git/hooks/pre-commit
```

The pre-commit hook will automatically:
- Run linting checks (`make lint`)
- Run code formatting (`make format`)
- Add any reformatted files back to staging
- Prevent commits if there are any linting or formatting errors

## Usage

### Basic Execution

To run the system with default settings (both deep thinking and search before planning enabled):

```bash
uv run main.py
```

You can also pass your immunological research query directly as an argument:

```bash
uv run main.py "Analyze TCR sequences associated with autoimmune diseases in VDJDB"
```

### Advanced Execution Options

The system supports several command line options to control the research workflow behavior:

```bash
# Show all available options
uv run main.py --help

# Disable deep thinking mode (for faster but less thorough analysis)
uv run main.py --no-deep-thinking "Your research query here"

# Disable search before planning (skip initial literature review phase)
uv run main.py --no-search-before-planning "Your research query here"

# Disable both modes for fastest execution
uv run main.py --no-deep-thinking --no-search-before-planning "Your research query here"

# Explicitly enable modes (default behavior)
uv run main.py --deep-thinking --search-before-planning "Your research query here"
```

**Command Line Options:**
- `--deep-thinking` / `--no-deep-thinking`: Enable/disable deep immunological analysis mode (default: enabled)
- `--search-before-planning` / `--no-search-before-planning`: Enable/disable literature search before planning (default: enabled)
- `--help`: Show usage information and available options

### API Server

The system provides a FastAPI-based API server with streaming support for research workflows:

```bash
# Start the API server
make serve

# Or run directly
uv run server.py
```

The API server exposes the following endpoints:

- `POST /api/chat/stream`: Research endpoint for immunological queries with streaming support
    - Request body:
    ```json
    {
      "messages": [
        {"role": "user", "content": "Your immunological research query here"}
      ],
      "debug": false
    }
    ```
    - Returns a Server-Sent Events (SSE) stream with the agent's research responses

### Advanced Configuration

The system can be customized through various configuration files in the `src/config` directory:
- `env.py`: Configure LLM models, API keys, and base URLs
- `tools.py`: Adjust tool-specific settings for biomedical databases
- `agents.py`: Modify research team composition and agent system prompts
- `vdjdb.py`: Configure VDJDB database access and analysis parameters

### Agent Prompts System

The system uses a sophisticated prompting system in the `src/prompts` directory to define specialized agent behaviors for immunological research:

#### Core Agent Roles

- **Supervisor ([`src/prompts/supervisor.md`](src/prompts/supervisor.md))**: Coordinates the research team and delegates immunological tasks by analyzing research requests and determining which specialist should handle them.

- **Biomedical Researcher ([`src/prompts/biomedical_researcher.md`](src/prompts/biomedical_researcher.md))**: Specializes in immunological literature search, biomedical database queries, and scientific hypothesis generation using PubMed, BioArxiv, and other biomedical resources.

- **Data Analyst ([`src/prompts/data_analyst.md`](src/prompts/data_analyst.md))**: Handles TCR database analysis, statistical computations, and data visualization for immunological datasets.

- **Researcher ([`src/prompts/researcher.md`](src/prompts/researcher.md))**: General information gathering through web searches and data collection, complementing specialized biomedical research.

- **Coder ([`src/prompts/coder.md`](src/prompts/coder.md))**: Handles Python code execution for bioinformatics analysis, statistical modeling, and immunological data processing.

- **File Manager ([`src/prompts/file_manager.md`](src/prompts/file_manager.md))**: Manages research outputs, reports, and data files with proper formatting for scientific documentation.

- **Browser ([`src/prompts/browser.md`](src/prompts/browser.md))**: Web interaction specialist for accessing online biomedical databases and research portals.

#### Prompt System Architecture

The prompts system uses a template engine ([`src/prompts/template.py`](src/prompts/template.py)) that:
- Loads role-specific markdown templates optimized for biomedical research
- Handles variable substitution for research context
- Formats system prompts for each specialized agent

Each agent's prompt is defined in a separate markdown file, making it easy to modify behavior and research capabilities without changing the underlying code.

## Web UI

The system provides a specialized web UI for immunological research workflows.

Please refer to the frontend directory for the research-focused web interface.

## Development

### Testing

Run the test suite:

```bash
# Run all tests
make test

# Run specific biomedical test file
pytest tests/agents/test_biomedical_researcher.py

# Run TCR analysis tests
pytest tests/integration/test_tcr_analysis.py

# Run with coverage
make coverage
```

### Code Quality

```bash
# Run linting
make lint

# Format code
make format
```

## Contributing

We welcome contributions from immunologists, bioinformaticians, and AI researchers! Whether you're fixing a bug, improving documentation, adding new biomedical integrations, or enhancing TCR analysis capabilities, your help is appreciated. Please see our [Contributing Guide](CONTRIBUTING.md) for details on how to get started.

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

Special thanks to:
- [LangManus](https://github.com/langmanus/langmanus) for the inspiring multi-agent architecture
- The VDJDB team for maintaining the T-cell receptor database
- PubMed and other biomedical database providers
- The open source bioinformatics community
- All contributors advancing immunological research through AI
