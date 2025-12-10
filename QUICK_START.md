# 🎂 BakeSmart - Quick Start Guide

**Status**: ✅ Production Ready (Phase 1 Complete)

---

## 🚀 Quick Start (2 steps)

### Step 1: Start Backend

```powershell
cd backend
python run.py
```

**Expected Output**:

```
✅ Database initialized
📊 Running on http://0.0.0.0:5000
```

### Step 2: Start Flutter

```powershell
flutter run -d chrome
```

**What happens automatically**:

- ✅ App opens on localhost:55879
- ✅ Login page shows
- ✅ API connects to backend
- ✅ Data loads from MySQL

---

## 🔐 Login

**Credentials**:

- Email: `admin@bakesmart.com`
- Password: `admin123`

**What it does**:

1. Sends login to backend
2. Receives JWT token
3. Stores token securely
4. Loads dashboard with real data from MySQL

---

## ✅ What's Working

| Feature                      | Status                 |
| ---------------------------- | ---------------------- |
| MySQL Database               | ✅ Running             |
| Flask Backend (11 endpoints) | ✅ Working             |
| Login Page                   | ✅ Real API            |
| Dashboard                    | ✅ Real Data (5 items) |
| Token Auth                   | ✅ JWT Tokens          |
| Secure Storage               | ✅ Token saved         |
| Error Handling               | ✅ Implemented         |
| CORS                         | ✅ Enabled             |

---

## 📊 Database Stats

- **Database**: `prediksi_stok_kue` (MySQL)
- **Tables**: 7
- **Records**: 5 bahan items + 1 admin user
- **Ready to use**: YES ✅

---

## 🔧 Verify Everything Works

```bash
# Test backend API
cd backend
python test_api.py

# Expected: All tests pass ✅
```

---

## 📁 Key Files

```
backend/run.py              # Flask API server
backend/database.py         # Database models
backend/.env                # Configuration
lib/pages/login_page.dart   # Login (real API)
lib/pages/dashboard_page.dart # Dashboard (real data)
FLUTTER_API_INTEGRATION.md  # Complete guide
DATABASE_SETUP.md           # Database guide
```

---

## ⏳ Next Phase (Ready When You Are)

Remaining pages to integrate:

- Input Data → Connect to API
- Prediksi → Connect to API
- Permintaan → Connect to API
- Optimasi → Connect to API
- Notifications → Connect to API

**Estimated time**: 8-10 hours

---

## 🆘 Troubleshooting

**Backend not starting?**

```powershell
# Stop all Python processes
Stop-Process -Name python -Force

# Start fresh
python backend/run.py
```

**Flutter can't connect?**

- Make sure backend is running first
- Check port 5000 is not blocked
- Verify .env file has correct DATABASE_URL

**Login fails?**

- Use exact credentials: admin@bakesmart.com / admin123
- Check backend console for errors
- Verify MySQL is running in Laragon

---

## 📞 Quick Help

**Q: How do I know if it's working?**  
A: After login, you should see 5 items on dashboard from real MySQL database

**Q: Where is my data stored?**  
A: In MySQL database: `prediksi_stok_kue` (via Laragon)

**Q: How long is token valid?**  
A: 1 hour. After that, login again.

**Q: Can I use other credentials?**  
A: Only admin@bakesmart.com works currently. More users can be added via database.

---

## 🎯 Current Architecture

```
Flutter App (Chrome)
       ↓ (HTTP/REST)
Flask API Server (port 5000)
       ↓ (SQLAlchemy ORM)
MySQL Database (Laragon)
```

---

## 📊 API Endpoints Ready

```
✅ POST /login           - User authentication
✅ GET /stok             - List all materials
✅ GET /bahan/<id>       - Get material detail
✅ POST /stock-record    - Record stock transaction
✅ GET /notifications    - User notifications
✅ POST /prediksi        - Demand prediction
✅ POST /permintaan      - Purchase request
✅ POST /logout          - User logout
✅ GET /health           - Server status
```

---

**Ready to go!** 🚀

Just run `python backend/run.py` then `flutter run -d chrome`
