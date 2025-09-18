# Smart Construction Planner - Environment Setup Script
# This script helps you configure your API keys for Docker deployment

Write-Host "🎯 Smart Construction Planner - Environment Setup" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan

# Check if .env file exists
if (!(Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "📝 Created .env file from template" -ForegroundColor Green
}

Write-Host "`n🔑 API Key Configuration" -ForegroundColor Yellow
Write-Host "To enable AI features, you need at least an OpenAI API key." -ForegroundColor White

# OpenAI API Key (Required)
Write-Host "`n🤖 OpenAI API Key (REQUIRED for AI features):" -ForegroundColor Cyan
Write-Host "Get your key from: https://platform.openai.com/api-keys" -ForegroundColor Gray
$openai_key = Read-Host "Enter your OpenAI API key (starts with 'sk-')"

if ($openai_key -and $openai_key.StartsWith("sk-")) {
    (Get-Content ".env") -replace "OPENAI_API_KEY=your_openai_api_key_here", "OPENAI_API_KEY=$openai_key" | Set-Content ".env"
    Write-Host "✅ OpenAI API key configured!" -ForegroundColor Green
} elseif ($openai_key) {
    Write-Host "⚠️  Warning: OpenAI API key should start with 'sk-'. Please verify your key." -ForegroundColor Yellow
    (Get-Content ".env") -replace "OPENAI_API_KEY=your_openai_api_key_here", "OPENAI_API_KEY=$openai_key" | Set-Content ".env"
} else {
    Write-Host "⚠️  No OpenAI API key provided. AI features will be disabled." -ForegroundColor Yellow
}

# Optional APIs
Write-Host "`n🌤️  Optional: OpenWeatherMap API Key (for weather data):" -ForegroundColor Cyan
Write-Host "Get free key from: https://openweathermap.org/api" -ForegroundColor Gray
Write-Host "Press Enter to skip, or enter your API key:" -ForegroundColor Gray
$weather_key = Read-Host

if ($weather_key) {
    (Get-Content ".env") -replace "OPENWEATHERMAP_API_KEY=your_weather_api_key_here", "OPENWEATHERMAP_API_KEY=$weather_key" | Set-Content ".env"
    Write-Host "✅ Weather API key configured!" -ForegroundColor Green
}

Write-Host "`n✅ Environment setup complete!" -ForegroundColor Green
Write-Host "`n📋 Your configuration:" -ForegroundColor Cyan
Get-Content ".env" | ForEach-Object {
    if ($_ -match "^[A-Z_]+=" -and $_ -notmatch "=your_.*_here") {
        $key = ($_ -split "=")[0]
        $value = ($_ -split "=",2)[1]
        if ($value -match "^sk-") {
            Write-Host "  $key=sk-***[hidden]***" -ForegroundColor White
        } else {
            Write-Host "  $_" -ForegroundColor White
        }
    }
}

Write-Host "`n🐳 Next Steps:" -ForegroundColor Cyan
Write-Host "1. Install Docker Desktop if you haven't already" -ForegroundColor White
Write-Host "2. Run: docker-compose up -d" -ForegroundColor White
Write-Host "3. Open http://localhost:8501 in your browser" -ForegroundColor White

Write-Host "`n🎉 Ready to deploy your Smart Construction Planner!" -ForegroundColor Green
