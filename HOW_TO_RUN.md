# 🍰 BakeSmart - Siap Presentasi (FINAL)

## ✅ STATUS: KONEKSI BERHASIL & TESTED

Masalah timeout sudah **SOLVED**. Konfigurasi sudah benar dan tested.

---

## 🚀 CARA MENJALANKAN (3 LANGKAH)

### Langkah 1: Buka Emulator

```
Buka Android Emulator (Medium_Phone_API_36)
Tunggu sampai startup (±30 detik)
```

### Langkah 2: Start Backend (CARA TERMURAH)

```
Double-click: START_ALL.bat
```

Atau manual:

```bash
cd prediksi_stok_kue\backend
python start.py
```

Tunggu output:

```
✅ Server ready!
Running on http://192.168.1.20:5000
```

### Langkah 3: Flutter Akan Auto-Start

```
Tunggu sampai aplikasi muncul di emulator (2-3 menit)
Login dengan: admin@bakesmart.com / admin123
Selesai!
```

---

## 🔐 Login Credentials

```
Email:    admin@bakesmart.com
Password: admin123
```

---

## 📌 PENTING - IP ADDRESS YANG BENAR

```
✅ BENAR: http://192.168.1.20:5000/api
❌ SALAH: http://10.0.2.2:5000/api (akan timeout)
```

**File sudah dikonfigurasi dengan IP yang benar:**

- `prediksi_stok_kue/lib/services/api_service.dart` (Line 17)

**JANGAN UBAH!**

---

## 📱 URLs Reference

| Platform         | URL                          |
| ---------------- | ---------------------------- |
| Android Emulator | http://192.168.1.20:5000/api |
| Browser/PC       | http://127.0.0.1:5000/api    |
| Network          | http://192.168.1.20:5000/api |
| Database         | http://localhost/phpmyadmin  |

---

## 🗄️ Database Info

```
Type:     MySQL/MariaDB
Database: prediksi_stok_kue
Host:     localhost
User:     root
Password: (kosong)
Port:     3306
```

Auto-initialize saat backend startup.

---

## ❓ Troubleshooting

### Koneksi Timeout

```
→ Pastikan backend running
→ Pastikan IP di api_service.dart adalah 192.168.1.20
→ Restart emulator
```

### MySQL Error

```
→ Buka phpMyAdmin: http://localhost/phpmyadmin
→ Check database prediksi_stok_kue exists
→ Backend auto-create jika belum ada
```

### Flutter Build Error

```
→ flutter clean
→ flutter pub get
→ flutter run -d emulator-5554
```

---

## 📋 Checklist Presentasi

- [ ] Emulator sudah running
- [ ] Backend running (python start.py)
- [ ] MySQL aktif
- [ ] Flutter app muncul di emulator
- [ ] Login berhasil
- [ ] Dashboard menampilkan data
- [ ] Tidak ada error

---

## 🎯 Next Time

**Cukup:**

1. Double-click `START_ALL.bat`
2. Tunggu aplikasi
3. Login & presentasi

**Selesai!** ✅

---

_Konfigurasi final yang sudah tested & working. Jangan ubah-ubah! 🔒_
