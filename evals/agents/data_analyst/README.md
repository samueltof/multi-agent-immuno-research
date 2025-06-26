# Data Analyst Agent Evaluation

This directory contains a comprehensive evaluation framework for the Data Analyst agent, designed to assess its ability to understand natural language queries, generate correct SQL, and provide meaningful insights from the VDJdb augmented database.

## Overview

The Data Analyst agent is the most complex agent in our multi-agent system, featuring:
- **Schema Understanding**: Automatic database schema retrieval and understanding
- **SQL Generation**: Converting natural language to SQLite queries using ReAct agent
- **Query Validation**: LLM-based SQL validation before execution
- **Query Execution**: Safe execution with error handling and recovery
- **Result Interpretation**: Clear presentation and analysis of results

## Evaluation Framework

### 🎯 **Evaluation Dimensions**

Our evaluation assesses the agent across multiple dimensions:

1. **SQL Correctness** (25% weight)
   - Syntactic correctness of generated SQL
   - Semantic alignment with natural language query
   - Use of appropriate SQLite functions and clauses

2. **Schema Understanding** (20% weight)
   - Correct table and column references
   - Proper foreign key relationships
   - Understanding of database structure

3. **Query Execution** (20% weight)
   - Successful query execution
   - Meaningful results returned
   - Error handling when applicable

4. **Result Interpretation** (15% weight)
   - Clear explanation of results
   - Appropriate context and insights
   - User-friendly presentation

5. **Domain Knowledge** (10% weight)
   - Understanding of immunological concepts
   - Proper use of TCR/epitope/MHC terminology
   - Biologically relevant insights

6. **Workflow Completeness** (10% weight)
   - Complete end-to-end processing
   - Proper step sequencing
   - Error recovery mechanisms

### 🧪 **Test Dataset**

Our test dataset includes **20 comprehensive test cases** covering:

#### Schema Exploration (2 cases)
- Database schema requests
- Table-specific schema queries

#### Simple Queries (3 cases)
- Basic counting and selection
- DISTINCT operations
- Simple filtering

#### Join Operations (3 cases)
- Multi-table joins with foreign keys
- Complex relationship navigation
- Tissue/donor sample analysis

#### Aggregation Queries (3 cases)
- GROUP BY operations
- Statistical functions (AVG, COUNT)
- MHC class distribution analysis

#### Statistical Analysis (2 cases)
- Correlation analysis
- Outlier detection

#### Temporal Analysis (2 cases)
- Time-based filtering
- Trend analysis

#### Immunological Domain Queries (4 cases)
- TCR alpha-beta pairing
- V-J segment analysis
- Promiscuous epitope identification
- CDR3 diversity calculations

#### Complex Multi-table Analysis (1 case)
- Comprehensive data integration
- Research contribution analysis

### 🧬 **VDJdb Augmented Database**

The evaluation uses a sophisticated hybrid database:

**Real Immunological Data:**
- 46,714 TCR complexes
- 116,740 TCR chains  
- 1,116 epitopes
- 155 MHC alleles
- 254 publications

**Synthetic Contextual Data:**
- 706 donors with demographics
- 1,177 biological samples
- 93,307 experimental assays

**Database Schema:**
```sql
epitopes: epitope_id, sequence, length, ic50, source_protein, species
mhc_alleles: allele_id, allele_name, locus, class, resolution  
donors: donor_id, species, age, sex, health_status
samples: sample_id, donor_id, tissue, collection_date
publications: pub_id, reference_id, title, journal, pub_date, authors
complexes: complex_id, epitope_id, mhc_a_id, mhc_b_id, sample_id, pub_id
chains: chain_id, complex_id, gene, cdr3, v_segm, j_segm, vdjdb_score
assays: assay_id, complex_id, assay_type, lab, date_run
```

## Usage

### Quick Start

```python
import asyncio
from evals.agents.data_analyst import run_quick_evaluation

# Run evaluation on specific test cases
results = await run_quick_evaluation(["simple_001", "join_001", "agg_001"])
```

### Full Evaluation Suite

```python
from evals.agents.data_analyst import DataAnalystEvaluationRunner

# Initialize runner
runner = DataAnalystEvaluationRunner(
    output_dir="evals/outputs/data_analyst",
    evaluator_model="openai:gpt-4o-mini"
)

# Run all test cases
results = await runner.run_evaluation_suite()
```

### Custom Test Selection

```python
from evals.agents.data_analyst import get_test_cases_by_difficulty, get_test_cases_by_type

# Run only hard difficulty cases
hard_cases = get_test_cases_by_difficulty("hard")
results = await runner.run_evaluation_suite(hard_cases)

# Run only immunological domain cases
immuno_cases = get_test_cases_by_type("immunological")
results = await runner.run_evaluation_suite(immuno_cases)
```

### Command Line Execution

```bash
# Quick evaluation
cd evals/agents/data_analyst
python run_evaluation.py

# Or run the evaluation runner directly
python evaluation_runner.py
```

## Output and Reporting

### Evaluation Results

The evaluation generates comprehensive results including:

```json
{
  "timestamp": "2024-01-15T10:30:00",
  "test_cases_count": 20,
  "successful_evaluations": 18,
  "failed_evaluations": 2,
  "summary": {
    "overall_average_score": 0.82,
    "average_scores_by_metric": {
      "sql_correctness": 0.85,
      "schema_understanding": 0.88,
      "query_execution": 0.79,
      "result_interpretation": 0.83,
      "domain_knowledge": 0.76,
      "workflow_completeness": 0.81
    },
    "performance_by_difficulty": {
      "easy": 0.91,
      "medium": 0.84,
      "hard": 0.72
    },
    "performance_by_query_type": {
      "simple": 0.94,
      "join": 0.87,
      "aggregation": 0.83,
      "immunological": 0.74
    }
  }
}
```

### File Outputs

- **JSON Results**: `evaluation_results_YYYYMMDD_HHMMSS.json`
- **Logs**: `data_analyst_evaluation_YYYYMMDD_HHMMSS.log`
- **Summary Report**: Console output with key metrics

## Test Case Examples

### Simple Query Example
```python
DataAnalystTestCase(
    id="simple_001",
    natural_language_query="How many epitopes are there in the database?",
    query_type="simple",
    difficulty="easy",
    expected_sql_pattern="SELECT COUNT(*) FROM epitopes",
    expected_tables=["epitopes"],
    expected_columns=["epitope_id"],
    success_criteria=[
        "Uses COUNT(*) or COUNT(epitope_id)",
        "Queries epitopes table",
        "Returns single count value"
    ],
    domain_context="Basic counting of peptide epitopes"
)
```

### Complex Immunological Query Example
```python
DataAnalystTestCase(
    id="immuno_003",
    natural_language_query="Find epitopes that are presented by multiple different MHC alleles",
    query_type="immunological", 
    difficulty="hard",
    expected_sql_pattern="SELECT.*epitope_id.*COUNT.*DISTINCT.*mhc.*HAVING COUNT.*> 1",
    expected_tables=["complexes", "epitopes"],
    expected_columns=["epitope_id", "mhc_a_id", "mhc_b_id"],
    success_criteria=[
        "Groups by epitope_id",
        "Counts distinct MHC alleles per epitope", 
        "Uses HAVING clause for multiple presentations",
        "Identifies promiscuous epitopes"
    ],
    domain_context="Finding epitopes presented by multiple MHC molecules (vaccine design relevance)"
)
```

## Evaluation Metrics

### Success Criteria
Each test case includes specific success criteria that are checked:
- Correct SQL syntax and logic
- Appropriate table and column usage
- Proper handling of relationships
- Domain-appropriate analysis
- Clear result interpretation

### Scoring System
- **0.0-0.2**: Poor performance, major issues
- **0.2-0.4**: Basic functionality with significant problems  
- **0.4-0.6**: Adequate performance with some issues
- **0.6-0.8**: Good performance with minor issues
- **0.8-1.0**: Excellent performance, minor to no issues

## Configuration

### Environment Setup
Ensure your `.env` file contains the VDJdb database paths:
```bash
DATABASE_NAME=/path/to/vdjdb_augmented.db
SQLITE_PATH=/path/to/vdjdb_augmented.db
DATABASE_SCHEMA_PATH=/path/to/schema_description.yaml
QUERY_EXAMPLES_PATH=/path/to/query_examples.csv
VDJDB_SQLITE_PATH=/path/to/vdjdb_augmented.db
```

### Model Configuration
The evaluation uses OpenEvals with configurable LLM models:
- Default: `openai:gpt-4o-mini`
- Alternative: `openai:gpt-4o`, `anthropic:claude-3-sonnet`

## Extending the Evaluation

### Adding New Test Cases
1. Create new `DataAnalystTestCase` objects in `test_dataset.py`
2. Add to appropriate category lists
3. Update `ALL_DATA_ANALYST_TEST_CASES`

### Custom Evaluators
1. Create new evaluator functions in `evaluators.py`
2. Add to `DataAnalystAgentEvaluator` class
3. Update scoring weights as needed

### New Evaluation Dimensions
1. Define new prompt templates
2. Create evaluator functions
3. Integrate into evaluation workflow

## Performance Benchmarks

### Expected Performance Ranges
Based on initial testing:
- **SQL Correctness**: 0.80-0.95
- **Schema Understanding**: 0.85-0.95  
- **Query Execution**: 0.75-0.90
- **Result Interpretation**: 0.80-0.90
- **Domain Knowledge**: 0.70-0.85
- **Overall Score**: 0.78-0.88

### Difficulty-Based Expectations
- **Easy**: >0.90 overall score
- **Medium**: 0.80-0.90 overall score  
- **Hard**: 0.70-0.85 overall score

## Troubleshooting

### Common Issues
1. **Database Connection**: Verify `.env` paths are correct
2. **Import Errors**: Ensure all dependencies are installed
3. **API Limits**: Monitor OpenEvals API usage
4. **Memory Issues**: Reduce concurrent evaluations for large test suites

### Debug Mode
Enable verbose logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Future Enhancements

- **Performance Benchmarking**: Historical tracking of evaluation scores
- **Regression Testing**: Automated evaluation on code changes  
- **Cross-Model Comparison**: Evaluation across different LLM backends
- **Interactive Analysis**: Web dashboard for evaluation results
- **Domain Expansion**: Additional immunological query types 