#!/usr/bin/env python
"""Simple Flask login test"""
import sys
import traceback

try:
    print("1. Importing Flask...")
    from flask import Flask, request
    from flask_cors import CORS
    print("   OK")
    
    print("2. Importing routes...")
    from app.routes import routes
    print("   OK")
    
    print("3. Creating Flask app...")
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(routes)
    print("   OK - Routes registered:", len(app.url_map._rules_by_endpoint))
    
    print("\n4. Testing login POST locally...")
    with app.test_client() as client:
        response = client.post('/login', 
            json={"email": "admin@bakesmart.com", "password": "admin123"},
            content_type='application/json')
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.get_json()}")
        
except Exception as e:
    print(f"\nERROR: {e}", file=sys.stderr)
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)

print("\nSUCCESS!")
