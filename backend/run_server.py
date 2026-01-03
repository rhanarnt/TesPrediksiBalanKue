#!/usr/bin/env python3
"""
Final working server - bypass Werkzeug completely
Use HTTP server at application level
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

print("[INFO] Loading application...")
from run import app, init_db, seed_db

print("[INFO] Initializing database...")
with app.app_context():
    init_db(app)
    seed_db(app)
print("[OK] Database ready")

if __name__ == '__main__':
    print("[OK] Server starting on http://127.0.0.1:5000\n")
    
    # Set environment to disable debugger/reloader completely
    os.environ['WERKZEUG_RUN_MAIN'] = 'true'
    
    # Disable Werkzeug's auto-reloader and debugger
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    
    try:
        # Run with minimal config - only threading, no debug/reload
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
