#!/usr/bin/env python
"""
Simple WSGI server untuk menghindari issue Werkzeug di Windows
"""
import sys
import os
from threading import Thread

sys.path.insert(0, os.path.dirname(__file__))

try:
    from run import app, init_db, seed_db
    print("[OK] Flask app loaded")
    
    # Initialize database
    with app.app_context():
        init_db(app)
        seed_db(app)
        print("[OK] Database initialized")
    
except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

if __name__ == '__main__':
    print("[INFO] Starting server on http://127.0.0.1:5000")
    print("=" * 60)
    
    # Use simple development server with threading
    try:
        app.run(
            host='127.0.0.1',
            port=5000,
            debug=False,
            use_reloader=False,
            threaded=True,
            processes=1
        )
    except KeyboardInterrupt:
        print("\n[INFO] Server stopped")
        sys.exit(0)
    except Exception as e:
        print(f"[ERROR] Server error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
