# Git Setup Script for Penetration Testing Framework
# Run this script after installing Git

Write-Host "🔧 Setting up Git repository for Penetration Testing Framework..." -ForegroundColor Cyan

# Check if Git is installed
try {
    $gitVersion = git --version
    Write-Host "✅ Git is installed: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git is not installed. Please install Git first:" -ForegroundColor Red
    Write-Host "   Download from: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

# Initialize repository
Write-Host "📁 Initializing Git repository..." -ForegroundColor Yellow
git init

# Configure Git (replace with your details)
Write-Host "⚙️  Configuring Git user (you can change these later)..." -ForegroundColor Yellow
# git config user.name "Your Name"
# git config user.email "your.email@example.com"

# Add all files
Write-Host "📝 Adding files to Git..." -ForegroundColor Yellow
git add .

# Create initial commit
Write-Host "💾 Creating initial commit..." -ForegroundColor Yellow
git commit -m "Initial commit: Penetration Testing Framework

- FastAPI-based REST API
- CrewAI agent orchestration 
- Docker security tool integration
- OpenSearch result storage
- Modular testing framework
- Ethical security testing for authorized targets"

Write-Host "✅ Git repository setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "🎯 Next steps:" -ForegroundColor Cyan
Write-Host "   1. Set your Git identity:" -ForegroundColor White
Write-Host "      git config user.name 'Your Name'" -ForegroundColor Gray
Write-Host "      git config user.email 'your.email@example.com'" -ForegroundColor Gray
Write-Host ""
Write-Host "   2. Create a remote repository (GitHub/GitLab):" -ForegroundColor White
Write-Host "      git remote add origin <your-repo-url>" -ForegroundColor Gray
Write-Host "      git push -u origin main" -ForegroundColor Gray
Write-Host ""
Write-Host "   3. Or view status:" -ForegroundColor White
Write-Host "      git status" -ForegroundColor Gray
Write-Host "      git log --oneline" -ForegroundColor Gray