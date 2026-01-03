#!/usr/bin/env python
"""
WSGI entry point for production deployment using Waitress
"""
import sys
import os

# Ensure run.py is imported from this directory
sys.path.insert(0, os.path.dirname(__file__))

try:
    from run import app, init_db, seed_db
    print("[OK] Flask app loaded successfully")
    
    # Initialize database
    with app.app_context():
        init_db(app)
        seed_db(app)
        print("[OK] Database initialized")
    
    print("[OK] WSGI app ready on http://127.0.0.1:5000")
    print("=" * 60)
    
except Exception as e:
    print(f"[ERROR] Failed to load app: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

if __name__ == '__main__':
    try:
        from waitress import serve
        print("[INFO] Starting Waitress server...")
        serve(app, host='127.0.0.1', port=5000, threads=4)
    except ImportError:
        print("[WARNING] Waitress not found, using wsgiref...")
        from wsgiref.simple_server import make_server
        print("[INFO] Starting wsgiref server...")
        httpd = make_server('127.0.0.1', 5000, app)
        print("[INFO] Server running on http://127.0.0.1:5000")
        httpd.serve_forever()
