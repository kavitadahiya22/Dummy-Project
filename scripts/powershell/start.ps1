# Penetration Testing Framework Startup Script (PowerShell)
# ===========================================================

Write-Host "🔐 Penetration Testing Framework Setup" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan

# Check if Docker is running
try {
    docker info | Out-Null
    Write-Host "✅ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not running. Please start Docker first." -ForegroundColor Red
    exit 1
}

# Check if Docker Compose is available
try {
    docker-compose --version | Out-Null
    Write-Host "✅ Docker Compose is available" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker Compose is not installed. Please install Docker Compose." -ForegroundColor Red
    exit 1
}

# Create logs directory
if (!(Test-Path "logs")) { New-Item -ItemType Directory -Path "logs" }
if (!(Test-Path "data")) { New-Item -ItemType Directory -Path "data" }

# Copy environment file if it doesn't exist
if (!(Test-Path ".env")) {
    Write-Host "📝 Creating environment configuration..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "✅ Created .env file. Please review and customize if needed." -ForegroundColor Green
}

Write-Host "🚀 Starting Penetration Testing Framework..." -ForegroundColor Yellow

# Build and start services
docker-compose up --build -d

Write-Host "⏳ Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Check if services are running
$services = docker-compose ps
if ($services -match "Up") {
    Write-Host "✅ Services started successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📊 Service Status:" -ForegroundColor Cyan
    docker-compose ps
    Write-Host ""
    Write-Host "🌐 Access URLs:" -ForegroundColor Cyan
    Write-Host "  - API Documentation: http://localhost:8000/docs" -ForegroundColor White
    Write-Host "  - Health Check: http://localhost:8000/health" -ForegroundColor White
    Write-Host "  - Ollama Service: http://localhost:11434" -ForegroundColor White
    Write-Host ""
    Write-Host "📖 Usage Example:" -ForegroundColor Cyan
    Write-Host 'curl -X POST "http://localhost:8000/invoke_pentest" \' -ForegroundColor White
    Write-Host '  -H "Content-Type: application/json" \' -ForegroundColor White
    Write-Host '  -d "{' -ForegroundColor White
    Write-Host '    \"target\": \"https://juice-shop.herokuapp.com\",' -ForegroundColor White
    Write-Host '    \"consent_acknowledged\": true' -ForegroundColor White
    Write-Host '  }"' -ForegroundColor White
    Write-Host ""
    Write-Host "🔗 OpenSearch Dashboard:" -ForegroundColor Cyan
    Write-Host "  https://cybrty-dev-ca.wonderfuldune-e921120d.eastus.azurecontainerapps.io" -ForegroundColor White
    Write-Host ""
    Write-Host "⚠️  REMEMBER: Only test authorized targets!" -ForegroundColor Red
} else {
    Write-Host "❌ Some services failed to start. Checking logs..." -ForegroundColor Red
    docker-compose logs
}