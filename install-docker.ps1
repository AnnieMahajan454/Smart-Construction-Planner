# Smart Construction Planner - Docker Installation Script
# Run this script as Administrator in PowerShell

Write-Host "🐳 Installing Docker Desktop for Smart Construction Planner..." -ForegroundColor Cyan

# Check if running as Administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "❌ This script requires Administrator privileges. Please run PowerShell as Administrator." -ForegroundColor Red
    exit 1
}

try {
    # Install Chocolatey if not present
    if (!(Get-Command choco -ErrorAction SilentlyContinue)) {
        Write-Host "📦 Installing Chocolatey package manager..." -ForegroundColor Yellow
        Set-ExecutionPolicy Bypass -Scope Process -Force
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
        Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
        
        # Refresh environment variables
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    }

    # Install Docker Desktop
    Write-Host "🐳 Installing Docker Desktop..." -ForegroundColor Yellow
    choco install docker-desktop -y

    Write-Host "✅ Docker installation completed!" -ForegroundColor Green
    Write-Host "🔄 Please restart your computer to complete the installation." -ForegroundColor Yellow
    Write-Host "📋 After restart, Docker Desktop should start automatically." -ForegroundColor Cyan
    Write-Host "🧪 Test your installation by running: docker --version" -ForegroundColor Cyan

} catch {
    Write-Host "❌ Installation failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "💡 Try manual installation from: https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe" -ForegroundColor Yellow
}

Write-Host "`n🎯 Next Steps:" -ForegroundColor Cyan
Write-Host "1. Restart your computer" -ForegroundColor White
Write-Host "2. Open Docker Desktop and complete setup" -ForegroundColor White
Write-Host "3. Return to deploy your Smart Construction Planner!" -ForegroundColor White
