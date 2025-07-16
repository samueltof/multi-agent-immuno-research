# Multi-Agent Immunological Research System

## Project Overview

The Multi-Agent Immunological Research System is a specialized AI-powered framework designed for comprehensive immunological research, particularly focusing on T-cell receptor (TCR) analysis and biomedical research workflows. This system implements a hierarchical multi-agent architecture where specialized AI agents collaborate to accomplish complex immunological research tasks.

## Vision Statement

**Mission**: Advancing immunological research through AI by providing researchers with automated tools for literature search, data analysis, and hypothesis generation in the immunology domain.

**Core Values**:
- Open source approach to accelerate immunological discoveries
- Scientific rigor and reproducibility
- Multi-modal analysis combining literature, clinical data, and molecular information
- Collaborative agent-based problem solving

## Architecture Overview

### Multi-Agent System Design

The system implements a hierarchical multi-agent architecture with 7 specialized agents:

1. **Coordinator** - Initial query handling and task routing
2. **Planner** - Research strategy development and execution planning
3. **Supervisor** - Workflow orchestration and agent management
4. **Biomedical Researcher** - Literature search and biomedical data analysis
5. **Data Analyst** - TCR database queries and statistical analysis
6. **Browser** - Web browsing and information retrieval
7. **Reporter** - Research report generation and insights synthesis

### Three-Tier LLM System

The system uses a sophisticated LLM configuration:
- **Reasoning LLM**: Complex immunological analysis and hypothesis generation
- **Basic LLM**: Simple text-based biomedical tasks
- **Vision-Language LLM**: Analysis of research plots and molecular diagrams

### Core Architecture Principles

- **Modularity**: Each agent has specific responsibilities and capabilities
- **Scalability**: Agents can be added or modified without affecting the core system
- **Flexibility**: Support for multiple LLM providers and models
- **Reliability**: Robust error handling and fallback mechanisms

## Technical Stack

### Core Technologies

- **Language**: Python 3.12+
- **Package Management**: uv (Astral UV) for dependency management
- **Web Framework**: FastAPI for API server with streaming support
- **Database Support**: PostgreSQL, MySQL, SQLite, MS SQL, AWS Athena
- **AI/ML**: OpenAI-compatible API interfaces, multi-provider LLM support

### Key Dependencies

- **Agent Framework**: LangGraph for multi-agent orchestration
- **Biomedical APIs**: PubMed, BioArxiv, ClinicalTrials.gov, DrugBank, OpenTargets
- **Database**: SQLAlchemy for database abstraction
- **Web Scraping**: Browser automation for biomedical data retrieval
- **Data Analysis**: Built-in Python REPL for statistical analysis

### Development Tools

- **Testing**: pytest with coverage reporting
- **Code Quality**: Pre-commit hooks with linting and formatting
- **Documentation**: Markdown-based documentation system
- **Version Control**: Git with structured branching

## Project Structure

```
multi-agent-immuno-research/
├── src/
│   ├── agents/                 # Agent implementations
│   │   ├── biomedical_researcher.py
│   │   ├── data_team.py
│   │   ├── agents.py
│   │   └── llm.py
│   ├── api/                    # FastAPI server
│   │   └── app.py
│   ├── config/                 # Configuration management
│   │   └── logger.py
│   ├── graph/                  # LangGraph workflow definitions
│   │   ├── nodes.py
│   │   └── types.py
│   ├── prompts/                # Agent prompt templates
│   │   ├── supervisor.md
│   │   ├── biomedical_researcher.md
│   │   ├── data_analyst.md
│   │   ├── researcher.md
│   │   ├── coder.md
│   │   ├── file_manager.md
│   │   ├── browser.md
│   │   └── template.py
│   ├── service/                # Core services
│   │   ├── database/           # Database connections
│   │   ├── mcps/              # Model Context Protocol servers
│   │   └── workflow_service.py
│   ├── tools/                  # Specialized tools
│   │   ├── database.py
│   │   ├── tcr_analysis.py
│   │   ├── search.py
│   │   ├── browser.py
│   │   └── crawl.py
│   └── crawler/                # Web crawling utilities
├── evals/                      # Evaluation framework
│   ├── agents/                 # Agent-specific evaluations
│   └── docs/                   # Evaluation documentation
├── tests/                      # Test suite
├── frontend/                   # Web UI (separate)
├── assets/                     # Documentation assets
├── main.py                     # CLI entry point
├── server.py                   # API server entry point
└── README.md                   # Project documentation
```

## Configuration Management

### Configuration Files

- `src/config/env.py`: LLM models and API configuration
- `src/config/tools.py`: Tool-specific settings
- `src/config/agents.py`: Agent system prompts and composition
- `src/config/vdjdb.py`: VDJDB database configuration

## Core Features and Capabilities

### Biomedical Research Tools

1. **Literature Search and Analysis**
   - PubMed integration for peer-reviewed literature
   - BioArxiv preprint analysis
   - Automated literature review generation

2. **Clinical Data Integration**
   - ClinicalTrials.gov database access
   - DrugBank pharmaceutical data
   - OpenTargets therapeutic target information

3. **TCR Database Analysis**
   - VDJDB integration for T-cell receptor analysis
   - Custom TCR sequence analysis tools
   - Pattern recognition in immunological data

4. **Statistical Analysis**
   - Built-in Python REPL for data analysis
   - Statistical modeling capabilities
   - Data visualization tools

### Workflow Management

1. **Research Modes**
   - Deep thinking mode for thorough analysis
   - Search-before-planning for literature review
   - Fast execution mode for quick queries

2. **Multi-Agent Orchestration**
   - Task delegation and progress monitoring
   - Workflow graph visualization
   - Agent coordination and communication

3. **Output Generation**
   - Research report generation
   - Scientific documentation formatting
   - Data export capabilities

## Constraints and Limitations

### Technical Constraints

- **Python 3.12+**: Minimum Python version requirement
- **Memory**: Large language models require substantial memory
- **API Limits**: Rate limiting on external biomedical APIs
- **Database**: Requires access to specialized biomedical databases

### Scientific Constraints

- **Data Quality**: Dependent on external database accuracy
- **Literature Coverage**: Limited to indexed publications
- **Domain Expertise**: Requires domain knowledge for result validation
- **Reproducibility**: Results may vary based on model versions

### Operational Constraints

- **API Costs**: LLM usage incurs costs based on tokens
- **Response Time**: Complex queries may take significant time
- **Scalability**: Limited by available computational resources
- **Dependencies**: Reliance on external services and APIs

## Usage Patterns

### Command Line Interface

```bash
# Basic execution
uv run main.py "Your research query"

# Advanced options
uv run main.py --no-deep-thinking --no-search-before-planning "Query"

# Help and documentation
uv run main.py --help
```

### API Server

```bash
# Start server
uv run server.py

# API endpoint
POST /api/chat/stream
Content-Type: application/json
{
  "messages": [{"role": "user", "content": "Research query"}],
  "debug": false
}
```

## Integration Points

### External Services

- **PubMed**: Literature search and retrieval
- **ClinicalTrials.gov**: Clinical trial data
- **DrugBank**: Pharmaceutical information
- **OpenTargets**: Therapeutic target data
- **VDJDB**: T-cell receptor database

### Database Connections

- **PostgreSQL**: Primary database option
- **MySQL**: Alternative database support
- **SQLite**: Local development database
- **MS SQL**: Enterprise database support
- **AWS Athena**: Cloud analytics database

### LLM Providers

- **OpenAI**: GPT models for reasoning tasks
- **DeepSeek**: Alternative reasoning model
- **Custom**: Support for custom API endpoints
- **Local**: Support for local model deployment

## Future Roadmap

### Planned Enhancements

1. **Agent Capabilities**
   - Additional specialized agents for specific research areas
   - Enhanced reasoning capabilities
   - Multi-modal analysis improvements

2. **Database Integration**
   - Additional biomedical database connections
   - Real-time data synchronization
   - Advanced query optimization

3. **User Interface**
   - Web-based research dashboard
   - Interactive visualization tools
   - Collaborative research features

4. **Performance Optimization**
   - Caching mechanisms for frequently accessed data
   - Parallel processing for complex queries
   - Resource usage optimization

### Research Applications

- **Drug Discovery**: Automated literature review and hypothesis generation
- **Vaccine Development**: TCR analysis and immune response prediction
- **Autoimmune Research**: Pattern recognition in immunological data
- **Clinical Trial Analysis**: Systematic review of clinical outcomes

## Testing & Quality Assurance

* **Framework**: `pytest` for unit and integration tests.
* **Coverage**: Target ≥ 90% line coverage; fail build if below threshold.
* **Test Types**:

  * **Unit Tests**: Service functions, utilities.
  * **Integration Tests**: API endpoints, authentication flows.
  * **End-to-End**: Simulated requests against a test instance (e.g., via `requests` or `httpx`).
* **Fixtures & Mocks**: Use `pytest-mock` or `responses` to stub external calls (Crawl4AI, Drive API).
* **LLM-as-Judge Evaluations**: Leverage an LLM-based judge framework to automatically assess qualitative outputs (e.g., summary accuracy, extraction quality).

## Documentation & Onboarding

* **README.md**: Quickstart instructions, env setup, sample calls.
* **TASKS.md**: Backlog of stories, tasks, and subtasks.