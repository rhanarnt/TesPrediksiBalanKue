#!/usr/bin/env python3
"""
Simple server with SQLite - No MySQL required
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

# Change database to SQLite
os.environ['DATABASE_URL'] = 'sqlite:///bakesmart.db'

print("[INFO] Loading application with SQLite backend...")
from run import app, init_db, seed_db

print("[INFO] Initializing database...")
with app.app_context():
    try:
        init_db(app)
        seed_db(app)
        print("[OK] Database ready")
    except Exception as e:
        print(f"[WARNING] Database init issue: {e}")

if __name__ == '__main__':
    print("\n" + "="*60)
    print("BakeSmart Backend - SQLite Version")
    print("="*60)
    print("[OK] Server starting on http://127.0.0.1:5000\n")
    
    try:
        app.run(
            host='127.0.0.1',
            port=5000,
            debug=False,
            use_reloader=False,
            use_debugger=False,
            threaded=True,
        )
    except KeyboardInterrupt:
        print("\n[INFO] Server stopped")
        sys.exit(0)
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
