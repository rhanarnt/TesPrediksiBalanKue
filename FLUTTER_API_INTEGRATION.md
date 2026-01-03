# BakeSmart Flutter - API Integration Guide

## Current Status ✅

- ✅ Flutter UI/UX design complete (6 pages)
- ✅ Backend Flask API running on localhost:5000
- ✅ MySQL database initialized with real data
- ✅ JWT authentication integrated
- ✅ Real API endpoints connected

## Running the Application

### Prerequisites

1. **Backend Server** - Must be running

   ```bash
   cd backend
   python run.py
   ```

2. **Flutter App** - On localhost:55879 (Chrome)
   ```bash
   flutter run -d chrome
   ```

### Ensure Both are Running

```powershell
# Terminal 1: Start Backend
cd backend
python run.py

# Terminal 2: Start Flutter
flutter run -d chrome
```

## API Integration Points

### 1. Login Page (`lib/pages/login_page.dart`)

**Status**: ✅ Connected to real API

```dart
POST http://127.0.0.1:5000/login
Headers: Content-Type: application/json
Body: {
  "email": "admin@bakesmart.com",
  "password": "admin123"
}
Response: {
  "token": "jwt_token_here",
  "user": {
    "id": 1,
    "email": "admin@bakesmart.com",
    "name": "Admin BakeSmart"
  }
}
```

**Test Credentials**:

- Email: `admin@bakesmart.com`
- Password: `admin123`

### 2. Dashboard Page (`lib/pages/dashboard_page.dart`)

**Status**: ✅ Connected to real API

```dart
GET http://127.0.0.1:5000/stok
Headers:
  - Authorization: Bearer <token>
  - Content-Type: application/json

Response: {
  "data": [
    {
      "id": 1,
      "nama": "Tepung Terigu Serbaguna",
      "unit": "kg",
      "stok_minimum": 50.0,
      "stok_optimal": 200.0,
      "harga_per_unit": 5000.0
    },
    ...
  ]
}
```

Displays:

- Total items dari database (5 bahan)
- Stock low count
- Real data dari MySQL

### 3. Input Data Page (`lib/pages/input_data_page.dart`)

**Status**: ⏳ Ready to integrate

Can use these endpoints:

- `POST /stock-record` - Record stok masuk/keluar/penyesuaian

### 4. Prediksi Page (`lib/pages/prediksi_page.dart`)

**Status**: ⏳ Ready to integrate

Can use:

- `POST /prediksi` - Get demand prediction
- `GET /bahan/<id>` - Get bahan detail

### 5. Optimasi & Permintaan Pages

**Status**: ⏳ Ready to integrate

Can use:

- `POST /permintaan` - Submit purchase requests
- `GET /notifications` - Get user notifications

## Database & API Verification

### Verify Backend is Running

```bash
curl http://localhost:5000/health
# Response: {"status": "healthy", ...}
```

### Verify Database Connection

```bash
python test_api.py  # Basic test
python test_api_extended.py  # Extended endpoints test
```

### Check Database

```bash
mysql -u root prediksi_stok_kue
mysql> SELECT * FROM bahan;
mysql> SELECT * FROM user;
```

## Current API Test Results ✅

```
✅ /health - Server healthy
✅ /login - Login dengan real credentials
✅ /stok - Get 5 bahan dari database
✅ /bahan/1 - Get bahan detail
✅ /stock-record - Create stock record
✅ /notifications - Get user notifications
✅ /logout - Logout user
```

## Database Data

### Default Bahan (5 items)

1. **Tepung Terigu Serbaguna** - 50kg minimum, 200kg optimal
2. **Gula Halus** - 20kg minimum, 80kg optimal
3. **Telur Ayam** - 50 butir minimum, 120 butir optimal
4. **Susu Cair** - 10L minimum, 60L optimal
5. **Mentega** - 5kg minimum, 50kg optimal

### Default User

- Email: `admin@bakesmart.com`
- Password: `admin123`
- Role: Admin

## Development Workflow

### Making Changes

1. **Backend** - Restart Flask server after changes

   ```bash
   Stop-Process -Name python -Force
   python run.py
   ```

2. **Flutter** - Hot restart
   - Press `r` to hot reload
   - Press `R` to hot restart

### Adding New Endpoints

1. Add route in `backend/run.py`
2. Add ORM model in `backend/database.py` if needed
3. Test with `backend/test_api_extended.py`
4. Update Flutter page to call new endpoint
5. Test in Flutter app

### Debugging

**Flutter Console Logs**:

- Check for 🌐, ✅, ❌ symbols
- JWT token validation errors
- API response status codes

**Backend Console Logs**:

- Flask development server shows all requests
- Check for database connection errors
- JWT validation issues

## Known Issues & Workarounds

### Issue: "Failed to establish connection"

**Solution**: Make sure backend is running

```bash
cd backend
python run.py
```

### Issue: "Unauthorized" (401 error)

**Solution**: Token expired - login again. Tokens valid for 1 hour.

### Issue: "Cannot POST /endpoint"

**Solution**: Endpoint may not be implemented. Check `backend/run.py` and `backend/DATABASE_SETUP.md`

## Next Steps

### Phase 1 - Complete (✅)

- [x] Database setup with MySQL
- [x] Backend API endpoints
- [x] Flutter UI/UX design
- [x] Real API integration (login, dashboard)

### Phase 2 - Ready

- [ ] Integrate all pages with API
- [ ] Implement input data submission
- [ ] Implement prediction page
- [ ] Test notification system
- [ ] Add error handling & validation

### Phase 3 - Future

- [ ] Implement local SQLite caching
- [ ] Offline mode support
- [ ] Enhanced security (password hashing)
- [ ] Pagination for large datasets
- [ ] Data export/report features
- [ ] Mobile app optimization

## Port Numbers

- **Flutter Web**: http://localhost:55879
- **Flask Backend**: http://127.0.0.1:5000
- **MySQL Laragon**: localhost:3306 (user: root, no password)
- **Flutter DevTools**: http://127.0.0.1:9101

## File Structure Reference

```
backend/
  run.py                 # Flask API server
  database.py           # SQLAlchemy ORM models
  model.py              # ML prediction models
  requirements.txt      # Python dependencies
  test_api.py          # Basic API tests
  test_api_extended.py # Extended endpoint tests
  .env                 # Configuration (DATABASE_URL, SECRET_KEY)
  DATABASE_SETUP.md    # This setup guide

lib/
  pages/
    login_page.dart              # Login with real API
    dashboard_page.dart          # Dashboard with real data
    input_data_page.dart         # Ready for API integration
    prediksi_page.dart           # Ready for API integration
    optimasi_stok_page.dart      # Ready for API integration
    permintaan_bahan_page.dart   # Ready for API integration
    notifications_page.dart      # Ready for API integration
  services/
    api_service.dart             # API helper methods
```

## Support & Issues

For issues:

1. Check backend logs: `python run.py`
2. Check Flutter console: See terminal output
3. Test API: Run `python test_api.py`
4. Check database: Use MySQL Laragon console
5. Check `.env` configuration

---

**Last Updated**: November 24, 2025  
**Backend Status**: Running ✅  
**Database Status**: Connected ✅  
**API Integration**: Active ✅
