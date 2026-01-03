@echo off
REM Setup Backend with MySQL Database
REM Make sure Laragon is running with MySQL

echo.
echo ========================================
echo BakeSmart Backend Setup
echo ========================================
echo.

REM Check if venv exists
if not exist venv (
    echo [1/4] Creating virtual environment...
    python -m venv venv
    echo ✓ Virtual environment created
) else (
    echo [1/4] Virtual environment already exists
)

echo.
echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo [3/4] Installing Python dependencies...
pip install -r requirements.txt --upgrade
echo ✓ Dependencies installed

echo.
echo [4/4] Database setup complete!
echo.
echo ========================================
echo Before running the server:
echo 1. Make sure Laragon MySQL is running
echo 2. Create database: prediksi_stok_kue
echo ========================================
echo.
echo To create database in MySQL Laragon:
echo   mysql -u root -p < database_setup.sql
echo.
echo To run the server:
echo   python run.py
echo.
pause
