"""
Custom LLM-as-a-Judge evaluators for the Biomedical Researcher agent.

This module provides specialized evaluators for assessing:
- Factual Correctness: Accuracy of biomedical data, statements, and claims
- Relevance: Degree to which the response addresses the biomedical research prompt
- Source Quality: Assessment of the quality and relevance of cited sources
- Confidence Alignment: How well the confidence level aligns with the response quality
"""

from typing import Any, Dict, List, Optional
from openevals.llm import create_llm_as_judge
from openevals.types import EvaluatorResult


# Custom prompts for biomedical research evaluation
BIOMEDICAL_FACTUAL_CORRECTNESS_PROMPT = """
You are an expert biomedical researcher and fact-checker evaluating the factual correctness of biomedical research outputs.

Your task is to assess the accuracy of biomedical data, statements, and claims made in the response.

Consider the following criteria:
- Scientific accuracy of medical facts, drug mechanisms, disease pathways
- Correctness of statistical data, clinical trial results, and research findings
- Proper use of biomedical terminology and concepts
- Absence of medical misinformation or outdated information

Rate the factual correctness on a scale of 0-1:
- 1.0: All facts are accurate, current, and properly contextualized
- 0.8: Mostly accurate with minor inaccuracies that don't affect core conclusions
- 0.6: Generally accurate but contains some notable factual errors
- 0.4: Mixed accuracy with significant factual errors
- 0.2: Mostly inaccurate with few correct facts
- 0.0: Severely inaccurate or contains dangerous misinformation

<prompt>
{inputs}
</prompt>

<response>
{outputs}
</response>

<reference_sources>
{reference_outputs}
</reference_sources>

Provide your evaluation as a score between 0.0 and 1.0, and explain your reasoning.
"""

BIOMEDICAL_RELEVANCE_PROMPT = """
You are an expert biomedical researcher evaluating the relevance of a research response to a given biomedical query.

Your task is to assess how well the response addresses the specific biomedical research question or prompt.

Consider the following criteria:
- Direct relevance to the research question or clinical problem
- Coverage of key aspects mentioned in the prompt
- Appropriateness of the biomedical context and scope
- Alignment with the intended research domain (e.g., oncology, immunology, pharmacology)

Rate the relevance on a scale of 0-1:
- 1.0: Perfectly addresses all aspects of the biomedical query
- 0.8: Addresses most key aspects with minor gaps
- 0.6: Addresses main aspects but misses some important elements
- 0.4: Partially relevant but significant gaps or tangential content
- 0.2: Minimally relevant with major gaps
- 0.0: Completely irrelevant or off-topic

<prompt>
{inputs}
</prompt>

<response>
{outputs}
</response>

Provide your evaluation as a score between 0.0 and 1.0, and explain your reasoning.
"""

BIOMEDICAL_SOURCE_QUALITY_PROMPT = """
You are an expert biomedical librarian and research methodologist evaluating the quality of sources cited in a biomedical research response.

Your task is to assess the quality, relevance, and appropriateness of the sources referenced.

Consider the following criteria:
- Credibility of sources (peer-reviewed journals, reputable databases, clinical trials)
- Recency and currency of the information
- Relevance of sources to the specific biomedical query
- Diversity and comprehensiveness of source types
- Proper attribution and citation practices

Rate the source quality on a scale of 0-1:
- 1.0: Excellent sources - all high-quality, relevant, and properly cited
- 0.8: Good sources with minor quality or relevance issues
- 0.6: Adequate sources but some quality concerns
- 0.4: Mixed quality with notable concerns about source credibility
- 0.2: Poor sources with significant quality issues
- 0.0: Unreliable or inappropriate sources

<prompt>
{inputs}
</prompt>

<response>
{outputs}
</response>

<sources_cited>
{sources}
</sources_cited>

Provide your evaluation as a score between 0.0 and 1.0, and explain your reasoning.
"""

BIOMEDICAL_CONFIDENCE_ALIGNMENT_PROMPT = """
You are an expert biomedical researcher evaluating whether the stated confidence level in a research response aligns with the quality and certainty of the information provided.

Your task is to assess if the confidence level is appropriate given the:
- Strength of evidence presented
- Quality of sources cited
- Certainty of the biomedical claims made
- Acknowledgment of limitations or uncertainties

Rate the confidence alignment on a scale of 0-1:
- 1.0: Confidence level perfectly matches the strength of evidence
- 0.8: Confidence level is well-aligned with minor mismatches
- 0.6: Generally appropriate confidence with some concerns
- 0.4: Confidence level somewhat mismatched (over or under-confident)
- 0.2: Significant mismatch between confidence and evidence quality
- 0.0: Severely inappropriate confidence level

<prompt>
{inputs}
</prompt>

<response>
{outputs}
</response>

<stated_confidence>
{confidence}
</stated_confidence>

Provide your evaluation as a score between 0.0 and 1.0, and explain your reasoning.
"""


def create_biomedical_factual_correctness_evaluator(model: str = "openai:gpt-4o-mini"):
    """Create an evaluator for biomedical factual correctness."""
    return create_llm_as_judge(
        prompt=BIOMEDICAL_FACTUAL_CORRECTNESS_PROMPT,
        model=model,
        choices=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
        feedback_key="biomedical_factual_correctness"
    )


def create_biomedical_relevance_evaluator(model: str = "openai:gpt-4o-mini"):
    """Create an evaluator for biomedical relevance."""
    return create_llm_as_judge(
        prompt=BIOMEDICAL_RELEVANCE_PROMPT,
        model=model,
        choices=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
        feedback_key="biomedical_relevance"
    )


def create_biomedical_source_quality_evaluator(model: str = "openai:gpt-4o-mini"):
    """Create an evaluator for biomedical source quality."""
    return create_llm_as_judge(
        prompt=BIOMEDICAL_SOURCE_QUALITY_PROMPT,
        model=model,
        choices=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
        feedback_key="biomedical_source_quality"
    )


def create_biomedical_confidence_alignment_evaluator(model: str = "openai:gpt-4o-mini"):
    """Create an evaluator for biomedical confidence alignment."""
    return create_llm_as_judge(
        prompt=BIOMEDICAL_CONFIDENCE_ALIGNMENT_PROMPT,
        model=model,
        choices=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
        feedback_key="biomedical_confidence_alignment"
    )


class BiomedicalResearcherEvaluator:
    """Comprehensive evaluator for the Biomedical Researcher agent."""
    
    def __init__(self, model: str = "openai:gpt-4o-mini"):
        self.model = model
        self.factual_correctness_evaluator = create_biomedical_factual_correctness_evaluator(model)
        self.relevance_evaluator = create_biomedical_relevance_evaluator(model)
        self.source_quality_evaluator = create_biomedical_source_quality_evaluator(model)
        self.confidence_alignment_evaluator = create_biomedical_confidence_alignment_evaluator(model)
    
    def evaluate_response(
        self,
        prompt: str,
        response: Dict[str, Any],
        reference_outputs: Optional[str] = None
    ) -> Dict[str, EvaluatorResult]:
        """
        Evaluate a biomedical researcher response comprehensively.
        
        Args:
            prompt: The original research question/prompt
            response: The agent's response (BiomedicalResearchOutput)
            reference_outputs: Reference information for comparison (optional)
        
        Returns:
            Dictionary of evaluation results by metric
        """
        # Extract relevant parts from the response
        summary = response.get('summary', '')
        key_findings = response.get('key_findings', [])
        sources = response.get('sources', [])
        confidence = response.get('confidence_level', 0.0)
        
        # Convert key_findings to text if it's a list
        if isinstance(key_findings, list):
            key_findings_text = '\n'.join([f"- {finding}" for finding in key_findings])
        else:
            key_findings_text = str(key_findings)
        
        # Combine summary and key findings for evaluation
        response_text = summary + '\n\nKey Findings:\n' + key_findings_text
        
        # Convert sources to text for evaluation
        if isinstance(sources, list):
            if sources and isinstance(sources[0], dict):
                # Handle sources as list of dicts
                sources_text = '\n'.join([f"- {source.get('title', 'Unknown')}: {source.get('url', 'No URL')}" for source in sources])
            else:
                # Handle sources as list of strings
                sources_text = '\n'.join([f"- {source}" for source in sources])
        else:
            sources_text = str(sources) if sources else "No sources cited"
        
        evaluations = {}
        
        # Factual Correctness
        evaluations['factual_correctness'] = self.factual_correctness_evaluator(
            inputs=prompt,
            outputs=response_text,
            reference_outputs=reference_outputs or "No reference provided"
        )
        
        # Relevance
        evaluations['relevance'] = self.relevance_evaluator(
            inputs=prompt,
            outputs=response_text
        )
        
        # Source Quality
        evaluations['source_quality'] = self.source_quality_evaluator(
            inputs=prompt,
            outputs=response_text,
            sources=sources_text
        )
        
        # Confidence Alignment
        evaluations['confidence_alignment'] = self.confidence_alignment_evaluator(
            inputs=prompt,
            outputs=response_text,
            confidence=str(confidence)
        )
        
        return evaluations
    
    def calculate_overall_score(self, evaluations: Dict[str, EvaluatorResult]) -> float:
        """Calculate an overall score from individual evaluations."""
        weights = {
            'factual_correctness': 0.4,  # Most important for biomedical research
            'relevance': 0.3,
            'source_quality': 0.2,
            'confidence_alignment': 0.1
        }
        
        total_score = 0.0
        total_weight = 0.0
        
        for metric, weight in weights.items():
            if metric in evaluations:
                score = evaluations[metric].get('score', 0.0)
                total_score += score * weight
                total_weight += weight
        
        return total_score / total_weight if total_weight > 0 else 0.0 