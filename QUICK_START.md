# 🍰 BakeSmart - Quick Start Guide

## ⚡ Quick Start (Recommended)

### 1. Run Everything dengan 1 Click

```bash
START_ALL.bat
```

Ini akan otomatis:

- ✅ Start Backend Server (Flask)
- ✅ Start Flutter on Android Emulator
- ✅ Initialize database jika belum ada

**Selesai! Tinggal buka aplikasi di emulator dan login**

---

## 📋 Startup Manual (Jika perlu)

### Option 1: Backend Only

```bash
START_BACKEND.bat
```

### Option 2: Flutter Only (pastikan backend sudah running)

```bash
START_FLUTTER.bat
```

---

## 👤 Default Login Credentials

```
Email: admin@bakesmart.com
Password: admin123
```

---

## 🔗 API Endpoints

### Dari Android Emulator

```
http://10.0.2.2:5000/api
```

### Dari PC/Browser

```
http://127.0.0.1:5000/api
http://192.168.1.20:5000/api
```

### Database

```
Database: prediksi_stok_kue
Host: localhost
User: root
Password: (kosong)
Access: http://localhost/phpmyadmin
```

---

## 🛠️ Manual Setup (Jika diperlukan)

### 1. Start Backend Manually

```bash
cd prediksi_stok_kue\backend
python start.py
```

### 2. Start Flutter Manually

```bash
cd prediksi_stok_kue
flutter run -d emulator-5554
```

---

## ✅ Verification Checklist

- [ ] Android Emulator sudah running
- [ ] MySQL/phpMyAdmin sudah running
- [ ] Backend server listening di port 5000
- [ ] Flutter app bisa connect ke backend
- [ ] Login berhasil dengan admin@bakesmart.com / admin123

---

## 🐛 Troubleshooting

### Connection Timeout di Emulator

**Problem**: "Koneksi timeout. Periksa apakah server berjalan."

**Solution**:

1. Pastikan backend running: `python start.py` di folder backend
2. Pastikan emulator bisa ping host: `adb shell ping 10.0.2.2`
3. Check firewall Windows - port 5000 harus terbuka

### MySQL Connection Error

**Problem**: "Can't connect to MySQL server"

**Solution**:

1. Buka phpMyAdmin: http://localhost/phpmyadmin
2. Pastikan database `prediksi_stok_kue` sudah exist
3. Jika belum, backend akan auto-create saat startup

### Flutter Build Error

**Problem**: "Flutter build failed"

**Solution**:

```bash
cd prediksi_stok_kue
flutter clean
flutter pub get
flutter run
```

---

## 📁 Project Structure

```
prediksi_stok_kue/
├── backend/              # Flask API Server
│   ├── start.py         # ⭐ Use this to start backend
│   ├── run.py           # Main Flask app
│   ├── database.py      # Database models
│   └── ...
├── prediksi_stok_kue/   # Flutter mobile app
│   ├── lib/             # Source code
│   ├── pubspec.yaml     # Dependencies
│   └── ...
├── START_ALL.bat        # ⭐ Click this to start everything
├── START_BACKEND.bat    # Start backend only
└── START_FLUTTER.bat    # Start flutter only
```

---

## 🎯 For Presentation

**Sebelum presentasi:**

1. Test dengan `START_ALL.bat`
2. Pastikan emulator bisa login
3. Test beberapa features
4. Biarkan backend running di background
5. Presentasikan dari Flutter emulator

**Jika perlu restart:**

- Close emulator window
- Backend akan terus running
- Run `START_FLUTTER.bat` lagi

---

## 📞 Important Notes

- Backend harus tetap running selama development
- Database otomatis di-create jika belum ada
- Default login credentials disimpan di database
- Setiap kali startup, semua credentials sudah tersedia

**Lebih detail? Baca file dokumentasi lain:**

- `prediksi_stok_kue/README.md` - Flutter setup
- `prediksi_stok_kue/backend/README.md` - Backend setup
