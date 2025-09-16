# PowerShell API Test Script for Penetration Testing Framework
# ===========================================================

# Test API endpoint using PowerShell
$apiUrl = "http://localhost:8000"
$endpoint = "$apiUrl/invoke_pentest"

# JSON payload
$body = @{
    target = "https://juice-shop.herokuapp.com"
    consent_acknowledged = $true
} | ConvertTo-Json

# Headers
$headers = @{
    "Content-Type" = "application/json"
}

Write-Host "🔐 Testing Penetration Testing Framework API" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan

# Test 1: Health Check
Write-Host "`n1. Testing Health Check..." -ForegroundColor Yellow
try {
    $healthResponse = Invoke-RestMethod -Uri "$apiUrl/health" -Method Get
    Write-Host "✅ Health Check Response:" -ForegroundColor Green
    $healthResponse | ConvertTo-Json -Depth 3
} catch {
    Write-Host "❌ Health Check Failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "💡 Make sure the API is running: uvicorn main:app --reload" -ForegroundColor Yellow
    exit 1
}

# Test 2: Get Authorized Targets
Write-Host "`n2. Getting Authorized Targets..." -ForegroundColor Yellow
try {
    $targetsResponse = Invoke-RestMethod -Uri "$apiUrl/authorized_targets" -Method Get
    Write-Host "✅ Authorized Targets:" -ForegroundColor Green
    $targetsResponse | ConvertTo-Json -Depth 3
} catch {
    Write-Host "❌ Failed to get authorized targets: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 3: Start Penetration Test
Write-Host "`n3. Starting Penetration Test..." -ForegroundColor Yellow
Write-Host "📤 Sending request:" -ForegroundColor Gray
Write-Host $body -ForegroundColor Gray

try {
    $response = Invoke-RestMethod -Uri $endpoint -Method Post -Body $body -Headers $headers
    Write-Host "✅ Penetration Test Started!" -ForegroundColor Green
    $response | ConvertTo-Json -Depth 3
    
    $runId = $response.run_id
    Write-Host "`n📋 Run ID: $runId" -ForegroundColor Cyan
    
    # Test 4: Check Status
    if ($runId) {
        Write-Host "`n4. Checking Test Status..." -ForegroundColor Yellow
        Start-Sleep -Seconds 2
        
        try {
            $statusResponse = Invoke-RestMethod -Uri "$apiUrl/pentest_status/$runId" -Method Get
            Write-Host "✅ Status Response:" -ForegroundColor Green
            $statusResponse | ConvertTo-Json -Depth 3
        } catch {
            Write-Host "❌ Failed to get status: $($_.Exception.Message)" -ForegroundColor Red
        }
    }
    
} catch {
    Write-Host "❌ Penetration Test Failed: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.Exception.Response) {
        $statusCode = $_.Exception.Response.StatusCode
        Write-Host "📊 Status Code: $statusCode" -ForegroundColor Red
        
        # Try to get error details
        try {
            $errorStream = $_.Exception.Response.GetResponseStream()
            $reader = New-Object System.IO.StreamReader($errorStream)
            $errorBody = $reader.ReadToEnd()
            Write-Host "📝 Error Details: $errorBody" -ForegroundColor Red
        } catch {
            Write-Host "📝 Could not read error details" -ForegroundColor Red
        }
    }
}

Write-Host "`n🔗 Useful Commands:" -ForegroundColor Cyan
Write-Host "  - Start API: uvicorn main:app --reload" -ForegroundColor White
Write-Host "  - View Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host "  - OpenSearch: https://cybrty-dev-ca.wonderfuldune-e921120d.eastus.azurecontainerapps.io" -ForegroundColor White