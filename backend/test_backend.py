#!/usr/bin/env python
import requests
import json
import time

print("[TEST] Testing BakeSmart Backend API")
print("=" * 60)

# Give server time to fully start
time.sleep(2)

# Test 1: Login
print("\n[1] Testing /login endpoint...")
login_data = {
    "email": "admin@bakesmart.com",
    "password": "admin123"
}

try:
    response = requests.post(
        "http://127.0.0.1:5000/login",
        json=login_data,
        timeout=5
    )
    print(f"    Status: {response.status_code}")
    print(f"    Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        token = response.json().get('token')
        print(f"✅ Login successful! Token: {token[:30]}...")
    else:
        print(f"❌ Login failed with status {response.status_code}")
        token = None
except Exception as e:
    print(f"❌ Login request failed: {e}")
    token = None

# Test 2: Get stock records with token
if token:
    print("\n[2] Testing /stock-records endpoint...")
    try:
        response = requests.get(
            "http://127.0.0.1:5000/stock-records",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5
        )
        print(f"    Status: {response.status_code}")
        print(f"    Response: {json.dumps(response.json(), indent=2)}")
        if response.status_code == 200:
            records = response.json().get('data', [])
            print(f"✅ Got {len(records)} stock records")
        else:
            print(f"❌ Request failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Request failed: {e}")

# Test 3: Create new stock record
if token:
    print("\n[3] Testing /stock-record endpoint (create)...")
    record_data = {
        "bahan_nama": "test_item_" + str(int(time.time())),
        "jumlah": 10,
        "unit": "kg",
        "tipe": "masuk"
    }
    try:
        response = requests.post(
            "http://127.0.0.1:5000/stock-record",
            json=record_data,
            headers={"Authorization": f"Bearer {token}"},
            timeout=5
        )
        print(f"    Status: {response.status_code}")
        print(f"    Response: {json.dumps(response.json(), indent=2)}")
        if response.status_code == 200 or response.status_code == 201:
            print(f"✅ Record created successfully")
        else:
            print(f"❌ Request failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Request failed: {e}")

print("\n" + "=" * 60)
print("[TEST] Testing complete")
