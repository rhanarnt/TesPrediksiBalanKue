#!/usr/bin/env python3
"""
Stable Flask server for Windows using custom HTTP implementation
Avoids Werkzeug and wsgiref issues on Windows
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import TCPServer
import io
import json
from urllib.parse import urlparse, parse_qs

# Load Flask app
from run import app, init_db, seed_db

print("[INFO] Initializing database...")
with app.app_context():
    init_db(app)
    seed_db(app)
print("[OK] Database initialized")


class WSGIHandler(BaseHTTPRequestHandler):
    """Simple WSGI adapter for Flask app"""
    
    def do_GET(self):
        self._handle_request('GET')
    
    def do_POST(self):
        self._handle_request('POST')
    
    def do_PUT(self):
        self._handle_request('PUT')
    
    def do_DELETE(self):
        self._handle_request('DELETE')
    
    def do_OPTIONS(self):
        self._handle_request('OPTIONS')
    
    def _handle_request(self, method):
        try:
            # Parse request
            environ = {
                'REQUEST_METHOD': method,
                'SCRIPT_NAME': '',
                'PATH_INFO': self.path.split('?')[0],
                'QUERY_STRING': self.path.split('?')[1] if '?' in self.path else '',
                'CONTENT_TYPE': self.headers.get('Content-Type', ''),
                'CONTENT_LENGTH': self.headers.get('Content-Length', '0'),
                'SERVER_NAME': 'localhost',
                'SERVER_PORT': '5000',
                'SERVER_PROTOCOL': 'HTTP/1.1',
                'wsgi.version': (1, 0),
                'wsgi.url_scheme': 'http',
                'wsgi.input': io.BytesIO(self._get_body()),
                'wsgi.errors': sys.stderr,
                'wsgi.multithread': True,
                'wsgi.multiprocess': False,
                'wsgi.run_once': False,
            }
            
            # Add headers to environ
            for header, value in self.headers.items():
                header = header.upper().replace('-', '_')
                if header not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
                    header = f'HTTP_{header}'
                environ[header] = value
            
            # Call Flask app
            status = None
            response_headers = []
            
            def start_response(stat, hdrs):
                nonlocal status, response_headers
                status = stat
                response_headers = hdrs
                return lambda x: None
            
            response = app.wsgi_app(environ, start_response)
            
            # Extract status code
            status_code = int(status.split(' ')[0])
            
            # Send response
            self.send_response(status_code)
            for header, value in response_headers:
                self.send_header(header, value)
            self.end_headers()
            
            # Send body
            for chunk in response:
                self.wfile.write(chunk)
                
        except Exception as e:
            print(f"[ERROR] {e}")
            self.send_error(500, str(e))
    
    def _get_body(self):
        """Get request body"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                return self.rfile.read(content_length)
        except:
            pass
        return b''
    
    def log_message(self, format, *args):
        """Custom logging"""
        print(f"[INFO] {self.client_address[0]} {format % args}")


class ReuseAddrTCPServer(TCPServer):
    """TCP Server that allows address reuse"""
    allow_reuse_address = True


def run_server():
    """Run the server"""
    try:
        print("[INFO] Starting stable server...")
        server = ReuseAddrTCPServer(('127.0.0.1', 5000), WSGIHandler)
        print("[OK] Server running on http://127.0.0.1:5000")
        print("[INFO] Press Ctrl+C to quit")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[INFO] Shutting down...")
        server.shutdown()
        sys.exit(0)
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    run_server()
