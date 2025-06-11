# TCR Data Analysis Agent - Tool Integration Guide

## Overview

The TCR (T-Cell Receptor) Data Analysis Agent extends the standard data analysis workflow with specialized tools for immunogenomics research. This agent is specifically designed for analyzing immune repertoire data from VDJdb and other TCR databases.

## How TCR Tools Are Integrated

### 1. **TCR-Specific Tools Available**

The TCR Data Agent has access to the following specialized tools:

#### Core Database Tools
- `get_vdjdb_schema` - Enhanced schema tool with TCR-specific context and analysis patterns
- `execute_sql_query` - Standard SQL execution against VDJdb SQLite database
- `get_random_subsamples` - Sample data extraction from TCR tables

#### TCR Analysis Tools
- `calculate_tcr_diversity_metrics` - Shannon diversity, Simpson index, clonality analysis
- `analyze_cdr3_motifs` - CDR3 sequence pattern analysis and amino acid usage
- `compare_tcr_repertoires` - Compare TCR repertoires between patient groups

### 2. **Agent Workflow Integration**

```python
# TCR tools are integrated into the ReAct agent
tcr_sql_generating_agent = create_react_agent(
    llm_client, 
    tools=[
        get_vdjdb_schema,                    # 🧬 TCR-specific schema
        execute_sql_query,                   # 📊 SQL execution  
        get_random_subsamples,               # 📋 Data sampling
        calculate_tcr_diversity_metrics,     # 📈 Diversity analysis
        analyze_cdr3_motifs,                 # 🔍 Motif analysis
        compare_tcr_repertoires              # ⚖️  Repertoire comparison
    ]
)
```

### 3. **Usage Examples**

#### Example 1: TCR Diversity Analysis
```python
# User query: "Calculate the diversity of TCR clonotypes in cancer patients"

# The agent will:
# 1. Use get_vdjdb_schema to understand the database structure
# 2. Generate SQL to extract clonotype counts:
#    SELECT cdr3_sequence, v_gene, j_gene, COUNT(*) as frequency 
#    FROM tcr_sequences 
#    WHERE LENGTH(cdr3_sequence) BETWEEN 8 AND 25 
#    GROUP BY cdr3_sequence, v_gene, j_gene
# 3. Use calculate_tcr_diversity_metrics on the results
# 4. Return Shannon diversity, Simpson index, and biological interpretation
```

#### Example 2: CDR3 Motif Analysis  
```python
# User query: "Analyze CDR3 sequence patterns in melanoma patients"

# The agent will:
# 1. Extract CDR3 sequences from relevant patients
# 2. Use analyze_cdr3_motifs to find common patterns
# 3. Return motif analysis with amino acid usage and common 3-mers/4-mers
```

#### Example 3: Repertoire Comparison
```python
# User query: "Compare TCR repertoires between responders and non-responders"

# The agent will:
# 1. Extract repertoires for both groups
# 2. Use compare_tcr_repertoires to calculate overlap
# 3. Return diversity differences and biological interpretation
```

### 4. **TCR-Specific Prompt Context**

The TCR agent uses a specialized prompt (`tcr_data_analyst.md`) that includes:

- **Immunological Expertise**: CDR3 biology, V/D/J genes, epitope binding
- **Analysis Patterns**: Clonotype identification, diversity metrics, clinical correlation
- **Query Guidelines**: TCR-specific SQL patterns and biological filters
- **Interpretation**: Biological context for statistical results

### 5. **Agent Selection**

Users can access the TCR-specialized agent through:

```python
from src.agents.agents import tcr_data_analyst_agent

# The agent automatically uses TCR tools when processing queries like:
# - "What is the clonal diversity in this dataset?"
# - "Find common CDR3 motifs"
# - "Compare repertoires between treatment groups"
# - "Identify epitope-specific TCR signatures"
```

### 6. **Integration with Main Workflow**

The TCR agent is integrated into the main agent system:

```python
# In src/agents/agents.py
AGENT_LLM_MAP = {
    # ... other agents
    "tcr_data_analyst": "reasoning",  # Uses reasoning LLM for complex analysis
}

# Available agents
__all__ = [
    "research_agent",
    "coder_agent", 
    "browser_agent",
    "data_analyst_agent",
    "tcr_data_analyst_agent",  # 🧬 TCR-specialized agent
    "biomedical_researcher_agent",
]
```

## Key Advantages

1. **Specialized Tools**: TCR-specific analysis functions beyond basic SQL
2. **Biological Context**: Immunogenomics expertise built into prompts
3. **Quality Filters**: Automatic application of TCR data quality standards
4. **Integrated Workflow**: Seamless combination of SQL queries and TCR analysis
5. **Clinical Relevance**: Built-in interpretation for cancer immunotherapy research

## Configuration

TCR analysis can be configured via environment variables:

```bash
# VDJdb Database
VDJDB_SQLITE_PATH=data/vdjdb.db

# Analysis Parameters  
MIN_CDR3_LENGTH=8
MAX_CDR3_LENGTH=25
MIN_CONFIDENCE_SCORE=0.5

# Feature Toggles
ENABLE_MOTIF_ANALYSIS=true
ENABLE_DIVERSITY_ANALYSIS=true
ENABLE_CLINICAL_CORRELATION=true
```

This integration makes the framework truly specialized for cancer immunogenomics research as described in your abstract. 