# 🍰 BakeSmart - Setup & Run Guide

## ✅ Status Backend

Backend server **SUDAH BERHASIL DIKONFIGURASI** dan siap digunakan!

## 🚀 Cara Menjalankan Project

### **CARA PALING MUDAH** (Recommended untuk Presentasi)

Buka folder root project, double-click file ini:

```
START_ALL.bat
```

File ini akan **otomatis**:

1. ✅ Start Backend Server (port 5000)
2. ✅ Initialize MySQL Database
3. ✅ Start Flutter App di Android Emulator

**Selesai! Tinggal tunggu sampai aplikasi muncul di emulator.**

---

## 📋 Alternative: Manual Startup

Jika ingin startup manual atau debug, ikuti langkah ini:

### Step 1: Start Backend

```bash
# Buka terminal di folder project root
cd prediksi_stok_kue\backend
python start.py
```

Tunggu hingga melihat:

```
======================================================================
✅ Server ready!
======================================================================
```

### Step 2: Start Flutter App

```bash
# Buka terminal baru di folder project root
cd prediksi_stok_kue
flutter run -d emulator-5554
```

Atau double-click:

```
START_FLUTTER.bat
```

---

## 👤 Default Login Credentials

Setelah aplikasi terbuka, login dengan:

```
Email: admin@bakesmart.com
Password: admin123
```

Credentials ini **sudah tersimpan di database** secara otomatis saat backend startup.

---

## 🔗 API Information

### Untuk Android Emulator

```
Base URL: http://10.0.2.2:5000/api
```

### Dari PC/Browser

```
Base URL: http://127.0.0.1:5000/api
IP Lokal: http://192.168.1.20:5000/api
```

---

## 🗄️ Database Information

- **Type**: MySQL/MariaDB
- **Database Name**: `prediksi_stok_kue`
- **Host**: localhost (127.0.0.1)
- **User**: root
- **Password**: (kosong/empty)
- **Port**: 3306
- **Access via**: http://localhost/phpmyadmin

Database **otomatis di-create** saat backend startup jika belum ada.

---

## 📁 Project Structure

```
prediksi_stok_kue/                    # Root folder
├── START_ALL.bat                     # ⭐ CLICK THIS!
├── START_BACKEND.bat                 # Start backend only
├── START_FLUTTER.bat                 # Start Flutter only
├── QUICK_START.md                    # Dokumentasi lengkap
│
├── prediksi_stok_kue/                # Flutter mobile app
│   ├── lib/                          # Source code
│   ├── pubspec.yaml                  # Dependencies
│   ├── README.md                     # Flutter setup details
│   └── ...
│
└── prediksi_stok_kue/backend/        # Flask API Server
    ├── start.py                      # ⭐ Script startup (recommended)
    ├── run.py                        # Main Flask application
    ├── database.py                   # Database models & setup
    ├── routes.py                     # API endpoints
    ├── requirements.txt              # Python dependencies
    ├── README.md                     # Backend setup details
    └── ...
```

---

## ✅ Troubleshooting

### 1. **Koneksi Timeout di Emulator**

**Error**: "Koneksi timeout. Periksa apakah server berjalan."

**Solusi**:

- Pastikan Backend Server sudah running dengan `START_BACKEND.bat`
- Pastikan MySQL sudah running (port 3306)
- Cek firewall Windows - pastikan port 5000 tidak di-block
- Coba restart Android Emulator

### 2. **MySQL Connection Error**

**Error**: "Can't connect to MySQL server"

**Solusi**:

1. Pastikan MySQL/MariaDB sudah running
2. Buka phpMyAdmin: http://localhost/phpmyadmin
3. Database akan auto-create saat backend startup
4. Jika error, cek di phpMyAdmin apakah database `prediksi_stok_kue` ada

### 3. **Flutter Build/Run Error**

**Error**: "Flutter build failed"

**Solusi**:

```bash
cd prediksi_stok_kue
flutter clean
flutter pub get
flutter run -d emulator-5554
```

### 4. **Python/Dependencies Error**

**Error**: "ModuleNotFoundError" atau error import

**Solusi**:

```bash
cd prediksi_stok_kue/backend
pip install -r requirements.txt
```

---

## 🎯 For Presentations / Demo

**Sebelum presentasi:**

1. ✅ Jalankan `START_ALL.bat`
2. ✅ Tunggu hingga Flutter app muncul
3. ✅ Test login dengan `admin@bakesmart.com` / `admin123`
4. ✅ Test beberapa features
5. ✅ Siap presentasi!

**Tips:**

- Jangan close terminal backend (biarkan berjalan di background)
- Jika emulator crash, cukup close emulator window
- Backend akan tetap running, tinggal buka ulang emulator
- Jika perlu restart, close semua dan jalankan `START_ALL.bat` lagi

---

## 📞 Important Notes

1. **Backend harus selalu running** saat menggunakan aplikasi Flutter
2. **MySQL harus aktif** (biasanya auto-start di Windows)
3. **Android Emulator** harus sudah dijalankan sebelum `START_ALL.bat`
4. **Database auto-initialize** - tidak perlu setup manual
5. **Semua credentials sudah tersedia** - tinggal login

---

## 🔧 Manual Database Setup (Jika diperlukan)

Jika database tidak auto-create, bisa manual dengan:

```sql
-- Login ke MySQL
mysql -u root

-- Buat database
CREATE DATABASE prediksi_stok_kue;

-- Backend akan auto-create tables saat startup
```

---

## 📚 More Information

- **Flutter Setup**: Lihat `prediksi_stok_kue/README.md`
- **Backend Setup**: Lihat `prediksi_stok_kue/backend/README.md`
- **API Documentation**: Lihat `prediksi_stok_kue/backend/API_REFERENCE.md`
- **Quick Start**: Lihat `QUICK_START.md`

---

## ✨ Summary

| Task                 | Command                        | Status         |
| -------------------- | ------------------------------ | -------------- |
| **Start Everything** | `START_ALL.bat`                | ✅ Ready       |
| **Backend Server**   | `python start.py`              | ✅ Ready       |
| **Flutter App**      | `flutter run -d emulator-5554` | ✅ Ready       |
| **Database**         | MySQL `prediksi_stok_kue`      | ✅ Auto-create |
| **Login**            | admin@bakesmart.com / admin123 | ✅ Available   |
| **API URL**          | http://10.0.2.2:5000/api       | ✅ Ready       |

**Semua sudah dikonfigurasi. Tinggal run dan presentasi! 🎉**
