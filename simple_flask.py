#!/usr/bin/env python
"""Flask test tanpa threading"""
from flask import Flask, request, jsonify
from werkzeug.serving import run_simple

app = Flask(__name__)

@app.route("/")
def home():
    print("[simple] GET /")
    return {"msg": "ok"}

@app.route("/test-post", methods=["POST"])
def test_post():
    print("[simple] POST received")
    print(f"[simple] Content-Type: {request.content_type}")
    print(f"[simple] Is JSON: {request.is_json}")
    
    if request.is_json:
        data = request.get_json()
        print(f"[simple] Data: {data}")
    
    print("[simple] Sending response...")
    return {"ok": True}

if __name__ == "__main__":
    print("[simple] Starting Flask tanpa threading...")
    # Try with run_simple instead of app.run
    run_simple("127.0.0.1", 5004, app, use_debugger=False, use_reloader=False, threaded=False)
