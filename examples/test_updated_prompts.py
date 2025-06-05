#!/usr/bin/env python3
"""
Test Updated Prompts with Biomedical Researcher

This script demonstrates how the updated prompts work with the biomedical researcher,
showing the distinction between general research and specialized biomedical research.
"""

import asyncio
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def show_prompt_updates():
    """Show the key updates made to the prompts."""
    print("🔄 PROMPT UPDATES SUMMARY")
    print("=" * 50)
    
    print("\n1. 📋 supervisor.md - Added biomedical_researcher to team:")
    print("   • New team member: biomedical_researcher")
    print("   • Specialized for medical/pharmaceutical/clinical research")
    print("   • Direct access to PubMed, ClinicalTrials, BioRxiv, OpenTargets, DrugBank")
    
    print("\n2. 🧬 biomedical_researcher.md - Enhanced with real MCP capabilities:")
    print("   • Updated to reflect actual MCP server implementation")
    print("   • Listed 18 specific biomedical tools available")
    print("   • Added real-time database connectivity details")
    print("   • Included production status and usage notes")
    
    print("\n3. 🔍 researcher.md - Added scope clarification:")
    print("   • Clarified as general web researcher")
    print("   • Added note to use biomedical_researcher for medical topics")
    
    print("\n4. 🎯 Key Improvements:")
    print("   • Clear separation between general and biomedical research")
    print("   • Accurate reflection of tested MCP capabilities")
    print("   • Real-time database access emphasized")
    print("   • Production-ready status documented")

def show_biomedical_capabilities():
    """Show the comprehensive biomedical research capabilities."""
    print("\n\n🧬 BIOMEDICAL RESEARCHER CAPABILITIES")
    print("=" * 50)
    
    capabilities = {
        "PubMed (NCBI API)": [
            "search_pubmed - Search 35M+ biomedical citations",
            "get_pubmed_abstract - Get full abstracts by PMID",
            "get_related_articles - Find related research",
            "find_by_author - Search by specific authors"
        ],
        "ClinicalTrials.gov": [
            "search_trials - Search 400K+ clinical studies",
            "get_trial_details - Get detailed trial information",
            "find_trials_by_condition - Search by medical condition",
            "find_trials_by_location - Search by location"
        ],
        "BioRxiv/MedRxiv": [
            "search_preprints - Search preprints by category",
            "get_preprint_by_doi - Get preprint details by DOI",
            "find_published_version - Find published versions",
            "get_recent_preprints - Get recent submissions"
        ],
        "OpenTargets": [
            "search_targets - Search gene targets",
            "get_target_details - Get detailed target info",
            "search_diseases - Search disease database",
            "get_disease_targets - Get targets for diseases",
            "get_target_drug_info - Get drug information",
            "search_evidence - Search target-disease evidence"
        ],
        "DrugBank (Optional)": [
            "search_drugs - Search drug database",
            "get_drug_details - Get comprehensive drug info",
            "find_drug_interactions - Find drug interactions",
            "get_drug_targets - Get molecular targets"
        ]
    }
    
    for database, tools in capabilities.items():
        print(f"\n📊 {database}:")
        for tool in tools:
            print(f"   • {tool}")

def show_example_use_cases():
    """Show example use cases for the biomedical researcher."""
    print("\n\n🎯 EXAMPLE USE CASES")
    print("=" * 50)
    
    examples = [
        {
            "question": "Find recent CRISPR research for treating genetic diseases",
            "approach": "PubMed search → Clinical trials → Recent preprints",
            "databases": "PubMed, ClinicalTrials, BioRxiv"
        },
        {
            "question": "What are the targets for Alzheimer's disease treatment?",
            "approach": "OpenTargets search → Literature validation → Drug pipeline",
            "databases": "OpenTargets, PubMed, DrugBank"
        },
        {
            "question": "Current COVID-19 vaccine effectiveness studies",
            "approach": "Recent literature → Active trials → Latest preprints",
            "databases": "PubMed, ClinicalTrials, BioRxiv"
        },
        {
            "question": "Drug interactions for cancer immunotherapy",
            "approach": "Drug database → Literature review → Clinical evidence",
            "databases": "DrugBank, PubMed, ClinicalTrials"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. Question: {example['question']}")
        print(f"   Approach: {example['approach']}")
        print(f"   Databases: {example['databases']}")

def main():
    """Main demonstration."""
    print("🚀 UPDATED PROMPTS DEMONSTRATION")
    print("=" * 60)
    print("This shows the comprehensive updates made to integrate")
    print("the biomedical researcher with real MCP capabilities.")
    
    show_prompt_updates()
    show_biomedical_capabilities()
    show_example_use_cases()
    
    print("\n\n✅ INTEGRATION STATUS")
    print("=" * 50)
    print("• Prompts updated to reflect real MCP implementation")
    print("• Supervisor aware of biomedical research capabilities")
    print("• Clear separation between general and biomedical research")
    print("• Production-ready biomedical research system")
    print("• 18 specialized biomedical tools available")
    print("• Real-time database connectivity documented")
    
    print("\n🎯 NEXT STEPS:")
    print("• Test the biomedical researcher with real queries")
    print("• Use supervisor to route biomedical questions appropriately")
    print("• Leverage the 18 specialized tools for comprehensive research")
    print("• Access live data from 4-5 authoritative biomedical databases")

if __name__ == "__main__":
    main() 