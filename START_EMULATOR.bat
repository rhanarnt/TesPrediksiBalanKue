@echo off
REM =========================================
REM BakeSmart Quick Start Script
REM =========================================
REM Ini script untuk memudahkan startup

setlocal enabledelayedexpansion

echo.
echo ==========================================
echo      BakeSmart - Quick Start
echo ==========================================
echo.

REM Set paths
SET ADB_PATH=C:\Users\roihan\AppData\Local\Android\sdk\platform-tools\adb
SET FLUTTER_PROJECT=prediksi_stok_kue
SET BACKEND_DIR=C:\fluuter.u\prediksi_stok_kue

echo [STEP 1] Setup ADB Port Forwarding...
%ADB_PATH% reverse tcp:5000 tcp:5000
if !ERRORLEVEL! EQU 0 (
    echo ✅ Port forwarding setup OK
) else (
    echo ❌ Failed to setup port forwarding
    echo    Make sure Android emulator is running
    pause
    exit /b 1
)

echo.
echo [STEP 2] Check Backend Status...
FOR /F "tokens=5" %%A in ('netstat -ano ^| findstr :5000') DO (
    echo ✅ Backend running on port 5000 (PID: %%A)
    goto :BACKEND_OK
)
echo ⚠️  Backend not running!
echo   Please start backend in another terminal:
echo   cd "%BACKEND_DIR%"
echo   python run.py
echo.
:BACKEND_OK

echo.
echo [STEP 3] Starting Flutter...
cd "%BACKEND_DIR%\%FLUTTER_PROJECT%"
flutter run -d emulator-5554

pause
