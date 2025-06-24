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

# Enhanced RAG evaluation prompts based on OpenEvals best practices

FAITHFULNESS_PROMPT = """
You are an expert evaluator assessing the faithfulness of generated responses to retrieved content.

Your task is to determine whether the generated response is factually grounded in the provided retrieved content, without hallucinations or unsupported claims.

Consider the following criteria:
- All claims in the response are supported by the retrieved content
- No fabricated information that doesn't exist in the sources
- Accurate representation of facts from the retrieved content
- No contradictions with the source material
- Proper context preservation from retrieval to generation

Rate the faithfulness on a scale of 0-1:
- 1.0: All information is fully supported by retrieved content with perfect accuracy
- 0.8: Mostly faithful with minor unsupported details that don't affect core facts
- 0.6: Generally faithful but contains some unsupported claims
- 0.4: Mixed faithfulness with notable unsupported or contradictory information
- 0.2: Mostly unfaithful with significant hallucinations or fabrications
- 0.0: Completely unfaithful response with widespread hallucinations

<research_question>
{inputs}
</research_question>

<generated_response>
{outputs}
</generated_response>

<retrieved_content>
{context}
</retrieved_content>

Provide your evaluation as a score between 0.0 and 1.0, and explain your reasoning focusing on specific examples of supported vs unsupported claims.
"""

CONTEXT_PRECISION_PROMPT = """
You are an expert evaluator assessing the precision of retrieved content for a research question.

Your task is to determine what fraction of the retrieved content is actually relevant and useful for answering the research question.

Consider the following criteria:
- Relevance of each piece of retrieved content to the research question
- Signal-to-noise ratio in the retrieved information
- Presence of irrelevant or distracting information
- Quality of content filtering and selection
- Efficiency of the retrieval process

Rate the context precision on a scale of 0-1:
- 1.0: All retrieved content is highly relevant and directly useful
- 0.8: Most content is relevant with minimal irrelevant information
- 0.6: Good relevance but some irrelevant content included
- 0.4: Mixed relevance with notable irrelevant content
- 0.2: Poor precision with mostly irrelevant content
- 0.0: Retrieved content is largely irrelevant to the question

<research_question>
{inputs}
</research_question>

<retrieved_content>
{context}
</retrieved_content>

<expected_topics>
{key_concepts}
</expected_topics>

Provide your evaluation as a score between 0.0 and 1.0, and explain your reasoning with specific examples of relevant vs irrelevant content.
"""

CONTEXT_RECALL_PROMPT = """
You are an expert evaluator assessing the recall of retrieved content for a research question.

Your task is to determine whether the retrieval system successfully found all the important and relevant information needed to comprehensively answer the research question.

Consider the following criteria:
- Coverage of all major aspects of the research question
- Inclusion of key facts, figures, and important details
- Representation of different perspectives or viewpoints where applicable
- Completeness of retrieved information relative to what should be available
- Absence of critical information gaps

Rate the context recall on a scale of 0-1:
- 1.0: All important and relevant information has been successfully retrieved
- 0.8: Most critical information retrieved with minor gaps
- 0.6: Good coverage but some important information missing
- 0.4: Adequate retrieval but notable information gaps
- 0.2: Poor recall with significant missing information
- 0.0: Failed to retrieve most of the important relevant information

<research_question>
{inputs}
</research_question>

<retrieved_content>
{context}
</retrieved_content>

<expected_key_concepts>
{key_concepts}
</expected_key_concepts>

<expected_information_types>
{expected_sources}
</expected_information_types>

Provide your evaluation as a score between 0.0 and 1.0, and explain your reasoning focusing on what important information is present vs missing.
"""

# Enhanced RAG Effectiveness prompt with better criteria
ENHANCED_RAG_EFFECTIVENESS_PROMPT = """
You are an expert in Retrieval-Augmented Generation (RAG) systems evaluating the end-to-end effectiveness of web-based RAG implementation.

Your task is to assess how effectively the system retrieved relevant web content and used it to generate accurate, comprehensive responses.

Consider the following criteria:
- **Retrieval Quality**: Relevance and completeness of retrieved web content
- **Faithfulness**: Accuracy of information extraction and use from retrieved content  
- **Attribution**: Proper citation and reference to source materials
- **Synthesis**: Effective integration of multiple retrieved sources
- **Completeness**: Coverage of the research question using retrieved content
- **Coherence**: Logical flow and organization of the generated response

Rate the overall RAG effectiveness on a scale of 0-1:
- 1.0: Excellent RAG implementation - perfect retrieval, faithful generation, complete coverage
- 0.8: Good RAG performance - effective retrieval and generation with minor issues
- 0.6: Adequate RAG implementation - reasonable performance but some weaknesses
- 0.4: Limited RAG effectiveness - notable issues in retrieval or generation quality
- 0.2: Poor RAG performance - significant problems in multiple aspects
- 0.0: Failed RAG implementation - system doesn't effectively use retrieved content

<research_question>
{inputs}
</research_question>

<generated_response>
{outputs}
</generated_response>

<retrieved_content>
{context}
</retrieved_content>

<sources_used>
{sources}
</sources_used>

Provide your evaluation as a score between 0.0 and 1.0, and explain your reasoning covering each of the six criteria above.
"""

# Advanced Enhancement Evaluators

TEMPORAL_ACCURACY_PROMPT = """
You are an expert evaluator assessing the temporal accuracy and currency of information in research responses.

Your task is to determine whether the information provided is current, up-to-date, and appropriate for time-sensitive queries.

Consider the following criteria:
- Currency of information relative to the research question's time requirements
- Use of recent data, statistics, and developments when relevant
- Appropriate handling of time-sensitive topics (current events, recent research, market trends)
- Clear indication of information recency and temporal context
- Avoidance of outdated information that could mislead

Rate the temporal accuracy on a scale of 0-1:
- 1.0: Information is perfectly current and appropriate for the time context
- 0.8: Mostly current information with minor temporal gaps
- 0.6: Generally current but some outdated elements present
- 0.4: Mixed currency with notable outdated information
- 0.2: Mostly outdated information that affects response quality
- 0.0: Severely outdated information that undermines response accuracy

<research_question>
{inputs}
</research_question>

<generated_response>
{outputs}
</generated_response>

<requires_recent_info>
{requires_recent_info}
</requires_recent_info>

<source_dates>
{source_dates}
</source_dates>

Provide your evaluation as a score between 0.0 and 1.0, and explain your reasoning focusing on the currency and temporal appropriateness of the information.
"""

BIAS_ASSESSMENT_PROMPT = """
You are an expert evaluator assessing information bias and perspective balance in research responses.

Your task is to determine whether the response presents balanced perspectives and avoids problematic bias.

Consider the following criteria:
- Balanced representation of different viewpoints and perspectives
- Absence of political, cultural, or ideological bias
- Fair treatment of controversial or disputed topics
- Acknowledgment of limitations and uncertainties
- Avoidance of leading language or one-sided presentations

Rate the bias assessment on a scale of 0-1:
- 1.0: Perfectly balanced and unbiased presentation of information
- 0.8: Mostly balanced with minor perspective gaps
- 0.6: Generally balanced but some bias indicators present
- 0.4: Notable bias affecting information presentation
- 0.2: Significant bias that distorts information quality
- 0.0: Severe bias that undermines response credibility

<research_question>
{inputs}
</research_question>

<generated_response>
{outputs}
</generated_response>

<source_diversity>
{source_diversity}
</source_diversity>

<topic_sensitivity>
{topic_sensitivity}
</topic_sensitivity>

Provide your evaluation as a score between 0.0 and 1.0, and explain your reasoning focusing on bias indicators and perspective balance.
"""

FACTUAL_VERIFICATION_PROMPT = """
You are an expert fact-checker evaluating the factual accuracy and verifiability of claims in research responses.

Your task is to assess whether factual claims can be verified and cross-referenced against authoritative sources.

Consider the following criteria:
- Accuracy of specific facts, figures, and statistical claims
- Verifiability of claims against authoritative sources
- Consistency of information across multiple sources
- Proper qualification of uncertain or disputed information
- Absence of factual errors or misrepresentations

Rate the factual verification on a scale of 0-1:
- 1.0: All factual claims are accurate and fully verifiable
- 0.8: Mostly accurate facts with minor verification gaps
- 0.6: Generally accurate but some unverifiable claims
- 0.4: Mixed accuracy with notable factual concerns
- 0.2: Significant factual errors affecting response quality
- 0.0: Widespread factual inaccuracies that undermine credibility

<research_question>
{inputs}
</research_question>

<generated_response>
{outputs}
</generated_response>

<authoritative_sources>
{authoritative_sources}
</authoritative_sources>

<fact_check_context>
{fact_check_context}
</fact_check_context>

Provide your evaluation as a score between 0.0 and 1.0, and explain your reasoning focusing on factual accuracy and verifiability of specific claims.
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


def create_faithfulness_evaluator(model: str = "openai:gpt-4o-mini"):
    """Create an evaluator for response faithfulness to retrieved content."""
    return create_llm_as_judge(
        prompt=FAITHFULNESS_PROMPT,
        model=model,
        choices=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
        feedback_key="faithfulness"
    )


def create_context_precision_evaluator(model: str = "openai:gpt-4o-mini"):
    """Create an evaluator for context precision (relevance of retrieved content)."""
    return create_llm_as_judge(
        prompt=CONTEXT_PRECISION_PROMPT,
        model=model,
        choices=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
        feedback_key="context_precision"
    )


def create_context_recall_evaluator(model: str = "openai:gpt-4o-mini"):
    """Create an evaluator for context recall (completeness of retrieved content)."""
    return create_llm_as_judge(
        prompt=CONTEXT_RECALL_PROMPT,
        model=model,
        choices=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
        feedback_key="context_recall"
    )


def create_temporal_accuracy_evaluator(model: str = "openai:gpt-4o-mini"):
    """Create an evaluator for temporal accuracy and information currency."""
    return create_llm_as_judge(
        prompt=TEMPORAL_ACCURACY_PROMPT,
        model=model,
        choices=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
        feedback_key="temporal_accuracy"
    )


def create_bias_assessment_evaluator(model: str = "openai:gpt-4o-mini"):
    """Create an evaluator for bias detection and perspective balance."""
    return create_llm_as_judge(
        prompt=BIAS_ASSESSMENT_PROMPT,
        model=model,
        choices=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
        feedback_key="bias_assessment"
    )


def create_factual_verification_evaluator(model: str = "openai:gpt-4o-mini"):
    """Create an evaluator for factual accuracy and verifiability."""
    return create_llm_as_judge(
        prompt=FACTUAL_VERIFICATION_PROMPT,
        model=model,
        choices=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
        feedback_key="factual_verification"
    )


class ResearcherEvaluator:
    """Comprehensive evaluator for the Web Researcher agent with enhanced RAG evaluation."""
    
    def __init__(self, model: str = "openai:gpt-4o-mini"):
        self.model = model
        self.search_quality_evaluator = create_search_quality_evaluator(model)
        self.crawling_quality_evaluator = create_crawling_quality_evaluator(model)
        self.information_synthesis_evaluator = create_information_synthesis_evaluator(model)
        self.source_quality_evaluator = create_source_quality_evaluator(model)
        self.research_completeness_evaluator = create_research_completeness_evaluator(model)
        
        # Enhanced RAG evaluators
        self.faithfulness_evaluator = create_faithfulness_evaluator(model)
        self.context_precision_evaluator = create_context_precision_evaluator(model)
        self.context_recall_evaluator = create_context_recall_evaluator(model)
        
        # Advanced enhancement evaluators
        self.temporal_accuracy_evaluator = create_temporal_accuracy_evaluator(model)
        self.bias_assessment_evaluator = create_bias_assessment_evaluator(model)
        self.factual_verification_evaluator = create_factual_verification_evaluator(model)
        
        # Update RAG effectiveness evaluator with enhanced prompt
        self.rag_effectiveness_evaluator = create_llm_as_judge(
            prompt=ENHANCED_RAG_EFFECTIVENESS_PROMPT,
            model=model,
            choices=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
            feedback_key="rag_effectiveness"
        )
    
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
        requires_recent_info = test_case_info.get("requires_recent_info", False) if test_case_info else False
        
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
        
        # Enhanced RAG evaluations
        if crawled_content:
            try:
                # Faithfulness evaluation
                evaluations["faithfulness"] = self.faithfulness_evaluator(
                    inputs=prompt,
                    outputs=research_content,
                    context=crawled_content
                )
            except Exception as e:
                evaluations["faithfulness"] = {"error": str(e)}
            
            try:
                # Context precision evaluation
                evaluations["context_precision"] = self.context_precision_evaluator(
                    inputs=prompt,
                    context=crawled_content,
                    key_concepts=", ".join(key_concepts)
                )
            except Exception as e:
                evaluations["context_precision"] = {"error": str(e)}
            
            try:
                # Context recall evaluation
                evaluations["context_recall"] = self.context_recall_evaluator(
                    inputs=prompt,
                    context=crawled_content,
                    key_concepts=", ".join(key_concepts),
                    expected_sources=", ".join(expected_sources)
                )
            except Exception as e:
                evaluations["context_recall"] = {"error": str(e)}
            
            try:
                # Enhanced RAG effectiveness evaluation
                evaluations["rag_effectiveness"] = self.rag_effectiveness_evaluator(
                    inputs=prompt,
                    outputs=research_content,
                    context=crawled_content,
                    sources=", ".join(sources_used) if isinstance(sources_used, list) else str(sources_used)
                )
            except Exception as e:
                evaluations["rag_effectiveness"] = {"error": str(e)}
        
        # Advanced enhancement evaluations
        try:
            # Temporal accuracy evaluation
            source_dates = "Recent sources" if requires_recent_info else "Standard sources"
            evaluations["temporal_accuracy"] = self.temporal_accuracy_evaluator(
                inputs=prompt,
                outputs=research_content,
                requires_recent_info=str(requires_recent_info),
                source_dates=source_dates
            )
        except Exception as e:
            evaluations["temporal_accuracy"] = {"error": str(e)}
        
        try:
            # Bias assessment evaluation
            source_diversity = f"Sources from {len(set(sources_used))} different domains" if sources_used else "Limited source diversity"
            topic_sensitivity = "Standard research topic"  # Could be enhanced with topic classification
            evaluations["bias_assessment"] = self.bias_assessment_evaluator(
                inputs=prompt,
                outputs=research_content,
                source_diversity=source_diversity,
                topic_sensitivity=topic_sensitivity
            )
        except Exception as e:
            evaluations["bias_assessment"] = {"error": str(e)}
        
        try:
            # Factual verification evaluation
            authoritative_sources = ", ".join(expected_sources) if expected_sources else "General web sources"
            fact_check_context = f"Research on {', '.join(key_concepts)}" if key_concepts else "General research context"
            evaluations["factual_verification"] = self.factual_verification_evaluator(
                inputs=prompt,
                outputs=research_content,
                authoritative_sources=authoritative_sources,
                fact_check_context=fact_check_context
            )
        except Exception as e:
            evaluations["factual_verification"] = {"error": str(e)}
        
        return evaluations
    
    def calculate_overall_score(self, evaluations: Dict[str, EvaluatorResult]) -> float:
        """Calculate an overall score from individual evaluation results with enhanced weighting."""
        weights = {
            # Core web research capabilities
            "search_quality": 0.10,
            "crawling_quality": 0.08,
            "information_synthesis": 0.12,
            "source_quality": 0.10,
            "research_completeness": 0.12,
            
            # Enhanced RAG-specific metrics
            "faithfulness": 0.15,  # Critical for factual accuracy
            "context_precision": 0.05,  # Quality of retrieval
            "context_recall": 0.05,    # Completeness of retrieval
            "rag_effectiveness": 0.05,   # Overall RAG performance
            
            # Advanced enhancement metrics
            "temporal_accuracy": 0.08,    # Information currency
            "bias_assessment": 0.05,      # Perspective balance
            "factual_verification": 0.05  # Fact checking
        }
        
        total_weight = 0.0
        weighted_sum = 0.0
        
        for metric, result in evaluations.items():
            if isinstance(result, dict) and "error" not in result:
                score = result.get("score", 0.0)
                if isinstance(score, (int, float)):
                    weight = weights.get(metric, 0.01)  # Small default weight for unexpected metrics
                    weighted_sum += score * weight
                    total_weight += weight
        
        # Normalize by actual total weight to handle missing evaluations
        return weighted_sum / total_weight if total_weight > 0 else 0.0 