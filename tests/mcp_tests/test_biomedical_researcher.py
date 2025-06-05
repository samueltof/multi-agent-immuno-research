#!/usr/bin/env python3
"""
Biomedical Researcher System Testing Interface

This script provides an interactive way to test the biomedical researcher with
curated example questions that exercise different MCP servers and capabilities.
"""

import asyncio
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.agents.biomedical_researcher import biomedical_researcher_node

# Example questions organized by research type and complexity
EXAMPLE_QUESTIONS = {
    "Literature Search (PubMed)": [
        "Find recent research papers about CRISPR gene editing in cancer treatment from 2023-2024",
        "What are the latest findings on COVID-19 long-term effects on the cardiovascular system?",
        "Search for papers by Dr. Jennifer Doudna about CRISPR applications in the last 5 years",
        "Find systematic reviews about the efficacy of mRNA vaccines",
        "What recent research exists on Alzheimer's disease biomarkers?"
    ],
    
    "Clinical Trials Research": [
        "Find ongoing clinical trials for Alzheimer's disease treatments",
        "What Phase 3 trials are currently recruiting for cancer immunotherapy?",
        "Search for completed trials studying diabetes medications in the last 2 years",
        "Find clinical trials for rare diseases currently accepting participants",
        "What trials are investigating new treatments for Parkinson's disease?"
    ],
    
    "Preprint Research (BioRxiv)": [
        "Find recent preprints about artificial intelligence in drug discovery",
        "What new research on gene therapy has been posted on BioRxiv recently?",
        "Search for preprints about machine learning applications in genomics",
        "Find recent preprints studying COVID-19 variants",
        "What new research on personalized medicine is available?"
    ],
    
    "Target-Disease Research (OpenTargets)": [
        "What are the genetic targets associated with breast cancer?",
        "Find drug targets for treating depression and anxiety",
        "What genes are associated with Type 2 diabetes susceptibility?",
        "Search for therapeutic targets in autoimmune diseases",
        "What molecular targets are being studied for neurodegenerative diseases?"
    ],
    
    "Multi-Database Complex Research": [
        "I'm researching CAR-T cell therapy for leukemia. Find recent papers, ongoing trials, and potential genetic targets",
        "Provide a comprehensive overview of current research on immunotherapy for melanoma including clinical trials and molecular targets",
        "Research the current state of gene therapy for sickle cell disease - include literature, trials, and drug development",
        "Investigate current approaches to treating Huntington's disease across all research phases",
        "Study the development of personalized cancer vaccines - from basic research to clinical applications"
    ],
    
    "Specific Medical Questions": [
        "What are the side effects and contraindications of pembrolizumab?",
        "Compare the efficacy of different COVID-19 vaccines in elderly populations",
        "What biomarkers are used to predict Alzheimer's disease progression?",
        "How effective is metformin for weight loss in non-diabetic patients?",
        "What are the latest treatment options for treatment-resistant depression?"
    ],
    
    "Drug Discovery & Development": [
        "What new drugs are in development for treating ALS?",
        "Find information about AI-driven drug discovery platforms and their recent successes",
        "Research the pipeline for new antibiotics to combat resistant bacteria",
        "What novel approaches are being developed for pain management?",
        "Investigate current research on longevity and anti-aging compounds"
    ]
}

def display_menu():
    """Display the main testing menu."""
    print("\n" + "="*80)
    print("🧬 BIOMEDICAL RESEARCHER SYSTEM TESTING")
    print("="*80)
    print("Choose a testing approach:")
    print("1. Browse example questions by category")
    print("2. Quick test with a pre-selected question")
    print("3. Ask your own research question")
    print("4. Run multiple test questions automatically")
    print("5. Exit")
    print("-"*80)

def display_categories():
    """Display available question categories."""
    print("\n📚 Example Question Categories:")
    print("-"*50)
    for i, category in enumerate(EXAMPLE_QUESTIONS.keys(), 1):
        count = len(EXAMPLE_QUESTIONS[category])
        print(f"{i}. {category} ({count} questions)")

def display_questions_in_category(category):
    """Display questions in a specific category."""
    questions = EXAMPLE_QUESTIONS[category]
    print(f"\n📋 {category} - Example Questions:")
    print("-"*60)
    for i, question in enumerate(questions, 1):
        print(f"{i}. {question}")

async def test_question(question: str, show_details: bool = True):
    """Test a specific research question."""
    if show_details:
        print(f"\n🔬 Testing Question:")
        print(f"❓ {question}")
        print("-"*80)
    
    try:
        # Create input state for biomedical researcher
        state = {
            "messages": [question]
        }
        
        print("🤖 Biomedical Researcher is working...")
        print("   (This may take 30-60 seconds for complex queries)")
        print()
        
        # Run the biomedical researcher
        result = await biomedical_researcher_node(state)
        
        if show_details:
            print("✅ Research completed!")
            print("="*80)
            print("🔍 RESEARCH RESULTS:")
            print("="*80)
        
        # Extract and display the response
        if 'biomedical_research_result' in result:
            research_result = result['biomedical_research_result']
            print(f"Summary: {research_result.summary}")
            if research_result.key_findings:
                print(f"\nKey Findings:")
                for finding in research_result.key_findings:
                    print(f"• {finding}")
            if research_result.sources:
                print(f"\nSources:")
                for source in research_result.sources[:3]:  # Show first 3 sources
                    print(f"• {source.get('title', 'N/A')}")
            if research_result.recommendations:
                print(f"\nRecommendations:")
                for rec in research_result.recommendations:
                    print(f"• {rec}")
            print(f"\nConfidence Level: {research_result.confidence_level:.2f}")
        elif 'messages' in result and result['messages']:
            last_message = result['messages'][-1]
            print(last_message)
        else:
            print("No response generated")
            
        return True
        
    except Exception as e:
        print(f"❌ Error during research: {e}")
        return False

async def run_quick_test():
    """Run a quick test with a pre-selected question."""
    quick_questions = [
        "Find recent research about CRISPR applications in treating genetic diseases",
        "What clinical trials are currently studying new Alzheimer's treatments?",
        "Search for latest preprints on AI in drug discovery",
        "What are the genetic targets for treating Type 2 diabetes?"
    ]
    
    print("\n🚀 Quick Test Questions:")
    print("-"*40)
    for i, q in enumerate(quick_questions, 1):
        print(f"{i}. {q}")
    
    try:
        choice = int(input("\nSelect a question (1-4): "))
        if 1 <= choice <= len(quick_questions):
            question = quick_questions[choice - 1]
            await test_question(question)
        else:
            print("Invalid choice")
    except ValueError:
        print("Invalid input")

async def run_multiple_tests():
    """Run multiple test questions automatically."""
    print("\n🔄 Running Multiple Test Questions")
    print("="*50)
    
    # Select one question from each category for variety
    test_questions = [
        "Find recent research papers about CRISPR gene editing in cancer treatment",
        "Find ongoing clinical trials for Alzheimer's disease treatments", 
        "Find recent preprints about artificial intelligence in drug discovery",
        "What are the genetic targets associated with breast cancer?"
    ]
    
    results = []
    for i, question in enumerate(test_questions, 1):
        print(f"\n[{i}/{len(test_questions)}] Testing: {question[:60]}...")
        success = await test_question(question, show_details=False)
        results.append(success)
        print(f"Result: {'✅ SUCCESS' if success else '❌ FAILED'}")
        
        if i < len(test_questions):
            print("Waiting 5 seconds before next test...")
            await asyncio.sleep(5)
    
    # Summary
    print(f"\n📊 Test Summary: {sum(results)}/{len(results)} tests passed")

async def interactive_testing():
    """Main interactive testing loop."""
    while True:
        display_menu()
        
        try:
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == "1":
                # Browse by category
                display_categories()
                try:
                    cat_choice = int(input("\nSelect category (1-7): "))
                    categories = list(EXAMPLE_QUESTIONS.keys())
                    if 1 <= cat_choice <= len(categories):
                        category = categories[cat_choice - 1]
                        display_questions_in_category(category)
                        
                        questions = EXAMPLE_QUESTIONS[category]
                        try:
                            q_choice = int(input(f"\nSelect question (1-{len(questions)}): "))
                            if 1 <= q_choice <= len(questions):
                                question = questions[q_choice - 1]
                                await test_question(question)
                            else:
                                print("Invalid question choice")
                        except ValueError:
                            print("Invalid input")
                    else:
                        print("Invalid category choice")
                except ValueError:
                    print("Invalid input")
            
            elif choice == "2":
                # Quick test
                await run_quick_test()
            
            elif choice == "3":
                # Custom question
                question = input("\n❓ Enter your research question: ").strip()
                if question:
                    await test_question(question)
                else:
                    print("No question entered")
            
            elif choice == "4":
                # Multiple tests
                await run_multiple_tests()
            
            elif choice == "5":
                print("\n👋 Thank you for testing the Biomedical Researcher!")
                break
            
            else:
                print("Invalid choice. Please select 1-5.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Testing interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")

def main():
    """Main entry point."""
    print("🧬 Biomedical Researcher System Testing")
    print("="*50)
    print("This interface lets you test the biomedical researcher with curated")
    print("example questions that exercise different databases and capabilities.")
    print(f"\nAvailable databases: PubMed, ClinicalTrials, BioRxiv, OpenTargets")
    print(f"Total tools available: 18 biomedical research tools")
    
    try:
        asyncio.run(interactive_testing())
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Failed to start testing interface: {e}")
        print("Make sure the biomedical researcher is properly configured.")

if __name__ == "__main__":
    main() 