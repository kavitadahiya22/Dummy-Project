#!/bin/bash

# Penetration Testing Framework Startup Script
# ============================================

set -e

echo "🔐 Penetration Testing Framework Setup"
echo "======================================"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose."
    exit 1
fi

# Create logs directory
mkdir -p logs data

# Copy environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating environment configuration..."
    cp .env.example .env
    echo "✅ Created .env file. Please review and customize if needed."
fi

echo "🚀 Starting Penetration Testing Framework..."

# Build and start services
docker-compose up --build -d

echo "⏳ Waiting for services to start..."
sleep 30

# Check if services are running
if docker-compose ps | grep -q "Up"; then
    echo "✅ Services started successfully!"
    echo ""
    echo "📊 Service Status:"
    docker-compose ps
    echo ""
    echo "🌐 Access URLs:"
    echo "  - API Documentation: http://localhost:8000/docs"
    echo "  - Health Check: http://localhost:8000/health"
    echo "  - Ollama Service: http://localhost:11434"
    echo ""
    echo "📖 Usage Example:"
    echo 'curl -X POST "http://localhost:8000/invoke_pentest" \'
    echo '  -H "Content-Type: application/json" \'
    echo '  -d "{'
    echo '    \"target\": \"https://juice-shop.herokuapp.com\",'
    echo '    \"consent_acknowledged\": true'
    echo '  }"'
    echo ""
    echo "🔗 OpenSearch Dashboard:"
    echo "  https://cybrty-dev-ca.wonderfuldune-e921120d.eastus.azurecontainerapps.io"
    echo ""
    echo "⚠️  REMEMBER: Only test authorized targets!"
else
    echo "❌ Some services failed to start. Checking logs..."
    docker-compose logs
fi