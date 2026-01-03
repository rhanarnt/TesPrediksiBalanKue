# Backend Prediksi Stok Kue

Backend Flask untuk aplikasi prediksi permintaan stok kue.

## Setup Environment

### 1. Pastikan Python 3.8+ terinstall

```bash
python --version
```

### 2. Buat Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Menjalankan Server

```bash
python run.py
```

Server akan berjalan di `http://127.0.0.1:5000`

## API Endpoints

### 1. Home

- **URL**: `GET /`
- **Response**:

```json
{
  "message": "Backend Prediksi Stok Kue - Server berjalan dengan baik"
}
```

### 2. Prediksi Stok

- **URL**: `POST /prediksi`
- **Request Body**:

```json
{
  "jumlah": 10,
  "harga": 5000
}
```

- **Response**:

```json
{
  "prediksi_permintaan": 8.5,
  "status_stok": "Stok Tinggi"
}
```

### 3. Health Check

- **URL**: `GET /health`
- **Response**:

```json
{
  "status": "ok"
}
```

## Testing dengan Postman/Curl

```bash
# Test home
curl http://127.0.0.1:5000/

# Test health
curl http://127.0.0.1:5000/health

# Test prediksi
curl -X POST http://127.0.0.1:5000/prediksi \
  -H "Content-Type: application/json" \
  -d '{"jumlah": 20, "harga": 10000}'
```

## Struktur Model

Model menggunakan Random Forest Regressor untuk memprediksi permintaan berdasarkan:

- **Input**: Jumlah stok saat ini dan harga per satuan
- **Output**: Prediksi permintaan dan status stok (Stok Rendah/Sedang/Tinggi)

Model dilatih dengan data dummy dan akan otomatis disimpan ke file `stok_model.pkl`.
