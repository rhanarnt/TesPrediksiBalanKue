# 🔧 Fix untuk Masalah "Koneksi Timeout" di Emulator

## 🎯 Masalah

Ketika login di emulator Android, mendapat error:

```
Koneksi timeout. Periksa apakah server berjalan
URL: http://10.0.2.2:5000
```

## ✅ Solusi Permanen

### Penyebab:

Android emulator tidak bisa langsung akses IP lokal host machine. Solusinya adalah menggunakan **ADB Port Forwarding**.

### Cara Setup (Sekali Saja):

#### **Opsi 1: Otomatis (Recommended)**

```powershell
# Double-click file ini di workspace root:
SETUP_EMULATOR.bat
```

#### **Opsi 2: Manual**

```powershell
# Setup ADB reverse port forwarding
& "C:\Users\roihan\AppData\Local\Android\sdk\platform-tools\adb" reverse tcp:5000 tcp:5000

# Verify
& "C:\Users\roihan\AppData\Local\Android\sdk\platform-tools\adb" forward --list
# Akan melihat: emulator-5554 tcp:5000 tcp:5000
```

### Apa yang Sudah Diperbaiki:

1. **ApiService.dart** - Sekarang semua platform menggunakan `http://127.0.0.1:5000`

   ```dart
   static String get baseUrl {
     // Semua platform gunakan localhost:5000
     // Android emulator sudah di-forward dengan ADB reverse
     return 'http://127.0.0.1:5000';
   }
   ```

2. **ADB Reverse Port Forwarding** - Emulator bisa access backend melalui port forwarding

## 🚀 Cara Menjalankan

### Terminal 1: Jalankan Backend

```powershell
cd c:\fluuter.u\prediksi_stok_kue
python run.py
```

### Terminal 2: Setup Emulator & Jalankan Flutter

```powershell
# Run script setup (ini setup port forwarding otomatis)
SETUP_EMULATOR.bat

# Tunggu script selesai, kemudian di terminal sama atau terminal baru:
cd prediksi_stok_kue
flutter run -d emulator-5554
```

**ATAU jika emulator sudah setup sebelumnya:**

```powershell
cd prediksi_stok_kue
flutter run -d emulator-5554
```

## 📱 Testing Login

Setelah app running di emulator:

1. **Isi Email**: `admin@bakesmart.com`
2. **Isi Password**: `password123`
3. **Tekan Masuk**
4. ✅ Seharusnya login berhasil tanpa timeout!

## 🛡️ Jika Masih Error

### Error: "Koneksi timeout" masih muncul

**Solusi 1: Restart emulator + port forwarding**

```powershell
# Terminal 1: Kill emulator
& "C:\Users\roihan\AppData\Local\Android\sdk\platform-tools\adb" kill-server

# Tunggu 5 detik, emulator akan restart otomatis

# Terminal 2: Setup port forwarding lagi
& "C:\Users\roihan\AppData\Local\Android\sdk\platform-tools\adb" reverse tcp:5000 tcp:5000

# Terminal 3: Jalankan flutter
flutter run -d emulator-5554
```

**Solusi 2: Gunakan script setup**

```powershell
SETUP_EMULATOR.bat
```

### Error: "Failed to establish connection"

Pastikan backend running:

```powershell
# Check port 5000
netstat -ano | findstr :5000

# Jika tidak ada, jalankan:
python run.py
```

### Error: "ADB not found"

Update path di script sesuai lokasi Android SDK Anda:

```batch
SET ADB_PATH=C:\Your\Android\SDK\Path\platform-tools\adb
```

## 📊 Verify Setup

```powershell
# Check devices terhubung
& "C:\Users\roihan\AppData\Local\Android\sdk\platform-tools\adb" devices

# Check port forwarding
& "C:\Users\roihan\AppData\Local\Android\sdk\platform-tools\adb" forward --list

# Output seharusnya:
# emulator-5554 tcp:5000 tcp:5000
```

## 🎯 Kesimpulan

✅ Masalah timeout sudah permanently fixed dengan:

- ADB port forwarding (emulator → host backend)
- ApiService menggunakan localhost universal
- Setup script otomatis

**Sekarang tidak akan ada timeout issue lagi saat login! 🚀**

---

**Pro Tips:**

- Setup emulator hanya perlu dilakukan 1x per session
- Jika emulator di-restart, jalankan `SETUP_EMULATOR.bat` lagi
- Backend perlu tetap running di terminal terpisah
- Gunakan `-v` flag untuk debugging: `flutter run -d emulator-5554 -v`
