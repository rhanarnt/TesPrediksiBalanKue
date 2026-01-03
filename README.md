# Prediksi Stok Kue

Aplikasi Flask sederhana untuk memprediksi permintaan dan status stok kue menggunakan model ML (Linear Regression dan RandomForestClassifier).

## Struktur Proyek
```
prediksi_stok_kue/
├─ app/
│  ├─ __init__.py
│  ├─ models.py           # training & simpan model ke app/*.pkl
│  └─ routes.py           # endpoint Flask
├─ data/
│  └─ penjualan.csv       # dataset Anda (jumlah,harga,permintaan,status_stok)
├─ run.py                 # jalankan API
├─ requirements.txt       # dependensi Python
├─ test.html              # halaman uji sederhana (frontend)
└─ README.md
```

## Persiapan Lingkungan (Windows/PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

## Siapkan Data
- File: `data/penjualan.csv`
- Kolom minimal: `jumlah,harga,permintaan,status_stok`
- Contoh baris:
  ```csv
  jumlah,harga,permintaan,status_stok
  10,15000,12,lebih
  8,16000,7,kurang
  ```

## Training Model
Model disimpan ke `app/lr_model.pkl` dan `app/rf_model.pkl`.
```powershell
python .\app\models.py
```
Output: `✅ Model berhasil dilatih dan disimpan.`

## Menjalankan API
```powershell
python .\run.py
```
Default: `http://127.0.0.1:5000`

### Endpoint
- `GET /` – status singkat
- `GET /health` – health check + status model
- `GET /init-db` – inisialisasi tabel MySQL (`predictions`, `stocks`)
- `GET /history` – riwayat prediksi (opsional `start`, `end`, `limit`)
- `GET /history/weekly` – agregasi mingguan
- `GET /history.csv` – unduh CSV riwayat
- `POST /prediksi` – prediksi permintaan + status stok (body JSON):
  ```json
  { "jumlah": 12, "harga": 16000 }
  ```
  Respons:
  ```json
  { "prediksi_permintaan": 12.4, "status_stok": "Aman" }
  ```
- `POST /predict` – alias dari `/prediksi` (untuk konsistensi integrasi mobile)
- `GET /stock` – daftar stok saat ini
- `POST /stock` – tambah/ubah stok (upsert, berdasarkan `name` unik)
  ```json
  { "name": "Tepung", "qty": 42, "unit": "kg" }
  ```
- `DELETE /stock/<id>` – hapus item stok

## Uji dengan PowerShell
```powershell
# Cek root
(Invoke-WebRequest -Uri http://127.0.0.1:5000/).Content

# Prediksi
(Invoke-WebRequest `
  -Uri http://127.0.0.1:5000/prediksi `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"jumlah": 12, "harga": 16000}'
).Content

# Stock - Upsert
(Invoke-WebRequest `
  -Uri http://127.0.0.1:5000/stock `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"name": "Tepung", "qty": 42, "unit": "kg"}'
).Content

# Stock - List
(Invoke-WebRequest -Uri http://127.0.0.1:5000/stock).Content
```

## Akses dari Mobile (PWA)

- Jalankan API (bind ke seluruh interface sudah diatur di `run.py`):
  ```powershell
  python .\run.py
  ```
- Temukan IP laptop: `ipconfig | findstr /I "IPv4"` → contoh `192.168.1.23`
- Buka dari ponsel (Wi‑Fi yang sama): `http://192.168.1.23:5000/app`
- Install sebagai aplikasi (Chrome/Edge Android: menu → Add to Home screen/Install app)
- Offline fallback: halaman navigasi akan menampilkan `offline.html`. Endpoint `/prediksi` tetap butuh koneksi ke server.

> Catatan: CORS telah diaktifkan menggunakan `flask-cors`. UI `/app` melayani `test.html` langsung dari server sehingga aman diakses dari ponsel.

### Uji Frontend Lokal (alternatif)
Jika ingin menyajikan `test.html` via server statis lokal:
```powershell
python -m http.server 8000
```
Lalu buka `http://localhost:8000/test.html`.

## Troubleshooting
- `Model belum dilatih`: jalankan `python .\app\models.py` agar file `app/*.pkl` tersedia.
- `Unable to connect` saat request: pastikan API masih berjalan dan Anda mengirim dari terminal berbeda (server dibiarkan aktif).
- PowerShell error quoting JSON: gunakan contoh perintah di atas atau `curl.exe --%` agar tidak perlu escape kompleks.

## Akses dari Internet (Opsional)
- Gunakan ngrok:
  ```powershell
  ngrok http 5000
  ```
  Buka URL publik yang diberikan ke `/app` dan `/prediksi`.

## Android WebView Wrapper (Opsional)
1. Buat proyek Android Empty Activity (Android Studio).
2. Tambah permission Internet di `AndroidManifest.xml`:
   ```xml
   <uses-permission android:name="android.permission.INTERNET"/>
   ```
3. Di `MainActivity`, load URL `http://<IP-LAPTOP>:5000/app` pada `WebView`.
4. Aktifkan `setJavaScriptEnabled(true)` bila diperlukan.

## Lisensi
Gunakan bebas untuk pembelajaran dan pengembangan internal.
