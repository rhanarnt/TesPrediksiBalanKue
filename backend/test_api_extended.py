#!/usr/bin/env python
"""Test new API endpoints"""
import requests
import json
import time

BASE_URL = "http://127.0.0.1:5000"

def get_token():
    """Get JWT token dari login"""
    try:
        response = requests.post(
            f"{BASE_URL}/login",
            json={"email": "admin@bakesmart.com", "password": "admin123"},
            timeout=5
        )
        if response.status_code == 200:
            return response.json().get('token')
    except Exception as e:
        print(f"❌ Failed to get token: {e}")
    return None

def test_bahan_detail(token):
    """Test GET /bahan/<id>"""
    print("\n" + "="*60)
    print("Testing GET /bahan/1...")
    print("="*60)
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/bahan/1", headers=headers, timeout=5)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_notifications(token):
    """Test GET /notifications"""
    print("\n" + "="*60)
    print("Testing GET /notifications...")
    print("="*60)
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/notifications", headers=headers, timeout=5)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_stock_record(token):
    """Test POST /stock-record"""
    print("\n" + "="*60)
    print("Testing POST /stock-record...")
    print("="*60)
    try:
        headers = {"Authorization": f"Bearer {token}"}
        payload = {
            "bahan_id": 1,
            "jumlah": 10,
            "tipe": "masuk",
            "catatan": "Test input dari API"
        }
        response = requests.post(
            f"{BASE_URL}/stock-record",
            json=payload,
            headers=headers,
            timeout=5
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 201
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_logout(token):
    """Test POST /logout"""
    print("\n" + "="*60)
    print("Testing POST /logout...")
    print("="*60)
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(f"{BASE_URL}/logout", headers=headers, timeout=5)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("\n🎂 BakeSmart API Extended Endpoints Test")
    time.sleep(1)
    
    # Get token
    token = get_token()
    if not token:
        print("❌ Failed to get token!")
        return
    
    print(f"\n✅ Got token: {token[:50]}...")
    
    # Test all endpoints
    results = {
        'Bahan Detail': test_bahan_detail(token),
        'Notifications': test_notifications(token),
        'Stock Record': test_stock_record(token),
        'Logout': test_logout(token),
    }
    
    # Print summary
    print("\n" + "="*60)
    print("📊 Test Summary")
    print("="*60)
    for endpoint, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{endpoint}: {status}")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    print(f"\n{passed}/{total} tests passed")

if __name__ == "__main__":
    main()
