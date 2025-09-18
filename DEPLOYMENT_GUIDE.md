# Smart Construction Planner - Deployment Guide with AI Features

This guide covers multiple deployment options for the Smart Construction Planner with full AI features enabled.

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.9 or higher
- Git
- OpenAI API account (required for AI features)

### Step 1: Clone and Setup
```bash
git clone https://github.com/AnnieMahajan454/Smart-Construction-Planner.git
cd Smart-Construction-Planner
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
1. Copy the environment template:
   ```bash
   cp .env.example .env
   ```
2. Edit `.env` file with your API keys:
   ```env
   OPENAI_API_KEY=sk-your-actual-openai-api-key
   OPENWEATHERMAP_API_KEY=your-weather-api-key (optional)
   TRAFFIC_API_KEY=your-traffic-api-key (optional)
   ```

### Step 5: Run the Application
```bash
streamlit run main.py
```

The app will be available at `http://localhost:8501`

## ☁️ Streamlit Cloud Deployment (Recommended)

### Prerequisites
- GitHub repository (you already have this!)
- Streamlit Cloud account (free)
- OpenAI API key

### Step 1: Prepare for Streamlit Cloud
1. Make sure all changes are committed to GitHub
2. Create `.streamlit/secrets.toml` (locally for reference):
   ```toml
   [secrets]
   OPENAI_API_KEY = "sk-your-actual-openai-api-key"
   OPENWEATHERMAP_API_KEY = "your-weather-api-key"
   ```

### Step 2: Deploy to Streamlit Cloud
1. Visit [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository: `AnnieMahajan454/Smart-Construction-Planner`
5. Set main file path: `main.py`
6. Click "Advanced settings"
7. Add secrets in the secrets section:
   ```
   OPENAI_API_KEY = "sk-your-actual-openai-api-key"
   OPENWEATHERMAP_API_KEY = "your-weather-api-key"
   ```
8. Click "Deploy"

Your app will be live at: `https://your-app-name.streamlit.app`

## 🐳 Docker Deployment

### Prerequisites
- Docker and Docker Compose installed
- API keys ready

### Step 1: Configure Environment
```bash
cp .env.example .env
# Edit .env with your API keys
```

### Step 2: Build and Run with Docker Compose
```bash
docker-compose up -d
```

### Step 3: Access the Application
- Local: `http://localhost:8501`
- Check logs: `docker-compose logs -f smart-planner`

### Step 4: Stop the Application
```bash
docker-compose down
```

## 🏭 Production Deployment (AWS/Azure/GCP)

### Option 1: AWS EC2 + Docker
```bash
# On your EC2 instance
git clone https://github.com/AnnieMahajan454/Smart-Construction-Planner.git
cd Smart-Construction-Planner
cp .env.example .env
# Edit .env with your API keys
docker-compose up -d
```

### Option 2: Heroku
1. Install Heroku CLI
2. Create Heroku app:
   ```bash
   heroku create your-app-name
   ```
3. Set config vars:
   ```bash
   heroku config:set OPENAI_API_KEY=sk-your-key
   heroku config:set OPENWEATHERMAP_API_KEY=your-key
   ```
4. Deploy:
   ```bash
   git push heroku main
   ```

## 🔑 Required API Keys

### OpenAI API Key (Essential for AI features)
1. Visit [platform.openai.com](https://platform.openai.com)
2. Sign up or log in
3. Go to API Keys section
4. Create a new secret key
5. Copy the key (starts with `sk-`)

**Cost**: ~$0.002 per 1K tokens (GPT-4)

### Optional API Keys

#### OpenWeatherMap (Weather data)
- Free tier: 1,000 calls/day
- Sign up at [openweathermap.org](https://openweathermap.org/api)

#### Traffic APIs
- Here API, MapBox, or Google Maps
- Used for real-time traffic data

## 🧪 Testing Your Deployment

### 1. Basic Functionality Test
- Navigate to the app URL
- Check if all pages load
- Test basic calculations

### 2. AI Features Test
- Go to "💰 Cost Estimator" page
- Enter project details and click "Estimate Cost"
- Try the "What-If Simulator" - you should see AI explanations
- If you see "⚠️ OPENAI_API_KEY not found", check your configuration

### 3. Advanced Features Test
- Test "🌱 Sustainability Assessment"
- Test "⚠️ Risk Assessment"
- Check that all charts and analytics display correctly

## 🔧 Troubleshooting

### Common Issues

#### "Advanced features not available" Error
- Check if `smart_planner` modules are properly installed
- Ensure all dependencies from `requirements.txt` are installed

#### AI Features Not Working
- Verify `OPENAI_API_KEY` is set correctly
- Check API key has sufficient credits
- Ensure key has GPT-4 access

#### Geospatial Dependencies Issues
```bash
# On Ubuntu/Debian
sudo apt-get install gdal-bin libgdal-dev libproj-dev libspatialindex-dev

# On macOS
brew install gdal proj spatialindex

# On Windows
# Use conda: conda install -c conda-forge geopandas
```

#### Memory Issues
- Reduce model complexity in production
- Use lighter AI models if needed
- Consider increasing server memory

### Performance Optimization

#### For Production:
1. Enable caching:
   ```python
   @st.cache_data
   def expensive_function():
       # Your code here
   ```

2. Optimize AI calls:
   - Cache AI responses
   - Use cheaper models for simple tasks
   - Implement rate limiting

## 📊 Monitoring and Logs

### Docker Logs
```bash
docker-compose logs -f smart-planner
```

### Streamlit Cloud Logs
- Available in the Streamlit Cloud dashboard
- Check for API errors and performance issues

## 🔄 Updates and Maintenance

### Updating the Application
```bash
git pull origin main
docker-compose down
docker-compose up -d --build
```

### Backing Up Data
- Export any user configurations
- Backup environment variables
- Save custom datasets if any

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review application logs
3. Ensure all API keys are valid and have sufficient credits
4. Check GitHub issues for known problems

## 🎯 Next Steps

After successful deployment:
1. Set up monitoring and alerting
2. Configure SSL/HTTPS for production
3. Set up automated backups
4. Consider implementing user authentication
5. Monitor API usage and costs

---

**Your Smart Construction Planner is now ready for deployment with full AI capabilities!** 🎉
