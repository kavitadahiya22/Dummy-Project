# Complete test script that starts server and tests API
Write-Host "🚀 Starting Penetration Testing API Server..." -ForegroundColor Cyan

# Start server in background
$serverJob = Start-Job -ScriptBlock {
    Set-Location "C:\Users\Kavit\OneDrive\Desktop\Dummy-Project"
    python -m uvicorn main_demo:app --reload --host 127.0.0.1 --port 8090
}

Write-Host "⏳ Waiting for server to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

Write-Host "📡 Testing API endpoint..." -ForegroundColor Green

try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8090/invoke_pentest" -Method Post -Body '{"target": "https://juice-shop.herokuapp.com", "consent_acknowledged": true}' -ContentType "application/json" -TimeoutSec 10
    
    Write-Host "✅ SUCCESS! API Response:" -ForegroundColor Green
    Write-Host "=" * 60 -ForegroundColor Gray
    $response | ConvertTo-Json -Depth 10
    Write-Host "=" * 60 -ForegroundColor Gray
    
} catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.ErrorDetails) {
        Write-Host "Details: $($_.ErrorDetails.Message)" -ForegroundColor Red
    }
}

# Clean up
Write-Host "🧹 Stopping server..." -ForegroundColor Yellow
Stop-Job $serverJob -Force
Remove-Job $serverJob -Force

Write-Host "✅ Test completed!" -ForegroundColor Green