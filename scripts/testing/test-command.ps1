# This is the PowerShell equivalent of:
# curl -X POST http://127.0.0.1:8000/invoke_pentest -H "Content-Type: application/json" -d '{"target": "https://juice-shop.herokuapp.com", "consent_acknowledged": true}'

Write-Host "Testing API with your JSON data..." -ForegroundColor Green

Invoke-RestMethod -Uri "http://127.0.0.1:8000/invoke_pentest" -Method Post -Body '{"target": "https://juice-shop.herokuapp.com", "consent_acknowledged": true}' -ContentType "application/json"