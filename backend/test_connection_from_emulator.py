#!/usr/bin/env python
"""Quick connection test untuk verify API accessibility"""
import requests
import time

# IP machine yang benar (sesuai dengan api_service.dart)
MACHINE_IP = "192.168.1.27"
PORT = "5000"
URL = f"http://{MACHINE_IP}:{PORT}"

def test_connection():
    """Test koneksi ke backend"""
    print("\n" + "="*70)
    print(f"  Testing Connection to Backend Server")
    print("="*70)
    print(f"\nBackend URL: {URL}")
    print(f"Machine IP:  {MACHINE_IP}")
    print(f"Port:        {PORT}")
    
    # Test health endpoint
    print("\n[1/3] Testing /health endpoint...")
    try:
        response = requests.get(f"{URL}/health", timeout=5)
        if response.status_code == 200:
            print("    Status: 200 OK")
            data = response.json()
            print(f"    Response: {data}")
            print("    ✓ PASS - Server is healthy")
        else:
            print(f"    Status: {response.status_code}")
            print("    ✗ FAIL")
    except requests.exceptions.Timeout:
        print("    ✗ TIMEOUT - Server not responding")
    except requests.exceptions.ConnectionError:
        print("    ✗ CONNECTION ERROR - Cannot reach server")
        print(f"    Make sure:")
        print(f"      1. Backend is running (python run.py)")
        print(f"      2. Emulator is on same WiFi network")
        print(f"      3. Firewall allows port {PORT}")
    except Exception as e:
        print(f"    ✗ ERROR: {e}")
    
    # Test root endpoint
    print("\n[2/3] Testing / endpoint...")
    try:
        response = requests.get(f"{URL}/", timeout=5)
        if response.status_code == 200:
            print("    Status: 200 OK")
            print("    ✓ PASS - API is accessible")
        else:
            print(f"    Status: {response.status_code}")
            print("    ✗ FAIL")
    except Exception as e:
        print(f"    ✗ ERROR: {e}")
    
    # Test login (Flutter akan gunakan ini)
    print("\n[3/3] Testing /login endpoint...")
    try:
        payload = {
            "email": "admin@bakesmart.com",
            "password": "admin123"
        }
        response = requests.post(
            f"{URL}/login",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        if response.status_code == 200:
            print("    Status: 200 OK")
            data = response.json()
            token = data.get('token', 'N/A')[:20] + "..."
            print(f"    Token: {token}")
            print("    ✓ PASS - Authentication working")
        else:
            print(f"    Status: {response.status_code}")
            print(f"    Response: {response.text}")
            print("    ✗ FAIL")
    except Exception as e:
        print(f"    ✗ ERROR: {e}")
    
    print("\n" + "="*70)
    print("  SUMMARY")
    print("="*70)
    print(f"""
If all 3 tests passed:
  ✓ Backend is working correctly
  ✓ Flutter app should connect successfully
  ✓ Your IP: {MACHINE_IP}
  
If tests failed:
  1. Check if backend is running: python run.py
  2. Verify IP address: ipconfig
  3. Check firewall settings
  4. Ensure emulator is on same WiFi network
""")
    print("="*70 + "\n")

if __name__ == "__main__":
    test_connection()
