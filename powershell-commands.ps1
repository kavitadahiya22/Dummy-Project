# PowerShell Commands for Testing the Penetration Testing Framework API
# ====================================================================

Write-Host "🔐 PowerShell API Testing Commands" -ForegroundColor Cyan
Write-Host "=================================="

Write-Host "`n📝 Note: Make sure the API server is running first:" -ForegroundColor Yellow
Write-Host "   python -m uvicorn main_demo:app --reload --host 127.0.0.1 --port 8001" -ForegroundColor White

Write-Host "`n🌐 API Base URL: http://127.0.0.1:8001" -ForegroundColor Green

Write-Host "`n1. Health Check:" -ForegroundColor Cyan
Write-Host 'Invoke-RestMethod -Uri "http://127.0.0.1:8001/health" -Method Get' -ForegroundColor White

Write-Host "`n2. Get Authorized Targets:" -ForegroundColor Cyan
Write-Host 'Invoke-RestMethod -Uri "http://127.0.0.1:8001/authorized_targets" -Method Get' -ForegroundColor White

Write-Host "`n3. Start Penetration Test (PowerShell way):" -ForegroundColor Cyan
Write-Host '$body = @{' -ForegroundColor White
Write-Host '    target = "https://juice-shop.herokuapp.com"' -ForegroundColor White
Write-Host '    consent_acknowledged = $true' -ForegroundColor White
Write-Host '} | ConvertTo-Json' -ForegroundColor White
Write-Host '' -ForegroundColor White
Write-Host '$headers = @{ "Content-Type" = "application/json" }' -ForegroundColor White
Write-Host '' -ForegroundColor White
Write-Host 'Invoke-RestMethod -Uri "http://127.0.0.1:8001/invoke_pentest" -Method Post -Body $body -Headers $headers' -ForegroundColor White

Write-Host "`n4. Check Test Status (replace RUN_ID with actual ID):" -ForegroundColor Cyan
Write-Host 'Invoke-RestMethod -Uri "http://127.0.0.1:8001/pentest_status/YOUR_RUN_ID" -Method Get' -ForegroundColor White

Write-Host "`n5. Get Test Results (replace RUN_ID with actual ID):" -ForegroundColor Cyan
Write-Host 'Invoke-RestMethod -Uri "http://127.0.0.1:8001/pentest_results/YOUR_RUN_ID" -Method Get' -ForegroundColor White

Write-Host "`n🔍 Alternative: Use curl in PowerShell (if available):" -ForegroundColor Cyan
Write-Host 'curl.exe -X POST "http://127.0.0.1:8001/invoke_pentest" ^' -ForegroundColor White
Write-Host '  -H "Content-Type: application/json" ^' -ForegroundColor White
Write-Host '  -d "{\\"target\\": \\"https://juice-shop.herokuapp.com\\", \\"consent_acknowledged\\": true}"' -ForegroundColor White

Write-Host "`n📊 Interactive Documentation:" -ForegroundColor Cyan
Write-Host "   Browser: http://127.0.0.1:8001/docs" -ForegroundColor White

Write-Host "`n⚠️  Remember: This is demo mode. Install full dependencies for real testing!" -ForegroundColor Red