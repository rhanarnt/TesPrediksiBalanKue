#!/usr/bin/env python3
"""
Test all endpoints without running HTTP server
Uses Flask test client which bypasses socket issues
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from run import app, init_db, seed_db
import json

print("[INFO] Initializing database...")
with app.app_context():
    init_db(app)
    seed_db(app)
print("[OK] Database ready\n")

# Create test client
client = app.test_client()

print("=" * 60)
print("TESTING ALL ENDPOINTS")
print("=" * 60 + "\n")

# Test 1: Health check
print("1️⃣  Testing /health...")
response = client.get('/health')
assert response.status_code == 200
print(f"   ✅ Status 200 - {json.loads(response.data)['status']}\n")

# Test 2: Login
print("2️⃣  Testing /login...")
response = client.post('/login',
    data=json.dumps({'email': 'admin@bakesmart.com', 'password': 'admin123'}),
    content_type='application/json'
)
assert response.status_code == 200
login_data = json.loads(response.data)
token = login_data['token']
print(f"   ✅ Status 200")
print(f"   ✅ Token received: {token[:50]}...")
print(f"   ✅ User: {login_data['user']['name']}\n")

# Test 3: Get stok
print("3️⃣  Testing /stok...")
response = client.get('/stok',
    headers={'Authorization': f'Bearer {token}'}
)
assert response.status_code == 200
stok_data = json.loads(response.data)
print(f"   ✅ Status 200")
print(f"   ✅ Loaded {len(stok_data['data'])} bahan items\n")

# Test 4: Get stock-records
print("4️⃣  Testing /stock-records...")
response = client.get('/stock-records',
    headers={'Authorization': f'Bearer {token}'}
)
assert response.status_code == 200
records_data = json.loads(response.data)
print(f"   ✅ Status 200")
print(f"   ✅ Loaded {len(records_data['data'])} stock records\n")

# Test 5: Create stock-record
print("5️⃣  Testing POST /stock-record...")
response = client.post('/stock-record',
    data=json.dumps({
        'bahan_id': 1,
        'jumlah': 10.5,
        'tipe': 'masuk',
        'catatan': 'Test input via API'
    }),
    headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
)
assert response.status_code == 201
record_data = json.loads(response.data)
print(f"   ✅ Status 201 - Record created")
print(f"   ✅ Record ID: {record_data['data']['id']}\n")

# Test 6: Get stock-records again
print("6️⃣  Testing /stock-records after create...")
response = client.get('/stock-records',
    headers={'Authorization': f'Bearer {token}'}
)
assert response.status_code == 200
records_data = json.loads(response.data)
print(f"   ✅ Status 200")
print(f"   ✅ Now loaded {len(records_data['data'])} stock records")
if records_data['data']:
    latest = records_data['data'][0]
    print(f"   ✅ Latest: {latest['nama_bahan']} - {latest['jumlah']} {latest['unit']}\n")

# Test 7: Logout
print("7️⃣  Testing /logout...")
response = client.post('/logout',
    headers={'Authorization': f'Bearer {token}'}
)
assert response.status_code == 200
print(f"   ✅ Status 200\n")

print("=" * 60)
print("✅ ALL TESTS PASSED!")
print("=" * 60)
print("\n✨ Backend API is fully functional!")
print("🚀 Ready for Flutter integration\n")
