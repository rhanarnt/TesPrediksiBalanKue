# Backend Status & Connection Info

## Backend Server

**Status**: ✅ RUNNING

**Addresses**:

- Local: `http://127.0.0.1:5000`
- Network: `http://192.168.1.11:5000`

**Running Endpoints** (18 total):

- `GET /` - API Status
- `POST /login` - **AUTHENTICATION** ← NEW
- `GET /health` - Health check
- `POST /prediksi` - ML Prediction
- `GET /stock` - Stock list
- `POST /stock` - Stock CRUD
- `GET /history` - Prediction history
- `+ 11 more endpoints`

---

## Flutter Configuration

**API Service Updated**: ✅

**File**: `prediksi_stok_kue/lib/services/api_service.dart`

**Base URLs**:

```dart
Web/Desktop: http://127.0.0.1:5000
Android Emulator: http://localhost:5000 (dengan ADB reverse)
```

**No `/api` suffix** ← Fixed!

---

## Login Credentials

```
Email: admin@bakesmart.com
Password: admin123
```

---

## To Test Login

### Option 1: Flutter App

Run Flutter, go to login page, enter credentials above

### Option 2: Command Line

```powershell
$body = '{"email":"admin@bakesmart.com","password":"admin123"}'
Invoke-WebRequest -Uri "http://127.0.0.1:5000/login" -Method POST -ContentType "application/json" -Body $body -UseBasicParsing
```

---

## Expected Response

```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "email": "admin@bakesmart.com",
    "name": "Admin BakeSmart"
  }
}
```

**Status Code**: `200 OK`

---

## To Keep Backend Running

Backend is running in background. Terminal ID: `1ffb9c65-497e-4436-b345-a90772c3c69d`

If it crashes, restart with:

```powershell
cd c:\fluuter.u\prediksi_stok_kue
.\.venv\Scripts\python.exe run.py
```

---

**Date**: January 20, 2026
**Project**: BakeSmart - Prediksi Stok Kue
