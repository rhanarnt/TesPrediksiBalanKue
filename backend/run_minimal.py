#!/usr/bin/env python3
"""
Minimal Flask server - no fancy stuff
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
    print("[INFO] Starting Flask minimal server...")
    print("[OK] Server running on http://127.0.0.1:5000")
    print("[OK] Android Emulator: use http://10.0.2.2:5000")
    print("[INFO] Press Ctrl+C to quit\n")
    
    try:
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,
            use_reloader=False,
            use_debugger=False,
            threaded=True,
        )
    except KeyboardInterrupt:
        print("\n[INFO] Shutting down...")
        sys.exit(0)
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
