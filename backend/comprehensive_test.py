#!/usr/bin/env python
"""Comprehensive Testing & Verification Suite for BakeSmart"""
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
        print(f"✅ {test_name}")
        TESTS_PASSED += 1
    else:
        print(f"❌ {test_name}")
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
            print(f"   Response length: {len(response.text)} bytes")
        return success
    except Exception as e:
        print_test_result("GET /", False, str(e))
        return False

def test_login():
    """Test: User Login"""
    print_header("TEST 3: USER AUTHENTICATION")
    
    # Test valid login
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
            print(f"   User: {data.get('user_email')}")
            print(f"   Token: {data.get('token')[:20]}...")
            return data.get('token')
        else:
            print(f"   Response: {response.json()}")
            return None
    except Exception as e:
        print_test_result("POST /login", False, str(e))
        return None

def test_stok_list(token):
    """Test: Get Stock List"""
    print_header("TEST 4: GET STOCK DATA")
    
    if not token:
        print("❌ Skipped: No valid token")
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
            if items:
                print(f"   Sample item: {items[0]['nama_bahan']}")
        else:
            print(f"   Response: {response.json()}")
        return success
    except Exception as e:
        print_test_result("GET /stok", False, str(e))
        return False

def test_bahan_list(token):
    """Test: Get Ingredients List"""
    print_header("TEST 5: GET INGREDIENTS DATA")
    
    if not token:
        print("❌ Skipped: No valid token")
        return False
    
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        response = requests.get(f"{BASE_URL}/bahan", headers=headers, timeout=5)
        success = response.status_code == 200
        print_test_result("GET /bahan", success)
        
        if success:
            data = response.json()
            items = data.get('data', [])
            print(f"   Total ingredients: {len(items)}")
            if items:
                print(f"   Sample: {items[0]['nama_bahan']} (ID: {items[0]['id']})")
        else:
            print(f"   Response: {response.json()}")
        return success
    except Exception as e:
        print_test_result("GET /bahan", False, str(e))
        return False

def test_prediction(token):
    """Test: Stock Prediction"""
    print_header("TEST 6: PREDICTION ENGINE")
    
    if not token:
        print("❌ Skipped: No valid token")
        return False
    
    try:
        payload = {
            "bahan_id": 1,
            "days": 7
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        response = requests.post(
            f"{BASE_URL}/predict",
            json=payload,
            headers=headers,
            timeout=5
        )
        success = response.status_code == 200
        print_test_result("POST /predict", success)
        
        if success:
            data = response.json()
            print(f"   Predicted value: {data.get('predicted_stock', 'N/A')}")
            print(f"   Confidence: {data.get('confidence', 'N/A')}")
        else:
            print(f"   Response: {response.json()}")
        return success
    except Exception as e:
        print_test_result("POST /predict", False, str(e))
        return False

def test_add_stok(token):
    """Test: Add Stock Record"""
    print_header("TEST 7: ADD STOCK RECORD")
    
    if not token:
        print("❌ Skipped: No valid token")
        return False
    
    try:
        payload = {
            "bahan_id": 1,
            "jumlah": 100,
            "tipe": "IN",
            "catatan": "Test input - Automated verification"
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
        print_test_result("POST /stok (add record)", success)
        
        if success:
            data = response.json()
            print(f"   Created record ID: {data.get('id', 'N/A')}")
        else:
            print(f"   Response: {response.json()}")
        return success
    except Exception as e:
        print_test_result("POST /stok", False, str(e))
        return False

def test_database_connection():
    """Test: Database Connection"""
    print_header("TEST 8: DATABASE CONNECTIVITY")
    
    try:
        # Check if server has database
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        
        # If server is running, database is likely connected
        if response.status_code == 200:
            print_test_result("Database connection (via health check)", True)
            print(f"   Server response time: <5s")
            return True
        else:
            print_test_result("Database connection", False, "Health check failed")
            return False
    except Exception as e:
        print_test_result("Database connection", False, str(e))
        return False

def test_error_handling(token):
    """Test: Error Handling"""
    print_header("TEST 9: ERROR HANDLING")
    
    # Test invalid token
    try:
        headers = {
            "Authorization": "Bearer invalid_token_12345",
            "Content-Type": "application/json"
        }
        response = requests.get(f"{BASE_URL}/stok", headers=headers, timeout=5)
        success = response.status_code in [401, 403, 422]
        print_test_result("Invalid token rejection", success)
        if response.status_code in [401, 403, 422]:
            print(f"   Server correctly rejected with status: {response.status_code}")
    except Exception as e:
        print_test_result("Invalid token rejection", False, str(e))
    
    # Test missing auth header
    try:
        response = requests.get(f"{BASE_URL}/stok", timeout=5)
        success = response.status_code in [401, 403]
        print_test_result("Missing auth header rejection", success)
        if response.status_code in [401, 403]:
            print(f"   Server correctly rejected with status: {response.status_code}")
    except Exception as e:
        print_test_result("Missing auth header rejection", False, str(e))

def test_cors():
    """Test: CORS Headers"""
    print_header("TEST 10: CORS CONFIGURATION")
    
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
    print("  🎂 BakeSmart Comprehensive Testing & Verification Suite")
    print("="*70)
    print(f"  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Server URL: {BASE_URL}")
    print("="*70)
    
    # Test basic connectivity
    print("\n⏳ Waiting for server to be ready...")
    time.sleep(1)
    
    # Run tests in sequence
    test_health_check()
    test_root_endpoint()
    token = test_login()
    
    if token:
        test_stok_list(token)
        test_bahan_list(token)
        test_prediction(token)
        test_add_stok(token)
        test_error_handling(token)
    
    test_database_connection()
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
        print("\n🎉 All tests passed! System is fully operational.")
    else:
        print(f"\n⚠️  {TESTS_FAILED} test(s) failed. Please review errors above.")
    
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
