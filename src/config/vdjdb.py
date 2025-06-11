"""
VDJdb Configuration - Settings for T-cell receptor database connections.

This module handles configuration for VDJdb SQLite database connections
and TCR-specific analysis parameters.
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables
env_path = find_dotenv()
load_dotenv(dotenv_path=env_path)


class VDJdbSettings(BaseSettings):
    """Configuration settings for VDJdb and TCR analysis."""
    
    # VDJdb SQLite database path
    vdjdb_sqlite_path: str = os.getenv("VDJDB_SQLITE_PATH", "data/vdjdb.db")
    
    # TCR analysis parameters
    min_cdr3_length: int = int(os.getenv("MIN_CDR3_LENGTH", "8"))
    max_cdr3_length: int = int(os.getenv("MAX_CDR3_LENGTH", "25"))
    min_confidence_score: float = float(os.getenv("MIN_CONFIDENCE_SCORE", "0.5"))
    
    # Database schema path for VDJdb
    vdjdb_schema_path: Optional[str] = os.getenv("VDJDB_SCHEMA_PATH", "data/vdjdb_schema.txt")
    
    # TCR analysis settings
    enable_motif_analysis: bool = os.getenv("ENABLE_MOTIF_ANALYSIS", "true").lower() == "true"
    enable_diversity_analysis: bool = os.getenv("ENABLE_DIVERSITY_ANALYSIS", "true").lower() == "true"
    enable_clinical_correlation: bool = os.getenv("ENABLE_CLINICAL_CORRELATION", "true").lower() == "true"
    
    # Quality filters for TCR data
    exclude_ambiguous_sequences: bool = os.getenv("EXCLUDE_AMBIGUOUS_SEQUENCES", "true").lower() == "true"
    require_v_gene: bool = os.getenv("REQUIRE_V_GENE", "true").lower() == "true"
    require_j_gene: bool = os.getenv("REQUIRE_J_GENE", "true").lower() == "true"
    
    model_config = {
        "validate_assignment": True,
        "env_file": None,  # We handle .env loading manually above
        "extra": "ignore"
    }


def get_vdjdb_settings() -> VDJdbSettings:
    """Get VDJdb configuration settings."""
    return VDJdbSettings() 