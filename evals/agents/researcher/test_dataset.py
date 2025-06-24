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


# Comprehensive web research test dataset
RESEARCHER_TEST_CASES = [
    # Technology & AI Research
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
    
    # Science & Research
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
    
    # Business & Economics
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
        id="business_002",
        prompt="How has remote work affected commercial real estate markets? Analyze trends and future predictions.",
        domain="business",
        difficulty="intermediate",
        expected_sources=["business_publications", "real_estate_data", "research_firms"],
        key_concepts=["remote work", "commercial real estate", "office space", "market trends", "work from home"],
        search_keywords=["remote work commercial real estate", "office space demand", "WFH impact", "CRE trends"],
        reference_info="Should analyze market data, occupancy rates, and future office space demand"
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
    
    # Health & Medicine
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
    
    # Current Events & Politics
    ResearcherTestCase(
        id="current_001",
        prompt="What are the key issues in the 2024 U.S. presidential election? Analyze policy positions and polling trends.",
        domain="current_events",
        difficulty="intermediate",
        expected_sources=["news", "polling_organizations", "political_analysis"],
        key_concepts=["2024 election", "presidential candidates", "policy positions", "polling", "swing states"],
        search_keywords=["2024 presidential election", "election polls", "candidate positions", "swing states"],
        requires_recent_info=True,
        reference_info="Should cover major candidates, key policy differences, and electoral dynamics"
    ),
    
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
    
    # Environmental & Sustainability
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
        id="environment_002",
        prompt="How is plastic pollution affecting marine ecosystems? What solutions are being implemented globally?",
        domain="environment",
        difficulty="intermediate",
        expected_sources=["environmental_research", "marine_biology", "conservation_organizations"],
        key_concepts=["plastic pollution", "marine ecosystems", "microplastics", "ocean conservation", "waste management"],
        search_keywords=["plastic pollution ocean", "microplastics marine life", "plastic waste solutions", "ocean cleanup"],
        reference_info="Should cover impact mechanisms, ecosystem effects, and current mitigation efforts"
    ),
    
    # Education & Social Issues
    ResearcherTestCase(
        id="social_001",
        prompt="How has the rise of social media affected mental health among teenagers? What interventions are being tested?",
        domain="social_issues",
        difficulty="intermediate",
        expected_sources=["academic_research", "psychology_journals", "health_organizations"],
        key_concepts=["social media", "mental health", "teenagers", "depression", "anxiety", "digital wellness"],
        search_keywords=["social media mental health teens", "teenage depression social media", "digital wellness"],
        reference_info="Should cover research findings, correlation vs causation, and intervention strategies"
    ),
    
    ResearcherTestCase(
        id="social_002",
        prompt="What are the current debates around artificial intelligence ethics and regulation? Compare different national approaches.",
        domain="social_issues",
        difficulty="expert",
        expected_sources=["policy_research", "ethics_organizations", "government_sources"],
        key_concepts=["AI ethics", "AI regulation", "algorithmic bias", "privacy", "transparency", "governance"],
        search_keywords=["AI ethics regulation", "algorithmic bias", "AI governance", "AI policy"],
        reference_info="Should cover key ethical concerns, regulatory frameworks, and international differences"
    ),
    
    # Historical Research
    ResearcherTestCase(
        id="history_001",
        prompt="What were the key factors that led to the fall of the Roman Empire? Analyze different historical theories.",
        domain="history",
        difficulty="intermediate",
        expected_sources=["academic_sources", "historical_research", "educational_institutions"],
        key_concepts=["Roman Empire", "historical decline", "barbarian invasions", "economic factors", "political instability"],
        search_keywords=["fall of Roman Empire", "Roman decline theories", "barbarian invasions", "Roman history"],
        reference_info="Should present multiple historical theories and their supporting evidence"
    ),
    
    # Basic Research Tasks
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
        id="basic_002",
        prompt="How do electric vehicles work? Explain the technology and compare with traditional cars.",
        domain="technology",
        difficulty="basic",
        expected_sources=["automotive_sources", "educational_content", "manufacturer_information"],
        key_concepts=["electric vehicles", "EV technology", "batteries", "electric motors", "charging"],
        search_keywords=["how electric cars work", "EV technology", "electric vehicle batteries"],
        reference_info="Should explain basic EV technology and advantages/disadvantages vs conventional cars"
    ),
    
    # Complex Multi-faceted Research
    ResearcherTestCase(
        id="complex_001",
        prompt="Analyze the global impact of artificial intelligence on employment. Consider different sectors, geographical regions, and policy responses. Include both job displacement and job creation effects.",
        domain="technology",
        difficulty="expert",
        expected_sources=["economic_research", "labor_statistics", "policy_institutes", "tech_industry"],
        key_concepts=["AI employment impact", "job displacement", "job creation", "automation", "reskilling", "policy responses"],
        search_keywords=["AI impact jobs", "automation employment", "AI job displacement", "future of work"],
        reference_info="Should provide balanced analysis of both positive and negative employment effects across different sectors and regions"
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
    """Get a summary of the test dataset."""
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