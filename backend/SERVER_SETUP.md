# Backend Server Setup Guide

## Quick Start (Development)

### Method 1: Using Flask Test Client (Recommended for Testing)

```bash
cd backend
python test_endpoints.py
```

This runs all endpoint tests without needing an HTTP server. Good for verifying API works correctly.

### Method 2: Direct Flask Run (Simple)

```bash
cd backend
python run.py
```

Note: On Windows, the server may have stability issues with HTTP requests. This is a known Werkzeug/Windows socket issue.

### Method 3: Using test_api.py (If Python requests installed)

```bash
cd backend
python test_api.py
```

## Production Deployment

### Option A: Docker (Recommended)

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:5000", "run:app"]
```

Build and run:

```bash
docker build -t bakesmart .
docker run -p 5000:5000 bakesmart
```

### Option B: Gunicorn (Linux/Mac)

```bash
pip install gunicorn
gunicorn --workers 4 --bind 0.0.0.0:5000 run:app
```

### Option C: Waitress (Windows)

```bash
pip install waitress
python -m waitress --port=5000 run:app
```

## Android Device Testing

### Using ADB Port Forwarding

```bash
# Connect Android device via USB and enable Developer Mode

# Forward port 5000 from device to host
adb forward tcp:5000 tcp:5000

# Now Flutter APK can access localhost:5000
```

### Using Device IP Address

1. Find your PC's IP: `ipconfig`
2. Update Flutter app URL from `http://127.0.0.1:5000` to `http://YOUR_PC_IP:5000`
3. Make sure PC firewall allows port 5000

## API Endpoints

All endpoints require JWT token (except /health and /login):

- `GET /health` - Health check
- `POST /login` - Login (returns JWT token)
- `GET /stok` - Get list of bahan (ingredients)
- `GET /stock-records` - Get all input/output history
- `POST /stock-record` - Add new stock record
- `POST /logout` - Logout

## Testing

### Run All Tests

```bash
python test_endpoints.py
```

### Test Specific Endpoint

```bash
python test_api.py
```

## Troubleshooting

### "Connection refused" on Windows

This is due to Windows socket select() issues with certain Python/Werkzeug versions.

- Solution: Use Waitress (`pip install waitress; python -m waitress --port=5000 run:app`)
- Or use Docker
- Or test with `test_endpoints.py` instead

### "ModuleNotFoundError"

Install requirements:

```bash
pip install -r requirements.txt
```

### "Database locked"

Kill any other Python processes using the database:

```bash
# Windows
taskkill /IM python.exe /F

# Linux/Mac
pkill -f python
```

## Notes

- Database is auto-initialized on startup
- Default user: admin@bakesmart.com / admin123
- JWT token expires after 1 hour
- All responses are JSON format
