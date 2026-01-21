#!/usr/bin/env python
"""Corrected Comprehensive Testing & Verification Suite for BakeSmart"""
import requests
import json
import time
from datetime import datetime

BASE_URL = "http://127.0.0.1:5000"
TESTS_PASSED = 0
TESTS_FAILED = 0

def print_header(title):
    """Print formatted header"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")

def print_test_result(test_name, passed, error_msg=None):
    """Print individual test result"""
    global TESTS_PASSED, TESTS_FAILED
    if passed:
        print(f"[PASS] {test_name}")
        TESTS_PASSED += 1
    else:
        print(f"[FAIL] {test_name}")
        if error_msg:
            print(f"   Error: {error_msg}")
        TESTS_FAILED += 1

def test_health_check():
    """Test: Health/Status Check"""
    print_header("TEST 1: HEALTH CHECK")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        success = response.status_code == 200
        print_test_result("GET /health", success)
        if success:
            print(f"   Response: {response.json()}")
        return success
    except Exception as e:
        print_test_result("GET /health", False, str(e))
        return False

def test_root_endpoint():
    """Test: Root Endpoint"""
    print_header("TEST 2: ROOT ENDPOINT")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        success = response.status_code == 200
        print_test_result("GET /", success)
        if success:
            print(f"   Response: {response.json()}")
        return success
    except Exception as e:
        print_test_result("GET /", False, str(e))
        return False

def test_login():
    """Test: User Login"""
    print_header("TEST 3: USER AUTHENTICATION")
    
    try:
        payload = {
            "email": "admin@bakesmart.com",
            "password": "admin123"
        }
        response = requests.post(
            f"{BASE_URL}/login",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        success = response.status_code == 200
        print_test_result("POST /login (valid credentials)", success)
        
        if success:
            data = response.json()
            token = data.get('token')
            print(f"   Email: {data.get('user_email', 'N/A')}")
            print(f"   Token: {token[:20] if token else 'N/A'}...")
            return token
        else:
            print(f"   Response: {response.json()}")
            return None
    except Exception as e:
        print_test_result("POST /login", False, str(e))
        return None

def test_stok_list(token):
    """Test: Get Stock List"""
    print_header("TEST 4: GET STOCK DATA (/stok)")
    
    if not token:
        print("⏭️  Skipped: No valid token")
        return False
    
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        response = requests.get(f"{BASE_URL}/stok", headers=headers, timeout=5)
        success = response.status_code == 200
        print_test_result("GET /stok", success)
        
        if success:
            data = response.json()
            items = data.get('data', [])
            print(f"   Total items: {len(items)}")
            if items and len(items) > 0:
                first_item = items[0]
                print(f"   Sample item: {first_item}")
        else:
            print(f"   Status: {response.status_code}, Response: {response.text[:100]}")
        return success
    except Exception as e:
        print_test_result("GET /stok", False, str(e))
        return False

def test_get_ingredient(token):
    """Test: Get Single Ingredient"""
    print_header("TEST 5: GET INGREDIENT DATA (/bahan/<id>)")
    
    if not token:
        print("⏭️  Skipped: No valid token")
        return False
    
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        # Try bahan_id=1
        response = requests.get(f"{BASE_URL}/bahan/1", headers=headers, timeout=5)
        success = response.status_code == 200
        print_test_result("GET /bahan/1", success)
        
        if success:
            data = response.json()
            print(f"   Response: {data}")
        else:
            print(f"   Status: {response.status_code}")
        return success
    except Exception as e:
        print_test_result("GET /bahan/1", False, str(e))
        return False

def test_prediction(token):
    """Test: Stock Prediction (/prediksi)"""
    print_header("TEST 6: PREDICTION ENGINE (/prediksi)")
    
    if not token:
        print("⏭️  Skipped: No valid token")
        return False
    
    try:
        payload = {
            "jumlah": 150,
            "harga": 5000
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        response = requests.post(
            f"{BASE_URL}/prediksi",
            json=payload,
            headers=headers,
            timeout=5
        )
        success = response.status_code == 200
        print_test_result("POST /prediksi (with jumlah & harga)", success)
        
        if success:
            data = response.json()
            print(f"   Predicted stock: {data.get('predicted_stock', 'N/A')}")
            print(f"   Confidence: {data.get('confidence', 'N/A')}")
        else:
            print(f"   Status: {response.status_code}, Response: {response.text[:150]}")
        return success
    except Exception as e:
        print_test_result("POST /prediksi", False, str(e))
        return False

def test_add_stok(token):
    """Test: Add Stock Record / Create Bahan"""
    print_header("TEST 7: CREATE NEW INGREDIENT (POST /stok)")
    
    if not token:
        print("⏭️  Skipped: No valid token")
        return False
    
    try:
        payload = {
            "nama": f"Test Ingredient {int(time.time())}",
            "unit": "kg",
            "stok_minimum": 50,
            "stok_optimal": 200,
            "harga_per_unit": 25000
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        response = requests.post(
            f"{BASE_URL}/stok",
            json=payload,
            headers=headers,
            timeout=5
        )
        success = response.status_code in [200, 201]
        print_test_result("POST /stok (create ingredient)", success)
        
        if success:
            data = response.json()
            print(f"   Message: {data.get('message')}")
            created_data = data.get('data', {})
            print(f"   Created ID: {created_data.get('id')}, Name: {created_data.get('nama')}")
        else:
            print(f"   Status: {response.status_code}, Response: {response.text[:200]}")
        return success
    except Exception as e:
        print_test_result("POST /stok", False, str(e))
        return False

def test_stock_records(token):
    """Test: Get Stock Records History"""
    print_header("TEST 8: GET STOCK RECORDS HISTORY (/stock-records)")
    
    if not token:
        print("⏭️  Skipped: No valid token")
        return False
    
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        response = requests.get(f"{BASE_URL}/stock-records", headers=headers, timeout=5)
        success = response.status_code == 200
        print_test_result("GET /stock-records", success)
        
        if success:
            data = response.json()
            items = data.get('data', []) if isinstance(data, dict) else data
            print(f"   Total records: {len(items)}")
        else:
            print(f"   Status: {response.status_code}")
        return success
    except Exception as e:
        print_test_result("GET /stock-records", False, str(e))
        return False

def test_notifications(token):
    """Test: Get Notifications"""
    print_header("TEST 9: GET NOTIFICATIONS (/notifications)")
    
    if not token:
        print("⏭️  Skipped: No valid token")
        return False
    
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        response = requests.get(f"{BASE_URL}/notifications", headers=headers, timeout=5)
        success = response.status_code == 200
        print_test_result("GET /notifications", success)
        
        if success:
            data = response.json()
            items = data.get('data', []) if isinstance(data, dict) else data
            print(f"   Total notifications: {len(items)}")
        else:
            print(f"   Status: {response.status_code}")
        return success
    except Exception as e:
        print_test_result("GET /notifications", False, str(e))
        return False

def test_database_connection():
    """Test: Database Connection"""
    print_header("TEST 10: DATABASE CONNECTIVITY")
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print_test_result("Database connection (via health check)", True)
            data = response.json()
            print(f"   Status: {data.get('status')}")
            print(f"   Version: {data.get('version')}")
            return True
        else:
            print_test_result("Database connection", False, "Health check failed")
            return False
    except Exception as e:
        print_test_result("Database connection", False, str(e))
        return False

def test_error_handling(token):
    """Test: Error Handling"""
    print_header("TEST 11: ERROR HANDLING")
    
    # Test invalid token
    try:
        headers = {
            "Authorization": "Bearer invalid_token_12345",
            "Content-Type": "application/json"
        }
        response = requests.get(f"{BASE_URL}/stok", headers=headers, timeout=5)
        success = response.status_code == 401
        print_test_result("Invalid token rejection", success)
        if success:
            print(f"   Correctly rejected with status: {response.status_code}")
    except Exception as e:
        print_test_result("Invalid token rejection", False, str(e))
    
    # Test missing auth header
    try:
        response = requests.get(f"{BASE_URL}/stok", timeout=5)
        success = response.status_code == 401
        print_test_result("Missing auth header rejection", success)
        if success:
            print(f"   Correctly rejected with status: {response.status_code}")
    except Exception as e:
        print_test_result("Missing auth header rejection", False, str(e))

def test_cors():
    """Test: CORS Headers"""
    print_header("TEST 12: CORS CONFIGURATION")
    
    try:
        response = requests.options(
            f"{BASE_URL}/",
            headers={
                "Origin": "http://localhost:8080",
                "Access-Control-Request-Method": "GET"
            },
            timeout=5
        )
        
        cors_header = response.headers.get("Access-Control-Allow-Origin")
        success = cors_header is not None
        print_test_result("CORS headers present", success)
        if success:
            print(f"   CORS Origin: {cors_header}")
    except Exception as e:
        print_test_result("CORS check", False, str(e))

def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("  BakeSmart Comprehensive Testing & Verification Suite")
    print("="*70)
    print(f"  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Server URL: {BASE_URL}")
    print("="*70)
    
    # Test basic connectivity
    print("\nWaiting for server to be ready...")
    time.sleep(1)
    
    # Run tests in sequence
    test_health_check()
    test_root_endpoint()
    test_database_connection()
    token = test_login()
    
    if token:
        test_stok_list(token)
        test_get_ingredient(token)
        test_prediction(token)
        test_add_stok(token)
        test_stock_records(token)
        test_notifications(token)
        test_error_handling(token)
    
    test_cors()
    
    # Print summary
    print_header("SUMMARY")
    total = TESTS_PASSED + TESTS_FAILED
    pass_rate = (TESTS_PASSED / total * 100) if total > 0 else 0
    
    print(f"Total Tests: {total}")
    print(f"✅ Passed: {TESTS_PASSED}")
    print(f"❌ Failed: {TESTS_FAILED}")
    print(f"📊 Pass Rate: {pass_rate:.1f}%")
    
    if TESTS_FAILED == 0:
        print("\nAll tests passed! System is fully operational.")
    elif pass_rate >= 80:
        print(f"\nGood: {pass_rate:.1f}% of tests passed. Most features working.")
    elif pass_rate >= 50:
        print(f"\nWarning: {pass_rate:.1f}% of tests passed. Some issues found.")
    else:
        print(f"\nCritical: {pass_rate:.1f}% of tests passed. Please review errors.")
    
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
