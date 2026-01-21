# 🚀 Project Setup Complete

**Date**: January 15, 2026  
**Status**: ✅ Ready to Use

---

## ✅ Completed Tasks

### 1. **IP Address Configuration**

- Machine IP: `192.168.1.20`
- Updated in:
  - ✅ `lib/services/api_service.dart`
  - ✅ `prediksi_stok_kue/lib/services/api_service.dart`
  - ✅ `.env` file

### 2. **Backend Server**

- ✅ **Status**: Running & Listening
- ✅ **Port**: 5000
- ✅ **URL**: `http://192.168.1.20:5000`
- ✅ **Database**: MySQL Connected
- ✅ **CORS**: Enabled for all origins

### 3. **Flutter App Configuration**

- ✅ Web Platform: Uses `localhost:5000`
- ✅ Android Emulator: Uses `10.0.2.2:5000` (for emulator networking)
- ✅ iOS/Desktop: Uses `127.0.0.1:5000`

---

## 📝 How to Run

### **Option 1: Web (Chrome Browser)**

```bash
# Terminal 1: Start Backend
cd backend
python run.py

# Terminal 2: Run Flutter Web
flutter run -d chrome
```

### **Option 2: Physical Device (Wi-Fi)**

```bash
# Terminal 1: Start Backend
cd backend
python run.py

# Terminal 2: Connect physical Android device via Wi-Fi, then:
flutter run -d <device-id>
```

### **Option 3: Android Emulator** (Requires Network Fix)

```bash
# Terminal 1: Start Backend
cd backend
python run.py

# Terminal 2: Setup reverse port forwarding
adb reverse tcp:5000 tcp:5000

# Terminal 3: Run Flutter
flutter run -d emulator-5554
```

---

## 🔧 Current Configuration

| Component        | Setting                    | Status |
| ---------------- | -------------------------- | ------ |
| **Machine IP**   | `192.168.1.20`             | ✅     |
| **Backend Host** | `0.0.0.0` (all interfaces) | ✅     |
| **Backend Port** | `5000`                     | ✅     |
| **Database**     | MySQL (local)              | ✅     |
| **CORS**         | Enabled `*`                | ✅     |
| **Auth**         | JWT Tokens                 | ✅     |

---

## 🧪 Testing

### Test Backend Health

```bash
curl http://192.168.1.20:5000/health
# Expected: {"status": "ok"}
```

### Test Login Endpoint

```bash
curl -X POST http://192.168.1.20:5000/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@bakesmart.com","password":"admin123"}'
```

---

## 🎯 Default Credentials

- **Email**: `admin@bakesmart.com`
- **Password**: `admin123`

---

## ⚠️ Notes

1. **Android Emulator Networking**:

   - `10.0.2.2` is special DNS alias in Android emulator that points to host machine
   - May require reverse port forwarding or network reconfiguration
   - Recommend using physical device or web for testing

2. **Windows Firewall**:

   - Ensure port 5000 is allowed through firewall
   - Flask development server is configured to listen on `0.0.0.0`

3. **Database**:
   - MySQL must be running locally
   - Database `prediksi_stok_kue` is auto-created on first run

---

## 📚 Related Files

- Backend Config: `backend/run.py`
- Flutter Config: `lib/services/api_service.dart`
- Environment: `.env`
- Database: `backend/database.py`

---

**🎉 Project is ready! Choose your preferred platform and start development.**
