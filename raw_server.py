#!/usr/bin/env python
"""Simple raw socket server untuk test"""
import socket
import threading
import json

def handle_request(conn):
    try:
        print("[raw] Connected", flush=True)
        # Receive request
        data = conn.recv(4096)
        print(f"[raw] Received: {data[:100]}", flush=True)
        
        # Parse
        lines = data.decode().split('\r\n')
        method = lines[0].split()[0]
        path = lines[0].split()[1]
        
        print(f"[raw] Method: {method}, Path: {path}", flush=True)
        
        # For POST, extract body
        if method == "POST":
            # Find empty line separator
            sep_idx = 0
            for i, line in enumerate(lines):
                if line == '':
                    sep_idx = i
                    break
            
            if sep_idx < len(lines) - 1:
                body = '\r\n'.join(lines[sep_idx+1:])
                print(f"[raw] Body: {body}", flush=True)
        
        # Send response
        response = b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: 16\r\n\r\n{\"ok\": true}"
        conn.sendall(response)
        print("[raw] Response sent", flush=True)
    except Exception as e:
        print(f"[raw] Error: {e}", flush=True)
    finally:
        conn.close()

def server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("127.0.0.1", 5008))
    sock.listen(5)
    print("[raw] Listening on 127.0.0.1:5008", flush=True)
    
    while True:
        conn, addr = sock.accept()
        thread = threading.Thread(target=handle_request, args=(conn,))
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    server()
