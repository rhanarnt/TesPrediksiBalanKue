#!/usr/bin/env python
"""Test API endpoints directly"""
import requests
import json
import time

BASE_URL = "http://127.0.0.1:5000"

def test_health():
    """Test /health endpoint"""
    print("\n" + "="*60)
    print("Testing /health endpoint...")
    print("="*60)
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_login():
    """Test /login endpoint"""
    print("\n" + "="*60)
    print("Testing /login endpoint...")
    print("="*60)
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
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            token = response.json().get('token')
            return token
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_stok(token):
    """Test /stok endpoint"""
    print("\n" + "="*60)
    print("Testing /stok endpoint...")
    print("="*60)
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        response = requests.get(f"{BASE_URL}/stok", headers=headers, timeout=5)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("\n🎂 BakeSmart API Test Suite")
    print("Waiting for server to be ready...")
    
    # Give server time to startup
    time.sleep(2)
    
    # Test health check
    if not test_health():
        print("\n❌ Server is not responding. Make sure Flask server is running.")
        return
    
    # Test login
    token = test_login()
    if not token:
        print("\n❌ Login failed!")
        return
    
    # Test stok with token
    test_stok(token)
    
    print("\n" + "="*60)
    print("✅ All tests completed!")
    print("="*60)

if __name__ == "__main__":
    main()
