@echo off
REM BakeSmart Complete Launcher
REM Start Backend dan Flutter secara bersamaan

echo.
echo ======================================================================
echo.                    🍰 BakeSmart Complete Setup
echo.
echo ======================================================================
echo.

REM Start Backend in separate window
echo Starting Backend Server...
start "BakeSmart Backend" cmd /k "cd /d %cd%\prediksi_stok_kue\backend && python start.py"

echo.
echo Waiting for backend to initialize (5 seconds)...
timeout /t 5

REM Start Flutter in new window
echo.
echo Starting Flutter application...
start "BakeSmart Flutter" cmd /k "cd /d %cd%\prediksi_stok_kue && echo Make sure Android Emulator is running! && echo. && flutter run -d emulator-5554 --no-fast-start"

echo.
echo ======================================================================
echo.  ✅ Both Backend and Flutter are starting!
echo.
echo    Backend: http://127.0.0.1:5000
echo    Emulator: http://10.0.2.2:5000
echo.
echo    Login: admin@bakesmart.com / admin123
echo.
echo ======================================================================
echo.
echo Close this window to continue...
pause
