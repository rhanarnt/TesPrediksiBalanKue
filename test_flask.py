#!/usr/bin/env python
"""Test Flask app dengan login endpoint"""
import os
import sys

# Make sure we're using the right path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify
from flask_cors import CORS
from app.auth import ensure_users_table, authenticate_user, generate_jwt_token
import traceback

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return {"message": "Test server OK"}

@app.route("/login", methods=["POST"])
def login():
    """Test login endpoint"""
    try:
        print("[test_flask] Received POST /login request")
        print(f"[test_flask] Headers: {dict(request.headers)}")
        print(f"[test_flask] Is JSON: {request.is_json}")
        
        # Ensure users table exists
        print("[test_flask] Calling ensure_users_table...")
        result = ensure_users_table()
        print(f"[test_flask] ensure_users_table returned: {result}")
        
        # Get JSON body
        if not request.is_json:
            print("[test_flask] Content-Type not JSON")
            return {"error": "Content-Type must be application/json"}, 400
        
        data = request.get_json(silent=True)
        print(f"[test_flask] Request body: {data}")
        
        if not data:
            return {"error": "Invalid JSON body"}, 400
        
        email = (data.get("email") or "").strip()
        password = data.get("password") or ""
        
        print(f"[test_flask] Authenticating email: {email}")
        user = authenticate_user(email, password)
        print(f"[test_flask] authenticate_user returned: {user}")
        
        if not user:
            return {"error": "Invalid credentials"}, 401
        
        print(f"[test_flask] Generating token for user: {user['email']}")
        token = generate_jwt_token(user["id"], user["email"])
        print(f"[test_flask] Token generated: {token[:20]}...")
        
        return {
            "success": True,
            "token": token,
            "user": user
        }, 200
        
    except Exception as e:
        print(f"[test_flask] Exception occurred: {e}")
        traceback.print_exc()
        return {"error": str(e)}, 500

if __name__ == "__main__":
    print("[test_flask] Starting test Flask app...")
    print("[test_flask] Running on http://127.0.0.1:5001")
    app.run(debug=False, host="127.0.0.1", port=5001, threaded=True)
