# BakeSmart Backend - MySQL Setup Guide

## Prerequisites

- Python 3.8+
- Laragon (with MySQL running)
- Flask & SQLAlchemy

## Setup Steps

### 1. Create Database in MySQL

Open Laragon MySQL console and run:

```sql
CREATE DATABASE prediksi_stok_kue;
USE prediksi_stok_kue;
```

Or use the SQL script:

```bash
mysql -u root < database_setup.sql
```

### 2. Install Python Dependencies

```bash
# On Windows
setup.bat

# Or manually
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment

Check `.env` file - should have:

```
DATABASE_URL=mysql+pymysql://root:@127.0.0.1:3306/prediksi_stok_kue
SECRET_KEY=dev-secret-key-rahasia-bakesmart
FLASK_DEBUG=True
```

### 4. Run the Server

```bash
python run.py
```

Expected output:

```
============================================================
🎂 BakeSmart Backend Server
============================================================
✅ Database initialized
📊 Running on http://0.0.0.0:5000
============================================================
```

### 5. Test API

Check health endpoint:

```bash
curl http://localhost:5000/health
```

Expected response:

```json
{
  "status": "healthy",
  "timestamp": "2025-11-24T...",
  "version": "1.0.0"
}
```

## Database Models

- **User** - Aplikasi users
- **Bahan** - Master data bahan baku
- **StockRecord** - History stok masuk/keluar
- **Prediction** - Prediksi permintaan
- **Order** - Purchase orders
- **Notification** - User notifications
- **AuditLog** - Tracking perubahan data

## API Endpoints

### Authentication

- `POST /login` - Login user

  - Request: `{"email": "admin@bakesmart.com", "password": "admin123"}`
  - Response: JWT token + user info

- `POST /logout` - Logout user (requires auth)
  - Response: Logout confirmation

### Data Access

- `GET /stok` - Get semua bahan baku (requires auth)

  - Response: List of bahan with stok info

- `GET /bahan/<id>` - Get detail bahan berdasarkan ID (requires auth)

  - Response: Single bahan object

- `GET /notifications` - Get notifikasi user (requires auth)
  - Response: List of user notifications

### Data Modification

- `POST /prediksi` - Prediksi permintaan (requires auth)

  - Request: `{"jumlah": value, "harga": value}`
  - Response: Prediction result

- `POST /permintaan` - Submit order/request (requires auth)

  - Request: `{"nama_bahan": string, "kuantitas": value}`
  - Response: Order confirmation

- `POST /stock-record` - Create stock entry (masuk/keluar/penyesuaian) (requires auth)
  - Request: `{"bahan_id": int, "jumlah": value, "tipe": "masuk|keluar|penyesuaian", "catatan": string}`
  - Response: Created record info

### Health & Status

- `GET /health` - Server health check (no auth required)
  - Response: `{"status": "healthy", "timestamp": "...", "version": "1.0.0"}`

## Authentication

All endpoints except `/login` and `/health` require JWT token in Authorization header:

```
Authorization: Bearer <jwt_token>
```

Token valid for 1 hour. Get new token by logging in again.

## Troubleshooting

### Error: "No module named 'pymysql'"

```bash
pip install PyMySQL
```

### Error: "Can't connect to MySQL server"

- Pastikan Laragon MySQL running
- Check DATABASE_URL di .env
- Default: `mysql+pymysql://root:@127.0.0.1:3306/prediksi_stok_kue`

### Error: "Unknown database"

```bash
mysql -u root -e "CREATE DATABASE prediksi_stok_kue;"
```

## Default Credentials

- Email: `admin@bakesmart.com`
- Password: `admin123`

(Change in production!)

## Production Deployment

For production:

1. Use strong SECRET_KEY
2. Hash passwords (use werkzeug)
3. Enable HTTPS
4. Use environment variables
5. Set up proper logging
6. Use gunicorn or similar WSGI server
