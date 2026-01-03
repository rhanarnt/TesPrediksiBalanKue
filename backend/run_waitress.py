#!/usr/bin/env python3
"""
Production-ready server using Waitress WSGI server
Stable on Windows, works with Android Emulator
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from run import app, init_db, seed_db
from waitress import serve

print("[INFO] Initializing database...")
with app.app_context():
    init_db(app)
    seed_db(app)
print("[OK] Database initialized")

if __name__ == '__main__':
    print("[INFO] Starting Waitress WSGI server...")
    print("[OK] Server running on http://127.0.0.1:5000")
    print("[OK] Android Emulator: use http://10.0.2.2:5000")
    print("[INFO] Press Ctrl+C to quit\n")
    
    try:
        # Use Waitress instead of Flask development server
        # More stable on Windows, handles multiple concurrent connections
        serve(app, host='127.0.0.1', port=5000, threads=4, _quiet=True)
    except KeyboardInterrupt:
        print("\n[INFO] Shutting down...")
        sys.exit(0)
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
