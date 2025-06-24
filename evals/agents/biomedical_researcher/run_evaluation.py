#!/usr/bin/env python3
"""
Production script to run the full biomedical researcher evaluation.
"""

import asyncio
from dotenv import load_dotenv
from .evaluation_runner import run_full_evaluation

# Load environment variables
load_dotenv()


async def main():
    """Run the complete biomedical researcher evaluation suite."""
    print("🧬 BIOMEDICAL RESEARCHER AGENT - FULL EVALUATION")
    print("=" * 60)
    print("Model: o3-mini")
    print("Test Cases: 12 cases across 8 medical domains")
    print("Metrics: Factual Correctness, Relevance, Source Quality, Confidence Alignment")
    print("=" * 60)
    
    try:
        # Run the full evaluation suite
        results = await run_full_evaluation()
        
        print("\n🎉 EVALUATION COMPLETED SUCCESSFULLY!")
        print(f"Results saved to: evals/outputs/biomedical_researcher/")
        
        # Display key insights
        summary = results["evaluation_summary"]
        print(f"\n📊 KEY RESULTS:")
        print(f"   Success Rate: {summary['success_rate']:.1%}")
        print(f"   Average Score: {summary['average_score']:.3f}")
        print(f"   Score Range: {summary['min_score']:.3f} - {summary['max_score']:.3f}")
        
        print(f"\n🏆 TOP PERFORMING DOMAINS:")
        sorted_domains = sorted(summary['scores_by_domain'].items(), key=lambda x: x[1], reverse=True)
        for domain, score in sorted_domains[:3]:
            print(f"   {domain.title()}: {score:.3f}")
        
        print(f"\n📈 METRIC PERFORMANCE:")
        for metric, score in summary['metric_averages'].items():
            print(f"   {metric.replace('_', ' ').title()}: {score:.3f}")
            
    except Exception as e:
        print(f"❌ EVALUATION FAILED: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main()) 