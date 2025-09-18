# 🐳 Docker Deployment - Quick Start

## Prerequisites Checklist
- [ ] **Docker Desktop installed** (Download: https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe)
- [ ] **Docker Desktop is running** (check system tray for whale icon)
- [ ] **OpenAI API Key** (Get from: https://platform.openai.com/api-keys)

## 🚀 3-Step Deployment

### Step 1: Configure Environment
```powershell
# Run the interactive setup
.\setup-env.ps1
```

### Step 2: Deploy with Docker
```powershell
# Start the application
.\deploy-docker.ps1
```

### Step 3: Access Your Application
Open your browser: **http://localhost:8501**

## 📋 Management Commands

```powershell
# Start the application
.\deploy-docker.ps1 -Start

# Stop the application
.\deploy-docker.ps1 -Stop

# Restart the application
.\deploy-docker.ps1 -Restart

# View logs
.\deploy-docker.ps1 -Logs

# Check status
.\deploy-docker.ps1 -Status

# Setup environment only
.\deploy-docker.ps1 -Setup
```

## 🔍 Troubleshooting

### "Docker is not running"
- Start Docker Desktop from Start Menu
- Wait for whale icon in system tray
- Run `docker --version` to test

### "No OpenAI API key found"
- Get API key from https://platform.openai.com/api-keys
- Run `.\setup-env.ps1` to configure
- Make sure key starts with `sk-`

### "Port 8501 already in use"
```powershell
# Stop any existing containers
docker-compose down
# Or find and stop the process using port 8501
netstat -ano | findstr :8501
```

### "Container fails to start"
```powershell
# View detailed logs
.\deploy-docker.ps1 -Logs
```

## ✅ Verify Deployment

1. **Container Status**: `docker ps` should show `smart-construction-planner` running
2. **Web Access**: http://localhost:8501 should load the app
3. **AI Features**: Go to "💰 Cost Estimator" and test AI explanations

## 🎯 What You Get

✅ **Complete Smart Construction Planner**
✅ **AI-powered cost estimation**
✅ **Interactive maps and analytics**
✅ **Risk and sustainability assessment**
✅ **Automatic container management**
✅ **Persistent data storage**

## 🔄 Updates

```powershell
# Pull latest changes
git pull origin main

# Restart with new code
.\deploy-docker.ps1 -Restart
```

---

**🎉 That's it! Your Smart Construction Planner is running in Docker with full AI capabilities!**
