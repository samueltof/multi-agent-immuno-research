# Web Researcher Agent Evaluation System

A comprehensive evaluation framework for the Web Researcher agent using LLM-as-a-Judge methodology from OpenEvals.

## Overview

The Web Researcher agent is designed for general web research tasks, using web search and content crawling to gather information and answer queries. This evaluation system assesses the agent's performance across multiple dimensions:

### Key Capabilities Evaluated

1. **Search Quality**: Effectiveness of web search strategies and query formulation
2. **Crawling Quality**: Accuracy and relevance of content extraction from web pages
3. **Information Synthesis**: Quality of combining and synthesizing multiple web sources
4. **Source Quality**: Assessment of the credibility and relevance of web sources used
5. **Research Completeness**: Coverage and depth of research on given topics
6. **RAG Effectiveness**: Quality of retrieval and use of web content as knowledge base

### Agent Architecture

The researcher agent differs from the biomedical researcher by having:
- **Broader Information Access**: Uses general web search rather than specialized databases
- **Web Crawling Capabilities**: Extracts content from multiple web pages concurrently
- **General Domain Knowledge**: Covers technology, science, business, health, current events, etc.
- **RAG-based Approach**: Uses web content as a dynamic knowledge base

## Evaluation Framework

### LLM-as-a-Judge Methodology

The evaluation system uses OpenEvals' LLM-as-a-Judge framework with custom prompts designed for web research evaluation:

```python
from openevals.llm import create_llm_as_judge

# Example: Search Quality Evaluator
search_evaluator = create_llm_as_judge(
    prompt=SEARCH_QUALITY_PROMPT,
    model="openai:o3-mini",
    feedback_key="search_quality"
)
```

### Evaluation Metrics

1. **Search Quality (0-1 scale)**
   - Relevance of search queries to research questions
   - Use of appropriate search terms and keywords
   - Diversity of search strategies
   - Quality and relevance of search results

2. **Crawling Quality (0-1 scale)**
   - Accuracy of content extraction from web pages
   - Relevance of crawled content to research questions
   - Quality of content filtering and noise reduction
   - Effective handling of different content types

3. **Information Synthesis (0-1 scale)**
   - Integration of information from multiple sources
   - Identification of common themes and contradictions
   - Logical organization and structure
   - Clear attribution and source connections

4. **Source Quality (0-1 scale)**
   - Credibility and authority of source websites
   - Recency and currency of information
   - Relevance to specific research questions
   - Diversity of source types and perspectives

5. **Research Completeness (0-1 scale)**
   - Coverage of all major aspects of research questions
   - Depth of analysis and exploration
   - Identification of important subtopics
   - Appropriate level of detail

6. **Overall Score**: Weighted average of all individual metrics

## Test Dataset

The evaluation dataset contains 20+ carefully curated test cases covering various domains:

### Domains Covered

- **Technology**: AI/ML developments, quantum computing, autonomous vehicles
- **Science**: CRISPR research, climate change, dark matter/energy
- **Business**: Cryptocurrency regulation, real estate trends, inflation analysis
- **Health**: Long COVID, weight loss medications, Alzheimer's research
- **Current Events**: Elections, geopolitical conflicts
- **Environment**: Renewable energy, sustainability

### Difficulty Levels

- **Basic**: Straightforward research questions with clear answers
- **Intermediate**: Multi-faceted questions requiring analysis across sources
- **Expert**: Complex research requiring deep domain knowledge and synthesis

### Test Case Structure

```python
@dataclass
class ResearcherTestCase:
    id: str
    prompt: str
    domain: str
    difficulty: str
    expected_sources: List[str]  # Types of sources expected
    key_concepts: List[str]      # Key concepts to address
    search_keywords: List[str]   # Expected search terms
    reference_info: str          # Reference information
    requires_recent_info: bool   # Whether current info is needed
```

## Usage

### Quick Start

```bash
# Run a quick evaluation on selected test cases
cd evals/agents/researcher
python run_evaluation.py --mode quick

# Run evaluation on a specific domain
python run_evaluation.py --domain technology

# Run evaluation on specific difficulty level
python run_evaluation.py --difficulty expert

# Custom test cases
python run_evaluation.py --mode custom --test-cases tech_001 science_002
```

### Programmatic Usage

```python
from evals.agents.researcher import EvaluationRunner, RESEARCHER_TEST_CASES

# Initialize evaluation runner
runner = EvaluationRunner(
    output_dir="evals/outputs/researcher",
    evaluator_model="openai:o3-mini"
)

# Run evaluation on specific test case
test_case = RESEARCHER_TEST_CASES[0]
result = runner.run_single_evaluation(test_case)

# Run full evaluation suite
results = await runner.run_evaluation_suite()
```

### Running Demonstrations

```python
# Run comprehensive demo
python demo_evaluation.py

# Features demonstrated:
# - Single test case evaluation
# - Domain-specific evaluation
# - RAG component evaluation
# - Comparative metric analysis
```

## Results Analysis

### Visualization

The system provides comprehensive visualization capabilities:

```python
from evals.agents.researcher.visualize_results import visualize_results

# Generate all visualizations
visualize_results("path/to/results.json")
```

**Generated Visualizations:**
- Overall score distribution
- Performance by domain and difficulty
- Metric performance heatmap
- Search vs crawling quality correlation
- Source quality distribution
- Information synthesis performance
- RAG effectiveness analysis

### Report Generation

Detailed reports include:
- Summary statistics
- Domain performance analysis
- Metric performance breakdown
- Individual test case results
- Recommendations for improvement

## Configuration

### Environment Variables

```bash
# Required for LLM evaluation
OPENAI_API_KEY=your_openai_key

# Optional: for web search functionality
TAVILY_API_KEY=your_tavily_key
```

### Evaluator Configuration

```python
# Custom evaluator configuration
evaluator = ResearcherEvaluator(
    model="openai:o3-mini",  # LLM for evaluation
)

# Custom evaluation runner
runner = EvaluationRunner(
    output_dir="custom/output/dir",
    evaluator_model="openai:o3-mini",
    agent_config={
        # Custom agent configuration
    }
)
```

## RAG-Specific Evaluation

The system includes specialized evaluation for RAG components:

```python
# Evaluate RAG components separately
rag_results = evaluator.evaluate_rag_components(
    prompt="Research question",
    retrieved_content="Crawled web content",
    generated_response="Agent's final response"
)
```

**RAG Metrics:**
- **Retrieval Quality**: Relevance of retrieved web content
- **Content Utilization**: How well the agent uses retrieved content
- **Response Generation**: Quality of final response based on retrieved content

## Integration with LangSmith

The evaluation system can be integrated with LangSmith for advanced monitoring:

```python
from langsmith import Client
from openevals.llm import create_llm_as_judge

client = Client()

# Wrapper for LangSmith integration
def wrapped_evaluator(inputs, outputs, reference_outputs):
    eval_result = evaluator(inputs=inputs, outputs=outputs)
    return eval_result

# Run with LangSmith
experiment_results = client.evaluate(
    lambda inputs: research_agent.invoke(inputs),
    data="researcher_test_dataset",
    evaluators=[wrapped_evaluator]
)
```

## Best Practices

### Test Case Design

1. **Diverse Domains**: Cover multiple knowledge areas
2. **Varied Difficulty**: Include basic to expert-level questions
3. **Clear Expectations**: Define expected sources and concepts
4. **Current Relevance**: Include questions requiring recent information

### Evaluation Guidelines

1. **Consistent Criteria**: Use standardized evaluation prompts
2. **Multiple Runs**: Average results across multiple evaluations
3. **Error Handling**: Gracefully handle agent failures
4. **Comprehensive Metrics**: Evaluate all aspects of research quality

### Performance Optimization

1. **Concurrent Evaluation**: Limit concurrent evaluations to avoid rate limits
2. **Caching**: Cache evaluation results for repeated analysis
3. **Incremental Testing**: Start with quick evaluations before full runs

## Troubleshooting

### Common Issues

1. **API Rate Limits**: Reduce `max_concurrent` parameter
2. **Agent Timeouts**: Increase timeout settings in agent configuration
3. **Missing Dependencies**: Install required packages for visualization

```bash
pip install matplotlib seaborn pandas numpy
```

### Debug Mode

```python
# Enable detailed logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Run single evaluation with debug info
runner = EvaluationRunner(output_dir="debug_output")
result = runner.run_single_evaluation(test_case)
```

## Contributing

### Adding New Test Cases

1. Add test cases to `test_dataset.py`
2. Follow the `ResearcherTestCase` structure
3. Include appropriate metadata (domain, difficulty, expected sources)
4. Test the new cases with the evaluation system

### Extending Evaluators

1. Create new evaluation prompts in `evaluators.py`
2. Implement evaluator functions following the existing pattern
3. Update the `ResearcherEvaluator` class to include new metrics
4. Add corresponding visualization methods

### Custom Domains

1. Define domain-specific test cases
2. Create specialized evaluation criteria if needed
3. Update visualization methods to handle new domains

## License

This evaluation system is part of the multi-agent immuno-research project and follows the same licensing terms.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the demo scripts for usage examples
3. Examine the visualization outputs for insights
4. Create issues in the project repository

---

**Note**: This evaluation system is designed to work with the general web researcher agent. For biomedical research evaluation, see the `biomedical_researcher` evaluation system. 