"""
Expanded test dataset for Cancer Immunogenomics Biomedical Researcher agent.

This comprehensive dataset is designed for scientific conference presentations and
includes 33 test cases across 11 specialized domains with robust coverage of
current cancer immunogenomics research areas.

Dataset Design:
- 33 total cases for statistical robustness  
- 11 domains with exactly 3 cases each
- Priority system: 18 high (conference focus), 15 standard (comprehensive coverage)
- Balanced difficulty: 3 basic, 13 intermediate, 17 expert
- Covers cutting-edge topics and clinical applications
- Aligned with agent's MCP tool capabilities: PubMed, ClinicalTrials.gov, BioRxiv/MedRxiv, OpenTargets
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
    expected_sources: List[str]
    key_concepts: List[str]
    reference_info: str = ""
    priority: str = "standard"  # "high", "standard"


# Comprehensive 33-case cancer immunogenomics test dataset for scientific presentation
BIOMEDICAL_TEST_CASES_EXPANDED = [
    # ======================
    # T-Cell Receptor Analysis (3 cases)
    # ======================
    BiomedicalTestCase(
        id="tcr_001",
        prompt="How can TCR repertoire sequencing be used to monitor response to cancer immunotherapy? Include information about clonality metrics, diversity indices, and clinical correlations.",
        domain="tcr_analysis",
        difficulty="expert",
        expected_sources=["PubMed", "BioRxiv"],
        key_concepts=["TCR repertoire", "clonality", "Shannon entropy", "immunotherapy response", "TCR sequencing"],
        reference_info="TCR clonal expansion correlates with immunotherapy response; diversity metrics predict treatment outcomes",
        priority="high"
    ),
    
    BiomedicalTestCase(
        id="tcr_002",
        prompt="What are the computational methods for TCR-peptide-MHC binding prediction, and how accurate are current algorithms?",
        domain="tcr_analysis",
        difficulty="expert",
        expected_sources=["PubMed", "BioRxiv"],
        key_concepts=["TCR-pMHC binding", "NetTCR", "ERGO", "computational prediction", "binding affinity"],
        reference_info="Machine learning models achieve 70-80% accuracy in TCR-peptide binding prediction",
        priority="high"
    ),
    
    BiomedicalTestCase(
        id="tcr_003",
        prompt="How does TCR diversity change with age and what are the implications for cancer immunotherapy in elderly patients?",
        domain="tcr_analysis",
        difficulty="intermediate",
        expected_sources=["PubMed"],
        key_concepts=["TCR diversity", "aging", "immunosenescence", "elderly patients", "therapy efficacy"],
        reference_info="TCR diversity decreases with age, potentially reducing immunotherapy efficacy in elderly",
        priority="standard"
    ),
    
    # ======================
    # Neoantigen Prediction & HLA Typing (3 cases)
    # ======================
    BiomedicalTestCase(
        id="neoantigen_001",
        prompt="What are the current computational pipelines for neoantigen prediction from tumor sequencing data? Compare accuracy of HLA binding prediction tools.",
        domain="neoantigen_prediction",
        difficulty="expert",
        expected_sources=["PubMed", "BioRxiv"],
        key_concepts=["neoantigen prediction", "HLA binding", "NetMHCpan", "pVACseq", "tumor mutations"],
        reference_info="NetMHCpan shows >90% accuracy for strong binders; neoantigen load correlates with immunotherapy response",
        priority="high"
    ),
    
    BiomedicalTestCase(
        id="neoantigen_002",
        prompt="How do HLA Class I and Class II presentation pathways differ in neoantigen processing, and what are the implications for cancer vaccine design?",
        domain="neoantigen_prediction",
        difficulty="intermediate",
        expected_sources=["PubMed"],
        key_concepts=["HLA Class I", "HLA Class II", "antigen processing", "cancer vaccines", "CD8+ T cells", "CD4+ T cells"],
        reference_info="Class I presents to CD8+ T cells; Class II to CD4+ T cells; both important for effective cancer immunity",
        priority="high"
    ),
    
    BiomedicalTestCase(
        id="neoantigen_003",
        prompt="What factors influence neoantigen immunogenicity beyond HLA binding affinity? Discuss proteasomal cleavage, TAP transport, and T-cell recognition.",
        domain="neoantigen_prediction",
        difficulty="expert",
        expected_sources=["PubMed", "BioRxiv"],
        key_concepts=["neoantigen immunogenicity", "proteasomal cleavage", "TAP transport", "T-cell recognition", "HLA binding"],
        reference_info="Multiple steps beyond HLA binding affect neoantigen presentation and immunogenicity",
        priority="standard"
    ),
    
    # ======================
    # Tumor Microenvironment & Immune Infiltration (3 cases)
    # ======================
    BiomedicalTestCase(
        id="tme_001",
        prompt="What are the latest computational methods for quantifying immune cell infiltration in tumors from bulk RNA-seq data? Compare CIBERSORT, ESTIMATE, and newer approaches.",
        domain="tumor_microenvironment",
        difficulty="expert",
        expected_sources=["PubMed", "BioRxiv"],
        key_concepts=["immune infiltration", "CIBERSORT", "ESTIMATE", "deconvolution", "bulk RNA-seq"],
        reference_info="CIBERSORT and newer deep learning methods show improved accuracy in immune cell quantification",
        priority="high"
    ),
    
    BiomedicalTestCase(
        id="tme_002",
        prompt="How does the tumor microenvironment influence T-cell exhaustion, and what genomic signatures are associated with exhausted T-cell states?",
        domain="tumor_microenvironment",
        difficulty="expert",
        expected_sources=["PubMed", "BioRxiv"],
        key_concepts=["T-cell exhaustion", "PD-1", "TIM-3", "LAG-3", "exhaustion signatures", "tumor microenvironment"],
        reference_info="Exhausted T cells express inhibitory receptors; TOX and TCF1 are key transcriptional regulators",
        priority="high"
    ),
    
    BiomedicalTestCase(
        id="tme_003",
        prompt="What role do tumor-associated macrophages play in immunotherapy resistance, and how can their polarization be targeted therapeutically?",
        domain="tumor_microenvironment",
        difficulty="intermediate",
        expected_sources=["PubMed", "ClinicalTrials.gov"],
        key_concepts=["tumor-associated macrophages", "M1/M2 polarization", "immunotherapy resistance", "therapeutic targeting"],
        reference_info="M2-polarized macrophages promote immunosuppression and can be repolarized to enhance therapy",
        priority="standard"
    ),
    
    # ======================
    # Immunotherapy Biomarkers (3 cases)
    # ======================
    BiomedicalTestCase(
        id="biomarkers_001",
        prompt="What genomic biomarkers predict response to immune checkpoint inhibitors? Discuss tumor mutational burden, microsatellite instability, and HLA loss of heterozygosity.",
        domain="immunotherapy_biomarkers",
        difficulty="expert",
        expected_sources=["PubMed", "ClinicalTrials.gov"],
        key_concepts=["TMB", "MSI", "HLA LOH", "checkpoint inhibitors", "biomarkers", "immunotherapy response"],
        reference_info="High TMB and MSI-H status predict better response to checkpoint inhibitors; HLA LOH associated with resistance",
        priority="high"
    ),
    
    BiomedicalTestCase(
        id="biomarkers_002",
        prompt="How can interferon-gamma signatures and immune gene expression profiles be used to stratify patients for immunotherapy?",
        domain="immunotherapy_biomarkers",
        difficulty="intermediate",
        expected_sources=["PubMed"],
        key_concepts=["interferon-gamma signature", "immune gene expression", "patient stratification", "immunotherapy", "biomarkers"],
        reference_info="IFN-gamma signatures correlate with T-cell inflamed tumors and better immunotherapy response",
        priority="high"
    ),
    
    BiomedicalTestCase(
        id="biomarkers_003",
        prompt="What are the emerging blood-based biomarkers for monitoring immunotherapy response, including circulating tumor DNA and immune cell profiling?",
        domain="immunotherapy_biomarkers",
        difficulty="intermediate",
        expected_sources=["PubMed"],
        key_concepts=["liquid biopsy", "circulating tumor DNA", "immune cell profiling", "blood biomarkers", "therapy monitoring"],
        reference_info="ctDNA kinetics and circulating immune cell changes can predict therapy response",
        priority="standard"
    ),
    
    # ======================
    # CAR-T Cell Therapy & Engineering (3 cases)
    # ======================
    BiomedicalTestCase(
        id="cart_001",
        prompt="What are the latest advances in CAR-T cell therapy for solid tumors? Include challenges with tumor penetration, antigen escape, and immunosuppressive microenvironment.",
        domain="cart_therapy",
        difficulty="expert",
        expected_sources=["PubMed", "ClinicalTrials.gov"],
        key_concepts=["CAR-T cells", "solid tumors", "antigen escape", "tumor penetration", "immunosuppression"],
        reference_info="CAR-T therapy faces challenges in solid tumors including poor infiltration and immunosuppressive TME",
        priority="high"
    ),
    
    BiomedicalTestCase(
        id="cart_002",
        prompt="How are next-generation CAR designs addressing limitations of current CAR-T cell therapies? Discuss logic gates, universal CARs, and armored CAR-T cells.",
        domain="cart_therapy",
        difficulty="expert",
        expected_sources=["PubMed", "BioRxiv"],
        key_concepts=["next-generation CAR", "logic gates", "universal CAR", "armored CAR-T", "CAR design"],
        reference_info="Logic-gated CARs improve specificity; armored CAR-T cells resist immunosuppression",
        priority="high"
    ),
    
    BiomedicalTestCase(
        id="cart_003",
        prompt="What are the mechanisms and management strategies for CAR-T cell therapy-related toxicities, including cytokine release syndrome and neurotoxicity?",
        domain="cart_therapy",
        difficulty="intermediate",
        expected_sources=["PubMed"],
        key_concepts=["CAR-T toxicity", "cytokine release syndrome", "neurotoxicity", "management", "safety"],
        reference_info="CRS and neurotoxicity are major toxicities managed with tocilizumab and corticosteroids",
        priority="standard"
    ),
    
    # ======================
    # Cancer Genomics & Immune Evasion (3 cases)
    # ======================
    BiomedicalTestCase(
        id="genomics_001",
        prompt="What are the mechanisms of immune evasion in cancer, and how do genomic alterations in antigen presentation machinery contribute to immunotherapy resistance?",
        domain="cancer_genomics",
        difficulty="expert",
        expected_sources=["PubMed", "OpenTargets"],
        key_concepts=["immune evasion", "antigen presentation", "HLA", "beta-2-microglobulin", "immunotherapy resistance"],
        reference_info="Loss of HLA expression and antigen presentation defects are major immune evasion mechanisms",
        priority="high"
    ),
    
    BiomedicalTestCase(
        id="genomics_002",
        prompt="How do DNA mismatch repair deficiencies influence tumor immunogenicity and response to immune checkpoint inhibitors?",
        domain="cancer_genomics",
        difficulty="intermediate",
        expected_sources=["PubMed"],
        key_concepts=["mismatch repair", "MMR", "microsatellite instability", "tumor immunogenicity", "checkpoint inhibitors"],
        reference_info="MMR deficiency leads to high mutation burden and neoantigen load, improving immunotherapy response",
        priority="high"
    ),
    
    BiomedicalTestCase(
        id="genomics_003",
        prompt="What role do oncogenic signaling pathways (MAPK, PI3K/AKT, Wnt) play in modulating immune responses in cancer?",
        domain="cancer_genomics",
        difficulty="expert",
        expected_sources=["PubMed"],
        key_concepts=["oncogenic signaling", "MAPK", "PI3K/AKT", "Wnt", "immune modulation", "cancer immunity"],
        reference_info="Oncogenic pathways can both promote and suppress immune responses depending on context",
        priority="standard"
    ),
    
    # ======================
    # Immune Resistance Mechanisms (3 cases) - NEW DOMAIN
    # ======================
    BiomedicalTestCase(
        id="resistance_001",
        prompt="What are the mechanisms of acquired resistance to immune checkpoint inhibitors, and how can they be overcome therapeutically?",
        domain="immune_resistance",
        difficulty="expert",
        expected_sources=["PubMed"],
        key_concepts=["acquired resistance", "checkpoint inhibitors", "resistance mechanisms", "therapeutic strategies"],
        reference_info="Acquired resistance involves multiple mechanisms including T-cell exclusion and immune suppression",
        priority="high"
    ),
    
    BiomedicalTestCase(
        id="resistance_002",
        prompt="How do tumors evolve to escape immune surveillance during immunotherapy treatment? Discuss clonal evolution and neoantigen loss.",
        domain="immune_resistance",
        difficulty="expert",
        expected_sources=["PubMed"],
        key_concepts=["immune escape", "clonal evolution", "neoantigen loss", "immunotherapy", "tumor evolution"],
        reference_info="Tumors can lose neoantigens through mutation or HLA loss during treatment",
        priority="standard"
    ),
    
    BiomedicalTestCase(
        id="resistance_003",
        prompt="What role does the gut microbiome play in modulating immunotherapy response and resistance?",
        domain="immune_resistance",
        difficulty="intermediate",
        expected_sources=["PubMed"],
        key_concepts=["gut microbiome", "immunotherapy response", "resistance", "immune modulation"],
        reference_info="Specific bacterial species can enhance or diminish immunotherapy efficacy",
        priority="standard"
    ),
    
    # ======================
    # Combination Immunotherapy Strategies (3 cases) - NEW DOMAIN
    # ======================
    BiomedicalTestCase(
        id="combo_001",
        prompt="What are the rationales and current clinical results for combining immune checkpoint inhibitors with targeted therapies in cancer treatment?",
        domain="combination_therapy",
        difficulty="expert",
        expected_sources=["PubMed", "ClinicalTrials.gov"],
        key_concepts=["combination therapy", "checkpoint inhibitors", "targeted therapy", "synergy", "clinical trials"],
        reference_info="Combinations can overcome resistance mechanisms and improve response rates",
        priority="high"
    ),
    
    BiomedicalTestCase(
        id="combo_002",
        prompt="How can radiotherapy be combined with immunotherapy to enhance anti-tumor immune responses? Discuss the abscopal effect and optimal sequencing.",
        domain="combination_therapy",
        difficulty="intermediate",
        expected_sources=["PubMed"],
        key_concepts=["radiotherapy", "immunotherapy", "abscopal effect", "sequencing", "immune activation"],
        reference_info="Radiation can enhance immunotherapy through antigen release and immune activation",
        priority="standard"
    ),
    
    BiomedicalTestCase(
        id="combo_003",
        prompt="What are the challenges and opportunities in combining different immunotherapy modalities, such as checkpoint inhibitors with CAR-T cells or cancer vaccines?",
        domain="combination_therapy",
        difficulty="expert",
        expected_sources=["PubMed", "BioRxiv"],
        key_concepts=["immunotherapy combinations", "checkpoint inhibitors", "CAR-T", "cancer vaccines", "synergy"],
        reference_info="Multiple immunotherapy combinations are being explored to enhance efficacy",
        priority="standard"
    ),
    
    # ======================
    # Cancer Vaccines (3 cases)
    # ======================
    BiomedicalTestCase(
        id="vaccines_001",
        prompt="What are the current approaches for designing personalized cancer vaccines based on patient-specific neoantigens? Include mRNA, peptide, and dendritic cell platforms.",
        domain="cancer_vaccines",
        difficulty="expert",
        expected_sources=["PubMed", "ClinicalTrials.gov"],
        key_concepts=["personalized vaccines", "neoantigens", "mRNA vaccines", "peptide vaccines", "dendritic cells"],
        reference_info="Personalized vaccines target patient-specific neoantigens; mRNA and peptide platforms show promise",
        priority="high"
    ),
    
    BiomedicalTestCase(
        id="vaccines_002",
        prompt="How are shared tumor antigens being targeted in cancer vaccines, and what are the advantages and limitations compared to personalized approaches?",
        domain="cancer_vaccines",
        difficulty="intermediate",
        expected_sources=["PubMed", "ClinicalTrials.gov"],
        key_concepts=["shared tumor antigens", "cancer vaccines", "NY-ESO-1", "MAGE", "personalized vaccines"],
        reference_info="Shared antigens allow off-the-shelf vaccines but may have lower immunogenicity than neoantigens",
        priority="standard"
    ),
    
    BiomedicalTestCase(
        id="vaccines_003",
        prompt="What are the immunological mechanisms that determine cancer vaccine efficacy, and how can vaccine formulations be optimized?",
        domain="cancer_vaccines",
        difficulty="intermediate",
        expected_sources=["PubMed"],
        key_concepts=["vaccine efficacy", "immunological mechanisms", "vaccine formulation", "adjuvants", "optimization"],
        reference_info="Vaccine efficacy depends on antigen selection, delivery method, and adjuvant choice",
        priority="standard"
    ),
    
    # ======================
    # Computational Tools & Bioinformatics (3 cases) - NEW DOMAIN
    # ======================
    BiomedicalTestCase(
        id="computational_001",
        prompt="What are the key bioinformatics resources and databases for cancer immunogenomics research? Compare TCGA, ICGC, and newer single-cell atlases.",
        domain="computational_tools",
        difficulty="intermediate",
        expected_sources=["PubMed", "BioRxiv"],
        key_concepts=["bioinformatics resources", "TCGA", "ICGC", "single-cell atlases", "cancer genomics"],
        reference_info="TCGA and ICGC provide bulk tumor data; single-cell atlases reveal cellular heterogeneity",
        priority="high"
    ),
    
    BiomedicalTestCase(
        id="computational_002",
        prompt="How can single-cell RNA sequencing be applied to study tumor-immune interactions? Discuss analysis methods and computational challenges.",
        domain="computational_tools",
        difficulty="expert",
        expected_sources=["PubMed", "BioRxiv"],
        key_concepts=["single-cell RNA-seq", "tumor-immune interactions", "analysis methods", "computational challenges"],
        reference_info="scRNA-seq reveals cellular heterogeneity and cell-cell communication in tumor microenvironment",
        priority="high"
    ),
    
    BiomedicalTestCase(
        id="computational_003",
        prompt="What machine learning approaches are being used for cancer immunotherapy outcome prediction? Compare deep learning and traditional methods.",
        domain="computational_tools",
        difficulty="expert",
        expected_sources=["PubMed", "BioRxiv"],
        key_concepts=["machine learning", "immunotherapy prediction", "deep learning", "outcome prediction"],
        reference_info="Deep learning models show promise for integrating multi-modal data for therapy prediction",
        priority="standard"
    ),
    
    # ======================
    # Clinical Translation (3 cases)
    # ======================
    BiomedicalTestCase(
        id="clinical_001",
        prompt="What are the regulatory considerations and challenges for translating cancer immunogenomics discoveries into clinical practice? Include FDA guidance and biomarker validation.",
        domain="clinical_translation",
        difficulty="expert",
        expected_sources=["PubMed", "ClinicalTrials.gov"],
        key_concepts=["regulatory", "FDA guidance", "biomarker validation", "clinical translation", "immunogenomics"],
        reference_info="FDA requires analytical and clinical validation for companion diagnostics; standardization is key challenge",
        priority="high"
    ),
    
    BiomedicalTestCase(
        id="clinical_002",
        prompt="How can real-world evidence be leveraged to improve cancer immunotherapy outcomes? Discuss data collection, analysis challenges, and clinical applications.",
        domain="clinical_translation",
        difficulty="intermediate",
        expected_sources=["PubMed"],
        key_concepts=["real-world evidence", "immunotherapy outcomes", "data collection", "clinical applications"],
        reference_info="Real-world data provides insights into therapy effectiveness outside clinical trials",
        priority="standard"
    ),
    
    BiomedicalTestCase(
        id="clinical_003",
        prompt="What are the economic considerations and cost-effectiveness analyses for implementing precision immunogenomics in clinical practice?",
        domain="clinical_translation",
        difficulty="intermediate",
        expected_sources=["PubMed"],
        key_concepts=["health economics", "cost-effectiveness", "precision medicine", "immunogenomics", "implementation"],
        reference_info="Cost-effectiveness depends on test accuracy, treatment response rates, and healthcare costs",
        priority="standard"
    ),
    
    # ======================
    # Immune Foundations (3 cases)
    # ======================
    BiomedicalTestCase(
        id="foundations_001",
        prompt="What are the fundamental concepts of adaptive immunity relevant to cancer immunotherapy? Explain T-cell activation, memory formation, and antigen recognition.",
        domain="immune_foundations",
        difficulty="basic",
        expected_sources=["PubMed"],
        key_concepts=["adaptive immunity", "T-cell activation", "memory T cells", "antigen recognition", "MHC"],
        reference_info="T-cell activation requires TCR-MHC interaction plus costimulation; memory cells provide long-term protection",
        priority="high"
    ),
    
    BiomedicalTestCase(
        id="foundations_002",
        prompt="How does the immune system normally recognize and eliminate cancer cells? Describe the cancer-immunity cycle and immunosurveillance mechanisms.",
        domain="immune_foundations",
        difficulty="basic",
        expected_sources=["PubMed"],
        key_concepts=["cancer-immunity cycle", "immunosurveillance", "tumor antigens", "immune recognition"],
        reference_info="Cancer-immunity cycle involves antigen release, presentation, T-cell priming, and tumor killing",
        priority="high"
    ),
    
    BiomedicalTestCase(
        id="foundations_003",
        prompt="What are the key differences between innate and adaptive immune responses in cancer, and how do they interact in tumor immunity?",
        domain="immune_foundations",
        difficulty="basic",
        expected_sources=["PubMed"],
        key_concepts=["innate immunity", "adaptive immunity", "tumor immunity", "immune interactions", "cancer"],
        reference_info="Innate immunity provides initial tumor recognition; adaptive immunity provides specific and memory responses",
        priority="standard"
    )
]


def get_expanded_test_cases_by_domain(domain: str) -> List[BiomedicalTestCase]:
    """Get expanded test cases filtered by domain."""
    return [case for case in BIOMEDICAL_TEST_CASES_EXPANDED if case.domain == domain]


def get_expanded_test_cases_by_difficulty(difficulty: str) -> List[BiomedicalTestCase]:
    """Get expanded test cases filtered by difficulty level."""
    return [case for case in BIOMEDICAL_TEST_CASES_EXPANDED if case.difficulty == difficulty]


def get_expanded_test_cases_by_priority(priority: str) -> List[BiomedicalTestCase]:
    """Get expanded test cases filtered by priority level."""
    return [case for case in BIOMEDICAL_TEST_CASES_EXPANDED if case.priority == priority]


def get_expanded_test_case_by_id(test_id: str) -> BiomedicalTestCase:
    """Get a specific expanded test case by ID."""
    for case in BIOMEDICAL_TEST_CASES_EXPANDED:
        if case.id == test_id:
            return case
    raise ValueError(f"Test case with ID '{test_id}' not found")


def get_all_expanded_domains() -> List[str]:
    """Get all unique domains in the expanded dataset."""
    return list(set(case.domain for case in BIOMEDICAL_TEST_CASES_EXPANDED))


def get_expanded_dataset_summary() -> Dict[str, Any]:
    """Get summary statistics for the expanded dataset."""
    domains = {}
    difficulties = {}
    priorities = {}
    
    for case in BIOMEDICAL_TEST_CASES_EXPANDED:
        domains[case.domain] = domains.get(case.domain, 0) + 1
        difficulties[case.difficulty] = difficulties.get(case.difficulty, 0) + 1
        priorities[case.priority] = priorities.get(case.priority, 0) + 1
    
    return {
        "total_cases": len(BIOMEDICAL_TEST_CASES_EXPANDED),
        "domains": domains,
        "difficulties": difficulties,
        "priorities": priorities,
        "domain_count": len(domains),
        "avg_cases_per_domain": len(BIOMEDICAL_TEST_CASES_EXPANDED) / len(domains)
    }


def get_high_priority_cases() -> List[BiomedicalTestCase]:
    """Get only high priority test cases for focused evaluation."""
    return [case for case in BIOMEDICAL_TEST_CASES_EXPANDED if case.priority == "high"]


def get_balanced_subset(n_cases: int = 15) -> List[BiomedicalTestCase]:
    """Get a balanced subset of test cases across domains and difficulties."""
    import random
    
    # Get cases by difficulty
    basic_cases = [case for case in BIOMEDICAL_TEST_CASES_EXPANDED if case.difficulty == "basic"]
    intermediate_cases = [case for case in BIOMEDICAL_TEST_CASES_EXPANDED if case.difficulty == "intermediate"]
    expert_cases = [case for case in BIOMEDICAL_TEST_CASES_EXPANDED if case.difficulty == "expert"]
    
    # Calculate proportional distribution
    basic_count = max(1, int(n_cases * 0.2))  # ~20%
    intermediate_count = max(1, int(n_cases * 0.4))  # ~40%
    expert_count = n_cases - basic_count - intermediate_count  # Remaining
    
    # Sample from each difficulty level
    selected_cases = []
    selected_cases.extend(random.sample(basic_cases, min(basic_count, len(basic_cases))))
    selected_cases.extend(random.sample(intermediate_cases, min(intermediate_count, len(intermediate_cases))))
    selected_cases.extend(random.sample(expert_cases, min(expert_count, len(expert_cases))))
    
    return selected_cases[:n_cases] 