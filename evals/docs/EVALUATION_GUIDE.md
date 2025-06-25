# Biomedical Researcher Evaluation Guide

This guide explains how to run evaluations using the expanded cancer immunogenomics dataset.

## Dataset Overview

The expanded dataset contains **36 comprehensive test cases** across **12 specialized domains**:

- **Total Cases**: 36 (perfect for statistical robustness)
- **Domains**: 12 (3 cases each for balanced coverage)
- **Difficulty Distribution**: 3 basic, 14 intermediate, 19 expert
- **Priority Distribution**: 20 high-priority, 16 standard
- **Aligned with Agent Capabilities**: PubMed, ClinicalTrials.gov, BioRxiv/MedRxiv, OpenTargets

### Domains Covered:
1. **TCR Analysis** - T-cell receptor repertoire and binding prediction
2. **Neoantigen Prediction** - HLA typing and computational pipelines
3. **Tumor Microenvironment** - Immune infiltration and T-cell exhaustion
4. **Immunotherapy Biomarkers** - TMB, MSI, interferon signatures
5. **CAR-T Therapy** - Engineering and clinical applications
6. **Cancer Genomics** - Immune evasion mechanisms
7. **Immune Resistance** - Resistance mechanisms and microbiome
8. **Combination Therapy** - Multi-modal immunotherapy strategies
9. **Cancer Vaccines** - Personalized and shared antigen approaches
10. **Computational Tools** - Bioinformatics and machine learning
11. **Clinical Translation** - Regulatory and economic considerations
12. **Immune Foundations** - Basic immunology concepts

## Running Evaluations

### Prerequisites

1. **Environment Setup**:
   ```bash
   # Ensure you have the required API keys in your .env file
   OPENAI_API_KEY=your_openai_key_here
   LANGSMITH_API_KEY=your_langsmith_key_here  # Optional
   LANGSMITH_TRACING=true  # Optional
   ```

2. **Project Structure**:
   ```
   multi-agent-immuno-research/
   ├── evals/agents/biomedical_researcher/
   │   ├── run_expanded_evaluation.py
   │   ├── evaluation_runner.py
   │   ├── test_dataset_expanded.py
   │   ├── evaluators.py
   │   └── ...
   ```

### Command Line Interface

**Always run from the project root**:

```bash
cd /path/to/multi-agent-immuno-research
python evals/agents/biomedical_researcher/run_expanded_evaluation.py [OPTIONS]
```

### Evaluation Options

#### 1. Show Dataset Information
```bash
python evals/agents/biomedical_researcher/run_expanded_evaluation.py --info
```
Shows complete dataset statistics and domain distribution.

#### 2. Full Evaluation (36 cases)
```bash
python evals/agents/biomedical_researcher/run_expanded_evaluation.py --full
```
- **Duration**: ~50-70 minutes
- **Use Case**: Comprehensive evaluation for research papers/conferences
- **Output**: `evals/outputs/biomedical_researcher/full_expanded/`

#### 3. High-Priority Evaluation (20 cases)
```bash
python evals/agents/biomedical_researcher/run_expanded_evaluation.py --high-priority
```
- **Duration**: ~30-40 minutes
- **Use Case**: Conference presentation focus
- **Output**: `evals/outputs/biomedical_researcher/high_priority_expanded/`

#### 4. Balanced Subset Evaluation
```bash
python evals/agents/biomedical_researcher/run_expanded_evaluation.py --balanced 15
```
- **Duration**: ~20-30 minutes
- **Use Case**: Quick comprehensive testing
- **Output**: `evals/outputs/biomedical_researcher/balanced_15_expanded/`

#### 5. Domain-Specific Evaluation
```bash
python evals/agents/biomedical_researcher/run_expanded_evaluation.py --domain tcr_analysis
```
- **Duration**: ~5-10 minutes (3 cases)
- **Use Case**: Focused testing on specific research areas
- **Available Domains**: `tcr_analysis`, `neoantigen_prediction`, `tumor_microenvironment`, `immunotherapy_biomarkers`, `cart_therapy`, `cancer_genomics`, `immune_resistance`, `combination_therapy`, `cancer_vaccines`, `computational_tools`, `clinical_translation`, `immune_foundations`

#### 6. Specific Test Cases
```bash
python evals/agents/biomedical_researcher/run_expanded_evaluation.py --cases tcr_001 tcr_002 biomarkers_001
```
- **Duration**: ~2-5 minutes per case
- **Use Case**: Debug specific test cases or focused evaluation

### Output Files

Each evaluation generates multiple output files:

```
evals/outputs/biomedical_researcher/[evaluation_type]/
├── evaluation_results_[timestamp].json      # Complete results
├── evaluation_summary_[timestamp].json      # Summary statistics  
├── visualization_data_[timestamp].json      # Data for plotting
├── evaluation_[timestamp].log              # Detailed logs
└── visualizations/                         # Generated plots (if applicable)
```

### Results Structure

The evaluation results include:

```json
{
  "summary": {
    "total_cases": 36,
    "successful_cases": 35,
    "failed_cases": 1,
    "success_rate": 0.972,
    "average_score": 0.943,
    "min_score": 0.820,
    "max_score": 0.990,
    "domain_performance": {...},
    "difficulty_performance": {...}
  },
  "successful_evaluations": [...],
  "failed_evaluations": [...],
  "test_dataset_summary": {...}
}
```

### Performance Expectations

Based on previous evaluations, you can expect:

- **Success Rate**: 95-100%
- **Average Score**: 0.90-0.97
- **Score Range**: 0.80-0.99
- **Domain Variation**: Some domains may perform better than others
- **Difficulty Impact**: Expert cases may have slightly lower scores

### Troubleshooting

#### Common Issues:

1. **Import Errors**: Always run from project root
2. **API Key Issues**: Check `.env` file configuration
3. **MCP Server Conflicts**: Evaluations run sequentially (max_concurrent=1)
4. **Memory Issues**: For full evaluation, ensure adequate system resources

#### Debug Commands:

```bash
# Test single case
python evals/agents/biomedical_researcher/run_expanded_evaluation.py --cases foundations_001

# Test specific domain
python evals/agents/biomedical_researcher/run_expanded_evaluation.py --domain immune_foundations

# Small balanced subset
python evals/agents/biomedical_researcher/run_expanded_evaluation.py --balanced 5
```

### Evaluation Metrics

The evaluation uses 4 specialized LLM-as-a-judge metrics powered by **GPT-4o**:

1. **Factual Correctness** (40% weight) - Scientific accuracy and medical facts
2. **Relevance** (30% weight) - Query alignment and domain appropriateness
3. **Source Quality** (20% weight) - Citation credibility and evidence quality
4. **Confidence Alignment** (10% weight) - Confidence calibration

### Best Practices

1. **Start Small**: Begin with `--balanced 5` to test setup
2. **Monitor Progress**: Check logs for any issues during evaluation
3. **Resource Management**: Full evaluations can take 1+ hour
4. **Result Analysis**: Use visualization data for detailed analysis
5. **Conference Presentation**: Use `--high-priority` for key results

### Example Workflow

```bash
# 1. Check dataset info
python evals/agents/biomedical_researcher/run_expanded_evaluation.py --info

# 2. Quick test with small subset
python evals/agents/biomedical_researcher/run_expanded_evaluation.py --balanced 5

# 3. Run high-priority cases for conference
python evals/agents/biomedical_researcher/run_expanded_evaluation.py --high-priority

# 4. Full evaluation for comprehensive analysis
python evals/agents/biomedical_researcher/run_expanded_evaluation.py --full
```

This evaluation framework provides robust, scientifically-grounded assessment of your biomedical research agent's performance across the full spectrum of cancer immunogenomics research. 