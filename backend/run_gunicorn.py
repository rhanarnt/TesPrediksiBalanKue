#!/usr/bin/env python3
"""
Production server using Gunicorn
Most stable for Windows + Android emulator
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
    # Import and run Gunicorn
    from gunicorn.app.wsgiapp import run as gunicorn_run
    
    print("[INFO] Starting Gunicorn server...")
    print("[OK] Server running on http://127.0.0.1:5000")
    print("[OK] Android Emulator: use http://10.0.2.2:5000")
    print("[INFO] Press Ctrl+C to quit\n")
    
    # Gunicorn command line: gunicorn --bind 127.0.0.1:5000 --workers 2 --worker-class sync run:app
    sys.argv = [
        'gunicorn',
        '--bind', '127.0.0.1:5000',
        '--workers', '2',
        '--worker-class', 'sync',
        '--timeout', '30',
        '--access-logfile', '-',
        'run:app'
    ]
    
    try:
        gunicorn_run()
    except KeyboardInterrupt:
        print("\n[INFO] Shutting down...")
        sys.exit(0)
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
