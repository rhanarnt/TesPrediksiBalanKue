#!/usr/bin/env python
"""Test dengan HTTP module built-in"""
import http.server
import socketserver
import json
import threading
import time

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(b'{"ok": true}')
        print("[server] GET handled")
    
    def do_POST(self):
        print("[server] POST received")
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        print(f"[server] Body: {body}")
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(b'{"ok": true}')
        print("[server] POST handled")
    
    def log_message(self, format, *args):
        pass  # Suppress default logs

def start_server():
    with socketserver.TCPServer(("127.0.0.1", 5003), MyHandler) as httpd:
        print("[server] Listening on 127.0.0.1:5003")
        httpd.handle_request()
        httpd.handle_request()

print("[main] Starting server...")
thread = threading.Thread(target=start_server, daemon=True)
thread.start()

time.sleep(1)

print("[main] Testing GET...")
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 5003))
sock.sendall(b"GET / HTTP/1.1\r\nHost: 127.0.0.1\r\n\r\n")
response = sock.recv(1024)
print(f"[main] GET response: {response[:100]}")
sock.close()

time.sleep(1)

print("[main] Testing POST...")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 5003))
body = b'{"test": "data"}'
request = (
    b"POST / HTTP/1.1\r\n"
    b"Host: 127.0.0.1\r\n"
    b"Content-Type: application/json\r\n"
    b"Content-Length: " + str(len(body)).encode() + b"\r\n"
    b"\r\n"
    + body
)
print(f"[main] Sending: {request}")
sock.sendall(request)
response = sock.recv(1024)
print(f"[main] POST response: {response[:100]}")
sock.close()

thread.join(timeout=5)
print("[main] Test complete")
