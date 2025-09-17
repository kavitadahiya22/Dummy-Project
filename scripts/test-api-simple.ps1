# Simple API Test Script for Penetration Testing Framework
# Usage: Run this script while the server is running on port 8004

Write-Host "🚀 Testing Penetration Testing API" -ForegroundColor Cyan
Write-Host "Target: https://juice-shop.herokuapp.com" -ForegroundColor Yellow
Write-Host "Endpoint: http://127.0.0.1:8004/invoke_pentest" -ForegroundColor Yellow
Write-Host ""

# Create the JSON body
$requestBody = @{
    target = "https://juice-shop.herokuapp.com"
    consent_acknowledged = $true
} | ConvertTo-Json

# Set headers
$headers = @{ 
    "Content-Type" = "application/json" 
}

Write-Host "📤 Sending API Request..." -ForegroundColor Green

try {
    # Make the API call
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8004/invoke_pentest" -Method Post -Body $requestBody -Headers $headers -TimeoutSec 30
    
    Write-Host "✅ Success! API Response:" -ForegroundColor Green
    Write-Host "=" * 50 -ForegroundColor Gray
    $response | ConvertTo-Json -Depth 10
    Write-Host "=" * 50 -ForegroundColor Gray
    
} catch {
    Write-Host "❌ Error occurred:" -ForegroundColor Red
    Write-Host "Message: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Status: $($_.Exception.Response.StatusCode)" -ForegroundColor Red
    
    if ($_.Exception.Response) {
        Write-Host "Response: $($_.Exception.Response)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "🏁 Test completed" -ForegroundColor Cyan