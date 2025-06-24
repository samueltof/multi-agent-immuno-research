"""
Custom LLM-as-a-Judge evaluators for the Web Researcher agent.

This module provides specialized evaluators for assessing:
- Search Quality: Effectiveness of web search strategies and query formulation
- Crawling Quality: Accuracy and relevance of content extraction from web pages
- Information Synthesis: Quality of combining and synthesizing multiple web sources
- Source Quality: Assessment of the credibility and relevance of web sources used
- Research Completeness: Coverage and depth of research on the given topic
- RAG Effectiveness: Quality of retrieval and use of web content as knowledge base
"""

from typing import Any, Dict, List, Optional
from openevals.llm import create_llm_as_judge
from openevals.types import EvaluatorResult


# Custom prompts for web researcher evaluation

SEARCH_QUALITY_PROMPT = """
You are an expert information scientist evaluating the quality of web search strategies and results.

Your task is to assess how effectively the researcher formulated search queries and utilized search results.

Consider the following criteria:
- Relevance of search queries to the research question
- Use of appropriate search terms and keywords
- Diversity of search strategies employed
- Quality and relevance of search results obtained
- Effective use of domain filtering and search parameters

Rate the search quality on a scale of 0-1:
- 1.0: Excellent search strategy with highly relevant, comprehensive results
- 0.8: Good search approach with mostly relevant results and minor gaps
- 0.6: Adequate search strategy but some missed opportunities or irrelevant results
- 0.4: Limited search effectiveness with notable gaps in query formulation
- 0.2: Poor search strategy with mostly irrelevant or low-quality results
- 0.0: Ineffective search approach that fails to address the research question

<research_question>
{inputs}
</research_question>

<search_strategy_and_results>
{outputs}
</search_strategy_and_results>

<expected_keywords>
{search_keywords}
</expected_keywords>

Provide your evaluation as a score between 0.0 and 1.0, and explain your reasoning.
"""

CRAWLING_QUALITY_PROMPT = """
You are an expert web content analyst evaluating the quality of web crawling and content extraction.

Your task is to assess how effectively the researcher extracted and processed content from web sources.

Consider the following criteria:
- Accuracy of content extraction from web pages
- Relevance of crawled content to the research question
- Quality of content filtering and noise reduction
- Preservation of important information during extraction
- Effective handling of different content types and formats

Rate the crawling quality on a scale of 0-1:
- 1.0: Excellent content extraction with high accuracy and relevance
- 0.8: Good crawling with mostly accurate extraction and minor issues
- 0.6: Adequate content extraction but some quality concerns
- 0.4: Limited crawling effectiveness with notable extraction issues
- 0.2: Poor content extraction with significant accuracy problems
- 0.0: Failed content extraction that misses key information

<research_question>
{inputs}
</research_question>

<crawled_content>
{outputs}
</crawled_content>

<source_urls>
{sources}
</source_urls>

Provide your evaluation as a score between 0.0 and 1.0, and explain your reasoning.
"""

INFORMATION_SYNTHESIS_PROMPT = """
You are an expert research analyst evaluating the quality of information synthesis from multiple web sources.

Your task is to assess how well the researcher combined, analyzed, and synthesized information from different sources.

Consider the following criteria:
- Effective integration of information from multiple sources
- Identification of common themes and contradictions across sources
- Logical organization and structure of synthesized information
- Balanced representation of different perspectives and viewpoints
- Clear attribution and connection between claims and sources

Rate the information synthesis quality on a scale of 0-1:
- 1.0: Excellent synthesis that seamlessly integrates multiple sources with clear insights
- 0.8: Good synthesis with effective integration and minor organizational issues
- 0.6: Adequate synthesis but some gaps in integration or organization
- 0.4: Limited synthesis quality with notable issues in combining sources
- 0.2: Poor synthesis that fails to effectively integrate multiple sources
- 0.0: No meaningful synthesis, just disconnected information from sources

<research_question>
{inputs}
</research_question>

<synthesized_response>
{outputs}
</synthesized_response>

<source_information>
{sources}
</source_information>

Provide your evaluation as a score between 0.0 and 1.0, and explain your reasoning.
"""

SOURCE_QUALITY_PROMPT = """
You are an expert information literacy specialist evaluating the quality and credibility of web sources used in research.

Your task is to assess the credibility, relevance, and appropriateness of the sources cited and used.

Consider the following criteria:
- Credibility and authority of source websites and publications
- Recency and currency of information (especially for time-sensitive topics)
- Relevance of sources to the specific research question
- Diversity of source types and perspectives
- Appropriate use of authoritative sources for the domain

Rate the source quality on a scale of 0-1:
- 1.0: Excellent sources - all highly credible, relevant, and appropriate
- 0.8: Good sources with high credibility and minor relevance issues
- 0.6: Adequate sources but some credibility or relevance concerns
- 0.4: Mixed source quality with notable credibility issues
- 0.2: Poor sources with significant credibility or relevance problems
- 0.0: Unreliable or inappropriate sources that undermine research quality

<research_question>
{inputs}
</research_question>

<research_response>
{outputs}
</research_response>

<sources_used>
{sources}
</sources_used>

<expected_source_types>
{expected_sources}
</expected_source_types>

Provide your evaluation as a score between 0.0 and 1.0, and explain your reasoning.
"""

RESEARCH_COMPLETENESS_PROMPT = """
You are an expert research methodologist evaluating the completeness and depth of web-based research.

Your task is to assess how comprehensively the researcher addressed the research question and covered key aspects.

Consider the following criteria:
- Coverage of all major aspects mentioned in the research question
- Depth of analysis and exploration of key concepts
- Identification and discussion of important subtopics
- Balanced coverage without significant gaps or omissions
- Appropriate level of detail for the complexity of the question

Rate the research completeness on a scale of 0-1:
- 1.0: Comprehensive research that thoroughly addresses all aspects of the question
- 0.8: Good coverage with minor gaps or areas that could be expanded
- 0.6: Adequate research but some important aspects are underexplored
- 0.4: Limited completeness with notable gaps in coverage
- 0.2: Incomplete research that misses several important aspects
- 0.0: Severely incomplete research that fails to address the main question

<research_question>
{inputs}
</research_question>

<research_response>
{outputs}
</research_response>

<key_concepts_to_cover>
{key_concepts}
</key_concepts>
</research_response>

Provide your evaluation as a score between 0.0 and 1.0, and explain your reasoning.
"""

RAG_EFFECTIVENESS_PROMPT = """
You are an expert in Retrieval-Augmented Generation (RAG) systems evaluating the effectiveness of web-based RAG implementation.

Your task is to assess how effectively the researcher retrieved relevant web content and used it to generate accurate responses.

Consider the following criteria:
- Relevance of retrieved web content to the research question
- Accuracy of information extraction from retrieved content
- Effective use of retrieved content to support claims and conclusions
- Proper attribution and citation of retrieved information
- Quality of the generated response based on retrieved content

Rate the RAG effectiveness on a scale of 0-1:
- 1.0: Excellent RAG implementation with highly relevant retrieval and accurate generation
- 0.8: Good RAG performance with mostly relevant retrieval and minor generation issues
- 0.6: Adequate RAG implementation but some retrieval or generation concerns
- 0.4: Limited RAG effectiveness with notable issues in retrieval or generation
- 0.2: Poor RAG performance with significant problems in content use
- 0.0: Failed RAG implementation that doesn't effectively use retrieved content

<research_question>
{inputs}
</research_question>

<generated_response>
{outputs}
</generated_response>

<retrieved_content>
{context}
</retrieved_content>

Provide your evaluation as a score between 0.0 and 1.0, and explain your reasoning.
"""


def create_search_quality_evaluator(model: str = "openai:gpt-4o-mini"):
    """Create an evaluator for web search quality."""
    return create_llm_as_judge(
        prompt=SEARCH_QUALITY_PROMPT,
        model=model,
        choices=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
        feedback_key="search_quality"
    )


def create_crawling_quality_evaluator(model: str = "openai:gpt-4o-mini"):
    """Create an evaluator for web crawling quality."""
    return create_llm_as_judge(
        prompt=CRAWLING_QUALITY_PROMPT,
        model=model,
        choices=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
        feedback_key="crawling_quality"
    )


def create_information_synthesis_evaluator(model: str = "openai:gpt-4o-mini"):
    """Create an evaluator for information synthesis quality."""
    return create_llm_as_judge(
        prompt=INFORMATION_SYNTHESIS_PROMPT,
        model=model,
        choices=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
        feedback_key="information_synthesis"
    )


def create_source_quality_evaluator(model: str = "openai:gpt-4o-mini"):
    """Create an evaluator for source quality assessment."""
    return create_llm_as_judge(
        prompt=SOURCE_QUALITY_PROMPT,
        model=model,
        choices=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
        feedback_key="source_quality"
    )


def create_research_completeness_evaluator(model: str = "openai:gpt-4o-mini"):
    """Create an evaluator for research completeness."""
    return create_llm_as_judge(
        prompt=RESEARCH_COMPLETENESS_PROMPT,
        model=model,
        choices=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
        feedback_key="research_completeness"
    )


def create_rag_effectiveness_evaluator(model: str = "openai:gpt-4o-mini"):
    """Create an evaluator for RAG effectiveness."""
    return create_llm_as_judge(
        prompt=RAG_EFFECTIVENESS_PROMPT,
        model=model,
        choices=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
        feedback_key="rag_effectiveness"
    )


class ResearcherEvaluator:
    """Comprehensive evaluator for the Web Researcher agent."""
    
    def __init__(self, model: str = "openai:gpt-4o-mini"):
        self.model = model
        self.search_quality_evaluator = create_search_quality_evaluator(model)
        self.crawling_quality_evaluator = create_crawling_quality_evaluator(model)
        self.information_synthesis_evaluator = create_information_synthesis_evaluator(model)
        self.source_quality_evaluator = create_source_quality_evaluator(model)
        self.research_completeness_evaluator = create_research_completeness_evaluator(model)
        self.rag_effectiveness_evaluator = create_rag_effectiveness_evaluator(model)
    
    def evaluate_response(
        self,
        prompt: str,
        response: Dict[str, Any],
        test_case_info: Optional[Dict[str, Any]] = None
    ) -> Dict[str, EvaluatorResult]:
        """
        Evaluate a researcher agent response using multiple LLM-as-a-judge evaluators.
        
        Args:
            prompt: The original research question/prompt
            response: The agent's response containing research results
            test_case_info: Additional test case information (expected sources, keywords, etc.)
        
        Returns:
            Dictionary of evaluation results for each metric
        """
        evaluations = {}
        
        # Extract response components
        research_content = response.get("content", "")
        sources_used = response.get("sources", [])
        search_info = response.get("search_info", "")
        crawled_content = response.get("crawled_content", "")
        
        # Prepare test case context
        expected_sources = test_case_info.get("expected_sources", []) if test_case_info else []
        search_keywords = test_case_info.get("search_keywords", []) if test_case_info else []
        key_concepts = test_case_info.get("key_concepts", []) if test_case_info else []
        
        try:
            # Evaluate search quality
            evaluations["search_quality"] = self.search_quality_evaluator(
                inputs=prompt,
                outputs=search_info or research_content,
                search_keywords=", ".join(search_keywords)
            )
        except Exception as e:
            evaluations["search_quality"] = {"error": str(e)}
        
        try:
            # Evaluate crawling quality (if crawled content is available)
            if crawled_content:
                evaluations["crawling_quality"] = self.crawling_quality_evaluator(
                    inputs=prompt,
                    outputs=crawled_content,
                    sources=", ".join(sources_used) if isinstance(sources_used, list) else str(sources_used)
                )
        except Exception as e:
            evaluations["crawling_quality"] = {"error": str(e)}
        
        try:
            # Evaluate information synthesis
            evaluations["information_synthesis"] = self.information_synthesis_evaluator(
                inputs=prompt,
                outputs=research_content,
                sources=", ".join(sources_used) if isinstance(sources_used, list) else str(sources_used)
            )
        except Exception as e:
            evaluations["information_synthesis"] = {"error": str(e)}
        
        try:
            # Evaluate source quality
            evaluations["source_quality"] = self.source_quality_evaluator(
                inputs=prompt,
                outputs=research_content,
                sources=", ".join(sources_used) if isinstance(sources_used, list) else str(sources_used),
                expected_sources=", ".join(expected_sources)
            )
        except Exception as e:
            evaluations["source_quality"] = {"error": str(e)}
        
        try:
            # Evaluate research completeness
            evaluations["research_completeness"] = self.research_completeness_evaluator(
                inputs=prompt,
                outputs=research_content,
                key_concepts=", ".join(key_concepts)
            )
        except Exception as e:
            evaluations["research_completeness"] = {"error": str(e)}
        
        try:
            # Evaluate RAG effectiveness (if applicable)
            if crawled_content:
                evaluations["rag_effectiveness"] = self.rag_effectiveness_evaluator(
                    inputs=prompt,
                    outputs=research_content,
                    context=crawled_content
                )
        except Exception as e:
            evaluations["rag_effectiveness"] = {"error": str(e)}
        
        return evaluations
    
    def calculate_overall_score(self, evaluations: Dict[str, EvaluatorResult]) -> float:
        """Calculate an overall score from individual evaluation results."""
        scores = []
        weights = {
            "search_quality": 0.20,
            "crawling_quality": 0.15,
            "information_synthesis": 0.25,
            "source_quality": 0.20,
            "research_completeness": 0.20,
            "rag_effectiveness": 0.10  # Lower weight as it's not always applicable
        }
        
        total_weight = 0.0
        weighted_sum = 0.0
        
        for metric, result in evaluations.items():
            if isinstance(result, dict) and "error" not in result:
                score = result.get("score", 0.0)
                if isinstance(score, (int, float)):
                    weight = weights.get(metric, 0.1)
                    weighted_sum += score * weight
                    total_weight += weight
        
        # Normalize by actual total weight to handle missing evaluations
        return weighted_sum / total_weight if total_weight > 0 else 0.0
    
    def evaluate_rag_components(
        self,
        prompt: str,
        retrieved_content: str,
        generated_response: str
    ) -> Dict[str, EvaluatorResult]:
        """
        Specifically evaluate RAG components (retrieval and generation).
        
        Args:
            prompt: The original research question
            retrieved_content: Content retrieved from web sources
            generated_response: Final generated response
        
        Returns:
            Dictionary of RAG-specific evaluation results
        """
        evaluations = {}
        
        try:
            # Evaluate RAG effectiveness
            evaluations["rag_effectiveness"] = self.rag_effectiveness_evaluator(
                inputs=prompt,
                outputs=generated_response,
                context=retrieved_content
            )
        except Exception as e:
            evaluations["rag_effectiveness"] = {"error": str(e)}
        
        return evaluations 