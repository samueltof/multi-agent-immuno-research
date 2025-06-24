"""
Test dataset for evaluating the Web Researcher agent.

This module contains carefully curated research questions covering various domains
including technology, science, business, current events, and general knowledge to
comprehensively test the agent's web research capabilities, search strategies,
and information synthesis skills.
"""

from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class ResearcherTestCase:
    """Represents a single test case for web researcher evaluation."""
    id: str
    prompt: str
    domain: str
    difficulty: str  # "basic", "intermediate", "expert"
    expected_sources: List[str]  # Types of sources we expect (e.g., "news", "academic", "gov")
    key_concepts: List[str]  # Key concepts that should be addressed
    search_keywords: List[str]  # Expected search terms/keywords
    reference_info: str = ""  # Optional reference information for comparison
    requires_recent_info: bool = False  # Whether the query requires current/recent information


# Comprehensive web research test dataset - Optimized for Scientific Rigor (30 cases)
RESEARCHER_TEST_CASES = [
    # === TECHNOLOGY DOMAIN (8 cases) ===
    ResearcherTestCase(
        id="tech_001",
        prompt="What are the latest developments in large language models in 2024? Include key breakthroughs, new architectures, and performance improvements.",
        domain="technology",
        difficulty="intermediate",
        expected_sources=["news", "academic", "tech_blogs"],
        key_concepts=["large language models", "LLM", "AI breakthroughs", "model architectures", "performance"],
        search_keywords=["LLM 2024", "large language models", "AI breakthroughs", "transformer architecture"],
        requires_recent_info=True,
        reference_info="Should cover major LLM releases, architectural innovations, and performance benchmarks from 2024"
    ),
    
    ResearcherTestCase(
        id="tech_002",
        prompt="How does quantum computing work, and what are its potential applications in cryptography and drug discovery?",
        domain="technology",
        difficulty="expert",
        expected_sources=["academic", "research_institutions", "tech_companies"],
        key_concepts=["quantum computing", "qubits", "quantum supremacy", "cryptography", "drug discovery"],
        search_keywords=["quantum computing", "quantum cryptography", "quantum drug discovery", "qubits"],
        reference_info="Should explain quantum principles, current limitations, and specific applications in mentioned fields"
    ),
    
    ResearcherTestCase(
        id="tech_003",
        prompt="What is the current state of autonomous vehicle technology? Compare different approaches by major companies.",
        domain="technology",
        difficulty="intermediate",
        expected_sources=["news", "automotive_industry", "tech_companies"],
        key_concepts=["autonomous vehicles", "self-driving cars", "LIDAR", "computer vision", "Tesla", "Waymo"],
        search_keywords=["autonomous vehicles 2024", "self-driving cars", "Tesla FSD", "Waymo", "AV technology"],
        requires_recent_info=True,
        reference_info="Should compare approaches by Tesla, Waymo, Cruise, and other major players"
    ),
    
    ResearcherTestCase(
        id="basic_002",
        prompt="How do electric vehicles work? Explain the technology and compare with traditional cars.",
        domain="technology",
        difficulty="basic",
        expected_sources=["automotive_sources", "educational_content", "manufacturer_information"],
        key_concepts=["electric vehicles", "EV technology", "batteries", "electric motors", "charging"],
        search_keywords=["how electric cars work", "EV technology", "electric vehicle batteries"],
        reference_info="Should explain basic EV technology and advantages/disadvantages vs conventional cars"
    ),
    
    ResearcherTestCase(
        id="cross_domain_001",
        prompt="How do advances in artificial intelligence impact both healthcare delivery and medical research? Analyze applications, benefits, and ethical concerns.",
        domain="technology",
        difficulty="expert",
        expected_sources=["medical_journals", "tech_research", "healthcare_organizations", "ethics_committees"],
        key_concepts=["AI in healthcare", "medical AI", "diagnostic AI", "drug discovery", "healthcare ethics"],
        search_keywords=["AI healthcare applications", "medical AI ethics", "AI diagnosis", "AI drug discovery"],
        reference_info="Should bridge technology and healthcare domains with specific applications and ethical considerations"
    ),
    
    ResearcherTestCase(
        id="international_002",
        prompt="How do different countries approach data privacy regulation? Compare GDPR, CCPA, and other major frameworks.",
        domain="technology",
        difficulty="intermediate",
        expected_sources=["legal_documents", "privacy_organizations", "regulatory_analysis", "compliance_studies"],
        key_concepts=["data privacy", "GDPR", "CCPA", "privacy regulation", "international law"],
        search_keywords=["data privacy laws", "GDPR vs CCPA", "international privacy regulation", "data protection comparison"],
        reference_info="Should compare regulatory approaches with specific provisions and enforcement mechanisms"
    ),
    
    ResearcherTestCase(
        id="specialized_002",
        prompt="What are the latest developments in quantum computing hardware? Compare different technological approaches and their commercial viability.",
        domain="technology",
        difficulty="expert",
        expected_sources=["tech_research", "quantum_companies", "scientific_journals", "industry_analysis"],
        key_concepts=["quantum computing", "quantum hardware", "superconducting qubits", "trapped ions", "quantum advantage"],
        search_keywords=["quantum computing hardware", "quantum computer types", "quantum technology comparison", "quantum computing progress"],
        requires_recent_info=True,
        reference_info="Should analyze different hardware approaches with technical and commercial assessment"
    ),
    
    ResearcherTestCase(
        id="global_001",
        prompt="How do cultural differences affect the adoption and implementation of digital payment systems worldwide? Compare approaches in Asia, Europe, and Africa.",
        domain="technology",
        difficulty="intermediate",
        expected_sources=["fintech_research", "cultural_studies", "economic_analysis", "regional_studies"],
        key_concepts=["digital payments", "cultural adoption", "fintech", "mobile money", "financial inclusion"],
        search_keywords=["digital payments cultural differences", "mobile money adoption", "fintech global comparison", "payment systems culture"],
        reference_info="Should analyze how cultural, economic, and regulatory factors influence technology adoption across regions"
    ),
    
    # === SCIENCE DOMAIN (7 cases) ===
    ResearcherTestCase(
        id="science_001",
        prompt="What are the latest findings about CRISPR gene editing safety and its therapeutic applications?",
        domain="science",
        difficulty="expert",
        expected_sources=["academic", "medical_journals", "research_institutions"],
        key_concepts=["CRISPR", "gene editing", "safety", "therapeutic applications", "clinical trials"],
        search_keywords=["CRISPR safety", "gene editing therapeutics", "CRISPR clinical trials", "gene therapy"],
        reference_info="Should cover recent safety studies, approved therapies, and ongoing clinical applications"
    ),
    
    ResearcherTestCase(
        id="science_002",
        prompt="How does climate change affect ocean currents, and what are the implications for global weather patterns?",
        domain="science",
        difficulty="intermediate",
        expected_sources=["academic", "climate_research", "government_agencies"],
        key_concepts=["climate change", "ocean currents", "thermohaline circulation", "weather patterns", "AMOC"],
        search_keywords=["climate change ocean currents", "AMOC", "thermohaline circulation", "global weather"],
        reference_info="Should explain ocean circulation mechanisms and their connection to climate systems"
    ),
    
    ResearcherTestCase(
        id="science_003",
        prompt="What is the current understanding of dark matter and dark energy? What are the leading theories and experimental approaches?",
        domain="science",
        difficulty="expert",
        expected_sources=["academic", "physics_journals", "space_agencies"],
        key_concepts=["dark matter", "dark energy", "cosmology", "particle physics", "WIMP", "axions"],
        search_keywords=["dark matter theories", "dark energy", "cosmology", "particle physics experiments"],
        reference_info="Should cover current theories, experimental searches, and recent findings in cosmology"
    ),
    
    ResearcherTestCase(
        id="adversarial_001",
        prompt="What is the scientific consensus on climate change? Address common skeptical arguments and evaluate the strength of evidence.",
        domain="science",
        difficulty="expert",
        expected_sources=["peer_reviewed_journals", "scientific_organizations", "climate_data"],
        key_concepts=["climate change", "scientific consensus", "global warming", "skeptical arguments", "evidence evaluation"],
        search_keywords=["climate change consensus", "global warming evidence", "climate skepticism", "IPCC reports"],
        reference_info="Should present scientific consensus while addressing counterarguments objectively"
    ),
    
    ResearcherTestCase(
        id="methodology_002",
        prompt="How do different research methodologies in psychology (experimental vs. observational vs. meta-analysis) contribute to our understanding of cognitive bias?",
        domain="science",
        difficulty="expert",
        expected_sources=["psychology_journals", "methodology_studies", "cognitive_research", "meta_analyses"],
        key_concepts=["research methodology", "cognitive bias", "experimental design", "observational studies", "meta-analysis"],
        search_keywords=["psychology research methods", "cognitive bias research", "experimental vs observational", "meta-analysis psychology"],
        reference_info="Should compare methodological approaches with specific examples and their contributions to understanding bias"
    ),
    
    ResearcherTestCase(
        id="emerging_001",
        prompt="What are the potential applications and risks of brain-computer interfaces? Analyze current research and ethical implications.",
        domain="science",
        difficulty="expert",
        expected_sources=["neuroscience_research", "tech_companies", "ethics_organizations", "medical_journals"],
        key_concepts=["brain-computer interfaces", "BCI", "neurotechnology", "neural implants", "neuroethics"],
        search_keywords=["brain computer interfaces", "BCI research", "neural implants", "neuroethics", "brain technology"],
        reference_info="Should cover current capabilities, future applications, and comprehensive ethical analysis"
    ),
    
    ResearcherTestCase(
        id="basic_004",
        prompt="How does photosynthesis work and why is it important for life on Earth?",
        domain="science",
        difficulty="basic",
        expected_sources=["educational_content", "science_textbooks", "environmental_education", "biology_resources"],
        key_concepts=["photosynthesis", "plants", "oxygen", "carbon dioxide", "ecosystem"],
        search_keywords=["how photosynthesis works", "photosynthesis importance", "plants oxygen production", "photosynthesis process"],
        reference_info="Should explain the process clearly with environmental significance for general audience"
    ),
    
    # === HEALTH DOMAIN (6 cases) ===
    ResearcherTestCase(
        id="health_001",
        prompt="What are the long-term effects of COVID-19 (Long COVID)? What treatments are being developed?",
        domain="health",
        difficulty="intermediate",
        expected_sources=["medical_journals", "health_organizations", "clinical_studies"],
        key_concepts=["Long COVID", "post-acute sequelae", "symptoms", "treatments", "rehabilitation"],
        search_keywords=["Long COVID", "post-acute COVID", "COVID long-term effects", "Long COVID treatment"],
        reference_info="Should cover symptom patterns, prevalence, and current treatment approaches"
    ),
    
    ResearcherTestCase(
        id="health_002",
        prompt="How effective are weight loss medications like Ozempic and Wegovy? What are the benefits and risks?",
        domain="health",
        difficulty="intermediate",
        expected_sources=["medical_journals", "clinical_trials", "health_authorities"],
        key_concepts=["GLP-1 agonists", "Ozempic", "Wegovy", "weight loss", "diabetes", "side effects"],
        search_keywords=["Ozempic weight loss", "GLP-1 agonists", "Wegovy effectiveness", "semaglutide"],
        reference_info="Should cover clinical trial data, effectiveness rates, and safety profiles"
    ),
    
    ResearcherTestCase(
        id="health_003",
        prompt="What is the current state of Alzheimer's disease research? What are the most promising treatment approaches?",
        domain="health",
        difficulty="expert",
        expected_sources=["medical_journals", "research_institutions", "pharmaceutical_companies"],
        key_concepts=["Alzheimer's disease", "amyloid hypothesis", "tau protein", "neurodegeneration", "drug development"],
        search_keywords=["Alzheimer's research 2024", "amyloid drugs", "tau therapeutics", "neurodegeneration"],
        reference_info="Should cover recent drug approvals, ongoing trials, and emerging therapeutic targets"
    ),
    
    ResearcherTestCase(
        id="basic_001",
        prompt="What are the health benefits of the Mediterranean diet? Include scientific evidence and practical recommendations.",
        domain="health",
        difficulty="basic",
        expected_sources=["health_organizations", "nutrition_research", "medical_sources"],
        key_concepts=["Mediterranean diet", "health benefits", "nutrition", "heart health", "longevity"],
        search_keywords=["Mediterranean diet benefits", "Mediterranean diet research", "healthy eating"],
        reference_info="Should cover proven health benefits and dietary recommendations"
    ),
    
    ResearcherTestCase(
        id="systematic_001",
        prompt="Conduct a systematic analysis of COVID-19 vaccine effectiveness across different age groups and variants. Compare data from multiple countries.",
        domain="health",
        difficulty="expert",
        expected_sources=["medical_journals", "health_authorities", "clinical_data", "epidemiological_studies"],
        key_concepts=["COVID-19 vaccines", "vaccine effectiveness", "age groups", "variants", "comparative analysis"],
        search_keywords=["COVID vaccine effectiveness", "vaccine efficacy age groups", "COVID variants vaccines", "vaccine real world data"],
        reference_info="Should synthesize data from multiple studies and countries to provide comprehensive effectiveness analysis"
    ),
    
    ResearcherTestCase(
        id="credibility_001",
        prompt="What is the scientific evidence regarding the safety and efficacy of mRNA COVID-19 vaccines? Address common misconceptions and misinformation.",
        domain="health",
        difficulty="expert",
        expected_sources=["peer_reviewed_journals", "health_authorities", "clinical_trials", "medical_organizations"],
        key_concepts=["mRNA vaccines", "vaccine safety", "vaccine efficacy", "misinformation", "scientific evidence"],
        search_keywords=["mRNA vaccine safety", "COVID vaccine efficacy", "vaccine misinformation", "clinical trial data"],
        reference_info="Should distinguish between credible scientific evidence and misinformation while addressing common concerns"
    ),
    
    # === BUSINESS DOMAIN (4 cases) ===
    ResearcherTestCase(
        id="business_001",
        prompt="What are the current trends in cryptocurrency regulation globally? Compare approaches by different countries.",
        domain="business",
        difficulty="intermediate",
        expected_sources=["news", "financial_publications", "government_sources"],
        key_concepts=["cryptocurrency regulation", "Bitcoin", "digital assets", "regulatory frameworks", "compliance"],
        search_keywords=["crypto regulation 2024", "cryptocurrency laws", "Bitcoin regulation", "digital asset policy"],
        requires_recent_info=True,
        reference_info="Should compare regulatory approaches across major economies"
    ),
    
    ResearcherTestCase(
        id="business_003",
        prompt="What are the key factors driving inflation in 2024? Analyze supply chain, monetary policy, and geopolitical influences.",
        domain="business",
        difficulty="expert",
        expected_sources=["economic_data", "central_banks", "financial_news"],
        key_concepts=["inflation", "monetary policy", "supply chain", "geopolitical factors", "interest rates"],
        search_keywords=["inflation 2024", "monetary policy", "supply chain inflation", "Fed policy"],
        requires_recent_info=True,
        reference_info="Should analyze multiple inflation drivers and their relative contributions"
    ),
    
    ResearcherTestCase(
        id="basic_003",
        prompt="What are the main causes of inflation and how does it affect everyday consumers?",
        domain="business",
        difficulty="basic",
        expected_sources=["economic_education", "financial_news", "consumer_guides", "government_sources"],
        key_concepts=["inflation", "consumer prices", "economic basics", "cost of living", "purchasing power"],
        search_keywords=["what causes inflation", "inflation effects consumers", "inflation basics", "cost of living"],
        reference_info="Should explain inflation concepts clearly with practical examples for general audience"
    ),
    
    ResearcherTestCase(
        id="systematic_002",
        prompt="Compare the economic recovery strategies adopted by different countries during the COVID-19 pandemic. Analyze their effectiveness and trade-offs.",
        domain="business",
        difficulty="expert",
        expected_sources=["economic_data", "government_policies", "international_organizations", "economic_analysis"],
        key_concepts=["economic recovery", "COVID-19 pandemic", "fiscal policy", "monetary policy", "comparative analysis"],
        search_keywords=["COVID economic recovery", "pandemic fiscal policy", "economic stimulus comparison", "post-COVID recovery"],
        reference_info="Should compare multiple countries' approaches with quantitative outcomes and policy trade-offs"
    ),
    
    # === ENVIRONMENT DOMAIN (3 cases) ===
    ResearcherTestCase(
        id="environment_001",
        prompt="What are the most effective renewable energy technologies for reducing carbon emissions? Compare solar, wind, and emerging technologies.",
        domain="environment",
        difficulty="intermediate",
        expected_sources=["energy_agencies", "research_institutions", "environmental_organizations"],
        key_concepts=["renewable energy", "solar power", "wind energy", "carbon emissions", "energy efficiency"],
        search_keywords=["renewable energy efficiency", "solar vs wind", "carbon reduction", "clean energy"],
        reference_info="Should compare efficiency, cost, and scalability of different renewable technologies"
    ),
    
    ResearcherTestCase(
        id="adversarial_002",
        prompt="Analyze the debate around nuclear energy as a climate solution. Present arguments from both proponents and critics.",
        domain="environment",
        difficulty="expert",
        expected_sources=["energy_policy", "environmental_groups", "nuclear_industry", "scientific_studies"],
        key_concepts=["nuclear energy", "climate change", "renewable energy", "nuclear safety", "waste disposal"],
        search_keywords=["nuclear energy climate", "nuclear power pros cons", "nuclear vs renewable", "nuclear safety"],
        reference_info="Should present balanced view of nuclear energy debate with evidence from multiple perspectives"
    ),
    
    ResearcherTestCase(
        id="basic_006",
        prompt="What are renewable energy sources and how do they help the environment?",
        domain="environment",
        difficulty="basic",
        expected_sources=["environmental_education", "energy_agencies", "educational_content", "green_organizations"],
        key_concepts=["renewable energy", "solar power", "wind energy", "environmental benefits", "clean energy"],
        search_keywords=["renewable energy types", "clean energy benefits", "solar wind energy", "renewable vs fossil fuels"],
        reference_info="Should explain renewable energy concepts and environmental benefits for general audience"
    ),
    
    # === CURRENT EVENTS DOMAIN (2 cases) ===
    ResearcherTestCase(
        id="current_002",
        prompt="What is the current status of the conflict in Ukraine? Analyze recent developments and international responses.",
        domain="current_events",
        difficulty="intermediate",
        expected_sources=["news", "international_organizations", "government_sources"],
        key_concepts=["Ukraine conflict", "Russia", "international aid", "sanctions", "military support"],
        search_keywords=["Ukraine war 2024", "Russia Ukraine conflict", "international aid Ukraine", "sanctions Russia"],
        requires_recent_info=True,
        reference_info="Should cover recent military developments, diplomatic efforts, and international support"
    ),
    
    ResearcherTestCase(
        id="methodology_001",
        prompt="Evaluate the reliability of different polling methodologies in predicting election outcomes. Compare traditional vs. modern polling techniques.",
        domain="current_events",
        difficulty="expert",
        expected_sources=["polling_organizations", "methodology_studies", "election_analysis", "statistical_research"],
        key_concepts=["polling methodology", "election prediction", "survey research", "statistical accuracy", "polling bias"],
        search_keywords=["polling methodology accuracy", "election polling errors", "survey methodology", "polling bias"],
        reference_info="Should analyze methodological strengths and weaknesses with specific examples and accuracy metrics"
    ),
]


def get_test_cases_by_domain(domain: str) -> List[ResearcherTestCase]:
    """Get all test cases for a specific domain."""
    return [case for case in RESEARCHER_TEST_CASES if case.domain == domain]


def get_test_cases_by_difficulty(difficulty: str) -> List[ResearcherTestCase]:
    """Get all test cases for a specific difficulty level."""
    return [case for case in RESEARCHER_TEST_CASES if case.difficulty == difficulty]


def get_test_case_by_id(test_id: str) -> ResearcherTestCase:
    """Get a specific test case by ID."""
    for case in RESEARCHER_TEST_CASES:
        if case.id == test_id:
            return case
    raise ValueError(f"Test case with ID '{test_id}' not found")


def get_all_domains() -> List[str]:
    """Get all unique domains in the test dataset."""
    return list(set(case.domain for case in RESEARCHER_TEST_CASES))


def get_test_dataset_summary() -> Dict[str, Any]:
    """Get a summary of the optimized test dataset (30 cases focused on core scientific domains)."""
    domains = {}
    difficulties = {}
    
    for case in RESEARCHER_TEST_CASES:
        domains[case.domain] = domains.get(case.domain, 0) + 1
        difficulties[case.difficulty] = difficulties.get(case.difficulty, 0) + 1
    
    return {
        "total_test_cases": len(RESEARCHER_TEST_CASES),
        "domains": domains,
        "difficulties": difficulties,
        "recent_info_required": sum(1 for case in RESEARCHER_TEST_CASES if case.requires_recent_info),
        "domain_list": sorted(domains.keys()),
        "difficulty_levels": sorted(difficulties.keys()),
    } 