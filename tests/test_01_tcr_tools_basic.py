#!/usr/bin/env python3
"""
Test 01: Basic TCR Tools Testing

Tests individual TCR analysis tools in isolation to verify core functionality.
This is the most basic test level - testing tools directly without agent integration.
"""

import sys
import os
sys.path.append('src')

from src.tools.tcr_analysis import (
    get_vdjdb_schema,
    calculate_tcr_diversity_metrics,
    analyze_cdr3_motifs,
    compare_tcr_repertoires
)

def test_vdjdb_schema():
    """Test 1.1: VDJdb Schema Retrieval"""
    print("🔍 Test 1.1: VDJdb Schema Retrieval")
    print("-" * 40)
    
    try:
        result = get_vdjdb_schema.invoke({})
        
        # Basic validation
        assert isinstance(result, str), "Result should be a string"
        assert len(result) > 100, "Schema should contain substantial information"
        assert "table" in result.lower() or "column" in result.lower(), "Should contain table/column info"
        
        print("✅ Schema retrieval successful")
        print(f"   Length: {len(result)} characters")
        print(f"   Preview: {result[:150]}...")
        return True
        
    except Exception as e:
        print(f"❌ Schema retrieval failed: {e}")
        return False

def test_cdr3_motif_analysis():
    """Test 1.2: CDR3 Motif Analysis"""
    print("\n🧬 Test 1.2: CDR3 Motif Analysis")
    print("-" * 40)
    
    test_cases = [
        {
            "name": "Basic CDR3 sequences",
            "sequences": "CASSLAPGATNEKLFF,CASSLKPSYNEQFF,CASSIRDSSGANVLTF"
        },
        {
            "name": "Single sequence",
            "sequences": "CASSLAPGATNEKLFF"
        },
        {
            "name": "Mixed length sequences",
            "sequences": "CASSLAP,CASSLAPGATNEKLFF,CASSLKPSYNEQFF,CASS"
        }
    ]
    
    passed = 0
    for test_case in test_cases:
        try:
            print(f"\n   Testing: {test_case['name']}")
            result = analyze_cdr3_motifs.invoke({"cdr3_sequences": test_case["sequences"]})
            
            # Basic validation
            assert isinstance(result, str), "Result should be a string"
            assert len(result) > 50, "Analysis should contain substantial information"
            
            print(f"   ✅ {test_case['name']} - Success")
            print(f"      Length: {len(result)} characters")
            passed += 1
            
        except Exception as e:
            print(f"   ❌ {test_case['name']} - Failed: {e}")
    
    print(f"\n   Results: {passed}/{len(test_cases)} test cases passed")
    return passed == len(test_cases)

def test_diversity_metrics():
    """Test 1.3: TCR Diversity Metrics"""
    print("\n📊 Test 1.3: TCR Diversity Metrics")
    print("-" * 40)
    
    test_datasets = [
        {
            "name": "Balanced distribution",
            "data": """clonotype_id frequency
clone_1 100
clone_2 100
clone_3 100
clone_4 100
clone_5 100"""
        },
        {
            "name": "Skewed distribution",
            "data": """clonotype_id frequency
clone_1 500
clone_2 50
clone_3 25
clone_4 15
clone_5 10"""
        },
        {
            "name": "Minimal dataset",
            "data": """clonotype_id frequency
clone_1 10
clone_2 5"""
        }
    ]
    
    passed = 0
    for dataset in test_datasets:
        try:
            print(f"\n   Testing: {dataset['name']}")
            result = calculate_tcr_diversity_metrics.invoke({"query_result": dataset["data"]})
            
            # Basic validation
            assert isinstance(result, str), "Result should be a string"
            assert "shannon" in result.lower() or "diversity" in result.lower(), "Should contain diversity metrics"
            assert len(result) > 50, "Analysis should contain substantial information"
            
            print(f"   ✅ {dataset['name']} - Success")
            print(f"      Length: {len(result)} characters")
            passed += 1
            
        except Exception as e:
            print(f"   ❌ {dataset['name']} - Failed: {e}")
    
    print(f"\n   Results: {passed}/{len(test_datasets)} test cases passed")
    return passed == len(test_datasets)

def test_repertoire_comparison():
    """Test 1.4: TCR Repertoire Comparison"""
    print("\n🔬 Test 1.4: TCR Repertoire Comparison")
    print("-" * 40)
    
    test_scenarios = [
        {
            "name": "Overlapping repertoires",
            "rep1": """clonotype frequency
CASSLAPGATNEKLFF 0.15
CASSLKPSYNEQFF 0.12
CASSIRDSSGANVLTF 0.08""",
            "rep2": """clonotype frequency
CASSLAPGATNEKLFF 0.10
CASSLKPSYNEQFF 0.18
CASSQRDSSGANVLTF 0.09""",
            "group1": "Responders",
            "group2": "Non-responders"
        },
        {
            "name": "Non-overlapping repertoires",
            "rep1": """clonotype frequency
CASSA 0.20
CASSB 0.15
CASSC 0.10""",
            "rep2": """clonotype frequency
CASSD 0.25
CASSE 0.12
CASSF 0.08""",
            "group1": "Treatment",
            "group2": "Control"
        }
    ]
    
    passed = 0
    for scenario in test_scenarios:
        try:
            print(f"\n   Testing: {scenario['name']}")
            result = compare_tcr_repertoires.invoke({
                "repertoire1_data": scenario["rep1"],
                "repertoire2_data": scenario["rep2"],
                "group1_name": scenario["group1"],
                "group2_name": scenario["group2"]
            })
            
            # Basic validation
            assert isinstance(result, str), "Result should be a string"
            assert "overlap" in result.lower() or "comparison" in result.lower(), "Should contain comparison info"
            assert len(result) > 50, "Analysis should contain substantial information"
            
            print(f"   ✅ {scenario['name']} - Success")
            print(f"      Length: {len(result)} characters")
            passed += 1
            
        except Exception as e:
            print(f"   ❌ {scenario['name']} - Failed: {e}")
    
    print(f"\n   Results: {passed}/{len(test_scenarios)} test cases passed")
    return passed == len(test_scenarios)

def run_all_basic_tests():
    """Run all basic TCR tool tests"""
    print("🧬 TCR Tools Basic Testing Suite")
    print("=" * 50)
    print("Testing individual TCR analysis tools in isolation")
    print("This verifies core functionality before agent integration\n")
    
    tests = [
        ("VDJdb Schema", test_vdjdb_schema),
        ("CDR3 Motif Analysis", test_cdr3_motif_analysis),
        ("Diversity Metrics", test_diversity_metrics),
        ("Repertoire Comparison", test_repertoire_comparison)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed_tests += 1
        except Exception as e:
            print(f"❌ {test_name} test suite failed: {e}")
    
    print("\n" + "=" * 50)
    print(f"🔬 BASIC TESTING RESULTS: {passed_tests}/{total_tests} test suites passed")
    
    if passed_tests == total_tests:
        print("✅ All basic TCR tools are functional!")
        print("Ready to proceed to intermediate testing (agent integration)")
    else:
        print("⚠️  Some tools need attention before proceeding to advanced tests")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    # Check Python path
    if 'src' not in sys.path:
        print("Adding src to Python path...")
        sys.path.append('src')
    
    # Run the tests
    success = run_all_basic_tests()
    exit(0 if success else 1) 