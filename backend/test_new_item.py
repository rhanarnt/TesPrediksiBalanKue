#!/usr/bin/env python
"""Quick test for new item creation with bahan_nama"""
import requests
import json
import time

print("[TEST] Creating new item with bahan_nama...")
print("=" * 60)

# Get token first
login_data = {"email": "admin@bakesmart.com", "password": "admin123"}
response = requests.post("http://127.0.0.1:5000/login", json=login_data)
token = response.json().get('token')
print(f"✅ Logged in, got token")

# Create new item with name "Telur Ayam" (chicken eggs)
new_item_data = {
    "bahan_nama": "Telur Ayam",
    "jumlah": 12,
    "unit": "butir",
    "tipe": "masuk",
    "catatan": "Test creating new item with correct name"
}

response = requests.post(
    "http://127.0.0.1:5000/stock-record",
    json=new_item_data,
    headers={"Authorization": f"Bearer {token}"}
)

print(f"\n[CREATE] Response Status: {response.status_code}")
result = response.json()
print(f"[CREATE] Response: {json.dumps(result, indent=2)}")

if response.status_code in (200, 201):
    created_id = result.get('data', {}).get('id')
    bahan_id = result.get('data', {}).get('bahan_id')
    print(f"\n✅ Item created successfully!")
    print(f"   Record ID: {created_id}")
    print(f"   Bahan ID: {bahan_id}")
    
    # Now fetch all records to verify
    print(f"\n[FETCH] Fetching all stock records...")
    response = requests.get(
        "http://127.0.0.1:5000/stock-records",
        headers={"Authorization": f"Bearer {token}"}
    )
    records = response.json().get('data', [])
    
    # Find our new record
    new_record = next((r for r in records if r['id'] == created_id), None)
    if new_record:
        print(f"✅ Found our new record!")
        print(f"   ID: {new_record['id']}")
        print(f"   Nama Bahan: {new_record.get('nama_bahan')}")
        print(f"   Jumlah: {new_record['jumlah']} {new_record['unit']}")
        print(f"   Tanggal: {new_record['tanggal']}")
    else:
        print(f"❌ Could not find our new record in the list")
else:
    print(f"❌ Failed to create item: {result}")

print("\n" + "=" * 60)
