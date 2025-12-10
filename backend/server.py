#!/usr/bin/env python3
"""
BakeSmart Backend Server - Simple Flask runner
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

# Load environment
from dotenv import load_dotenv
load_dotenv()

print("[INFO] Starting BakeSmart Backend Server...")
print("[INFO] Loading Flask application...")

from run import app, init_db, seed_db

print("[INFO] Initializing database...")
with app.app_context():
    try:
        init_db(app)
        seed_db(app)
        print("[OK] Database initialized")
    except Exception as e:
        print(f"[WARNING] Database init: {e}")

if __name__ == '__main__':
    print("\n" + "="*60)
    print("BakeSmart Backend API")
    print("="*60)
    print("[OK] Server running on http://0.0.0.0:5000")
    print("[OK] Local access: http://127.0.0.1:5000")
    print("[OK] Emulator access: http://10.0.2.2:5000")
    print("[OK] Endpoints available:")
    print("     POST   /login - Authenticate user")
    print("     GET    /stok - Get all stock items")
    print("     POST   /stock-record - Add stock record")
    print("     GET    /stock-records - Get stock history")
    print("     GET    /health - Health check")
    print("="*60 + "\n")
    
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
        print("\n[INFO] Server stopped")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] Server failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
