# Smart Construction Planner - Deployment Guide

This guide provides instructions for deploying the Smart Construction Planner to various platforms.

## 🚀 Quick Deployment (Streamlit Cloud)

### Prerequisites
- GitHub account
- Forked copy of this repository
- (Optional) OpenAI API key for AI chatbot features

### Steps

1. **Fork the Repository**
   ```bash
   # Go to https://github.com/AnnieMahajan454/Smart-Construction-Planner
   # Click "Fork" to create your own copy
   ```

2. **Deploy to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account
   - Click "New app"
   - Select your forked repository
   - Set the main file path: `costestimator.py`
   - (Optional) Add environment variables:
     - `OPENAI_API_KEY`: Your OpenAI API key

3. **Deploy!**
   - Click "Deploy"
   - Wait for deployment to complete
   - Your app will be available at `https://[app-name].streamlit.app`

## 🔧 Local Development

### Setup
```bash
# Clone the repository
git clone https://github.com/AnnieMahajan454/Smart-Construction-Planner.git
cd Smart-Construction-Planner

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# (Optional) Create .env file for API keys
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env

# Run the application
streamlit run costestimator.py
```

### Running with Enhanced Features
```bash
# Install additional dependencies for advanced features
pip install -r requirements.txt

# Run with all features enabled
streamlit run costestimator.py
```

## 🌐 Alternative Deployment Options

### 1. Heroku Deployment

Create additional files:

**Procfile:**
```
web: sh setup.sh && streamlit run costestimator.py --server.port=$PORT --server.address=0.0.0.0
```

**setup.sh:**
```bash
mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
```

**Deploy Commands:**
```bash
heroku create your-app-name
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

### 2. Docker Deployment

**Dockerfile:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "costestimator.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**Build and Run:**
```bash
# Build the image
docker build -t smart-construction-planner .

# Run the container
docker run -p 8501:8501 smart-construction-planner
```

### 3. AWS EC2 Deployment

```bash
# Launch EC2 instance (Ubuntu 20.04)
# SSH into the instance

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3-pip python3-venv -y

# Clone repository
git clone https://github.com/AnnieMahajan454/Smart-Construction-Planner.git
cd Smart-Construction-Planner

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install nginx for reverse proxy
sudo apt install nginx -y

# Configure nginx (create /etc/nginx/sites-available/streamlit)
sudo nano /etc/nginx/sites-available/streamlit

# Nginx configuration:
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}

# Enable site
sudo ln -s /etc/nginx/sites-available/streamlit /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Run Streamlit
streamlit run costestimator.py --server.port 8501
```

## 📋 Environment Variables

### Required Variables
None - the app works with default data

### Optional Variables
- `OPENAI_API_KEY`: Enable AI chatbot features
- `LOG_LEVEL`: Set logging level (DEBUG, INFO, WARNING, ERROR)

### Setting Environment Variables

**Streamlit Cloud:**
- Go to your app settings
- Add secrets in the "Secrets" section:
```toml
OPENAI_API_KEY = "your_openai_api_key"
LOG_LEVEL = "INFO"
```

**Local Development (.env file):**
```env
OPENAI_API_KEY=your_openai_api_key
LOG_LEVEL=INFO
```

**Heroku:**
```bash
heroku config:set OPENAI_API_KEY=your_openai_api_key
heroku config:set LOG_LEVEL=INFO
```

## 🔍 Troubleshooting

### Common Issues

1. **Import Errors**
   - Make sure all dependencies are installed
   - Check Python version (3.8+ required)
   - Verify virtual environment is activated

2. **Streamlit Not Found**
   ```bash
   pip install streamlit
   ```

3. **Module Import Errors**
   ```bash
   # Set PYTHONPATH if needed
   export PYTHONPATH="${PYTHONPATH}:."
   ```

4. **Enhanced Features Not Available**
   - Enhanced features (sustainability, risk assessment, maps) are optional
   - App will work with basic features if advanced modules fail to load

### Performance Optimization

1. **Memory Usage**
   - Monitor RAM usage with large datasets
   - Use data caching appropriately
   - Consider data sampling for very large files

2. **Load Time**
   - Enable Streamlit caching with `@st.cache_data`
   - Preload common data
   - Use lazy loading for heavy computations

3. **User Experience**
   - Add progress bars for long operations
   - Use expanders for optional sections
   - Implement proper error handling

## 🧪 Testing Deployment

### Basic Functionality Test
1. Navigate to your deployed app
2. Try cost estimation with default values
3. Test what-if scenarios
4. Verify data visualizations load
5. (If enabled) Test AI chatbot features

### Enhanced Features Test
1. Navigate to "Enhanced Analytics" page
2. Test sustainability assessment
3. Test risk analysis
4. Navigate to "Interactive Maps" page
5. Verify map displays correctly

### Performance Test
1. Test with various input combinations
2. Monitor response times
3. Check error handling with invalid inputs
4. Verify mobile responsiveness

## 📊 Monitoring and Maintenance

### Streamlit Cloud
- Check app health at streamlit.io
- Monitor usage statistics
- Review app logs for errors

### Self-hosted Deployments
- Set up logging aggregation
- Monitor resource usage (CPU, RAM, disk)
- Implement health checks
- Set up automated backups

### Updates and Maintenance
```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Restart application (varies by deployment method)
```

## 🔒 Security Considerations

1. **API Keys**
   - Never commit API keys to version control
   - Use environment variables or secrets management
   - Rotate keys regularly

2. **Input Validation**
   - All user inputs are validated
   - Error messages don't expose system details
   - Rate limiting implemented where appropriate

3. **Data Privacy**
   - No user data is permanently stored
   - All calculations are performed client-side where possible
   - No sensitive data is logged

## 📞 Support

If you encounter issues during deployment:

1. Check the [Issues](https://github.com/AnnieMahajan454/Smart-Construction-Planner/issues) section
2. Review this deployment guide
3. Check Streamlit documentation
4. Create a new issue with:
   - Deployment method used
   - Error messages (without sensitive data)
   - Steps to reproduce the issue

---

**Happy Deploying! 🚀**
