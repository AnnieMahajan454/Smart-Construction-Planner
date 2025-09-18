# Docker Setup for Windows - Smart Construction Planner

## Step 1: Install Docker Desktop

### Download and Install
1. Visit [Docker Desktop for Windows](https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe)
2. Download the Docker Desktop Installer
3. Run the installer as Administrator
4. Follow the installation wizard
5. **Important**: Enable "Use WSL 2 instead of Hyper-V" if prompted
6. Restart your computer when prompted

### System Requirements
- Windows 10 64-bit: Home or Pro 21H1 (build 19043) or higher, or Enterprise or Education 20H1 (build 19041) or higher
- WSL 2 feature enabled
- BIOS-level hardware virtualization support enabled

## Step 2: Enable WSL 2 (if not already enabled)

Open PowerShell as Administrator and run:

```powershell
# Enable WSL and Virtual Machine Platform
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# Download and install WSL 2 Linux kernel update
# Visit: https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi

# Set WSL 2 as default
wsl --set-default-version 2
```

## Step 3: Verify Installation

After installation and restart, open PowerShell and run:

```powershell
docker --version
docker-compose --version
```

You should see version information for both Docker and Docker Compose.

## Step 4: Test Docker

```powershell
docker run hello-world
```

This should download and run a test container successfully.

## Quick Installation Alternative

If you prefer automated installation, you can use Chocolatey:

```powershell
# Install Chocolatey (if not installed)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install Docker Desktop
choco install docker-desktop
```

## Troubleshooting

### WSL 2 Installation Error
If you get WSL 2 errors:
1. Make sure Windows is updated
2. Enable virtualization in BIOS
3. Run Windows Update
4. Install WSL 2 kernel manually from Microsoft

### Docker Desktop Won't Start
1. Restart Docker Desktop
2. Reset Docker to factory defaults
3. Check Windows Defender/antivirus isn't blocking Docker

---

**Once Docker is installed, come back to continue with the Smart Construction Planner deployment!**
