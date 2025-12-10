#!/usr/bin/env python3
"""
Ultra-stable server using Bottle framework
Bottle handles Windows socket issues better than Werkzeug
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

print("[INFO] Loading Flask app...")
from run import app as flask_app, init_db, seed_db

print("[INFO] Initializing database...")
with flask_app.app_context():
    init_db(flask_app)
    seed_db(flask_app)
print("[OK] Database ready\n")

# Import bottle
from bottle import Bottle
bottle_app = Bottle()

# Create WSGI wrapper
@bottle_app.route('/<path:path>', method=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
def proxy(path=''):
    """Proxy all requests to Flask app"""
    from bottle import request
    # Pass through to Flask app
    environ = request.environ
    environ['PATH_INFO'] = f'/{path}' if path else '/'
    return flask_app(environ, lambda *args: None)

if __name__ == '__main__':
    print("[OK] Starting Bottle server on http://127.0.0.1:5000")
    print("[INFO] Using single-threaded mode for stability")
    print("[INFO] Press Ctrl+C to quit\n")
    
    try:
        bottle_app.run(
            host='127.0.0.1',
            port=5000,
            debug=False,
            # Bottle uses waitress or cherrypy by default on Windows
            # Both are more stable than Werkzeug
        )
    except KeyboardInterrupt:
        print("\n[INFO] Server stopped")
        sys.exit(0)
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
