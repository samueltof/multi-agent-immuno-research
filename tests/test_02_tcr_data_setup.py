#!/usr/bin/env python3
"""
Test 02: TCR Data Setup and Environment

Tests database setup, environment configuration, and data initialization.
This is intermediate level testing - ensuring the data infrastructure is ready.
"""

import sys
import os
import sqlite3
from pathlib import Path
sys.path.append('src')

from src.config.vdjdb import VDJdbConfig

def check_environment_variables():
    """Test 2.1: Environment Variables Configuration"""
    print("🔧 Test 2.1: Environment Variables Configuration")
    print("-" * 50)
    
    # Required environment variables for TCR analysis
    required_vars = {
        "VDJDB_SQLITE_PATH": "data/vdjdb.db",
        "MIN_CDR3_LENGTH": "8",
        "MAX_CDR3_LENGTH": "25", 
        "MIN_CONFIDENCE_SCORE": "0.5"
    }
    
    optional_vars = {
        "TCR_ANALYSIS_CACHE_DIR": "data/cache",
        "MAX_SEQUENCES_PER_ANALYSIS": "10000"
    }
    
    issues = []
    
    print("\n   Required Environment Variables:")
    for var, default in required_vars.items():
        value = os.getenv(var)
        if value:
            print(f"   ✅ {var}: {value}")
        else:
            print(f"   ⚠️  {var}: Not set (will use default: {default})")
            # Set default for testing
            os.environ[var] = default
    
    print("\n   Optional Environment Variables:")
    for var, default in optional_vars.items():
        value = os.getenv(var)
        if value:
            print(f"   ✅ {var}: {value}")
        else:
            print(f"   ⚠️  {var}: Not set (will use default: {default})")
            os.environ[var] = default
    
    # Validate config loading
    try:
        config = VDJdbConfig()
        print(f"\n   ✅ VDJdbConfig loaded successfully")
        print(f"      SQLite Path: {config.sqlite_path}")
        print(f"      CDR3 Length Range: {config.min_cdr3_length}-{config.max_cdr3_length}")
        return True
    except Exception as e:
        print(f"\n   ❌ VDJdbConfig loading failed: {e}")
        return False

def check_directory_structure():
    """Test 2.2: Directory Structure"""
    print("\n📁 Test 2.2: Directory Structure")
    print("-" * 50)
    
    required_dirs = [
        "data",
        "data/cache",
        "src",
        "src/tools",
        "src/agents",
        "src/config"
    ]
    
    missing_dirs = []
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"   ✅ {dir_path}/")
        else:
            print(f"   ⚠️  {dir_path}/ - Missing, creating...")
            try:
                os.makedirs(dir_path, exist_ok=True)
                print(f"      Created {dir_path}/")
            except Exception as e:
                print(f"      ❌ Failed to create {dir_path}/: {e}")
                missing_dirs.append(dir_path)
    
    if not missing_dirs:
        print("\n   ✅ All required directories are available")
        return True
    else:
        print(f"\n   ❌ Missing directories: {missing_dirs}")
        return False

def create_sample_vdjdb():
    """Test 2.3: Sample VDJdb Database Creation"""
    print("\n🗄️  Test 2.3: Sample VDJdb Database Creation")
    print("-" * 50)
    
    db_path = os.getenv("VDJDB_SQLITE_PATH", "data/vdjdb.db")
    
    try:
        # Create sample database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS vdjdb (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gene TEXT,
            cdr3 TEXT,
            v_gene TEXT,
            j_gene TEXT,
            species TEXT,
            mhc_a TEXT,
            mhc_b TEXT,
            mhc_class TEXT,
            epitope TEXT,
            antigen_gene TEXT,
            antigen_species TEXT,
            reference_id TEXT,
            method TEXT,
            confidence_score REAL,
            clone_count INTEGER
        )
        """)
        
        # Insert sample data
        sample_data = [
            ("TRB", "CASSLAPGATNEKLFF", "TRBV7-2", "TRBJ1-4", "HomoSapiens", "HLA-A*02:01", "B2M", "MHCI", "GILGFVFTL", "Flu-MP", "InfluenzaA", "PMID:123456", "tetramer", 3, 150),
            ("TRB", "CASSLKPSYNEQFF", "TRBV7-3", "TRBJ2-1", "HomoSapiens", "HLA-A*02:01", "B2M", "MHCI", "GILGFVFTL", "Flu-MP", "InfluenzaA", "PMID:123456", "tetramer", 3, 120),
            ("TRB", "CASSIRDSSGANVLTF", "TRBV12-3", "TRBJ2-6", "HomoSapiens", "HLA-A*02:01", "B2M", "MHCI", "NLVPMVATV", "CMV-pp65", "CMV", "PMID:789012", "multimer", 2, 80),
            ("TRB", "CASSLAPSGANVLTF", "TRBV7-2", "TRBJ2-6", "HomoSapiens", "HLA-A*02:01", "B2M", "MHCI", "NLVPMVATV", "CMV-pp65", "CMV", "PMID:789012", "multimer", 2, 50),
            ("TRB", "CASSQRDSSGANVLTF", "TRBV12-4", "TRBJ2-6", "HomoSapiens", "HLA-A*24:02", "B2M", "MHCI", "AYAQKIFKI", "EBV-BZLF1", "EBV", "PMID:345678", "tetramer", 1, 25),
            ("TRA", "CAVRDENTGELFF", "TRAV12-1", "TRAJ22", "HomoSapiens", "HLA-A*02:01", "B2M", "MHCI", "GILGFVFTL", "Flu-MP", "InfluenzaA", "PMID:123456", "tetramer", 3, 200),
            ("TRA", "CALDDENSGYSTLTF", "TRAV21", "TRAJ39", "HomoSapiens", "HLA-A*02:01", "B2M", "MHCI", "NLVPMVATV", "CMV-pp65", "CMV", "PMID:789012", "multimer", 2, 75),
            ("TRB", "CASSETGNEQFF", "TRBV5-1", "TRBJ2-1", "HomoSapiens", "HLA-DRB1*04:01", "HLA-DRA", "MHCII", "PKYVKQNTLKLAT", "Flu-HA", "InfluenzaA", "PMID:567890", "proliferation", 1, 30),
            ("TRB", "CASSLDRVGDEQFF", "TRBV6-1", "TRBJ2-7", "HomoSapiens", "HLA-DRB1*07:01", "HLA-DRA", "MHCII", "AKFVAAWTLKAAA", "SARS-CoV-2-S", "SARS-CoV-2", "PMID:901234", "cytokine", 2, 40),
            ("TRB", "CASSYLGGGNQPQHF", "TRBV20-1", "TRBJ1-5", "HomoSapiens", "HLA-A*01:01", "B2M", "MHCI", "VTEHDTLLY", "EBV-BMLF1", "EBV", "PMID:456789", "tetramer", 3, 90)
        ]
        
        cursor.executemany("""
        INSERT INTO vdjdb (gene, cdr3, v_gene, j_gene, species, mhc_a, mhc_b, mhc_class, 
                          epitope, antigen_gene, antigen_species, reference_id, method, 
                          confidence_score, clone_count)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, sample_data)
        
        conn.commit()
        
        # Verify the data
        cursor.execute("SELECT COUNT(*) FROM vdjdb")
        count = cursor.fetchone()[0]
        
        cursor.execute("SELECT DISTINCT gene FROM vdjdb")
        genes = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT DISTINCT mhc_class FROM vdjdb")
        mhc_classes = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        
        print(f"   ✅ Sample VDJdb database created successfully")
        print(f"      Path: {db_path}")
        print(f"      Records: {count}")
        print(f"      Genes: {', '.join(genes)}")
        print(f"      MHC Classes: {', '.join(mhc_classes)}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Database creation failed: {e}")
        return False

def test_database_connectivity():
    """Test 2.4: Database Connectivity"""
    print("\n🔗 Test 2.4: Database Connectivity")
    print("-" * 50)
    
    db_path = os.getenv("VDJDB_SQLITE_PATH", "data/vdjdb.db")
    
    if not os.path.exists(db_path):
        print(f"   ❌ Database file not found: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Test basic queries
        test_queries = [
            ("Table existence", "SELECT name FROM sqlite_master WHERE type='table' AND name='vdjdb'"),
            ("Record count", "SELECT COUNT(*) FROM vdjdb"),
            ("Sample records", "SELECT cdr3, epitope, confidence_score FROM vdjdb LIMIT 3"),
            ("TCR Beta chains", "SELECT COUNT(*) FROM vdjdb WHERE gene = 'TRB'"),
            ("High confidence", "SELECT COUNT(*) FROM vdjdb WHERE confidence_score >= 2")
        ]
        
        results = {}
        for test_name, query in test_queries:
            try:
                cursor.execute(query)
                result = cursor.fetchall()
                results[test_name] = result
                print(f"   ✅ {test_name}: {len(result)} result(s)")
            except Exception as e:
                print(f"   ❌ {test_name}: {e}")
                conn.close()
                return False
        
        conn.close()
        
        # Validate results
        if not results["Table existence"]:
            print("   ❌ VDJdb table not found")
            return False
        
        total_records = results["Record count"][0][0] if results["Record count"] else 0
        if total_records == 0:
            print("   ❌ No records in database")
            return False
        
        print(f"\n   ✅ Database connectivity successful")
        print(f"      Total records: {total_records}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Database connectivity failed: {e}")
        return False

def test_tool_database_integration():
    """Test 2.5: Tool-Database Integration"""
    print("\n🔧 Test 2.5: Tool-Database Integration")
    print("-" * 50)
    
    try:
        # Import after ensuring environment is set up
        from src.tools.tcr_analysis import get_vdjdb_schema
        
        # Test that tools can access the database
        result = get_vdjdb_schema.invoke({})
        
        if "vdjdb" in result.lower() and len(result) > 100:
            print("   ✅ Tools can access VDJdb database")
            print(f"      Schema response length: {len(result)} characters")
            return True
        else:
            print("   ❌ Tools cannot properly access VDJdb database")
            print(f"      Schema response: {result[:200]}...")
            return False
            
    except Exception as e:
        print(f"   ❌ Tool-database integration failed: {e}")
        return False

def run_all_setup_tests():
    """Run all data setup and environment tests"""
    print("🧬 TCR Data Setup and Environment Testing")
    print("=" * 60)
    print("Validating data infrastructure and environment configuration")
    print("This ensures the foundation is ready for agent testing\n")
    
    tests = [
        ("Environment Variables", check_environment_variables),
        ("Directory Structure", check_directory_structure),
        ("Sample VDJdb Creation", create_sample_vdjdb),
        ("Database Connectivity", test_database_connectivity),
        ("Tool-Database Integration", test_tool_database_integration)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed_tests += 1
        except Exception as e:
            print(f"❌ {test_name} test failed: {e}")
    
    print("\n" + "=" * 60)
    print(f"🔧 SETUP TESTING RESULTS: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("✅ Environment and data setup complete!")
        print("Ready for agent integration testing")
    else:
        print("⚠️  Setup issues need to be resolved before proceeding")
        print("Check the failed tests above for specific problems")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    # Ensure src is in path
    if 'src' not in sys.path:
        sys.path.append('src')
    
    success = run_all_setup_tests()
    exit(0 if success else 1) 