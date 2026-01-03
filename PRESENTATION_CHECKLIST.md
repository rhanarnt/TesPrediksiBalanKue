# 📋 CHECKLIST - Sebelum Presentasi

## ✅ SUDAH DIKERJAKAN:

- [x] Backend server dikonfigurasi dengan MySQL
- [x] Database connection tested dan working
- [x] Flask API server berjalan di port 5000
- [x] Android Emulator URL configured (10.0.2.2:5000)
- [x] Startup script dibuat (start.py)
- [x] Batch files dibuat untuk 1-click startup
- [x] Default credentials tersimpan di database
- [x] Documentation lengkap dibuat
- [x] Error handling ditambahkan

## 🎯 SEBELUM PRESENTASI - CHECKLIST:

```
□ Buka Android Emulator terlebih dahulu
  (AVD: Medium_Phone_API_36)

□ Run: START_ALL.bat
  ATAU: python prediksi_stok_kue/backend/start.py

□ Tunggu sampai Flutter app muncul di emulator

□ Login dengan:
  Email: admin@bakesmart.com
  Password: admin123

□ Test beberapa fitur:
  - Lihat dashboard
  - Input data stok
  - Lihat prediksi
  - Test search/filter

□ Pastikan tidak ada error messages

□ Backend tetap berjalan (jangan close terminal)

□ Siap untuk presentasi! 🎉
```

## 🔍 VERIFICATION:

Buka terminal baru dan test:

```powershell
# Test backend running
curl http://127.0.0.1:5000/api

# Test database
curl http://127.0.0.1:5000/api/login -Method POST `
  -Body '{"email":"admin@bakesmart.com","password":"admin123"}' `
  -ContentType "application/json"
```

## 📱 TEST DI EMULATOR:

1. Pastikan emulator connected:

   ```
   adb devices
   ```

2. Lihat logs:
   ```
   adb logcat
   ```

## 🛠️ JIKA ADA MASALAH:

| Problem               | Solution                                  |
| --------------------- | ----------------------------------------- |
| Koneksi timeout       | Pastikan backend running                  |
| MySQL error           | Buka phpMyAdmin & check database          |
| Flutter build error   | flutter clean && flutter pub get          |
| Port 5000 busy        | taskkill /F /PID (cari dengan netstat)    |
| Emulator tidak muncul | Buka AVD Manager & launch emulator manual |

## 📊 EXPECTED OUTPUT:

Setelah run `python start.py`:

```
======================================================================
🍰 BakeSmart Backend Server
======================================================================

📊 Checking MySQL connection...
✅ Connected to prediksi_stok_kue database

📦 Initializing database...
✅ Database initialized
✅ Initial data seeded

======================================================================
✅ Server ready!
======================================================================

 * Running on http://127.0.0.1:5000
 * Running on http://192.168.1.20:5000
Press CTRL+C to quit
```

## 🎬 PRESENTATION FLOW:

1. Start backend (START_ALL.bat)
2. Show login screen
3. Login dengan credentials
4. Show dashboard
5. Demo features:
   - Input data baru
   - Lihat prediksi
   - Batch view
   - Reports
6. Show database (phpMyAdmin)
7. Explain architecture

## 💾 BACKUP IMPORTANT:

```
✅ Database: c:\xampp\mysql\data\prediksi_stok_kue
✅ Backend: prediksi_stok_kue/backend/
✅ Flutter: prediksi_stok_kue/
✅ Config: .env files (if any)
```

## 🚀 QUICK START COMMANDS:

```bash
# Start everything
START_ALL.bat

# OR start backend only
cd prediksi_stok_kue\backend
python start.py

# OR start flutter only (backend harus already running)
cd prediksi_stok_kue
flutter run -d emulator-5554 --no-fast-start
```

## ⚠️ IMPORTANT NOTES:

- **Backend HARUS tetap running** saat presentasi
- **Jangan close terminal backend** - biarkan di background
- **Emulator bisa di-close** - backend tetap jalan
- **Database auto-backup** - tidak perlu setup
- **Credentials sudah tersimpan** - tinggal login

---

**Status: ✅ READY FOR PRESENTATION**

Tinggal klik START_ALL.bat dan siap presentasi! 🎉
