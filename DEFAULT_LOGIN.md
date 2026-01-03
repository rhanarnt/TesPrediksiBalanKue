# 🔐 Default Login Credentials

## Admin Account

- **Email:** `admin@bakesmart.com`
- **Password:** `admin123`

## How It Works

1. The backend automatically seeds the database with this admin user on first run
2. If you want to change the password, edit [backend/database.py](backend/database.py) in the `seed_db()` function
3. Make sure to restart the backend after making changes

## Important Notes

- ✅ Backend must be running on `http://127.0.0.1:5000` or `http://0.0.0.0:5000`
- ✅ Emulator uses `http://10.0.2.2:5000` to connect to host machine
- ✅ JWT token expires after 1 hour
- ✅ Token is stored in Flutter Secure Storage

## Troubleshooting Login Issues

### Issue 1: "Email atau password salah"

- Check you're using the correct credentials above
- Make sure database is seeded (backend should show "[OK] Database seeded...")
- Clear app cache and try again

### Issue 2: "Koneksi timeout"

- Ensure backend is running on `http://127.0.0.1:5000`
- Check if Windows Firewall is blocking port 5000
- Try `netstat -ano | findstr :5000` to verify port

### Issue 3: "User tidak aktif"

- The user account is marked as inactive in database
- Admin user should always be active by default
