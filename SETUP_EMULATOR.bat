@echo off
REM Script untuk setup emulator dengan port forwarding otomatis
REM Jalankan ini setiap kali mau test di emulator

echo ========================================
echo BakeSmart Emulator Setup
echo ========================================

REM Cari ADB path
SET ADB_PATH=C:\Users\roihan\AppData\Local\Android\sdk\platform-tools\adb

REM Check emulator status
echo.
echo [1] Checking emulator devices...
%ADB_PATH% devices

REM Setup port forwarding
echo.
echo [2] Setting up ADB reverse port forwarding...
%ADB_PATH% reverse tcp:5000 tcp:5000

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ SUCCESS: Port forwarding setup selesai!
    echo    Emulator sekarang bisa connect ke http://127.0.0.1:5000
    echo.
) else (
    echo.
    echo ❌ ERROR: Port forwarding failed!
    echo    Pastikan emulator sudah running
    echo.
    exit /b 1
)

REM Check backend status
echo [3] Checking backend server...
powershell -NoProfile -Command "try { $response = Invoke-WebRequest -Uri 'http://127.0.0.1:5000' -TimeoutSec 2 -ErrorAction Stop; Write-Host '✅ Backend Running on http://127.0.0.1:5000' } catch { Write-Host '❌ Backend NOT Running! Run: python run.py' }"

echo.
echo ========================================
echo Ready to run Flutter! Execute:
echo cd prediksi_stok_kue && flutter run -d emulator-5554
echo ========================================
echo.

pause
