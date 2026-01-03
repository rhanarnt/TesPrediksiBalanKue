# Test Backend API

Write-Host "Testing Backend Prediksi Stok Kue API" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan

# Test 1: Home endpoint
Write-Host "`nTest 1: Home Endpoint (GET /)" -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:5000/" -Method GET
    Write-Host $response.Content -ForegroundColor Green
} catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 2: Health endpoint
Write-Host "`nTest 2: Health Check (GET /health)" -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:5000/health" -Method GET
    Write-Host $response.Content -ForegroundColor Green
} catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 3: Prediksi endpoint
Write-Host "`nTest 3: Prediksi Stok (POST /prediksi)" -ForegroundColor Yellow
try {
    $body = @{
        jumlah = 20
        harga = 10000
    } | ConvertTo-Json
    
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:5000/prediksi" `
        -Method POST `
        -ContentType "application/json" `
        -Body $body
    
    Write-Host $response.Content -ForegroundColor Green
} catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 4: Prediksi dengan data berbeda
Write-Host "`nTest 4: Prediksi dengan data lain (POST /prediksi)" -ForegroundColor Yellow
try {
    $body = @{
        jumlah = 15
        harga = 7500
    } | ConvertTo-Json
    
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:5000/prediksi" `
        -Method POST `
        -ContentType "application/json" `
        -Body $body
    
    Write-Host $response.Content -ForegroundColor Green
} catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n" + "=" * 50 -ForegroundColor Cyan
Write-Host "Testing selesai!" -ForegroundColor Cyan
