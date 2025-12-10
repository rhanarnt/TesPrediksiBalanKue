#!/usr/bin/env python3
"""
Ultra-minimal test server to debug connection issues
"""
import socket

def simple_http_server():
    """Basic HTTP server without any framework"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('127.0.0.1', 5000))
    server_socket.listen(1)
    print("[OK] Socket server listening on 127.0.0.1:5000")
    
    try:
        while True:
            print("[INFO] Waiting for connection...")
            client_socket, address = server_socket.accept()
            print(f"[OK] Connection from {address}")
            
            data = client_socket.recv(1024).decode()
            print(f"[INFO] Request:\n{data}")
            
            response = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 7\r\n\r\nHello!\n"
            client_socket.send(response)
            client_socket.close()
            print("[OK] Response sent")
    except KeyboardInterrupt:
        print("[INFO] Shutting down...")
    finally:
        server_socket.close()

if __name__ == '__main__':
    simple_http_server()
