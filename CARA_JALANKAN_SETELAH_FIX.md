# 🚀 CARA MENJALANKAN BAKESMART SETELAH FIX

## ✅ MASALAH SUDAH DIPERBAIKI

IP address di Flutter app sudah diupdate dari `192.168.1.20` → `192.168.1.27` (IP machine yang benar).

Backend server sudah **TESTED & VERIFIED** - semua endpoint working 100%.

---

## 📋 CHECKLIST SEBELUM JALANKAN

- [x] Backend IP address: **192.168.1.27** (CORRECT)
- [x] Backend port: **5000** (CORRECT)
- [x] Backend server running: **http://192.168.1.27:5000**
- [x] Android Emulator running: **Medium_Phone_API_36**
- [x] Emulator connected ke WiFi: **SAMA DENGAN MACHINE**
- [x] Firewall: **Allow Python/Port 5000**

---

## 🎯 LANGKAH-LANGKAH MENJALANKAN

### STEP 1️⃣: Start Backend Server

```powershell
# Di PowerShell/CMD:
cd C:\fluuter.u\prediksi_stok_kue\backend
python run.py
```

**Output yang diharapkan:**

```
[OK] Database initialized successfully
[INFO] Database already seeded
BakeSmart Backend Server
Database initialized

 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.1.27:5000
```

✅ Tunggu sampai melihat output di atas sebelum lanjut ke step 2.

---

### STEP 2️⃣: Start Android Emulator

```powershell
# Di PowerShell baru, jalankan emulator:
emulator -avd Medium_Phone_API_36 -netdelay none -netspeed full -accel auto
```

Atau buka dari Android Studio > Virtual Device Manager > Launch "Medium_Phone_API_36"

**Tunggu sampai:** Emulator boot selesai (±30 detik)

---

### STEP 3️⃣: Run Flutter App

```powershell
# Di PowerShell baru, di folder project:
cd C:\fluuter.u\prediksi_stok_kue\prediksi_stok_kue
flutter run -d emulator-5554
```

Atau:

```powershell
# Lebih simple (jika hanya ada 1 emulator):
flutter run
```

**Proses:**

1. Flutter akan compile app (~2-3 menit first time)
2. App akan automatically install ke emulator
3. App akan launch di emulator

---

### STEP 4️⃣: Login ke App

Saat app sudah muncul, tekan tombol **"Masuk"** dan gunakan:

```
Email:    admin@bakesmart.com
Password: admin123
```

**Harusnya:**
✅ Tidak ada error "Koneksi timeout"
✅ Login berhasil dan masuk ke halaman utama
✅ Daftar bahan muncul

---

## 🔄 JIKA SUDAH RUNNING (Hot Restart)

Setelah app running pertama kali, untuk perubahan code:

```powershell
# Di terminal flutter (yang running app):
R  - Hot reload (cepat, tapi reload class bisa error)
r  - Hot restart (lebih aman)
q  - Quit
```

Atau langsung close dan `flutter run` lagi.

---

## 🧪 VERIFIKASI KONEKSI

### Cek dari Terminal:

```powershell
# Test health endpoint:
Invoke-WebRequest -Uri http://192.168.1.27:5000/health -UseBasicParsing

# Harusnya return 200 OK dengan JSON response
```

### Cek dari Emulator:

Aplikasi akan otomatis test koneksi saat:

- Startup
- Klik "Masuk"
- Akses menu apapun

Jika ada error "Koneksi timeout", lihat bagian **TROUBLESHOOTING** di bawah.

---

## 🚨 TROUBLESHOOTING

### Problem 1: "Koneksi timeout" di app

**Kemungkinan penyebab:**

1. Backend server tidak running
2. IP address salah
3. Emulator tidak bisa akses WiFi

**Solusi:**

```powershell
# 1. Pastikan backend running:
Invoke-WebRequest -Uri http://192.168.1.27:5000/health

# 2. Verifikasi IP machine Anda:
ipconfig
# Lihat IPv4 Address (harus 192.168.1.27)

# 3. Di emulator, cek Network settings:
# Emulator > Extended controls > Network
# Pastikan DNS dan routing sudah benar

# 4. Restart emulator:
emulator -avd Medium_Phone_API_36 -netdelay none -netspeed full
```

### Problem 2: "Flutter run" tidak menemukan emulator

```powershell
# List emulator yang available:
flutter devices

# Jika tidak ada, start emulator terlebih dahulu
```

### Problem 3: App crash saat login

1. Check console output Flutter
2. Make sure backend server running
3. Restart app: tekan `r` di terminal flutter

### Problem 4: "Failed to connect to..."

Ini berarti emulator tidak bisa reach IP 192.168.1.27:

```powershell
# Di emulator:
adb shell ping 192.168.1.27
# Jika "Destination Host Unreachable", emulator tidak bisa akses network machine

# Solusi:
# 1. Pastikan emulator WiFi sama dengan machine
# 2. Check firewall Windows: Settings > Firewall > Allow Python
# 3. Restart emulator dan machine
```

---

## 📊 NETWORK SUMMARY

```
┌─ MACHINE ──────────────────────┐
│ IP: 192.168.1.27               │
│ WiFi: Connected                │
│ Python Backend: Port 5000       │
└────────────────────────────────┘
          ↓ (Network Connection)
┌─ ANDROID EMULATOR ─────────────┐
│ Connected to: Same WiFi Network │
│ Backend URL: 192.168.1.27:5000  │
│ Flutter App: Running            │
└────────────────────────────────┘
```

---

## ✅ SUCCESS INDICATORS

Jika berhasil, Anda akan melihat:

✅ App muncul di emulator
✅ Splash screen "BakeSmart" muncul
✅ Login screen muncul tanpa error
✅ Bisa login dengan admin@bakesmart.com
✅ Halaman utama menampilkan daftar bahan
✅ Tidak ada error timeout/connection

---

## 📝 NOTES

- Backend IP: **192.168.1.27** (bukan 192.168.1.20!)
- Backend Port: **5000**
- Flutter API Base: `http://192.168.1.27:5000/api`
- Jangan gunakan `10.0.2.2` - itu hanya untuk direct localhost
- Jangan gunakan `127.0.0.1` dari emulator - itu localhost emulator, bukan machine

---

## 🎯 NEXT STEPS

Setelah app berhasil running:

1. **Test fitur prediksi** - Input data stok
2. **Check berbagai screen** - Navigate app
3. **Lakukan perubahan code** - Hot reload/restart
4. **Final testing** - Semua fitur berjalan

---

**Status:** ✅ READY TO RUN
**Updated:** 2026-01-04 21:35:08
**Machine IP:** 192.168.1.27
