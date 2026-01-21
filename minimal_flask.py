#!/usr/bin/env python
"""Minimal Flask test"""
from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return {"msg": "ok"}

@app.route("/test-post", methods=["POST"])
def test_post():
    print("[app] POST received")
    print(f"[app] Data: {request.get_json()}")
    return {"ok": True}

if __name__ == "__main__":
    print("[app] Starting minimal Flask...")
    app.run(debug=False, host="127.0.0.1", port=5002, threaded=True)
