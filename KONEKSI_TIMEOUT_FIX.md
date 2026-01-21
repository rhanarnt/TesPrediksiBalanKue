# 🔧 SOLUSI KONEKSI TIMEOUT - BAKESMART

## Masalah

Flutter app di Android Emulator menunjukkan error:

```
Koneksi timeout. Periksa apakah server berjalan.
URL: http://10.0.2.2:5000
```

## Penyebab

IP address yang digunakan salah. IP `10.0.2.2` hanya work untuk localhost tetapi server berjalan di network IP yang berbeda.

---

## ✅ SOLUSI (SUDAH DITERAPKAN)

### 1. Update IP Address di Flutter App

**File:** `prediksi_stok_kue/lib/services/api_service.dart`

**Perubahan:**

```dart
// BEFORE:
return 'http://192.168.1.20:5000/api';

// AFTER:
return 'http://192.168.1.27:5000/api';
```

IP yang benar: **192.168.1.27** (IP machine Anda)

### 2. Pastikan Backend Server Running

```powershell
cd C:\fluuter.u\prediksi_stok_kue\backend
python run.py
```

Server akan start di:

- `http://127.0.0.1:5000` (local)
- `http://192.168.1.27:5000` (network) ← **Gunakan ini untuk emulator**

### 3. Restart Flutter App

Di Android Emulator:

1. Tunggu proses build flutter selesai
2. Tekan tombol RELOAD atau hot restart (R key)
3. Atau close app dan buka lagi

---

## ✅ CHECKLIST SEBELUM TESTING

- [ ] Backend server running (`python run.py`)
- [ ] Server accessible di `http://192.168.1.27:5000`
- [ ] Flutter app dikompilasi dengan API URL yang benar
- [ ] Android Emulator connected ke WiFi yang sama
- [ ] Firewall tidak blocking port 5000

---

## 🧪 TESTING CONNECTION

### Dari Terminal/Browser:

```powershell
Invoke-WebRequest -Uri http://192.168.1.27:5000/health
```

Harusnya return status 200 dengan response:

```json
{
  "status": "healthy",
  "timestamp": "...",
  "version": "1.0.0"
}
```

### Dari Emulator:

Aplikasi akan otomatis test connection saat login.

---

## 📱 LOGIN CREDENTIALS

```
Email:    admin@bakesmart.com
Password: admin123
```

---

## 🚨 TROUBLESHOOTING

### Masih Timeout?

1. **Cek IP address machine Anda:**

   ```powershell
   ipconfig
   # Lihat IPv4 Address di WiFi adapter
   ```

2. **Update IP di api_service.dart jika berbeda**

3. **Pastikan emulator bisa akses IP tersebut:**

   ```
   Emulator > Extended Controls > Network
   Pastikan menggunakan WiFi yang sama dengan machine
   ```

4. **Cek firewall:**
   - Windows Defender Firewall mungkin blocking port 5000
   - Settings > Firewall > Allow app through firewall
   - Pastikan Python/Flask tidak di-block

### Backend Tidak Bisa Diakses?

```powershell
# Test dari machine lokal
Invoke-WebRequest -Uri http://127.0.0.1:5000/health

# Test dari IP machine
Invoke-WebRequest -Uri http://192.168.1.27:5000/health

# Jika gagal, check firewall
netstat -ano | findstr :5000
```

---

## 📊 NETWORK CONFIGURATION YANG BENAR

```
Machine IP:        192.168.1.27
Backend Port:      5000
Backend URL:       http://192.168.1.27:5000
Flutter API Base:  http://192.168.1.27:5000/api

Android Emulator:
├─ WiFi Network:   SAME AS MACHINE
├─ Gateway:        192.168.1.1
└─ Connect to:     http://192.168.1.27:5000/api
```

---

## ✅ VERIFICATION

Setelah fix, Anda seharusnya bisa:

1. ✅ Login dengan `admin@bakesmart.com` / `admin123`
2. ✅ Lihat daftar bahan di halaman utama
3. ✅ Akses fitur prediksi stok
4. ✅ Tidak ada error "Koneksi timeout"

---

**Status:** ✅ FIXED
**Date:** 2026-01-04
**IP Address Used:** 192.168.1.27
