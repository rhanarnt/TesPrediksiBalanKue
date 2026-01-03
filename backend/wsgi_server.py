#!/usr/bin/env python3
"""
Run Flask app with wsgiref.simple_server
This avoids Werkzeug's run_simple issues on Windows
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from run import app, init_db, seed_db
from wsgiref.simple_server import make_server

print("[INFO] Loading application...")

# Initialize database
init_db(app)
seed_db(app)

print("=" * 60)
print("BakeSmart Backend Server")
print("=" * 60)
print("Database initialized")
print("Running on http://127.0.0.1:5000")
print("=" * 60)
print("[DEBUG] Starting WSGI server...")
sys.stdout.flush()

try:
    # Create simple WSGI server
    with make_server('127.0.0.1', 5000, app) as httpd:
        print("[OK] Server started - listening on http://127.0.0.1:5000")
        print("Press CTRL+C to quit")
        sys.stdout.flush()
        httpd.serve_forever()
        
except KeyboardInterrupt:
    print("\n[INFO] Shutting down...")
    sys.exit(0)
except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)


