# Biomedical Researcher Agent Evaluation Framework

This directory contains a comprehensive evaluation framework for the Biomedical Researcher agent using LLM-as-a-Judge methodology with the `openevals` package.

## Overview

The evaluation framework assesses the Biomedical Researcher agent across four key dimensions:

- **Factual Correctness**: Accuracy of biomedical data, statements, and claims
- **Relevance**: How well the response addresses the biomedical research query
- **Source Quality**: Assessment of cited sources' credibility and relevance
- **Confidence Alignment**: Whether stated confidence matches evidence quality

## Components

### 1. Evaluators (`evaluators.py`)

Custom LLM-as-a-Judge evaluators specifically designed for biomedical research:

```python
from evaluators import BiomedicalResearcherEvaluator

evaluator = BiomedicalResearcherEvaluator()
results = evaluator.evaluate_response(prompt, response, reference_outputs)
```

**Individual Evaluators:**
- `create_biomedical_factual_correctness_evaluator()`: Assesses scientific accuracy
- `create_biomedical_relevance_evaluator()`: Evaluates query relevance
- `create_biomedical_source_quality_evaluator()`: Reviews source credibility
- `create_biomedical_confidence_alignment_evaluator()`: Checks confidence calibration

### 2. Test Dataset (`test_dataset.py`)

Comprehensive test cases covering multiple biomedical domains:

- **Oncology**: Cancer research, immunotherapy, clinical trials
- **Immunology**: Vaccines, autoimmune diseases, immune mechanisms
- **Pharmacology**: Drug mechanisms, interactions, pharmacogenomics
- **Clinical Research**: Biomarkers, diagnostic methods, treatment protocols
- **Rare Diseases**: Gene therapies, orphan drugs
- **Infectious Diseases**: Antimicrobial resistance, treatment strategies

```python
from test_dataset import BIOMEDICAL_TEST_CASES, get_test_case_by_id

test_case = get_test_case_by_id("oncology_001")
print(test_case.prompt)
```

### 3. Evaluation Runner (`evaluation_runner.py`)

Orchestrates the complete evaluation process:

```python
from evaluation_runner import EvaluationRunner

runner = EvaluationRunner()
results = await runner.run_evaluation_suite()
```

**Features:**
- Concurrent evaluation processing
- Comprehensive result logging
- Automatic report generation
- Error handling and recovery
- Result persistence

### 4. Demo Script (`demo_evaluation.py`)

Demonstrates the framework with mock data:

```python
python -m evals.agents.biomedical_researcher.demo_evaluation
```

## Quick Start

### 1. Install Dependencies

```bash
pip install openevals langsmith
```

### 2. Run Demo

```bash
cd evals/agents/biomedical_researcher
python demo_evaluation.py
```

### 3. Run Evaluation on Specific Test Cases

```python
import asyncio
from evaluation_runner import run_quick_evaluation

# Run on specific test cases
results = await run_quick_evaluation(
    test_case_ids=["basic_001", "oncology_002"]
)
```

### 4. Run Full Evaluation Suite

```python
import asyncio
from evaluation_runner import run_full_evaluation

# Run on all test cases
results = await run_full_evaluation()
```

## Configuration

### Environment Variables

Set these environment variables for API access:

```bash
export OPENAI_API_KEY="your-openai-key"
export LANGSMITH_API_KEY="your-langsmith-key"  # Optional
```

### Evaluator Configuration

```python
evaluator = BiomedicalResearcherEvaluator(
    model="openai:gpt-4o-mini"  # or "openai:gpt-4o"
)
```

### Runner Configuration

```python
runner = EvaluationRunner(
    output_dir="evals/outputs/biomedical_researcher",
    evaluator_model="openai:gpt-4o-mini",
    agent_config={
        # Your agent configuration
    }
)
```

## Test Dataset Structure

Each test case includes:

```python
@dataclass
class BiomedicalTestCase:
    id: str                    # Unique identifier
    prompt: str               # Research question/prompt
    domain: str               # Medical domain (oncology, immunology, etc.)
    difficulty: str           # basic, intermediate, expert
    expected_sources: List[str]  # Expected source types
    key_concepts: List[str]   # Key concepts to address
    reference_info: str       # Reference information (optional)
```

## Evaluation Metrics

### Scoring Scale

All metrics use a 0.0-1.0 scale with specific thresholds:
- **1.0**: Excellent/Perfect
- **0.8**: Good with minor issues
- **0.6**: Adequate with some concerns
- **0.4**: Poor with significant issues
- **0.2**: Very poor with major problems
- **0.0**: Unacceptable/Dangerous

### Overall Score Calculation

Weighted average of individual metrics:
- Factual Correctness: 40% (most critical)
- Relevance: 30%
- Source Quality: 20%
- Confidence Alignment: 10%

## Results Structure

```json
{
  "evaluation_summary": {
    "total_cases": 12,
    "successful_cases": 11,
    "failed_cases": 1,
    "success_rate": 0.917,
    "average_score": 0.756,
    "scores_by_domain": {...},
    "scores_by_difficulty": {...},
    "metric_averages": {...}
  },
  "successful_evaluations": [...],
  "failed_evaluations": [...],
  "evaluation_config": {...}
}
```

## Integration with Actual Agent

✅ **COMPLETED**: The evaluation framework is now fully integrated with the actual `BiomedicalResearcherWrapper` agent. The integration includes:

- Proper async context management for MCP servers
- Correct dependency passing (research focus, preferred databases)
- Automatic conversion from `BiomedicalResearchOutput` to evaluation format
- Robust error handling for agent failures

The agent is called using:
```python
async with self.agent as researcher:
    result = await researcher.run_research(test_case.prompt, deps)
```

Response format automatically handled:
```python
{
    "summary": str,                    # Research summary
    "key_findings": List[str],         # List of key findings
    "sources": List[Dict[str, str]],   # Cited sources with metadata
    "recommendations": List[str],      # Research recommendations
    "confidence_level": float          # 0.0-1.0
}
```

## Extending the Framework

### Adding New Test Cases

```python
# Add to BIOMEDICAL_TEST_CASES in test_dataset.py
new_case = BiomedicalTestCase(
    id="new_domain_001",
    prompt="What are the latest developments in...",
    domain="new_domain",
    difficulty="intermediate",
    expected_sources=["PubMed", "ClinicalTrials.gov"],
    key_concepts=["concept1", "concept2"],
    reference_info="Reference information..."
)
```

### Adding New Evaluators

```python
# Create custom evaluator
CUSTOM_PROMPT = """
Your custom evaluation prompt here...
"""

def create_custom_evaluator(model="openai:gpt-4o-mini"):
    return create_llm_as_judge(
        prompt=CUSTOM_PROMPT,
        model=model,
        choices=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
        feedback_key="custom_metric"
    )
```

### Custom Evaluation Metrics

Add new metrics to the `BiomedicalResearcherEvaluator` class:

```python
class BiomedicalResearcherEvaluator:
    def __init__(self, model="openai:gpt-4o-mini"):
        # ... existing evaluators ...
        self.custom_evaluator = create_custom_evaluator(model)
    
    def evaluate_response(self, prompt, response, reference_outputs=None):
        # ... existing evaluations ...
        evaluations['custom_metric'] = self.custom_evaluator(...)
        return evaluations
```

## Best Practices

### 1. Test Case Design
- Write clear, specific research questions
- Include appropriate difficulty levels
- Cover diverse biomedical domains
- Provide reference information when possible

### 2. Evaluation Interpretation
- Consider domain-specific challenges
- Account for difficulty level differences
- Focus on consistent evaluation criteria
- Review individual metric comments for insights

### 3. Agent Improvement
- Analyze low-scoring categories
- Review failed test cases for patterns
- Iterate on agent design based on results
- Monitor improvement over time

## Troubleshooting

### Common Issues

1. **API Rate Limits**: Reduce `max_concurrent` parameter
2. **Evaluation Timeouts**: Use shorter prompts or faster models
3. **Memory Issues**: Process test cases in smaller batches
4. **Import Errors**: Ensure all dependencies are installed

### Debugging

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Performance Optimization

- Use `openai:gpt-4o-mini` for faster/cheaper evaluation
- Implement result caching for repeated evaluations
- Process evaluations in parallel when possible

## Future Enhancements

- [ ] Integration with LangSmith for experiment tracking
- [ ] Automated evaluation scheduling
- [ ] Performance benchmarking against baselines
- [ ] A/B testing framework for agent improvements
- [ ] Domain-specific evaluation fine-tuning
- [ ] Real-time evaluation dashboards

## Contributing

To contribute to the evaluation framework:

1. Add test cases for underrepresented domains
2. Improve evaluation prompt engineering
3. Add new evaluation metrics
4. Enhance result visualization
5. Optimize evaluation performance

## License

This evaluation framework is part of the multi-agent immuno-research project. 