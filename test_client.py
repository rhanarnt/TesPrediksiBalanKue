#!/usr/bin/env python
"""Test login dengan requests library"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import requests
import json
import time

# Wait for server to start
time.sleep(2)

print("[test_client] Testing POST /login...")
try:
    payload = {
        "email": "admin@bakesmart.com",
        "password": "admin123"
    }
    
    print(f"[test_client] Payload: {json.dumps(payload)}")
    response = requests.post(
        "http://127.0.0.1:5001/login",
        json=payload,
        timeout=10
    )
    
    print(f"[test_client] Status Code: {response.status_code}")
    print(f"[test_client] Response: {response.text}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"[test_client] Token: {data.get('token', '')[:20]}...")
    
except Exception as e:
    import traceback
    print(f"[test_client] Error: {e}")
    traceback.print_exc()
