# Coder Agent Evaluation Framework

This directory contains a comprehensive evaluation framework for the Coder agent using OpenEvals with LLM-as-a-judge methodology.

## Overview

The Coder agent is a ReAct agent that specializes in:
- Python code generation and execution
- Data analysis and statistical computation
- Data visualization and plotting
- Data processing and manipulation
- Algorithm implementation
- Debugging and error handling

## Evaluation Framework

### Key Components

1. **Evaluators** (`evaluators.py`)
   - **Code Correctness**: Uses OpenEvals prebuilt evaluator for code quality
   - **Code Execution**: Evaluates successful execution and meaningful output
   - **Data Analysis Quality**: Assesses statistical methods and insights
   - **Visualization Quality**: Evaluates plot quality and appropriateness
   - **Code Style**: Reviews readability and best practices
   - **Task Completion**: Measures how well requirements were met

2. **Test Dataset** (`test_dataset.py`)
   - Comprehensive test cases covering various coding scenarios
   - Categorized by task type and difficulty level
   - Includes sample data and success criteria

3. **Evaluation Runner** (`evaluation_runner.py`)
   - Orchestrates the evaluation process
   - Handles agent execution and result collection
   - Generates comprehensive reports and summaries

### Evaluation Metrics

#### Overall Score Weighting
- **Task Completion**: 30% - Most important metric
- **Code Correctness**: 25% - Technical accuracy
- **Code Execution**: 20% - Functional success
- **Data Analysis**: 15% - Quality of insights
- **Visualization**: 5% - Plot quality (when applicable)
- **Code Style**: 5% - Readability and best practices

#### Individual Metrics
Each metric is scored on a 0.0-1.0 scale with detailed explanations.

### Test Case Categories

1. **Data Analysis** (`data_analysis_*`)
   - Statistical computation and analysis
   - Descriptive statistics and correlations
   - Trend analysis and insights

2. **Visualization** (`visualization_*`)
   - Plot generation and formatting
   - Multi-plot dashboards
   - Interactive visualizations

3. **Data Processing** (`data_processing_*`)
   - Data cleaning and preprocessing
   - Data pipeline creation
   - File merging and transformations

4. **Algorithm Implementation** (`algorithm_*`)
   - Recommendation systems
   - Time series forecasting
   - Machine learning algorithms (clustering, classification)

5. **Debugging** (`debugging_*`)
   - Error identification and fixing
   - Code improvement and optimization
   - Error handling implementation

### Data Sources

Test cases use two approaches to provide data, mimicking real-world agent usage:

1. **File-based data**: Some tests reference CSV files in `test_data/` folder to evaluate the agent's ability to read from the filesystem
2. **Memory-based data**: Other tests include data directly in task descriptions, simulating data passed through state memory

This hybrid approach ensures comprehensive evaluation of the coder agent's data handling capabilities in different scenarios.

## Usage

### Quick Start

```bash
# Run quick evaluation (subset of test cases)
python run_evaluation.py --quick

# Run full evaluation (all test cases)
python run_evaluation.py --full

# Run specific test case
python run_evaluation.py --case data_analysis_001
```

### Programmatic Usage

```python
from evals.agents.coder import run_quick_evaluation, run_full_evaluation

# Quick evaluation
results = await run_quick_evaluation()

# Full evaluation
results = await run_full_evaluation()

# Custom evaluation
from evals.agents.coder import CoderEvaluationRunner, get_test_cases_by_type

runner = CoderEvaluationRunner()
data_analysis_cases = get_test_cases_by_type("data_analysis")
results = await runner.run_evaluation_suite(data_analysis_cases)
```

### Custom Evaluators

```python
from evals.agents.coder.evaluators import (
    create_code_correctness_evaluator,
    create_code_execution_evaluator,
    CoderAgentEvaluator
)

# Use individual evaluators
correctness_eval = create_code_correctness_evaluator()
execution_eval = create_code_execution_evaluator()

# Use comprehensive evaluator
evaluator = CoderAgentEvaluator(model="openai:o3-mini")
results = evaluator.evaluate_response(
    task_description="Your task description",
    agent_response="Agent's response with code",
    expected_deliverables="What should be delivered"
)
```

## Configuration

### Environment Variables
Ensure these are set in your `.env` file:
```
OPENAI_API_KEY=your_openai_api_key
```

### Dependencies
The evaluation framework requires:
- `openevals` - LLM-as-judge evaluation framework
- `langchain` - Agent framework
- Standard Python data science stack (pandas, numpy, matplotlib)

## Output Structure

Evaluation results are saved in JSON format with the following structure:

```json
{
  "timestamp": "2024-01-15T10:30:00",
  "summary": {
    "total_cases": 10,
    "successful_cases": 9,
    "failed_cases": 1,
    "success_rate": 0.9,
    "average_score": 0.78,
    "by_task_type": {...},
    "by_difficulty": {...},
    "by_metric": {...}
  },
  "successful_evaluations": [...],
  "failed_evaluations": [...],
  "dataset_info": {...}
}
```

## Example Test Case

```python
CoderTestCase(
    id="data_analysis_002",
    task_description="""
    Analyze the following sales data (passed from state memory):

    ```
    date,product_category,units_sold,revenue,region
    2024-01-15,Electronics,120,24000,North
    2024-01-20,Clothing,85,4250,South
    ...
    ```
    
    Tasks:
    1. Parse the CSV data from the text above
    2. Calculate total revenue by product category
    3. Find monthly sales trends
    4. Identify the best performing region
    """,
    task_type="data_analysis",
    difficulty="medium",
    expected_deliverables="Statistical analysis with data parsing, revenue summaries...",
    sample_data="date,product_category,units_sold,revenue,region\n...",
    success_criteria=[
        "Parses CSV data from text correctly",
        "Aggregates revenue by category correctly",
        "Identifies monthly trends"
    ]
)
```

## Adding New Test Cases

1. Add test case to appropriate category in `test_dataset.py`
2. Include comprehensive task description and expected deliverables
3. Specify success criteria for evaluation
4. Add sample data if needed

## Extending Evaluators

To add new evaluation metrics:

1. Create custom prompt template
2. Implement evaluator function using `create_llm_as_judge`
3. Add to `CoderAgentEvaluator` class
4. Update scoring weights as needed

## Integration with OpenEvals

This framework leverages OpenEvals capabilities:
- **Prebuilt Code Evaluators**: `create_code_llm_as_judge` with `CODE_CORRECTNESS_PROMPT`
- **Custom LLM-as-Judge**: Custom prompts for domain-specific evaluation
- **Code Extraction**: Automatic extraction of Python code from agent responses
- **Plot Detection**: Identification of generated visualizations

## Best Practices

1. **Test Case Design**
   - Clear, specific task descriptions
   - Realistic sample data
   - Measurable success criteria

2. **Evaluation Consistency**
   - Use consistent evaluation model (e.g., `openai:o3-mini`)
   - Regular calibration of evaluation prompts
   - Multiple runs for statistical significance

3. **Result Analysis**
   - Focus on overall trends rather than individual scores
   - Compare performance across task types and difficulty levels
   - Use detailed comments to understand failure modes

## Troubleshooting

**Common Issues:**
- **Import Errors**: Ensure project root is in Python path
- **API Errors**: Check OpenAI API key and quotas
- **Agent Errors**: Verify coder agent configuration and tool availability

**Performance Tips:**
- Use smaller model for quick iterations (`gpt-3.5-turbo`)
- Run subset evaluations during development
- Cache evaluation results for analysis

## Future Enhancements

- **Execution Sandboxing**: Integration with E2B for safe code execution
- **Performance Metrics**: Code efficiency and runtime analysis  
- **Security Evaluation**: Assessment of code security practices
- **Multi-language Support**: Extension to other programming languages 