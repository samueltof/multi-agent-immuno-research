"""
Test dataset for evaluating the Cancer Immunogenomics Biomedical Researcher agent.

This module contains carefully curated cancer immunogenomics research questions covering
T-cell receptor analysis, neoantigen prediction, tumor microenvironment, immunotherapy
biomarkers, and personalized cancer immunology to comprehensively test the agent's 
specialized capabilities in cancer immunogenomics research.
"""

from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class BiomedicalTestCase:
    """Represents a single test case for biomedical research evaluation."""
    id: str
    prompt: str
    domain: str
    difficulty: str  # "basic", "intermediate", "expert"
    expected_sources: List[str]  # Types of sources we expect (e.g., "PubMed", "ClinicalTrials")
    key_concepts: List[str]  # Key biomedical concepts that should be addressed
    reference_info: str = ""  # Optional reference information for comparison


# Comprehensive cancer immunogenomics test dataset
BIOMEDICAL_TEST_CASES = [
    # T-Cell Receptor (TCR) Analysis & Repertoire Sequencing
    BiomedicalTestCase(
        id="tcr_001",
        prompt="How can TCR repertoire sequencing be used to monitor response to cancer immunotherapy? Include information about clonality metrics, diversity indices, and clinical correlations.",
        domain="tcr_analysis",
        difficulty="expert",
        expected_sources=["PubMed", "BioRxiv"],
        key_concepts=["TCR repertoire", "clonality", "Shannon entropy", "immunotherapy response", "TCR sequencing"],
        reference_info="TCR clonal expansion correlates with immunotherapy response; diversity metrics predict treatment outcomes"
    ),
    
    BiomedicalTestCase(
        id="tcr_002",
        prompt="What are the computational methods for TCR-peptide-MHC binding prediction, and how accurate are current algorithms?",
        domain="tcr_analysis",
        difficulty="expert",
        expected_sources=["PubMed", "BioRxiv"],
        key_concepts=["TCR-pMHC binding", "NetTCR", "ERGO", "computational prediction", "binding affinity"],
        reference_info="Machine learning models achieve 70-80% accuracy in TCR-peptide binding prediction"
    ),
    
    # Neoantigen Prediction & HLA Typing
    BiomedicalTestCase(
        id="neoantigen_001",
        prompt="What are the current computational pipelines for neoantigen prediction from tumor sequencing data? Compare accuracy of HLA binding prediction tools.",
        domain="neoantigen_prediction",
        difficulty="expert",
        expected_sources=["PubMed", "BioRxiv"],
        key_concepts=["neoantigen prediction", "HLA binding", "NetMHCpan", "pVACseq", "tumor mutations"],
        reference_info="NetMHCpan shows >90% accuracy for strong binders; neoantigen load correlates with immunotherapy response"
    ),
    
    BiomedicalTestCase(
        id="neoantigen_002",
        prompt="How do HLA Class I and Class II presentation pathways differ in neoantigen processing, and what are the implications for cancer vaccine design?",
        domain="neoantigen_prediction",
        difficulty="intermediate",
        expected_sources=["PubMed"],
        key_concepts=["HLA Class I", "HLA Class II", "antigen processing", "cancer vaccines", "CD8+ T cells", "CD4+ T cells"],
        reference_info="Class I presents to CD8+ T cells; Class II to CD4+ T cells; both important for effective cancer immunity"
    ),
    
    # Tumor Microenvironment & Immune Infiltration
    BiomedicalTestCase(
        id="tme_001",
        prompt="What are the latest computational methods for quantifying immune cell infiltration in tumors from bulk RNA-seq data? Compare CIBERSORT, ESTIMATE, and newer approaches.",
        domain="tumor_microenvironment",
        difficulty="expert",
        expected_sources=["PubMed", "BioRxiv"],
        key_concepts=["immune infiltration", "CIBERSORT", "ESTIMATE", "deconvolution", "bulk RNA-seq"],
        reference_info="CIBERSORT and newer deep learning methods show improved accuracy in immune cell quantification"
    ),
    
    BiomedicalTestCase(
        id="tme_002",
        prompt="How does the tumor microenvironment influence T-cell exhaustion, and what genomic signatures are associated with exhausted T-cell states?",
        domain="tumor_microenvironment",
        difficulty="expert",
        expected_sources=["PubMed", "BioRxiv"],
        key_concepts=["T-cell exhaustion", "PD-1", "TIM-3", "LAG-3", "exhaustion signatures", "tumor microenvironment"],
        reference_info="Exhausted T cells express inhibitory receptors; TOX and TCF1 are key transcriptional regulators"
    ),
    
    # Cancer Immunotherapy Biomarkers
    BiomedicalTestCase(
        id="biomarkers_001",
        prompt="What genomic biomarkers predict response to immune checkpoint inhibitors? Discuss tumor mutational burden, microsatellite instability, and HLA loss of heterozygosity.",
        domain="immunotherapy_biomarkers",
        difficulty="expert",
        expected_sources=["PubMed", "ClinicalTrials.gov"],
        key_concepts=["TMB", "MSI", "HLA LOH", "checkpoint inhibitors", "biomarkers", "immunotherapy response"],
        reference_info="High TMB and MSI-H status predict better response to checkpoint inhibitors; HLA LOH associated with resistance"
    ),
    
    BiomedicalTestCase(
        id="biomarkers_002",
        prompt="How can interferon-gamma signatures and immune gene expression profiles be used to stratify patients for immunotherapy?",
        domain="immunotherapy_biomarkers",
        difficulty="intermediate",
        expected_sources=["PubMed"],
        key_concepts=["interferon-gamma signature", "immune gene expression", "patient stratification", "immunotherapy", "biomarkers"],
        reference_info="IFN-gamma signatures correlate with T-cell inflamed tumors and better immunotherapy response"
    ),
    
    # CAR-T Cell Therapy & Engineering
    BiomedicalTestCase(
        id="cart_001",
        prompt="What are the latest advances in CAR-T cell therapy for solid tumors? Include challenges with tumor penetration, antigen escape, and immunosuppressive microenvironment.",
        domain="cart_therapy",
        difficulty="expert",
        expected_sources=["PubMed", "ClinicalTrials.gov"],
        key_concepts=["CAR-T cells", "solid tumors", "antigen escape", "tumor penetration", "immunosuppression"],
        reference_info="CAR-T therapy faces challenges in solid tumors including poor infiltration and immunosuppressive TME"
    ),
    
    BiomedicalTestCase(
        id="cart_002",
        prompt="How are next-generation CAR designs addressing limitations of current CAR-T cell therapies? Discuss logic gates, universal CARs, and armored CAR-T cells.",
        domain="cart_therapy",
        difficulty="expert",
        expected_sources=["PubMed", "BioRxiv"],
        key_concepts=["next-generation CAR", "logic gates", "universal CAR", "armored CAR-T", "CAR design"],
        reference_info="Logic-gated CARs improve specificity; armored CAR-T cells resist immunosuppression"
    ),
    
    # Cancer Genomics & Immune Evasion
    BiomedicalTestCase(
        id="genomics_001",
        prompt="What are the mechanisms of immune evasion in cancer, and how do genomic alterations in antigen presentation machinery contribute to immunotherapy resistance?",
        domain="cancer_genomics",
        difficulty="expert",
        expected_sources=["PubMed", "OpenTargets"],
        key_concepts=["immune evasion", "antigen presentation", "HLA", "beta-2-microglobulin", "immunotherapy resistance"],
        reference_info="Loss of HLA expression and antigen presentation defects are major immune evasion mechanisms"
    ),
    
    BiomedicalTestCase(
        id="genomics_002",
        prompt="How do DNA mismatch repair deficiencies influence tumor immunogenicity and response to immune checkpoint inhibitors?",
        domain="cancer_genomics",
        difficulty="intermediate",
        expected_sources=["PubMed"],
        key_concepts=["mismatch repair", "MMR", "microsatellite instability", "tumor immunogenicity", "checkpoint inhibitors"],
        reference_info="MMR deficiency leads to high mutation burden and neoantigen load, improving immunotherapy response"
    ),
    
    # Personalized Cancer Vaccines
    BiomedicalTestCase(
        id="vaccines_001",
        prompt="What are the current approaches for designing personalized cancer vaccines based on patient-specific neoantigens? Include mRNA, peptide, and dendritic cell platforms.",
        domain="cancer_vaccines",
        difficulty="expert",
        expected_sources=["PubMed", "ClinicalTrials.gov"],
        key_concepts=["personalized vaccines", "neoantigens", "mRNA vaccines", "peptide vaccines", "dendritic cells"],
        reference_info="Personalized vaccines target patient-specific neoantigens; mRNA and peptide platforms show promise"
    ),
    
    BiomedicalTestCase(
        id="vaccines_002",
        prompt="How are shared tumor antigens being targeted in cancer vaccines, and what are the advantages and limitations compared to personalized approaches?",
        domain="cancer_vaccines",
        difficulty="intermediate",
        expected_sources=["PubMed", "ClinicalTrials.gov"],
        key_concepts=["shared tumor antigens", "cancer vaccines", "NY-ESO-1", "MAGE", "personalized vaccines"],
        reference_info="Shared antigens allow off-the-shelf vaccines but may have lower immunogenicity than neoantigens"
    ),
    
    # Computational Immunogenomics Tools
    BiomedicalTestCase(
        id="tools_001",
        prompt="What are the key bioinformatics tools and databases for cancer immunogenomics research? Compare TCGA immune subtypes, TIMER, and other resources.",
        domain="computational_tools",
        difficulty="intermediate",
        expected_sources=["PubMed", "BioRxiv"],
        key_concepts=["bioinformatics tools", "TCGA", "TIMER", "immune subtypes", "cancer immunogenomics"],
        reference_info="TCGA provides immune subtypes; TIMER quantifies immune infiltration; multiple specialized databases available"
    ),
    
    BiomedicalTestCase(
        id="tools_002",
        prompt="How can single-cell RNA sequencing be applied to cancer immunogenomics research? Discuss cell type identification, trajectory analysis, and immune cell interactions.",
        domain="computational_tools",
        difficulty="expert",
        expected_sources=["PubMed", "BioRxiv"],
        key_concepts=["single-cell RNA-seq", "cell type identification", "trajectory analysis", "immune interactions", "cancer"],
        reference_info="scRNA-seq reveals immune cell heterogeneity and states; enables study of cell-cell interactions in TME"
    ),
    
    # Clinical Translation & Regulatory
    BiomedicalTestCase(
        id="clinical_001",
        prompt="What are the regulatory considerations and challenges for translating cancer immunogenomics discoveries into clinical practice? Include FDA guidance and biomarker validation.",
        domain="clinical_translation",
        difficulty="expert",
        expected_sources=["PubMed", "ClinicalTrials.gov"],
        key_concepts=["regulatory", "FDA guidance", "biomarker validation", "clinical translation", "immunogenomics"],
        reference_info="FDA requires analytical and clinical validation for companion diagnostics; standardization is key challenge"
    ),
    
    # Basic Foundations
    BiomedicalTestCase(
        id="foundations_001",
        prompt="What are the fundamental concepts of adaptive immunity relevant to cancer immunotherapy? Explain T-cell activation, memory formation, and antigen recognition.",
        domain="immune_foundations",
        difficulty="basic",
        expected_sources=["PubMed"],
        key_concepts=["adaptive immunity", "T-cell activation", "memory T cells", "antigen recognition", "MHC"],
        reference_info="T-cell activation requires TCR-MHC interaction plus costimulation; memory cells provide long-term protection"
    ),
    
    BiomedicalTestCase(
        id="foundations_002",
        prompt="How does the immune system normally recognize and eliminate cancer cells? Describe the cancer-immunity cycle and immunosurveillance mechanisms.",
        domain="immune_foundations",
        difficulty="intermediate",
        expected_sources=["PubMed"],
        key_concepts=["cancer-immunity cycle", "immunosurveillance", "tumor antigens", "immune recognition"],
        reference_info="Cancer-immunity cycle involves antigen release, presentation, T-cell priming, and tumor killing"
    )
]


def get_test_cases_by_domain(domain: str) -> List[BiomedicalTestCase]:
    """Get test cases filtered by domain."""
    return [case for case in BIOMEDICAL_TEST_CASES if case.domain == domain]


def get_test_cases_by_difficulty(difficulty: str) -> List[BiomedicalTestCase]:
    """Get test cases filtered by difficulty level."""
    return [case for case in BIOMEDICAL_TEST_CASES if case.difficulty == difficulty]


def get_test_case_by_id(test_id: str) -> BiomedicalTestCase:
    """Get a specific test case by ID."""
    for case in BIOMEDICAL_TEST_CASES:
        if case.id == test_id:
            return case
    raise ValueError(f"Test case with ID '{test_id}' not found")


def get_all_domains() -> List[str]:
    """Get all unique domains in the test dataset."""
    return list(set(case.domain for case in BIOMEDICAL_TEST_CASES))


def get_test_dataset_summary() -> Dict[str, Any]:
    """Get a summary of the test dataset."""
    domains = {}
    difficulties = {}
    
    for case in BIOMEDICAL_TEST_CASES:
        domains[case.domain] = domains.get(case.domain, 0) + 1
        difficulties[case.difficulty] = difficulties.get(case.difficulty, 0) + 1
    
    return {
        "total_cases": len(BIOMEDICAL_TEST_CASES),
        "domains": domains,
        "difficulties": difficulties,
        "average_concepts_per_case": sum(len(case.key_concepts) for case in BIOMEDICAL_TEST_CASES) / len(BIOMEDICAL_TEST_CASES)
    } 