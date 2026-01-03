# BakeSmart Project Launcher (PowerShell)
# Run this from project root

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "                    🍰 BakeSmart Project Launcher" -ForegroundColor Magenta
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

$choices = @("Start Everything (Backend + Flutter)", "Backend Only", "Flutter Only", "Exit")
$selection = Read-Host "Pilih opsi (1-4)"

switch ($selection) {
    "1" {
        Write-Host ""
        Write-Host "Starting Backend Server..." -ForegroundColor Green
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$(Get-Location)\prediksi_stok_kue\backend'; python start.py"
        
        Write-Host "Waiting 5 seconds for backend to initialize..." -ForegroundColor Yellow
        Start-Sleep -Seconds 5
        
        Write-Host ""
        Write-Host "Starting Flutter Application..." -ForegroundColor Green
        Write-Host "Make sure Android Emulator is already running!" -ForegroundColor Yellow
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$(Get-Location)\prediksi_stok_kue'; flutter run -d emulator-5554 --no-fast-start"
        
        Write-Host ""
        Write-Host "======================================================================" -ForegroundColor Cyan
        Write-Host "✅ Backend and Flutter are starting!" -ForegroundColor Green
        Write-Host ""
        Write-Host "    Backend: http://127.0.0.1:5000" -ForegroundColor Cyan
        Write-Host "    Emulator: http://10.0.2.2:5000" -ForegroundColor Cyan
        Write-Host "    Login: admin@bakesmart.com / admin123" -ForegroundColor Yellow
        Write-Host "======================================================================" -ForegroundColor Cyan
    }
    "2" {
        Write-Host ""
        Write-Host "Starting Backend Server..." -ForegroundColor Green
        Set-Location "prediksi_stok_kue\backend"
        python start.py
    }
    "3" {
        Write-Host ""
        Write-Host "Starting Flutter Application..." -ForegroundColor Green
        Write-Host "Make sure Backend is already running!" -ForegroundColor Yellow
        Set-Location "prediksi_stok_kue"
        flutter run -d emulator-5554 --no-fast-start
    }
    "4" {
        Write-Host "Goodbye!" -ForegroundColor Yellow
        exit
    }
    default {
        Write-Host "Invalid selection. Please try again." -ForegroundColor Red
    }
}
