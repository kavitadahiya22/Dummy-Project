# Quick Start Script - Runs the project with all fixes
Write-Host "🚀 Starting Penetration Testing Framework..." -ForegroundColor Cyan

# Kill any existing servers on port 8000
Write-Host "🧹 Cleaning up any existing servers..." -ForegroundColor Yellow
Get-Process | Where-Object {$_.ProcessName -eq "python" -and $_.MainWindowTitle -like "*uvicorn*"} | Stop-Process -Force -ErrorAction SilentlyContinue

# Wait a moment
Start-Sleep -Seconds 2

# Start the server in background
Write-Host "▶️  Starting server on port 8000..." -ForegroundColor Green
$serverJob = Start-Job -ScriptBlock {
    Set-Location "C:\Users\Kavit\OneDrive\Desktop\Dummy-Project"
    python -m uvicorn main_demo:app --reload --host 127.0.0.1 --port 8000
}

# Wait for server to start
Write-Host "⏳ Waiting for server to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Test the API
Write-Host "🧪 Testing API endpoint..." -ForegroundColor Cyan
try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/invoke_pentest" -Method Post -Body '{"target": "https://juice-shop.herokuapp.com", "consent_acknowledged": true}' -ContentType "application/json" -TimeoutSec 10
    
    Write-Host "✅ SUCCESS! Your Penetration Testing Framework is working!" -ForegroundColor Green
    Write-Host "=" * 60 -ForegroundColor Gray
    $response | ConvertTo-Json -Depth 3
    Write-Host "=" * 60 -ForegroundColor Gray
    Write-Host ""
    Write-Host "🌐 Server is running at: http://127.0.0.1:8000" -ForegroundColor Yellow
    Write-Host "📚 API docs available at: http://127.0.0.1:8000/docs" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To stop the server, run: Stop-Job $($serverJob.Id) -Force" -ForegroundColor Cyan
    
} catch {
    Write-Host "❌ Error testing API: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.ErrorDetails) {
        Write-Host "Details: $($_.ErrorDetails.Message)" -ForegroundColor Red
    }
    
    # Clean up on error
    Stop-Job $serverJob -Force -ErrorAction SilentlyContinue
    Remove-Job $serverJob -Force -ErrorAction SilentlyContinue
}

Write-Host ""
Write-Host "🎯 Your project is now running! Use the API endpoints to test penetration testing scenarios." -ForegroundColor Green