# Smart Construction Planner - Docker Deployment Script
# This script handles the complete Docker deployment process

param(
    [switch]$Setup,
    [switch]$Start,
    [switch]$Stop,
    [switch]$Restart,
    [switch]$Logs,
    [switch]$Status
)

$ErrorActionPreference = "Stop"

Write-Host "🐳 Smart Construction Planner - Docker Deployment" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan

# Function to check if Docker is running
function Test-Docker {
    try {
        docker ps > $null 2>&1
        return $true
    } catch {
        return $false
    }
}

# Function to check if Docker Compose is available
function Test-DockerCompose {
    try {
        docker-compose --version > $null 2>&1
        return $true
    } catch {
        try {
            docker compose version > $null 2>&1
            return $true
        } catch {
            return $false
        }
    }
}

# Setup function
function Setup-Environment {
    Write-Host "`n🔧 Setting up environment..." -ForegroundColor Yellow
    
    # Check Docker installation
    if (!(Test-Docker)) {
        Write-Host "❌ Docker is not running or not installed." -ForegroundColor Red
        Write-Host "Please install Docker Desktop and ensure it's running." -ForegroundColor Yellow
        Write-Host "Download from: https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe" -ForegroundColor Cyan
        return $false
    }
    
    # Check Docker Compose
    if (!(Test-DockerCompose)) {
        Write-Host "❌ Docker Compose is not available." -ForegroundColor Red
        return $false
    }
    
    # Check .env file
    if (!(Test-Path ".env")) {
        Write-Host "📝 Creating .env file from template..." -ForegroundColor Yellow
        Copy-Item ".env.example" ".env"
        Write-Host "⚠️  Please edit .env file with your API keys before starting." -ForegroundColor Yellow
        Write-Host "Run: .\setup-env.ps1 to configure interactively" -ForegroundColor Cyan
        return $false
    }
    
    # Check OpenAI API key
    $envContent = Get-Content ".env"
    $hasOpenAIKey = $envContent | Where-Object { $_ -match "^OPENAI_API_KEY=" -and $_ -notmatch "your_openai_api_key_here" }
    
    if (!$hasOpenAIKey) {
        Write-Host "⚠️  No OpenAI API key found in .env file." -ForegroundColor Yellow
        Write-Host "AI features will be disabled without a valid OpenAI API key." -ForegroundColor Yellow
        Write-Host "Run: .\setup-env.ps1 to configure your API keys" -ForegroundColor Cyan
    }
    
    # Create required directories
    @("data", "logs") | ForEach-Object {
        if (!(Test-Path $_)) {
            New-Item -ItemType Directory -Path $_ | Out-Null
            Write-Host "📁 Created $_ directory" -ForegroundColor Green
        }
    }
    
    Write-Host "✅ Environment setup complete!" -ForegroundColor Green
    return $true
}

# Start services
function Start-Services {
    Write-Host "`n🚀 Starting Smart Construction Planner..." -ForegroundColor Yellow
    
    try {
        # Determine Docker Compose command
        $composeCmd = if (Get-Command docker-compose -ErrorAction SilentlyContinue) { "docker-compose" } else { "docker compose" }
        
        Write-Host "📦 Building and starting containers..." -ForegroundColor Cyan
        & $composeCmd up -d --build
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "`n✅ Smart Construction Planner is now running!" -ForegroundColor Green
            Write-Host "🌐 Access your application at: http://localhost:8501" -ForegroundColor Cyan
            Write-Host "📊 View container status: docker ps" -ForegroundColor Gray
            Write-Host "📋 View logs: docker-compose logs -f smart-planner" -ForegroundColor Gray
        } else {
            throw "Docker Compose failed to start services"
        }
    } catch {
        Write-Host "❌ Failed to start services: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
    
    return $true
}

# Stop services
function Stop-Services {
    Write-Host "`n⏹️ Stopping Smart Construction Planner..." -ForegroundColor Yellow
    
    try {
        $composeCmd = if (Get-Command docker-compose -ErrorAction SilentlyContinue) { "docker-compose" } else { "docker compose" }
        & $composeCmd down
        
        Write-Host "✅ Services stopped successfully!" -ForegroundColor Green
    } catch {
        Write-Host "❌ Failed to stop services: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
    
    return $true
}

# Show logs
function Show-Logs {
    Write-Host "`n📋 Showing application logs..." -ForegroundColor Yellow
    Write-Host "Press Ctrl+C to exit logs view" -ForegroundColor Gray
    
    try {
        $composeCmd = if (Get-Command docker-compose -ErrorAction SilentlyContinue) { "docker-compose" } else { "docker compose" }
        & $composeCmd logs -f smart-planner
    } catch {
        Write-Host "❌ Failed to show logs: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Show status
function Show-Status {
    Write-Host "`n📊 Container Status:" -ForegroundColor Cyan
    docker ps -a --filter "name=smart-construction-planner"
    
    Write-Host "`n🔍 Service Health:" -ForegroundColor Cyan
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8501" -UseBasicParsing -TimeoutSec 5
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ Application is responding at http://localhost:8501" -ForegroundColor Green
        }
    } catch {
        Write-Host "❌ Application is not responding at http://localhost:8501" -ForegroundColor Red
    }
}

# Main execution logic
if ($Setup -or (!$Start -and !$Stop -and !$Restart -and !$Logs -and !$Status)) {
    if (!(Setup-Environment)) {
        exit 1
    }
    if (!$Setup) {
        $Start = $true
    }
}

if ($Stop) {
    Stop-Services
    exit $LASTEXITCODE
}

if ($Restart) {
    Stop-Services
    Start-Sleep -Seconds 2
    $Start = $true
}

if ($Start) {
    if (!(Setup-Environment)) {
        exit 1
    }
    Start-Services
    Show-Status
}

if ($Logs) {
    Show-Logs
}

if ($Status) {
    Show-Status
}

Write-Host "`n🎯 Deployment Commands:" -ForegroundColor Cyan
Write-Host "  .\deploy-docker.ps1 -Setup    # Setup environment only" -ForegroundColor White
Write-Host "  .\deploy-docker.ps1 -Start    # Start the application" -ForegroundColor White
Write-Host "  .\deploy-docker.ps1 -Stop     # Stop the application" -ForegroundColor White
Write-Host "  .\deploy-docker.ps1 -Restart  # Restart the application" -ForegroundColor White
Write-Host "  .\deploy-docker.ps1 -Logs     # View application logs" -ForegroundColor White
Write-Host "  .\deploy-docker.ps1 -Status   # Check service status" -ForegroundColor White
