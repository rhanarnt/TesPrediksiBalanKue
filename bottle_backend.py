#!/usr/bin/env python
"""Backend dengan Bottle (stable alternative untuk Flask)"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bottle import Bottle, request, response
import json
from app.auth import ensure_users_table, authenticate_user, generate_jwt_token
import traceback

app = Bottle()

@app.route('/')
def home():
    return {"message": "API Prediksi Stok Kue siap digunakan"}

@app.route('/health')
def health():
    return {"status": "ok"}

@app.route('/login', method='POST')
def login():
    """Login endpoint"""
    try:
        print("[bottle] POST /login received")
        
        # Set content type
        response.content_type = 'application/json'
        
        # Ensure users table
        try:
            ensure_users_table()
        except Exception as e:
            print(f"[bottle] Database error: {e}")
            return {"error": "Database error", "detail": str(e)}
        
        # Get JSON body
        try:
            data = request.json
        except:
            data = {}
        
        print(f"[bottle] Request data: {data}")
        
        email = (data.get("email") or "").strip()
        password = data.get("password") or ""
        
        if not email or not password:
            return {"error": "Email dan password wajib"}
        
        # Authenticate
        user = authenticate_user(email, password)
        if not user:
            print(f"[bottle] Auth failed for: {email}")
            response.status = 401
            return {"error": "Email atau password salah"}
        
        # Generate token
        token = generate_jwt_token(user["id"], user["email"])
        print(f"[bottle] Auth success for: {email}")
        
        return {
            "token": token,
            "user": user
        }
        
    except Exception as e:
        print(f"[bottle] Exception: {e}")
        traceback.print_exc()
        response.status = 500
        return {"error": f"Internal error: {str(e)}"}

if __name__ == "__main__":
    print("[bottle] Starting Bottle server...")
    print("[bottle] Listening on http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=False, quiet=False)
