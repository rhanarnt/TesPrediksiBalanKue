#!/usr/bin/env python
"""Workaround untuk Flask POST crash di Windows"""
import sys
import os
os.environ['WERKZEUG_RUN_MAIN'] = 'true'

from flask import Flask, request

app = Flask(__name__)

@app.route("/test", methods=["POST"])
def test():
    print("[app] POST test received", flush=True)
    data = request.get_json(silent=True)
    print(f"[app] Data: {data}", flush=True)
    return {"ok": True}

if __name__ == "__main__":
    print("[app] Starting...", flush=True)
    # Try different approach
    from werkzeug.serving import make_server
    server = make_server('127.0.0.1', 5007, app, threaded=False)
    print("[app] Server created, listening...", flush=True)
    sys.stdout.flush()
    server.serve_forever()
