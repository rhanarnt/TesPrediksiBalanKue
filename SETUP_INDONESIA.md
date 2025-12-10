# 📱 PANDUAN LENGKAP - Aplikasi Prediksi Stok Kue

Dokumentasi lengkap dalam bahasa Indonesia untuk setup dan menjalankan aplikasi Prediksi Stok Kue.

---

## 📋 DAFTAR ISI

1. [Prasyarat](#prasyarat)
2. [Setup Backend (Python Flask)](#setup-backend)
3. [Setup Frontend (Flutter)](#setup-frontend)
4. [Menjalankan Aplikasi](#menjalankan-aplikasi)
5. [Struktur Proyek](#struktur-proyek)
6. [API Endpoints](#api-endpoints)
7. [Troubleshooting](#troubleshooting)
8. [Contoh Penggunaan Lengkap](#contoh-penggunaan-lengkap)

---

## 🔧 PRASYARAT

Sebelum memulai, pastikan Anda telah menginstall:

| Software | Versi      | Link Download                                |
| -------- | ---------- | -------------------------------------------- |
| Python   | 3.8+       | https://www.python.org/downloads/            |
| Flutter  | 3.0+       | https://flutter.dev/docs/get-started/install |
| Git      | (opsional) | https://git-scm.com/download/win             |

### Verifikasi Instalasi

Buka PowerShell dan jalankan:

```powershell
python --version
flutter --version
dart --version
```

Jika semua menampilkan versi, maka Anda siap melanjutkan.

---

## 🚀 SETUP BACKEND (PYTHON FLASK)

Backend adalah server yang menerima data dari frontend dan mengembalikan prediksi menggunakan model machine learning.

### Langkah 1️⃣: Navigasi ke Folder Backend

```powershell
cd c:\fluuter.u\prediksi_stok_kue\prediksi_stok_kue\backend
```

### Langkah 2️⃣: Buat Virtual Environment Python

Jalankan perintah ini untuk membuat lingkungan Python terpisah:

```powershell
python -m venv venv
```

Harapan output: folder `venv` akan terbuat di dalam folder `backend`.

### Langkah 3️⃣: Aktifkan Virtual Environment

**Windows (PowerShell):**

```powershell
venv\Scripts\Activate.ps1
```

Jika muncul error permission denied, jalankan PowerShell sebagai Administrator.

**Windows (Command Prompt):**

```cmd
venv\Scripts\activate.bat
```

**Linux/Mac:**

```bash
source venv/bin/activate
```

Jika berhasil, prompt Anda akan berubah menjadi:

```
(venv) C:\fluuter.u\prediksi_stok_kue\prediksi_stok_kue\backend>
```

### Langkah 4️⃣: Install Dependencies

Dengan virtual environment aktif, install semua package yang diperlukan:

```powershell
pip install -r requirements.txt
```

Harapan output:

```
Successfully installed Flask-3.1.2 Flask-CORS-6.0.1 numpy-2.3.4 scikit-learn-1.7.2 scipy-1.16.3 joblib-1.5.2
```

Jika ada error, coba:

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

### Langkah 5️⃣: Jalankan Backend Server

```powershell
python run.py
```

Jika berhasil, Anda akan melihat output seperti ini:

```
==================================================
Backend Prediksi Stok Kue
==================================================
Server berjalan di http://127.0.0.1:5000
Endpoint tersedia:
  GET  / - Home
  POST /prediksi - Prediksi stok
  GET  /health - Health check
==================================================
 * Serving Flask app 'run'
 * Debug mode: off
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

✅ **Backend sudah siap!** Biarkan terminal ini terbuka.

---

## 💻 SETUP FRONTEND (FLUTTER)

Frontend adalah aplikasi yang menampilkan UI dan berinteraksi dengan user.

### Langkah 1️⃣: Buka Terminal Baru

**JANGAN tutup terminal backend.** Buka PowerShell/terminal baru.

### Langkah 2️⃣: Masuk ke Root Folder Proyek

```powershell
cd c:\fluuter.u\prediksi_stok_kue\prediksi_stok_kue
```

### Langkah 3️⃣: Download Dependencies Flutter

```powershell
flutter pub get
```

Harapan output:

```
Running "flutter pub get" in prediksi_stok_kue...
Got dependencies!
```

### Langkah 4️⃣: Jalankan Analisis Kode (Opsional tapi Disarankan)

```powershell
flutter analyze
```

Harapan: `No issues found!`

Jika ada error, baca pesan error dan hubungi untuk debugging.

### Langkah 5️⃣: Jalankan Test (Opsional)

```powershell
flutter test
```

Harapan: semua test pass.

✅ **Frontend siap dijalankan!**

---

## 🎮 MENJALANKAN APLIKASI

Ada beberapa opsi untuk menjalankan aplikasi. Pilih salah satu yang paling sesuai.

### OPSI 1️⃣: Menjalankan di Web Browser (Paling Mudah)

**Persyaratan:**

- Backend berjalan di `http://127.0.0.1:5000`
- Google Chrome atau Microsoft Edge terinstall

**Jalankan:**

```powershell
flutter run -d chrome
```

Aplikasi akan membuka di browser otomatis. Jika tidak, buka manual di tab yang ditampilkan di console.

**Kelebihan:**

- Tidak perlu emulator
- Paling cepat untuk testing
- Bisa debug di browser developer tools

**Kekurangan:**

- Hanya untuk testing, bukan untuk production

---

### OPSI 2️⃣: Menjalankan di Android Emulator

**Persyaratan:**

- Android SDK terinstall
- Android Emulator tersedia

**Langkah 1: Lihat Emulator yang Tersedia**

```powershell
flutter emulators
```

Output akan menampilkan daftar emulator yang tersedia.

**Langkah 2: Jalankan Emulator**

```powershell
flutter emulators --launch <nama_emulator>
```

Contoh:

```powershell
flutter emulators --launch Pixel_5_API_30
```

**Langkah 3: Tunggu Emulator Siap**
Tunggu sampai Android home screen muncul (bisa 1-2 menit).

**Langkah 4: Jalankan Aplikasi**

```powershell
flutter run
```

**⚠️ CATATAN PENTING:**

- Android emulator tidak bisa akses `127.0.0.1` dari host.
- File `lib/services/api_service.dart` sudah otomatis menggunakan `10.0.2.2` untuk Android.
- **Backend HARUS berjalan di host (Windows)** pada port 5000.

---

### OPSI 3️⃣: Menjalankan di iOS Simulator (Mac Only)

**Persyaratan:**

- Xcode terinstall
- Mac dengan Apple Silicon atau Intel

**Jalankan:**

```powershell
flutter run -d iphone
```

**Catatan:**

- iOS simulator bisa akses `127.0.0.1` langsung (tidak perlu 10.0.2.2).

---

### OPSI 4️⃣: Menjalankan di Desktop Windows

**Persyaratan:**

- Visual Studio 2022 dengan workload "Desktop development with C++"

**Jika sudah tersedia:**

```powershell
flutter run -d windows
```

**Jika tidak tersedia, install:**

1. Download Visual Studio Community: https://visualstudio.microsoft.com/
2. Jalankan installer
3. Pilih "Desktop development with C++"
4. Klik "Install"
5. Tunggu selesai (30-60 menit)
6. Restart komputer
7. Jalankan `flutter run -d windows`

---

## 📁 STRUKTUR PROYEK

```
prediksi_stok_kue/
│
├── backend/                         # Folder backend (Python Flask)
│   ├── venv/                        # Virtual environment Python
│   │   ├── Scripts/                 # Executable (python.exe, pip.exe, dll)
│   │   └── Lib/                     # Installed packages
│   │
│   ├── model.py                     # Model ML (Random Forest)
│   ├── run.py                       # Server Flask utama
│   ├── requirements.txt             # Daftar dependencies Python
│   ├── test_api.ps1                 # Script test API dengan PowerShell
│   ├── .gitignore                   # File yang tidak perlu di-commit
│   └── README.md                    # Dokumentasi backend
│
├── lib/                             # Folder source code Flutter
│   ├── main.dart                    # Entry point aplikasi
│   │
│   ├── pages/                       # Folder untuk halaman
│   │   ├── input_page.dart          # Halaman input data stok & harga
│   │   └── result_page.dart         # Halaman tampil hasil prediksi
│   │
│   └── services/                    # Folder untuk service
│       └── api_service.dart         # Service HTTP ke backend
│
├── test/
│   └── widget_test.dart             # Unit test untuk UI
│
├── pubspec.yaml                     # Dependencies Flutter & konfigurasi
├── analysis_options.yaml            # Konfigurasi Dart analyzer
├── README.md                        # Dokumentasi utama
└── SETUP_INDONESIA.md               # File ini
```

---

## 🔌 API ENDPOINTS

Backend menyediakan 3 endpoint REST:

### 1. GET / (Home)

**Tujuan:** Mengecek apakah server berjalan.

**Request:**

```bash
curl http://127.0.0.1:5000/
```

**Response (200 OK):**

```json
{
  "message": "Backend Prediksi Stok Kue - Server berjalan dengan baik"
}
```

---

### 2. GET /health (Health Check)

**Tujuan:** Mengecek status kesehatan server.

**Request:**

```bash
curl http://127.0.0.1:5000/health
```

**Response (200 OK):**

```json
{
  "status": "ok"
}
```

---

### 3. POST /prediksi (Prediksi Utama)

**Tujuan:** Mengirim data stok dan harga, menerima prediksi permintaan.

**Request:**

```bash
curl -X POST http://127.0.0.1:5000/prediksi \
  -H "Content-Type: application/json" \
  -d '{"jumlah": 20, "harga": 10000}'
```

**Response (200 OK):**

```json
{
  "prediksi_permintaan": 16.85,
  "status_stok": "Stok Rendah"
}
```

**Parameter Input:**
| Parameter | Tipe | Deskripsi |
|-----------|------|-----------|
| `jumlah` | number | Jumlah stok saat ini (harus > 0) |
| `harga` | number | Harga per satuan (harus > 0) |

**Response Output:**
| Field | Tipe | Deskripsi |
|-------|------|-----------|
| `prediksi_permintaan` | number | Prediksi permintaan dari model ML |
| `status_stok` | string | Status: "Stok Rendah", "Stok Sedang", atau "Stok Tinggi" |

**Error Response (400 Bad Request):**

```json
{
  "error": "Missing required fields: jumlah, harga"
}
```

---

## 🐛 TROUBLESHOOTING

### ❌ Masalah 1: "Unable to connect to http://127.0.0.1:5000"

**Tanda-tanda:**

- Error di aplikasi Flutter: "Terjadi kesalahan: Failed host lookup"
- Tombol prediksi tidak merespons

**Solusi:**

1. **Pastikan backend sudah dijalankan:**

   ```powershell
   cd backend
   venv\Scripts\Activate.ps1
   python run.py
   ```

   Tunggu sampai muncul "Running on http://127.0.0.1:5000"

2. **Cek apakah port 5000 terbuka:**

   ```powershell
   netstat -ano | findstr ":5000"
   ```

   Jika tidak muncul output, port tidak terpakai (baik).
   Jika muncul, cek apakah process-nya adalah Python.

3. **Test backend secara langsung:**

   ```powershell
   curl http://127.0.0.1:5000/
   ```

   atau di PowerShell:

   ```powershell
   Invoke-WebRequest -Uri "http://127.0.0.1:5000/" -Method GET
   ```

4. **Jika port 5000 sudah terpakai:**
   Ganti port di `backend/run.py`:
   ```python
   app.run(debug=False, host='127.0.0.1', port=5001)  # Ubah dari 5000 ke 5001
   ```
   Lalu update `lib/services/api_service.dart`:
   ```dart
   return 'http://127.0.0.1:5001';  // Ubah port
   ```

---

### ❌ Masalah 2: "CORS error" atau "Cross-Origin Request Blocked"

**Tanda-tanda:**

- Browser console menunjukkan "CORS policy blocked"
- Request tidak sampai ke backend

**Solusi:**

Backend sudah dikonfigurasi dengan Flask-CORS, jadi seharusnya tidak ada masalah. Jika masih ada:

1. **Pastikan frontend dan backend di URL yang sama:**

   - Frontend: `http://localhost:xxxxx` (web)
   - Backend: `http://127.0.0.1:5000`
     Keduanya adalah localhost, jadi seharusnya OK.

2. **Untuk Android emulator:**

   - Frontend: emulator (172.17.x.x)
   - Backend: `http://10.0.2.2:5000` (sudah dikonfigurasi di `api_service.dart`)

3. **Restart backend:**
   ```powershell
   # Tekan CTRL+C untuk stop
   # Jalankan lagi:
   python run.py
   ```

---

### ❌ Masalah 3: "Module 'numpy' not found" atau error import

**Tanda-tanda:**

- Error saat menjalankan `python run.py`
- `ModuleNotFoundError: No module named 'numpy'`

**Solusi:**

1. **Pastikan virtual environment aktif:**

   ```powershell
   venv\Scripts\Activate.ps1
   ```

   Prompt harus menunjukkan `(venv)` di awal.

2. **Re-install dependencies:**

   ```powershell
   pip install -r requirements.txt
   ```

3. **Verifikasi instalasi:**

   ```powershell
   pip list
   ```

   Cek apakah Flask, numpy, scikit-learn ada dalam list.

4. **Jika masih error, coba:**
   ```powershell
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

---

### ❌ Masalah 4: Flutter Error: "Unable to find suitable Visual Studio toolchain"

**Tanda-tanda:**

- Error saat menjalankan `flutter run -d windows`

**Solusi:**

1. **Gunakan browser sebagai gantinya:**

   ```powershell
   flutter run -d chrome
   ```

2. **Atau install Visual Studio:**
   - Download: https://visualstudio.microsoft.com/
   - Jalankan installer
   - Pilih workload: "Desktop development with C++"
   - Klik Install (tunggu 30-60 menit)
   - Restart komputer
   - Coba lagi: `flutter run -d windows`

---

### ❌ Masalah 5: Android Emulator tidak bisa terhubung ke backend

**Tanda-tanda:**

- App berjalan di emulator tapi error saat klik prediksi
- Error: "Unable to connect"

**Solusi:**

1. **Pastikan backend berjalan di host (Windows):**

   ```powershell
   cd backend
   venv\Scripts\Activate.ps1
   python run.py
   ```

2. **File `lib/services/api_service.dart` sudah otomatis menggunakan `10.0.2.2` untuk Android.** Cek:

   ```dart
   if (Platform.isAndroid) {
     return 'http://10.0.2.2:5000';
   }
   ```

3. **Pastikan firewall Windows memperbolehkan koneksi ke port 5000:**

   ```powershell
   netsh advfirewall firewall add rule name="Flask Backend" dir=in action=allow protocol=tcp localport=5000
   ```

4. **Coba test dari dalam emulator:**
   ```bash
   # Di dalam emulator terminal atau adb shell:
   curl http://10.0.2.2:5000/
   ```

---

### ❌ Masalah 6: "flutter run" tidak mendeteksi device

**Tanda-tanda:**

- `flutter run` tidak merespons atau error

**Solusi:**

1. **Lihat device tersedia:**

   ```powershell
   flutter devices
   ```

2. **Jika tidak ada device:**
   - **Chrome/Edge:** Mereka sudah built-in. Coba:
     ```powershell
     flutter run -d chrome
     ```
   - **Android Emulator:** Jalankan emulator dulu:
     ```powershell
     flutter emulators --launch Pixel_5_API_30
     ```
     Tunggu sampai Android siap, lalu:
     ```powershell
     flutter run
     ```
   - **Real Android Device:** Sambungkan via USB, enable USB debugging, lalu:
     ```powershell
     flutter run
     ```

---

## 📊 CONTOH PENGGUNAAN LENGKAP

Berikut contoh lengkap dari awal sampai selesai.

### STEP 1: Start Backend

**Terminal 1 (Backend):**

```powershell
cd c:\fluuter.u\prediksi_stok_kue\prediksi_stok_kue\backend
venv\Scripts\Activate.ps1
python run.py
```

Output:

```
==================================================
Backend Prediksi Stok Kue
==================================================
Server berjalan di http://127.0.0.1:5000
...
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

✅ Backend siap. **Jangan tutup terminal ini.**

---

### STEP 2: Start Frontend

**Terminal 2 (Frontend):**

```powershell
cd c:\fluuter.u\prediksi_stok_kue\prediksi_stok_kue
flutter run -d chrome
```

Output:

```
Launching lib\main.dart on Chrome in debug mode...
...
Flutter DevTools running on http://127.0.0.1:...
...
Application finished with exit code 0.
```

Browser akan membuka dengan aplikasi Flutter.

---

### STEP 3: Gunakan Aplikasi

1. Di halaman input:

   - **"Stok Saat Ini"**: masukkan `20`
   - **"Permintaan Terakhir"**: masukkan `10000`

2. Klik tombol **"Prediksi Sekarang"**

3. Tunggu loading (1-2 detik)

4. Di halaman hasil, Anda akan melihat:

   - **"Prediksi Permintaan: 16.85"** (contoh)
   - **"Status Stok: Stok Rendah"** (contoh)

5. Klik **"Kembali"** untuk kembali ke halaman input

6. Ulangi dengan data berbeda untuk testing lebih lanjut

---

### STEP 4: Stop Aplikasi

- **Frontend:** Tekan `q` di terminal atau tutup browser
- **Backend:** Tekan `CTRL+C` di terminal 1

---

## 📝 CATATAN PENTING

1. **Backend harus SELALU dijalankan terlebih dahulu** sebelum membuka frontend
2. **Jangan tutup terminal backend** selama menggunakan aplikasi
3. **Port 5000 harus tersedia**; jika terpakai, ganti port
4. **Untuk production**, gunakan production WSGI server seperti Gunicorn, bukan Flask development server
5. **ApiService sudah dikonfigurasi otomatis** untuk berbagai platform (web, Android, iOS, desktop)

---

## 🆘 BANTUAN LEBIH LANJUT

Jika mengalami masalah yang tidak terdaftar di atas:

1. **Baca output error dengan seksama**
2. **Cek koneksi internet** (untuk download dependencies)
3. **Jalankan diagnostic:**
   ```powershell
   flutter doctor
   pip check
   ```
4. **Lihat log backend** (terminal backend untuk error message)
5. **Cek firewall Windows** (port 5000 harus terbuka)

---

**Dibuat dengan ❤️ untuk Prediksi Stok Kue - Setup version 1.0**
