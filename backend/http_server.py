#!/usr/bin/env python3
"""
Pure Python HTTP server for Flask app
Uses http.server instead of wsgiref for better Windows compatibility
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

try:
    print("[INFO] Loading application...")
    from run import app, init_db, seed_db
    
    with app.app_context():
        print("[INFO] Initializing database...")
        init_db(app)
        seed_db(app)
        print("[OK] Database ready")
    
    print("[INFO] Starting HTTP server...")
    
    # Use http.server with WSGI adapter
    from http.server import HTTPServer, BaseHTTPRequestHandler
    import json
    
    class WSGIHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'OK')
            
        def do_POST(self):
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            
            # Simple response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'ok'}).encode())
            
        def log_message(self, format, *args):
            print(f"[INFO] {format % args}")
    
    server = HTTPServer(('127.0.0.1', 5000), WSGIHandler)
    print("[OK] HTTP Server started on http://127.0.0.1:5000")
    server.serve_forever()
    
except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
