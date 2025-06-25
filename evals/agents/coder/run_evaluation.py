#!/usr/bin/env python3
"""
Simple script to run Coder agent evaluations.

Usage:
    python run_evaluation.py --quick      # Run quick evaluation
    python run_evaluation.py --full       # Run full evaluation
    python run_evaluation.py --case <id>  # Run specific test case
"""

import asyncio
import argparse
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from evals.agents.coder import run_quick_evaluation, run_full_evaluation, get_test_case_by_id


async def main():
    parser = argparse.ArgumentParser(description="Run Coder agent evaluations")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--quick", action="store_true", help="Run quick evaluation on subset of test cases")
    group.add_argument("--full", action="store_true", help="Run full evaluation on all test cases")
    group.add_argument("--case", type=str, help="Run evaluation on specific test case ID")
    
    parser.add_argument("--output-dir", type=str, default="evals/outputs/coder", 
                       help="Output directory for results")
    
    args = parser.parse_args()
    
    try:
        if args.quick:
            print("🚀 Running quick coder agent evaluation...")
            results = await run_quick_evaluation(output_dir=args.output_dir)
            
        elif args.full:
            print("🚀 Running full coder agent evaluation...")
            results = await run_full_evaluation(output_dir=args.output_dir)
            
        elif args.case:
            test_case = get_test_case_by_id(args.case)
            if not test_case:
                print(f"❌ Test case '{args.case}' not found")
                return 1
                
            print(f"🚀 Running evaluation for test case: {args.case}")
            results = await run_quick_evaluation(
                test_case_ids=[args.case], 
                output_dir=args.output_dir
            )
        
        print(f"\n✅ Evaluation completed successfully!")
        print(f"📊 Results saved to: {args.output_dir}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Evaluation failed with error: {e}")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code) 