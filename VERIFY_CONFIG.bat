@echo off
REM Verification Script untuk BakeSmart Configuration
REM Cek apakah semua konfigurasi masih benar

echo.
echo ======================================================================
echo                  🍰 BakeSmart Configuration Checker
echo ======================================================================
echo.

setlocal enabledelayedexpansion

REM Check if port 5000 is listening
echo Checking port 5000...
netstat -ano | findstr :5000 >nul
if %errorlevel% equ 0 (
    echo ✅ Port 5000 is LISTENING
) else (
    echo ❌ Port 5000 is NOT listening - Backend not running!
    echo    Start backend with: python prediksi_stok_kue/backend/start.py
)

REM Check MySQL connection
echo.
echo Checking MySQL connection...
python -c "import pymysql; conn = pymysql.connect(host='127.0.0.1', user='root'); print('✅ MySQL Connected'); conn.close()" 2>nul
if %errorlevel% equ 0 (
    echo ✅ MySQL is running
) else (
    echo ❌ MySQL is NOT running - Start MySQL service!
)

REM Check API endpoint
echo.
echo Checking API endpoint...
powershell -Command "$response = Invoke-WebRequest -Uri 'http://192.168.1.20:5000/api' -UseBasicParsing -ErrorAction SilentlyContinue; if ($response.StatusCode -eq 200) { Write-Host '✅ API is accessible' } else { Write-Host '❌ API is not responding' }" 2>nul

REM Check api_service configuration
echo.
echo Checking api_service.dart configuration...
findstr /C:"192.168.1.20:5000" prediksi_stok_kue\lib\services\api_service.dart >nul
if %errorlevel% equ 0 (
    echo ✅ api_service.dart is correctly configured
) else (
    echo ❌ api_service.dart is NOT configured for 192.168.1.20!
    echo    Edit: prediksi_stok_kue/lib/services/api_service.dart
)

echo.
echo ======================================================================
echo                        Verification Complete
echo ======================================================================
echo.

pause
