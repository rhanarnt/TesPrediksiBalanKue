# 🚀 Cara Menjalankan BakeSmart Application

## ✅ Status Saat Ini

- **Backend (Flask)**: ✅ Berjalan di http://127.0.0.1:5000
- **Frontend (Flutter)**: 🚀 Siap dijalankan
- **Database**: MySQL terkoneksi

## 📋 Prerequisite

- Python 3.8+
- Flutter SDK
- Chrome/Edge Browser (untuk web)
- MySQL Server

## 🔧 Konfigurasi API (Sudah Otomatis)

### Konfigurasi berdasarkan Platform:

```dart
// File: lib/services/api_service.dart
static String get baseUrl {
  if (kIsWeb) {
    return 'http://127.0.0.1:5000'; // Web: localhost
  } else if (Platform.isAndroid) {
    return 'http://10.0.2.2:5000';  // Android emulator
  } else {
    return 'http://127.0.0.1:5000'; // Desktop/iOS
  }
}
```

## 🎯 Cara Menjalankan

### **1. Jalankan Backend Flask**

```powershell
cd c:\fluuter.u\prediksi_stok_kue
python run.py
```

**Output yang diharapkan:**

```
[run] Starting Flask application...
[run] Routes: 18
[run] Server running on http://0.0.0.0:5000
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.1.19:5000
```

✅ Backend siap menerima request

### **2. Jalankan Flutter Application**

#### Opsi A: Web (Recommended untuk testing)

```powershell
cd c:\fluuter.u\prediksi_stok_kue\prediksi_stok_kue
flutter run -d chrome
```

#### Opsi B: Android Emulator

```powershell
cd c:\fluuter.u\prediksi_stok_kue\prediksi_stok_kue
flutter run -d emulator-5554
```

#### Opsi C: Windows Desktop

```powershell
cd c:\fluuter.u\prediksi_stok_kue\prediksi_stok_kue
flutter run -d windows
```

## 🔓 Login Credentials

### Default Test Account:

- **Email**: `test@example.com`
- **Password**: `password123`

### Buat User Baru (jika diperlukan):

Jalankan script di MySQL:

```sql
USE bakesmart_db;

INSERT INTO users (name, email, password, created_at, updated_at)
VALUES (
  'Test User',
  'test@example.com',
  '5e884898da28047151d0e56f8dc62927945b2d3d74d312450e4e3077c91ebc01',
  NOW(),
  NOW()
);
```

**Password hash**: `password123` (SHA256)

## ⚠️ Solusi Error "Koneksi Timeout"

### **Masalah**: Login terus timeout

### **Penyebab**:

- Backend belum running
- URL backend tidak benar
- Firewall blocking

### **Solusi**:

#### 1️⃣ **Pastikan Backend Berjalan**

```powershell
# Check apakah server sudah running
curl http://127.0.0.1:5000
```

Jika dapat response 200, backend OK ✅

#### 2️⃣ **Test Endpoint Login Manual**

```powershell
$body = @{
    email = "test@example.com"
    password = "password123"
} | ConvertTo-Json

curl -X POST http://127.0.0.1:5000/login `
  -Headers @{"Content-Type"="application/json"} `
  -Body $body
```

Expected response:

```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "name": "Test User",
    "email": "test@example.com"
  }
}
```

#### 3️⃣ **Check Firewall Windows**

```powershell
# Allow port 5000
netsh advfirewall firewall add rule name="Allow Flask" dir=in action=allow protocol=tcp localport=5000
```

#### 4️⃣ **Increase Timeout (jika server lambat)**

Edit file `lib/pages/login_page.dart`:

```dart
// Ubah dari 10 detik menjadi 30 detik
.timeout(
  const Duration(seconds: 30),  // ← Ubah angkanya
  onTimeout: () {
    throw TimeoutException(
      'Koneksi ke server timeout. Silakan coba lagi.'
    );
  },
)
```

## 📊 Database Setup

### Create Database:

```sql
CREATE DATABASE bakesmart_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Tables auto-created by Flask pada first run

## 🧪 Testing Endpoints

### Test endpoint stok:

```powershell
$headers = @{
    "Authorization" = "Bearer YOUR_TOKEN_HERE"
    "Content-Type" = "application/json"
}
curl -X GET http://127.0.0.1:5000/stok -Headers $headers
```

### Test endpoint prediksi:

```powershell
$body = @{
    bahan_id = 1
    jumlah = 10
} | ConvertTo-Json

curl -X POST http://127.0.0.1:5000/prediksi `
  -Headers @{
    "Authorization" = "Bearer YOUR_TOKEN_HERE"
    "Content-Type" = "application/json"
  } `
  -Body $body
```

## 🐛 Debugging

### Enable Flutter Debug Logging:

```powershell
flutter run -d chrome --verbose
```

### View Backend Logs:

Backend Flask akan show semua request/response di terminal

### Check Network in Browser:

1. Buka DevTools (F12)
2. Buka tab Network
3. Lihat request dan response ke API

## ❌ Common Issues & Solutions

| Issue                | Solusi                                          |
| -------------------- | ----------------------------------------------- |
| `Connection refused` | Backend belum running, jalankan `python run.py` |
| `Koneksi timeout`    | Check firewall, atau increase timeout value     |
| `401 Unauthorized`   | Token expired atau invalid, login ulang         |
| `404 Not Found`      | Endpoint tidak ada atau URL salah               |
| `500 Internal Error` | Check backend logs untuk detail error           |

## 🎉 Verify Installation

Jalankan command berikut untuk verify semua berjalan OK:

```powershell
# Terminal 1: Check Backend
curl http://127.0.0.1:5000 -v

# Terminal 2: Check Flutter Web
flutter run -d chrome

# Browser: Coba login dengan test@example.com / password123
```

---

**Happy Coding! 🚀**
