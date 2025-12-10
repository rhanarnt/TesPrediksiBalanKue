#!/usr/bin/env python3
"""
Ultra-stable backend server for Windows Android Emulator
Uses simple HTTP server with threading
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from run import app, init_db, seed_db
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
import json
from urllib.parse import parse_qs
import traceback

print("[INFO] Initializing database...")
with app.app_context():
    init_db(app)
    seed_db(app)
print("[OK] Database initialized")

class FlaskRequestHandler(BaseHTTPRequestHandler):
    """Delegate to Flask app"""
    def do_GET(self):
        with app.test_client() as client:
            response = client.get(self.path)
            self.send_response(response.status_code)
            for header, value in response.headers:
                self.send_header(header, value)
            self.end_headers()
            self.wfile.write(response.data)
    
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            
            with app.test_client() as client:
                response = client.post(
                    self.path,
                    data=body,
                    headers=dict(self.headers),
                    content_type=self.headers.get('Content-Type', 'application/json')
                )
                self.send_response(response.status_code)
                for header, value in response.headers:
                    self.send_header(header, value)
                self.end_headers()
                self.wfile.write(response.data)
        except Exception as e:
            print(f"[ERROR] POST error: {e}")
            traceback.print_exc()
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    
    def log_message(self, format, *args):
        # Reduce spam
        pass

if __name__ == '__main__':
    print("[INFO] Starting HTTP server with Flask test client...")
    print("[OK] Server running on http://127.0.0.1:5000")
    print("[OK] Android Emulator: use http://10.0.2.2:5000")
    print("[INFO] Press Ctrl+C to quit\n")
    
    try:
        server = HTTPServer(('127.0.0.1', 5000), FlaskRequestHandler)
        print("[OK] HTTP Server initialized")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[INFO] Shutting down...")
        sys.exit(0)
    except Exception as e:
        print(f"[ERROR] {e}")
        traceback.print_exc()
        sys.exit(1)
