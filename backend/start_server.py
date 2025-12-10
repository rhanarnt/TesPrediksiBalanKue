#!/usr/bin/env python3
"""
Production-ready Flask server for Windows
Uses threading and blocking I/O to avoid select() issues
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from run import app, init_db, seed_db

print("[INFO] Initializing database...")
with app.app_context():
    init_db(app)
    seed_db(app)
print("[OK] Database initialized")

if __name__ == '__main__':
    print("[INFO] Starting Flask development server...")
    print("[OK] Server running on http://127.0.0.1:5000")
    print("[INFO] Press Ctrl+C to quit\n")
    
    # Run with threading enabled, but WITHOUT debugger/reloader
    # This avoids the Werkzeug issues on Windows
    try:
        app.run(
            host='127.0.0.1',
            port=5000,
            debug=False,
            use_reloader=False,
            use_debugger=False,
            threaded=True,
            # Use blocking socket operations
        )
    except KeyboardInterrupt:
        print("\n[INFO] Shutting down...")
        sys.exit(0)
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
