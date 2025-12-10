#!/usr/bin/env python
"""
Flask app without using app.run() to avoid Werkzeug Windows bugs
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

try:
    # Load app minimal
    from run import app, init_db, seed_db
    print("[OK] App ready")
    
    # Initialize DB
    with app.app_context():
        init_db(app)
        seed_db(app)
        print("[OK] Database ready")
    
except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Export for WSGI - ALWAYS run on direct execution
if __name__ == '__main__':
    print("[INFO] Server ready - use external WSGI server or:")
    print("[INFO] FLASK_APP=simple_app.py flask run --host 127.0.0.1 --port 5000 --no-debugger --no-reload")
    
    # Try with native HTTP server - NOT Werkzeug
    from wsgiref.simple_server import make_server, WSGIRequestHandler
    
    class Handler(WSGIRequestHandler):
        def log_message(self, format, *args):
            sys.stderr.write('[%s] %s\n' % (self.log_date_time_string(), format%args))
    
    try:
        httpd = make_server('127.0.0.1', 5000, app, handler_class=Handler)
        print("[INFO] Server started on http://127.0.0.1:5000 (non-Werkzeug)")
        httpd.serve_forever()
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
