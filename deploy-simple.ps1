# Smart Construction Planner - Simple Docker Deployment Script

param(
    [switch]$Setup,
    [switch]$Start,
    [switch]$Stop,
    [switch]$Restart,
    [switch]$Logs,
    [switch]$Status
)

Write-Host "Docker Deployment - Smart Construction Planner" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan

# Function to check if Docker is running
function Test-Docker {
    try {
        docker ps *> $null
        return $true
    } catch {
        return $false
    }
}

# Function to check Docker Compose
function Test-DockerCompose {
    try {
        docker-compose --version *> $null
        return $true
    } catch {
        try {
            docker compose version *> $null
            return $true
        } catch {
            return $false
        }
    }
}

# Setup function
function Setup-Environment {
    Write-Host "`nSetting up environment..." -ForegroundColor Yellow
    
    # Check Docker
    if (!(Test-Docker)) {
        Write-Host "ERROR: Docker is not running or not installed." -ForegroundColor Red
        Write-Host "Please install Docker Desktop and ensure it's running." -ForegroundColor Yellow
        Write-Host "Download: https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe" -ForegroundColor Cyan
        return $false
    }
    
    # Check Docker Compose
    if (!(Test-DockerCompose)) {
        Write-Host "ERROR: Docker Compose is not available." -ForegroundColor Red
        return $false
    }
    
    # Check .env file
    if (!(Test-Path ".env")) {
        Write-Host "Creating .env file from template..." -ForegroundColor Yellow
        Copy-Item ".env.example" ".env"
        Write-Host "WARNING: Please edit .env file with your API keys." -ForegroundColor Yellow
        Write-Host "Run: .\setup-env.ps1 to configure interactively" -ForegroundColor Cyan
        return $false
    }
    
    # Check OpenAI API key
    $envContent = Get-Content ".env"
    $hasOpenAIKey = $envContent | Where-Object { $_ -match "^OPENAI_API_KEY=" -and $_ -notmatch "your_openai_api_key_here" }
    
    if (!$hasOpenAIKey) {
        Write-Host "WARNING: No OpenAI API key found in .env file." -ForegroundColor Yellow
        Write-Host "AI features will be disabled without a valid OpenAI API key." -ForegroundColor Yellow
        Write-Host "Run: .\setup-env.ps1 to configure your API keys" -ForegroundColor Cyan
    }
    
    # Create directories
    @("data", "logs") | ForEach-Object {
        if (!(Test-Path $_)) {
            New-Item -ItemType Directory -Path $_ | Out-Null
            Write-Host "Created $_ directory" -ForegroundColor Green
        }
    }
    
    Write-Host "Environment setup complete!" -ForegroundColor Green
    return $true
}

# Start services
function Start-Services {
    Write-Host "`nStarting Smart Construction Planner..." -ForegroundColor Yellow
    
    try {
        $composeCmd = if (Get-Command docker-compose -ErrorAction SilentlyContinue) { "docker-compose" } else { "docker compose" }
        
        Write-Host "Building and starting containers..." -ForegroundColor Cyan
        & $composeCmd up -d --build
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "`nSmart Construction Planner is now running!" -ForegroundColor Green
            Write-Host "Access your application at: http://localhost:8501" -ForegroundColor Cyan
            Write-Host "View container status: docker ps" -ForegroundColor Gray
            Write-Host "View logs: docker-compose logs -f smart-planner" -ForegroundColor Gray
        } else {
            throw "Docker Compose failed to start services"
        }
    } catch {
        Write-Host "ERROR: Failed to start services: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
    
    return $true
}

# Stop services
function Stop-Services {
    Write-Host "`nStopping Smart Construction Planner..." -ForegroundColor Yellow
    
    try {
        $composeCmd = if (Get-Command docker-compose -ErrorAction SilentlyContinue) { "docker-compose" } else { "docker compose" }
        & $composeCmd down
        
        Write-Host "Services stopped successfully!" -ForegroundColor Green
    } catch {
        Write-Host "ERROR: Failed to stop services: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
    
    return $true
}

# Show logs
function Show-Logs {
    Write-Host "`nShowing application logs..." -ForegroundColor Yellow
    Write-Host "Press Ctrl+C to exit logs view" -ForegroundColor Gray
    
    try {
        $composeCmd = if (Get-Command docker-compose -ErrorAction SilentlyContinue) { "docker-compose" } else { "docker compose" }
        & $composeCmd logs -f smart-planner
    } catch {
        Write-Host "ERROR: Failed to show logs: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Show status
function Show-Status {
    Write-Host "`nContainer Status:" -ForegroundColor Cyan
    docker ps -a --filter "name=smart-construction-planner"
    
    Write-Host "`nService Health:" -ForegroundColor Cyan
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8501" -UseBasicParsing -TimeoutSec 5
        if ($response.StatusCode -eq 200) {
            Write-Host "SUCCESS: Application is responding at http://localhost:8501" -ForegroundColor Green
        }
    } catch {
        Write-Host "ERROR: Application is not responding at http://localhost:8501" -ForegroundColor Red
    }
}

# Main execution
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

Write-Host "`nDeployment Commands:" -ForegroundColor Cyan
Write-Host "  .\deploy-simple.ps1 -Setup    # Setup environment only" -ForegroundColor White
Write-Host "  .\deploy-simple.ps1 -Start    # Start the application" -ForegroundColor White
Write-Host "  .\deploy-simple.ps1 -Stop     # Stop the application" -ForegroundColor White
Write-Host "  .\deploy-simple.ps1 -Restart  # Restart the application" -ForegroundColor White
Write-Host "  .\deploy-simple.ps1 -Logs     # View application logs" -ForegroundColor White
Write-Host "  .\deploy-simple.ps1 -Status   # Check service status" -ForegroundColor White
