#!/usr/bin/env python3
"""
Bottle-based server - alternative to Flask/Werkzeug for Windows
Bottle is lightweight and doesn't have threading issues
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

try:
    print("[INFO] Loading application...")
    from run import app, init_db, seed_db
    
    with app.app_context():
        print("[INFO] Initializing database...")
        init_db(app)
        seed_db(app)
        print("[OK] Database ready")
    
    print("[INFO] Starting server...")
    
    # Instead of using werkzeug, we'll just use Python's built-in HTTP server
    # But wrap the Flask app properly
    from wsgiref.simple_server import make_server
    import threading
    
    # Run in a thread to avoid blocking
    def run_server():
        try:
            with make_server('127.0.0.1', 5000, app) as httpd:
                print("[OK] Server started on http://127.0.0.1:5000")
                httpd.serve_forever()
        except Exception as e:
            print(f"[ERROR] Server error: {e}")
            import traceback
            traceback.print_exc()
    
    server_thread = threading.Thread(target=run_server, daemon=False)
    server_thread.start()
    server_thread.join()
    
except Exception as e:
    print(f"[ERROR] Startup failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
