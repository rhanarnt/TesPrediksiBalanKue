#!/usr/bin/env python3
"""
Super-stable Flask server wrapper
Handles all errors gracefully
"""
import sys
import os
import logging
import traceback

sys.path.insert(0, os.path.dirname(__file__))

# Set up logging to suppress Flask debug messages
logging.basicConfig(level=logging.WARNING)

from run import app, init_db, seed_db

# Disable Flask's default error handling to catch them ourselves
@app.errorhandler(404)
def handle_404(error):
    return {'error': 'Not found'}, 404

@app.errorhandler(500)
def handle_500(error):
    traceback.print_exc()
    return {'error': 'Internal server error'}, 500

@app.errorhandler(Exception)
def handle_exception(error):
    print(f"[ERROR] Exception: {error}")
    traceback.print_exc()
    return {'error': str(error)}, 500

if __name__ == '__main__':
    print("[INFO] Initializing database...")
    try:
        with app.app_context():
            init_db(app)
            seed_db(app)
        print("[OK] Database initialized")
    except Exception as e:
        print(f"[ERROR] Failed to initialize database: {e}")
        traceback.print_exc()
        sys.exit(1)
    
    print("[INFO] Starting Flask server...")
    print("[OK] Server running on http://127.0.0.1:5000")
    print("[OK] Android Emulator: use http://10.0.2.2:5000")
    print("[INFO] Press Ctrl+C to quit\n")
    
    try:
        app.run(
            host='127.0.0.1',
            port=5000,
            debug=False,
            use_reloader=False,
            use_debugger=False,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n[INFO] Shutting down...")
        sys.exit(0)
    except Exception as e:
        print(f"[ERROR] Server error: {e}")
        traceback.print_exc()
        sys.exit(1)
