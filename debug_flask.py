#!/usr/bin/env python
"""Flask dengan exception catching - fixed"""
import sys
import traceback
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    print("[debug] GET /", flush=True)
    return {"msg": "ok"}

@app.route("/test-post", methods=["POST"])
def test_post():
    try:
        print("[debug] POST received", flush=True)
        print(f"[debug] Content-Type: {request.content_type}", flush=True)
        
        if request.is_json:
            data = request.get_json()
            print(f"[debug] Data: {data}", flush=True)
        
        return {"ok": True}
    except Exception as e:
        print(f"[debug] Exception in handler: {e}", flush=True)
        traceback.print_exc()
        return {"error": str(e)}, 500

@app.errorhandler(Exception)
def handle_error(e):
    print(f"[debug] Flask error handler: {e}", flush=True)
    traceback.print_exc()
    return {"error": "Internal server error"}, 500

if __name__ == "__main__":
    print("[debug] Starting Flask with error handler...", flush=True)
    sys.stdout.flush()
    sys.stderr.flush()
    app.run(debug=False, host="127.0.0.1", port=5005, use_reloader=False, threaded=False)
