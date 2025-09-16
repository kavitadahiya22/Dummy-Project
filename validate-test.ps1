# Quick test of the validation fix
Write-Host "🧪 Testing the validation fix locally..." -ForegroundColor Cyan

# Test the URL validation logic
$testUrl = "https://juice-shop.herokuapp.com"
$testUrlWithSlash = "https://juice-shop.herokuapp.com/"

Write-Host "Testing URL: $testUrl" -ForegroundColor Yellow
$cleaned = $testUrl.TrimEnd('/')
$allowedBase = "juice-shop.herokuapp.com"

if ($cleaned.EndsWith($allowedBase) -and ($cleaned.StartsWith("http://") -or $cleaned.StartsWith("https://"))) {
    Write-Host "✅ Validation should PASS for: $testUrl" -ForegroundColor Green
} else {
    Write-Host "❌ Validation would FAIL for: $testUrl" -ForegroundColor Red
}

Write-Host "Testing URL: $testUrlWithSlash" -ForegroundColor Yellow
$cleaned2 = $testUrlWithSlash.TrimEnd('/')
if ($cleaned2.EndsWith($allowedBase) -and ($cleaned2.StartsWith("http://") -or $cleaned2.StartsWith("https://"))) {
    Write-Host "✅ Validation should PASS for: $testUrlWithSlash" -ForegroundColor Green
} else {
    Write-Host "❌ Validation would FAIL for: $testUrlWithSlash" -ForegroundColor Red
}

Write-Host ""
Write-Host "🚀 Now starting server and testing API..." -ForegroundColor Cyan