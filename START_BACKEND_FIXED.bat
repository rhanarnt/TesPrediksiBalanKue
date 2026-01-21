@echo off
REM Script untuk start BakeSmart Backend Server
REM Berguna untuk debugging koneksi emulator

echo.
echo ================================================================================
echo              BAKESMART BACKEND SERVER STARTUP
echo ================================================================================
echo.
echo Machine IP:    192.168.1.27
echo Backend Port:  5000
echo URL:           http://192.168.1.27:5000
echo API Base:      http://192.168.1.27:5000/api
echo.
echo Untuk Flutter Android Emulator, gunakan IP ini di api_service.dart
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python tidak ditemukan!
    echo Please install Python atau add ke PATH
    pause
    exit /b 1
)

REM Go to backend directory
cd /d "%~dp0backend"

REM Start Python server
echo.
echo Starting Flask server...
echo Tunggu sampai melihat: "Running on http://192.168.1.27:5000"
echo.
echo Tekan CTRL+C untuk stop server
echo.
echo ================================================================================
echo.

python run.py

pause
