"""
TCR Analysis Tools - Specialized functions for T-cell receptor and immunogenomics analysis.

This module provides tools specifically designed for analyzing TCR data from VDJdb
and other immune repertoire databases.
"""

from langchain_core.tools import tool
import pandas as pd
import numpy as np
from typing import Optional, List, Dict, Any, Tuple
import logging
import sqlite3
import re
from collections import Counter
import math

from src.tools.database import get_database_manager
from src.config.vdjdb import get_vdjdb_settings

logger = logging.getLogger(__name__)


@tool
def get_vdjdb_schema() -> str:
    """Get the VDJdb database schema optimized for TCR analysis.
    
    Returns:
        A string containing the VDJdb schema description with TCR-specific context.
    """
    try:
        logger.info("🧬 Fetching VDJdb schema for TCR analysis...")
        
        # Get VDJdb settings and database manager
        vdjdb_settings = get_vdjdb_settings()
        db_manager = get_database_manager()
        
        # Get base schema
        base_schema = db_manager.load_schema_description()
        
        # Add TCR-specific context and guidance
        tcr_context = """
        
=== TCR-SPECIFIC ANALYSIS CONTEXT ===

Key TCR Analysis Patterns:
- Clonotype: Unique combination of CDR3 sequence + V gene + J gene
- Repertoire Diversity: Shannon entropy, Simpson index, clonality metrics
- Epitope Specificity: TCR-epitope binding associations
- HLA Restriction: MHC allele compatibility filtering
- Clinical Correlation: Link TCR signatures to treatment outcomes

Common Query Patterns:
1. Clonotype Frequency: GROUP BY cdr3_sequence, v_gene, j_gene
2. Diversity Metrics: COUNT(DISTINCT clonotype_id), entropy calculations
3. Epitope Analysis: JOIN with epitope and antigen tables
4. Clinical Comparison: Compare repertoires between patient cohorts
5. Temporal Analysis: Track clonotype changes over treatment time

TCR Data Quality Filters:
- CDR3 length: 8-25 amino acids (LENGTH(cdr3_sequence) BETWEEN 8 AND 25)
- Confidence scores: Use high-confidence entries only
- Remove ambiguous sequences: Filter out sequences with 'X' or unknown residues
        """
        
        full_schema = base_schema + tcr_context
        
        logger.info("🔘 VDJdb schema with TCR context fetched successfully")
        return full_schema
        
    except Exception as e:
        error_msg = f"Error fetching VDJdb schema: {str(e)}"
        logger.error(f"❌ {error_msg}")
        return error_msg


@tool
def calculate_tcr_diversity_metrics(query_result: str) -> str:
    """Calculate TCR repertoire diversity metrics from query results.
    
    Args:
        query_result: String representation of SQL query results containing clonotype frequencies
        
    Returns:
        String with calculated diversity metrics (Shannon diversity, Simpson index, etc.)
    """
    try:
        logger.info("🧬 Calculating TCR diversity metrics...")
        
        # Parse the query result string to extract frequency data
        lines = query_result.strip().split('\n')
        frequencies = []
        
        # Extract frequency/count columns from the result
        for line in lines[2:]:  # Skip header lines
            if line.strip():
                parts = line.split()
                if parts:
                    try:
                        # Try to find a numeric frequency value
                        for part in parts:
                            if part.replace('.', '').isdigit():
                                frequencies.append(float(part))
                                break
                    except ValueError:
                        continue
        
        if not frequencies:
            return "No frequency data found in query results. Ensure your query includes clonotype counts or frequencies."
        
        # Convert to relative frequencies if they appear to be counts
        total = sum(frequencies)
        if total > 1.0:  # Likely counts, not frequencies
            frequencies = [f/total for f in frequencies]
        
        # Calculate diversity metrics
        results = {
            'total_clonotypes': len(frequencies),
            'shannon_diversity': calculate_shannon_diversity(frequencies),
            'simpson_index': calculate_simpson_index(frequencies),
            'inverse_simpson': 1 / calculate_simpson_index(frequencies) if calculate_simpson_index(frequencies) > 0 else float('inf'),
            'evenness': calculate_evenness(frequencies),
            'clonality': 1 - calculate_shannon_diversity(frequencies) / math.log(len(frequencies)) if len(frequencies) > 1 else 0
        }
        
        # Format results
        result_str = "TCR Repertoire Diversity Metrics:\n\n"
        result_str += f"Total Clonotypes: {results['total_clonotypes']}\n"
        result_str += f"Shannon Diversity: {results['shannon_diversity']:.4f}\n"
        result_str += f"Simpson Index: {results['simpson_index']:.4f}\n"
        result_str += f"Inverse Simpson: {results['inverse_simpson']:.4f}\n"
        result_str += f"Evenness: {results['evenness']:.4f}\n"
        result_str += f"Clonality: {results['clonality']:.4f}\n\n"
        
        # Add interpretation
        result_str += "Interpretation:\n"
        if results['shannon_diversity'] > 4:
            result_str += "- High repertoire diversity (Shannon > 4)\n"
        elif results['shannon_diversity'] > 2:
            result_str += "- Moderate repertoire diversity (Shannon 2-4)\n"
        else:
            result_str += "- Low repertoire diversity (Shannon < 2)\n"
            
        if results['clonality'] > 0.5:
            result_str += "- High clonal expansion (Clonality > 0.5)\n"
        else:
            result_str += "- Polyclonal repertoire (Clonality < 0.5)\n"
        
        logger.info(f"🔘 TCR diversity metrics calculated: Shannon={results['shannon_diversity']:.4f}")
        return result_str
        
    except Exception as e:
        error_msg = f"Error calculating TCR diversity metrics: {str(e)}"
        logger.error(f"❌ {error_msg}")
        return error_msg


@tool
def analyze_cdr3_motifs(cdr3_sequences: str) -> str:
    """Analyze CDR3 sequence motifs and patterns.
    
    Args:
        cdr3_sequences: String containing CDR3 sequences (one per line or comma-separated)
        
    Returns:
        String with motif analysis results including common patterns and amino acid usage
    """
    try:
        logger.info("🧬 Analyzing CDR3 motifs...")
        
        # Parse CDR3 sequences
        sequences = []
        if ',' in cdr3_sequences:
            sequences = [seq.strip() for seq in cdr3_sequences.split(',')]
        else:
            sequences = [line.strip() for line in cdr3_sequences.split('\n') if line.strip()]
        
        if not sequences:
            return "No CDR3 sequences found in input."
        
        # Clean sequences (remove non-amino acid characters)
        clean_sequences = []
        valid_aa = set('ACDEFGHIKLMNPQRSTVWY')
        for seq in sequences:
            clean_seq = ''.join(c for c in seq.upper() if c in valid_aa)
            if clean_seq:
                clean_sequences.append(clean_seq)
        
        if not clean_sequences:
            return "No valid CDR3 sequences found after cleaning."
        
        # Analyze sequence properties
        lengths = [len(seq) for seq in clean_sequences]
        aa_counts = Counter()
        
        for seq in clean_sequences:
            aa_counts.update(seq)
        
        # Find common motifs (3-mers and 4-mers)
        motifs_3 = Counter()
        motifs_4 = Counter()
        
        for seq in clean_sequences:
            for i in range(len(seq) - 2):
                motifs_3[seq[i:i+3]] += 1
            for i in range(len(seq) - 3):
                motifs_4[seq[i:i+4]] += 1
        
        # Format results
        result_str = f"CDR3 Motif Analysis Results ({len(clean_sequences)} sequences):\n\n"
        
        # Length distribution
        result_str += f"Length Statistics:\n"
        result_str += f"- Average length: {np.mean(lengths):.1f} amino acids\n"
        result_str += f"- Length range: {min(lengths)}-{max(lengths)} amino acids\n"
        result_str += f"- Most common length: {Counter(lengths).most_common(1)[0][0]} amino acids\n\n"
        
        # Amino acid usage
        total_aa = sum(aa_counts.values())
        result_str += "Top Amino Acid Usage:\n"
        for aa, count in aa_counts.most_common(10):
            frequency = count / total_aa * 100
            result_str += f"- {aa}: {frequency:.1f}% ({count} occurrences)\n"
        result_str += "\n"
        
        # Common 3-mer motifs
        result_str += "Most Common 3-mer Motifs:\n"
        for motif, count in motifs_3.most_common(10):
            frequency = count / len(clean_sequences) * 100
            result_str += f"- {motif}: {frequency:.1f}% of sequences ({count} occurrences)\n"
        result_str += "\n"
        
        # Common 4-mer motifs (if enough sequences)
        if len(clean_sequences) > 10:
            result_str += "Most Common 4-mer Motifs:\n"
            for motif, count in motifs_4.most_common(8):
                frequency = count / len(clean_sequences) * 100
                result_str += f"- {motif}: {frequency:.1f}% of sequences ({count} occurrences)\n"
        
        logger.info(f"🔘 CDR3 motif analysis completed for {len(clean_sequences)} sequences")
        return result_str
        
    except Exception as e:
        error_msg = f"Error analyzing CDR3 motifs: {str(e)}"
        logger.error(f"❌ {error_msg}")
        return error_msg


@tool
def compare_tcr_repertoires(repertoire1_data: str, repertoire2_data: str, group1_name: str = "Group 1", group2_name: str = "Group 2") -> str:
    """Compare two TCR repertoires and calculate overlap and diversity differences.
    
    Args:
        repertoire1_data: Query results for first repertoire (clonotype frequencies)
        repertoire2_data: Query results for second repertoire (clonotype frequencies)
        group1_name: Name for first group (e.g., "Responders")
        group2_name: Name for second group (e.g., "Non-responders")
        
    Returns:
        String with repertoire comparison results including overlap analysis
    """
    try:
        logger.info(f"🧬 Comparing TCR repertoires: {group1_name} vs {group2_name}...")
        
        def parse_repertoire_data(data: str) -> Dict[str, float]:
            """Parse repertoire data from query results."""
            clonotypes = {}
            lines = data.strip().split('\n')
            
            for line in lines[2:]:  # Skip headers
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 2:
                        try:
                            clonotype = parts[0]  # Assume first column is clonotype ID
                            frequency = float(parts[-1])  # Assume last column is frequency
                            clonotypes[clonotype] = frequency
                        except (ValueError, IndexError):
                            continue
            return clonotypes
        
        rep1 = parse_repertoire_data(repertoire1_data)
        rep2 = parse_repertoire_data(repertoire2_data)
        
        if not rep1 or not rep2:
            return "Error: Could not parse clonotype data from one or both repertoires."
        
        # Calculate overlap
        common_clonotypes = set(rep1.keys()) & set(rep2.keys())
        unique_to_rep1 = set(rep1.keys()) - set(rep2.keys())
        unique_to_rep2 = set(rep2.keys()) - set(rep1.keys())
        
        total_unique_clonotypes = len(set(rep1.keys()) | set(rep2.keys()))
        
        # Calculate diversity metrics for each repertoire
        div1 = calculate_diversity_from_frequencies(list(rep1.values()))
        div2 = calculate_diversity_from_frequencies(list(rep2.values()))
        
        # Format results
        result_str = f"TCR Repertoire Comparison: {group1_name} vs {group2_name}\n\n"
        
        result_str += "Repertoire Sizes:\n"
        result_str += f"- {group1_name}: {len(rep1)} unique clonotypes\n"
        result_str += f"- {group2_name}: {len(rep2)} unique clonotypes\n"
        result_str += f"- Total unique across both: {total_unique_clonotypes}\n\n"
        
        result_str += "Clonotype Overlap:\n"
        result_str += f"- Shared clonotypes: {len(common_clonotypes)} ({len(common_clonotypes)/total_unique_clonotypes*100:.1f}% of total)\n"
        result_str += f"- Unique to {group1_name}: {len(unique_to_rep1)} ({len(unique_to_rep1)/len(rep1)*100:.1f}%)\n"
        result_str += f"- Unique to {group2_name}: {len(unique_to_rep2)} ({len(unique_to_rep2)/len(rep2)*100:.1f}%)\n\n"
        
        result_str += "Diversity Comparison:\n"
        result_str += f"- {group1_name} Shannon Diversity: {div1['shannon']:.4f}\n"
        result_str += f"- {group2_name} Shannon Diversity: {div2['shannon']:.4f}\n"
        result_str += f"- Diversity Difference: {abs(div1['shannon'] - div2['shannon']):.4f}\n\n"
        
        result_str += f"- {group1_name} Simpson Index: {div1['simpson']:.4f}\n"
        result_str += f"- {group2_name} Simpson Index: {div2['simpson']:.4f}\n\n"
        
        # Biological interpretation
        result_str += "Biological Interpretation:\n"
        overlap_percent = len(common_clonotypes) / total_unique_clonotypes * 100
        
        if overlap_percent > 30:
            result_str += "- High repertoire similarity (>30% overlap) - may indicate shared immune responses\n"
        elif overlap_percent > 10:
            result_str += "- Moderate repertoire similarity (10-30% overlap) - some shared specificities\n"
        else:
            result_str += "- Low repertoire similarity (<10% overlap) - distinct immune signatures\n"
        
        if abs(div1['shannon'] - div2['shannon']) > 1.0:
            result_str += "- Significant diversity difference - one group shows more clonal expansion\n"
        else:
            result_str += "- Similar diversity levels between groups\n"
        
        logger.info(f"🔘 Repertoire comparison completed: {overlap_percent:.1f}% overlap")
        return result_str
        
    except Exception as e:
        error_msg = f"Error comparing TCR repertoires: {str(e)}"
        logger.error(f"❌ {error_msg}")
        return error_msg


# Helper functions for diversity calculations
def calculate_shannon_diversity(frequencies: List[float]) -> float:
    """Calculate Shannon diversity index."""
    total = sum(frequencies)
    if total == 0:
        return 0
    
    normalized_freqs = [f/total for f in frequencies if f > 0]
    return -sum(f * math.log(f) for f in normalized_freqs)


def calculate_simpson_index(frequencies: List[float]) -> float:
    """Calculate Simpson diversity index."""
    total = sum(frequencies)
    if total == 0:
        return 0
    
    normalized_freqs = [f/total for f in frequencies]
    return sum(f**2 for f in normalized_freqs)


def calculate_evenness(frequencies: List[float]) -> float:
    """Calculate Pielou's evenness index."""
    shannon = calculate_shannon_diversity(frequencies)
    n = len(frequencies)
    if n <= 1:
        return 0
    return shannon / math.log(n)


def calculate_diversity_from_frequencies(frequencies: List[float]) -> Dict[str, float]:
    """Calculate multiple diversity metrics from frequencies."""
    return {
        'shannon': calculate_shannon_diversity(frequencies),
        'simpson': calculate_simpson_index(frequencies),
        'evenness': calculate_evenness(frequencies)
    } 