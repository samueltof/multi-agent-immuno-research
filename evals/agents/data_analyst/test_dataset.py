"""
Test dataset for evaluating the Data Analyst agent.

This module contains test cases covering various SQL query scenarios against the VDJdb augmented database:
- Schema exploration and understanding
- Simple single-table queries
- Complex multi-table joins
- Aggregation and statistical analysis
- Temporal analysis
- Immunological domain-specific queries
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class DataAnalystTestCase:
    """Test case for evaluating the data analyst agent."""
    id: str
    natural_language_query: str
    query_type: str  # "schema", "simple", "join", "aggregation", "temporal", "statistical", "immunological"
    difficulty: str  # "easy", "medium", "hard"
    expected_sql_pattern: Optional[str]  # Pattern the SQL should match
    expected_tables: List[str]  # Tables that should be involved
    expected_columns: List[str]  # Key columns that should be selected/used
    success_criteria: List[str]
    domain_context: str  # Immunology context for domain-specific evaluation
    
    def __post_init__(self):
        if self.success_criteria is None:
            self.success_criteria = []


# Schema Exploration Test Cases
SCHEMA_EXPLORATION_CASES = [
    DataAnalystTestCase(
        id="schema_001",
        natural_language_query="Show me the database schema for all tables",
        query_type="schema",
        difficulty="easy",
        expected_sql_pattern=None,  # This should return schema description, not SQL
        expected_tables=[],
        expected_columns=[],
        success_criteria=[
            "Returns complete database schema",
            "Shows all 8 tables (epitopes, mhc_alleles, donors, samples, publications, complexes, chains, assays)",
            "Includes column information for each table",
            "Provides table relationships"
        ],
        domain_context="Understanding the VDJdb database structure is crucial for immunological data analysis"
    ),
    
    DataAnalystTestCase(
        id="schema_002",
        natural_language_query="What columns are available in the epitopes table?",
        query_type="schema",
        difficulty="easy",
        expected_sql_pattern=None,
        expected_tables=["epitopes"],
        expected_columns=["epitope_id", "sequence", "length", "ic50", "source_protein", "species"],
        success_criteria=[
            "Returns epitopes table schema",
            "Lists all columns with types",
            "Explains column purposes"
        ],
        domain_context="Epitope table contains peptide sequences that T-cells recognize"
    ),
]

# Simple Query Test Cases
SIMPLE_QUERY_CASES = [
    DataAnalystTestCase(
        id="simple_001",
        natural_language_query="How many epitopes are there in the database?",
        query_type="simple",
        difficulty="easy",
        expected_sql_pattern="SELECT COUNT(*) FROM epitopes",
        expected_tables=["epitopes"],
        expected_columns=["epitope_id"],
        success_criteria=[
            "Uses COUNT(*) or COUNT(epitope_id)",
            "Queries epitopes table",
            "Returns single count value"
        ],
        domain_context="Basic counting of peptide epitopes"
    ),
    
    DataAnalystTestCase(
        id="simple_002",
        natural_language_query="List the first 10 epitope sequences and their lengths",
        query_type="simple",
        difficulty="easy",
        expected_sql_pattern="SELECT sequence, length FROM epitopes LIMIT 10",
        expected_tables=["epitopes"],
        expected_columns=["sequence", "length"],
        success_criteria=[
            "Selects sequence and length columns",
            "Uses LIMIT 10",
            "Returns epitope sequences with lengths",
            "Handles NULL values appropriately"
        ],
        domain_context="Viewing peptide sequences and their amino acid lengths"
    ),
    
    DataAnalystTestCase(
        id="simple_003",
        natural_language_query="What are the different species in the epitopes table?",
        query_type="simple",
        difficulty="medium",
        expected_sql_pattern="SELECT DISTINCT species FROM epitopes",
        expected_tables=["epitopes"],
        expected_columns=["species"],
        success_criteria=[
            "Uses DISTINCT to get unique species",
            "Queries epitopes table",
            "Returns all unique species values",
            "Excludes NULL values",
            "Provides interpretation of species diversity"
        ],
        domain_context="Understanding species diversity of epitope sources (Human, Mouse, etc.)"
    ),
]

# Join Query Test Cases
JOIN_QUERY_CASES = [
    DataAnalystTestCase(
        id="join_001",
        natural_language_query="Show me the epitope sequences along with their MHC allele information for the first 5 complexes",
        query_type="join",
        difficulty="easy",
        expected_sql_pattern="SELECT.*FROM complexes.*JOIN epitopes.*JOIN mhc_alleles.*LIMIT 5",
        expected_tables=["complexes", "epitopes", "mhc_alleles"],
        expected_columns=["sequence", "allele_name", "complex_id"],
        success_criteria=[
            "Joins complexes, epitopes, and mhc_alleles tables",
            "Uses proper foreign key relationships",
            "Selects epitope sequence and MHC allele information",
            "Limits results to 5 rows"
        ],
        domain_context="Connecting T-cell receptor complexes with their target epitopes and presenting MHC molecules"
    ),
    
    DataAnalystTestCase(
        id="join_002",
        natural_language_query="Find all TCR chains (alpha and beta) for complexes that target Human epitopes",
        query_type="join",
        difficulty="easy",
        expected_sql_pattern="SELECT.*FROM chains.*JOIN complexes.*JOIN epitopes.*WHERE.*species.*Human",
        expected_tables=["chains", "complexes", "epitopes"],
        expected_columns=["cdr3", "gene", "v_segm", "j_segm", "sequence"],
        success_criteria=[
            "Joins chains, complexes, and epitopes tables",
            "Filters for Human epitopes using WHERE clause",
            "Returns TCR chain information (CDR3, gene segments)"
        ],
        domain_context="Finding T-cell receptor sequences that recognize human-derived epitopes"
    ),
    
    DataAnalystTestCase(
        id="join_003",
        natural_language_query="Show donor information along with sample details for all samples collected from PBMC tissue",
        query_type="join",
        difficulty="medium",
        expected_sql_pattern="SELECT.*FROM donors.*JOIN samples.*WHERE.*tissue.*PBMC",
        expected_tables=["donors", "samples"],
        expected_columns=["donor_id", "species", "age", "tissue", "collection_date"],
        success_criteria=[
            "Joins donors and samples tables",
            "Filters for PBMC tissue type",
            "Returns donor demographics and sample information",
            "Uses proper foreign key relationship"
        ],
        domain_context="Analyzing peripheral blood mononuclear cell (PBMC) samples and their donor context"
    ),
]

# Aggregation Query Test Cases
AGGREGATION_CASES = [
    DataAnalystTestCase(
        id="agg_001",
        natural_language_query="What is the average epitope length by species?",
        query_type="aggregation",
        difficulty="medium",
        expected_sql_pattern="SELECT species, AVG(length) FROM epitopes GROUP BY species",
        expected_tables=["epitopes"],
        expected_columns=["species", "length"],
        success_criteria=[
            "Uses AVG() function for length calculation",
            "Groups by species",
            "Returns species and average length",
            "Handles NULL values appropriately",
            "Provides meaningful interpretation"
        ],
        domain_context="Understanding peptide length differences across species"
    ),
    
    DataAnalystTestCase(
        id="agg_002",
        natural_language_query="How many TCR complexes are there for each MHC class (MHCI vs MHCII)?",
        query_type="aggregation",
        difficulty="medium",
        expected_sql_pattern="SELECT.*class.*COUNT.*FROM complexes.*JOIN mhc_alleles.*GROUP BY.*class",
        expected_tables=["complexes", "mhc_alleles"],
        expected_columns=["class", "complex_id"],
        success_criteria=[
            "Joins complexes with mhc_alleles table",
            "Groups by MHC class",
            "Counts complexes per class",
            "Returns MHCI and MHCII counts"
        ],
        domain_context="Analyzing distribution of T-cell receptor complexes by MHC class (CD8+ vs CD4+ T-cells)"
    ),
    
    DataAnalystTestCase(
        id="agg_003",
        natural_language_query="What is the distribution of VDJdb confidence scores for TCR chains?",
        query_type="aggregation",
        difficulty="easy",
        expected_sql_pattern="SELECT vdjdb_score, COUNT(*) FROM chains GROUP BY vdjdb_score ORDER BY vdjdb_score",
        expected_tables=["chains"],
        expected_columns=["vdjdb_score"],
        success_criteria=[
            "Groups by vdjdb_score",
            "Counts occurrences of each score",
            "Orders results by score"
        ],
        domain_context="Understanding confidence scores for T-cell receptor sequence reliability"
    ),
]

# Statistical Analysis Test Cases
STATISTICAL_CASES = [
    DataAnalystTestCase(
        id="stat_001",
        natural_language_query="Calculate the correlation between epitope length and IC50 binding affinity values",
        query_type="statistical",
        difficulty="hard",
        expected_sql_pattern="SELECT.*length.*ic50.*FROM epitopes WHERE.*ic50.*NOT NULL",
        expected_tables=["epitopes"],
        expected_columns=["length", "ic50"],
        success_criteria=[
            "Selects length and ic50 columns",
            "Filters out NULL ic50 values",
            "Could calculate correlation or provide data for correlation analysis",
            "Handles missing values appropriately"
        ],
        domain_context="Analyzing relationship between peptide length and binding strength"
    ),
    
    DataAnalystTestCase(
        id="stat_002",
        natural_language_query="Find epitopes with unusually high or low binding affinities (outliers in IC50 values)",
        query_type="statistical",
        difficulty="hard",
        expected_sql_pattern="SELECT.*FROM epitopes WHERE ic50.*AND.*",
        expected_tables=["epitopes"],
        expected_columns=["epitope_id", "sequence", "ic50", "length"],
        success_criteria=[
            "Identifies outliers in IC50 values",
            "Uses statistical thresholds (e.g., percentiles, standard deviations)",
            "Returns epitope details for outliers",
            "Excludes NULL values from analysis"
        ],
        domain_context="Identifying epitopes with exceptional binding characteristics"
    ),
]

# Temporal Analysis Test Cases
TEMPORAL_CASES = [
    DataAnalystTestCase(
        id="temporal_001",
        natural_language_query="Show the number of assays conducted by month in 2023",
        query_type="temporal",
        difficulty="medium",
        expected_sql_pattern="SELECT.*strftime.*date_run.*COUNT.*FROM assays WHERE.*2023.*GROUP BY",
        expected_tables=["assays"],
        expected_columns=["date_run"],
        success_criteria=[
            "Extracts month/year from date_run",
            "Filters for 2023 data",
            "Groups by month",
            "Counts assays per month",
            "Handles date formatting properly"
        ],
        domain_context="Analyzing experimental activity over time"
    ),
    
    DataAnalystTestCase(
        id="temporal_002",
        natural_language_query="Which laboratory has been most active in the last 6 months?",
        query_type="temporal",
        difficulty="medium",
        expected_sql_pattern="SELECT lab.*COUNT.*FROM assays WHERE date_run.*GROUP BY lab ORDER BY COUNT.*DESC",
        expected_tables=["assays"],
        expected_columns=["lab", "date_run"],
        success_criteria=[
            "Filters for recent 6-month period",
            "Groups by lab",
            "Counts assays per lab",
            "Orders by count descending"
        ],
        domain_context="Identifying most productive research laboratories"
    ),
]

# Immunological Domain-Specific Test Cases
IMMUNOLOGICAL_CASES = [
    DataAnalystTestCase(
        id="immuno_001",
        natural_language_query="Find all TCR alpha-beta pairs that recognize the same epitope",
        query_type="immunological",
        difficulty="hard",
        expected_sql_pattern="SELECT.*FROM chains.*JOIN complexes.*WHERE gene.*TRA.*TRB.*GROUP BY complex_id",
        expected_tables=["chains", "complexes"],
        expected_columns=["complex_id", "gene", "cdr3"],
        success_criteria=[
            "Joins chains with complexes",
            "Filters for both TRA (alpha) and TRB (beta) chains",
            "Groups by complex_id to get pairs",
            "Returns CDR3 sequences for both chains"
        ],
        domain_context="Understanding paired alpha-beta T-cell receptor recognition"
    ),
    
    DataAnalystTestCase(
        id="immuno_002",
        natural_language_query="What are the most common V-segment and J-segment combinations in human TCR beta chains?",
        query_type="immunological",
        difficulty="medium",
        expected_sql_pattern="SELECT v_segm, j_segm, COUNT(*) FROM chains WHERE gene.*TRB.*species.*Human.*GROUP BY v_segm, j_segm ORDER BY COUNT.*DESC",
        expected_tables=["chains"],
        expected_columns=["v_segm", "j_segm", "gene", "species"],
        success_criteria=[
            "Filters for TRB (beta chains) and Human species",
            "Groups by V-segment and J-segment combinations",
            "Counts occurrences",
            "Orders by frequency"
        ],
        domain_context="Analyzing T-cell receptor gene segment usage patterns in humans"
    ),
    
    DataAnalystTestCase(
        id="immuno_003",
        natural_language_query="Find epitopes that are presented by multiple different MHC alleles (promiscuous epitopes)",
        query_type="immunological",
        difficulty="hard",
        expected_sql_pattern="SELECT.*epitope_id.*COUNT.*DISTINCT.*mhc.*FROM complexes.*GROUP BY epitope_id HAVING COUNT.*> 1",
        expected_tables=["complexes", "epitopes"],
        expected_columns=["epitope_id", "mhc_a_id", "mhc_b_id"],
        success_criteria=[
            "Groups by epitope_id",
            "Counts distinct MHC alleles per epitope",
            "Uses HAVING clause to filter for multiple MHC presentations",
            "Identifies promiscuous epitopes"
        ],
        domain_context="Finding epitopes that can be presented by multiple MHC molecules (important for vaccine design)"
    ),
    
    DataAnalystTestCase(
        id="immuno_004",
        natural_language_query="Analyze the diversity of CDR3 sequences by calculating the number of unique CDR3s per V-J combination",
        query_type="immunological",
        difficulty="medium",
        expected_sql_pattern="SELECT v_segm, j_segm, COUNT(DISTINCT cdr3) FROM chains GROUP BY v_segm, j_segm",
        expected_tables=["chains"],
        expected_columns=["v_segm", "j_segm", "cdr3"],
        success_criteria=[
            "Groups by V-segment and J-segment combinations",
            "Counts distinct CDR3 sequences",
            "Returns diversity metrics"
        ],
        domain_context="Understanding T-cell receptor diversity within gene segment contexts"
    ),
]

# Complex Multi-table Analysis Cases
COMPLEX_ANALYSIS_CASES = [
    DataAnalystTestCase(
        id="complex_001",
        natural_language_query="Create a comprehensive summary of TCR complexes: include epitope information, MHC alleles, donor demographics, and experimental details",
        query_type="join",
        difficulty="hard",
        expected_sql_pattern="SELECT.*FROM complexes.*JOIN epitopes.*JOIN mhc_alleles.*JOIN samples.*JOIN donors",
        expected_tables=["complexes", "epitopes", "mhc_alleles", "samples", "donors"],
        expected_columns=["sequence", "allele_name", "species", "age", "tissue"],
        success_criteria=[
            "Joins multiple tables (complexes, epitopes, mhc_alleles, samples, donors)",
            "Includes epitope sequences",
            "Shows MHC allele information",
            "Provides donor demographics",
            "Creates comprehensive view"
        ],
        domain_context="Integrating all aspects of T-cell receptor data for comprehensive analysis"
    ),
    
    DataAnalystTestCase(
        id="complex_002",
        natural_language_query="Which research laboratories have contributed the most high-confidence TCR data (VDJdb score >= 2)?",
        query_type="aggregation",
        difficulty="hard",
        expected_sql_pattern="SELECT.*lab.*COUNT.*FROM assays.*JOIN complexes.*JOIN chains WHERE vdjdb_score.*>= 2.*GROUP BY lab",
        expected_tables=["assays", "complexes", "chains"],
        expected_columns=["lab", "vdjdb_score"],
        success_criteria=[
            "Joins assays, complexes, and chains tables",
            "Filters for high-confidence data (vdjdb_score >= 2)",
            "Groups by laboratory",
            "Counts contributions per lab",
            "Orders by contribution volume"
        ],
        domain_context="Identifying laboratories producing high-quality T-cell receptor data"
    ),
]

# Compile all test cases
ALL_DATA_ANALYST_TEST_CASES = (
    SCHEMA_EXPLORATION_CASES +
    SIMPLE_QUERY_CASES +
    JOIN_QUERY_CASES +
    AGGREGATION_CASES +
    STATISTICAL_CASES +
    TEMPORAL_CASES +
    IMMUNOLOGICAL_CASES +
    COMPLEX_ANALYSIS_CASES
)

# Advanced Statistical Analysis Cases
ADVANCED_STATISTICAL_CASES = [
    DataAnalystTestCase(
        id="adv_stat_001",
        natural_language_query="Calculate the median CDR3 length for each gene segment family (TRAV, TRBV, etc.) and identify segments with extreme length distributions",
        query_type="statistical",
        difficulty="hard",
        expected_sql_pattern="SELECT.*v_segm.*LENGTH.*cdr3.*FROM chains WHERE.*GROUP BY.*ORDER BY",
        expected_tables=["chains"],
        expected_columns=["v_segm", "cdr3"],
        success_criteria=[
            "Calculates CDR3 length for each chain",
            "Groups by V-segment families",
            "Computes median or percentile statistics",
            "Identifies outliers in length distribution",
            "Handles NULL values appropriately"
        ],
        domain_context="CDR3 length variation is crucial for understanding T-cell receptor diversity and binding specificity"
    ),
    
    DataAnalystTestCase(
        id="adv_stat_002",
        natural_language_query="Perform a statistical analysis of epitope binding affinity (IC50) distributions across different source proteins",
        query_type="statistical",
        difficulty="hard",
        expected_sql_pattern="SELECT source_protein.*AVG.*STDDEV.*MIN.*MAX.*ic50.*FROM epitopes WHERE ic50 IS NOT NULL GROUP BY source_protein",
        expected_tables=["epitopes"],
        expected_columns=["source_protein", "ic50"],
        success_criteria=[
            "Groups by source protein",
            "Calculates descriptive statistics (mean, std dev, min, max)",
            "Filters out NULL IC50 values",
            "Provides statistical interpretation",
            "Identifies proteins with unusual binding patterns"
        ],
        domain_context="Understanding binding affinity patterns across different pathogen proteins for drug target identification"
    ),
]

# Data Quality and Validation Cases
DATA_QUALITY_CASES = [
    DataAnalystTestCase(
        id="quality_001",
        natural_language_query="Identify potential data quality issues: find complexes with missing chain information or orphaned records",
        query_type="join",
        difficulty="hard",
        expected_sql_pattern="SELECT.*complexes.*LEFT JOIN chains.*WHERE.*chain_id IS NULL",
        expected_tables=["complexes", "chains"],
        expected_columns=["complex_id", "chain_id"],
        success_criteria=[
            "Uses LEFT JOIN to find orphaned records",
            "Identifies complexes without corresponding chains",
            "Reports data completeness metrics",
            "Suggests data quality improvements"
        ],
        domain_context="Ensuring data integrity is critical for reliable immunological research conclusions"
    ),
    
    DataAnalystTestCase(
        id="quality_002",
        natural_language_query="Find duplicate epitope sequences and analyze if they have conflicting IC50 values or species annotations",
        query_type="aggregation",
        difficulty="medium",
        expected_sql_pattern="SELECT sequence.*COUNT.*GROUP BY sequence HAVING COUNT.*> 1",
        expected_tables=["epitopes"],
        expected_columns=["sequence", "ic50", "species"],
        success_criteria=[
            "Groups by epitope sequence",
            "Identifies duplicates using HAVING clause",
            "Compares IC50 values for same sequences"
        ],
        domain_context="Duplicate epitopes with conflicting annotations can indicate data integration issues"
    ),
]

# Cross-Species Comparative Analysis Cases
CROSS_SPECIES_CASES = [
    DataAnalystTestCase(
        id="species_001",
        natural_language_query="Compare TCR gene segment usage patterns between human and mouse: which V-J combinations are conserved across species?",
        query_type="immunological",
        difficulty="hard",
        expected_sql_pattern="SELECT.*v_segm.*j_segm.*species.*COUNT.*FROM chains.*JOIN complexes.*JOIN epitopes.*GROUP BY.*species.*v_segm.*j_segm",
        expected_tables=["chains", "complexes", "epitopes"],
        expected_columns=["v_segm", "j_segm", "species"],
        success_criteria=[
            "Joins chains through complexes to epitopes for species info",
            "Groups by species, V-segment, and J-segment",
            "Compares usage patterns between human and mouse",
            "Identifies conserved combinations",
            "Provides evolutionary insights"
        ],
        domain_context="Comparing TCR repertoires across species reveals evolutionary conservation and species-specific adaptations"
    ),
    
    DataAnalystTestCase(
        id="species_002",
        natural_language_query="Analyze epitope length preferences across species: do different species have distinct epitope length distributions?",
        query_type="statistical",
        difficulty="easy",
        expected_sql_pattern="SELECT species.*length.*COUNT.*AVG.*FROM epitopes GROUP BY species.*length ORDER BY species.*length",
        expected_tables=["epitopes"],
        expected_columns=["species", "length"],
        success_criteria=[
            "Groups by species and length",
            "Calculates length distributions per species",
            "Compares average lengths across species"
        ],
        domain_context="Species-specific epitope length preferences reflect different MHC molecule structures and immune system evolution"
    ),
]

# Publication and Research Trend Analysis Cases
PUBLICATION_ANALYSIS_CASES = [
    DataAnalystTestCase(
        id="pub_001",
        natural_language_query="Analyze research trends: which years had the highest number of publications and what were the dominant research focuses?",
        query_type="temporal",
        difficulty="easy",
        expected_sql_pattern="SELECT.*year.*COUNT.*FROM publications GROUP BY.*year ORDER BY.*year",
        expected_tables=["publications"],
        expected_columns=["year", "title", "journal"],
        success_criteria=[
            "Extracts year from publication data",
            "Groups by year",
            "Counts publications per year"
        ],
        domain_context="Understanding publication trends reveals the evolution of T-cell receptor research field"
    ),
    
    DataAnalystTestCase(
        id="pub_002",
        natural_language_query="Which journals have published the most high-impact TCR studies (based on number of epitopes contributed to the database)?",
        query_type="join",
        difficulty="hard",
        expected_sql_pattern="SELECT.*journal.*COUNT.*FROM publications.*JOIN.*epitopes.*GROUP BY journal ORDER BY COUNT.*DESC",
        expected_tables=["publications", "epitopes"],
        expected_columns=["journal", "epitope_id"],
        success_criteria=[
            "Joins publications with epitopes through appropriate relationships",
            "Groups by journal",
            "Counts epitopes per journal",
            "Orders by contribution volume",
            "Identifies high-impact journals"
        ],
        domain_context="Journal analysis reveals publication venues that drive T-cell receptor research forward"
    ),
]

# Advanced Immunological Analysis Cases
ADVANCED_IMMUNOLOGICAL_CASES = [
    DataAnalystTestCase(
        id="adv_immuno_001",
        natural_language_query="Identify potential cross-reactive TCRs: find TCR chains that appear in complexes targeting epitopes from different source proteins",
        query_type="immunological",
        difficulty="hard",
        expected_sql_pattern="SELECT.*cdr3.*COUNT.*DISTINCT.*source_protein.*FROM chains.*JOIN complexes.*JOIN epitopes.*GROUP BY cdr3 HAVING COUNT.*> 1",
        expected_tables=["chains", "complexes", "epitopes"],
        expected_columns=["cdr3", "source_protein", "complex_id"],
        success_criteria=[
            "Joins chains through complexes to epitopes",
            "Groups by CDR3 sequence",
            "Counts distinct source proteins per CDR3",
            "Identifies cross-reactive TCRs",
            "Provides immunological interpretation"
        ],
        domain_context="Cross-reactive TCRs can recognize multiple pathogens, which is important for vaccine design and autoimmunity"
    ),
]

# Compile all test cases including new ones
ALL_DATA_ANALYST_TEST_CASES = (
    SCHEMA_EXPLORATION_CASES +
    SIMPLE_QUERY_CASES +
    JOIN_QUERY_CASES +
    AGGREGATION_CASES +
    STATISTICAL_CASES +
    TEMPORAL_CASES +
    IMMUNOLOGICAL_CASES +
    COMPLEX_ANALYSIS_CASES +
    ADVANCED_STATISTICAL_CASES +
    DATA_QUALITY_CASES +
    CROSS_SPECIES_CASES +
    PUBLICATION_ANALYSIS_CASES +
    ADVANCED_IMMUNOLOGICAL_CASES
)


def get_test_case_summary():
    """Get summary statistics of the test dataset."""
    total_cases = len(ALL_DATA_ANALYST_TEST_CASES)
    
    # Count by difficulty
    difficulty_counts = {}
    query_type_counts = {}
    
    for case in ALL_DATA_ANALYST_TEST_CASES:
        difficulty_counts[case.difficulty] = difficulty_counts.get(case.difficulty, 0) + 1
        query_type_counts[case.query_type] = query_type_counts.get(case.query_type, 0) + 1
    
    return {
        "total_test_cases": total_cases,
        "difficulty_distribution": difficulty_counts,
        "query_type_distribution": query_type_counts,
        "test_case_ids": [case.id for case in ALL_DATA_ANALYST_TEST_CASES]
    }


def get_test_case_by_id(test_id: str) -> DataAnalystTestCase:
    """Get a specific test case by ID."""
    for case in ALL_DATA_ANALYST_TEST_CASES:
        if case.id == test_id:
            return case
    raise ValueError(f"Test case with ID '{test_id}' not found")


def get_test_cases_by_difficulty(difficulty: str) -> List[DataAnalystTestCase]:
    """Get all test cases of a specific difficulty level."""
    return [case for case in ALL_DATA_ANALYST_TEST_CASES if case.difficulty == difficulty]


def get_test_cases_by_type(query_type: str) -> List[DataAnalystTestCase]:
    """Get all test cases of a specific query type."""
    return [case for case in ALL_DATA_ANALYST_TEST_CASES if case.query_type == query_type]


def get_dataset_summary() -> Dict[str, Any]:
    """Get comprehensive dataset summary with statistics."""
    summary = get_test_case_summary()
    
    # Add more detailed analysis
    tables_coverage = set()
    columns_coverage = set()
    
    for case in ALL_DATA_ANALYST_TEST_CASES:
        tables_coverage.update(case.expected_tables)
        columns_coverage.update(case.expected_columns)
    
    summary.update({
        "tables_covered": sorted(list(tables_coverage)),
        "columns_covered": sorted(list(columns_coverage)),
        "schema_coverage": {
            "total_tables": 8,  # From VDJdb schema
            "covered_tables": len(tables_coverage),
            "coverage_percentage": len(tables_coverage) / 8 * 100
        }
    })
    
    return summary 