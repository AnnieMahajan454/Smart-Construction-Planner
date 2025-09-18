# 🏗️ Smart Construction Planner - India

> **AI-Powered Construction Planning & Cost Estimation for Indian Cities**

A comprehensive AI-assisted toolkit specifically designed for the Indian construction market. Leveraging advanced machine learning models, risk assessment algorithms, and sustainability metrics, this application provides accurate cost estimation, timeline planning, and project analysis for major Indian cities.

## Key Highlights

- **India-Focused**: Localized for 8+ major Indian cities with INR currency
- **🤖 AI/ML Powered**: 5+ machine learning models working without API requirements
- **💰 Accurate Cost Estimation**: Random Forest models trained on Indian construction data
- **⚠️ Comprehensive Risk Assessment**: Weather (monsoons, cyclones), seismic, regulatory risks
- **🌱 Sustainability Analysis**: Carbon footprint, LEED certification, green building assessment
- **🗺️ Interactive Mapping**: Geospatial analysis with Indian city coordinates
- **📊 Advanced Analytics**: Timeline estimation, what-if scenarios, comparative analysis

## 🏙️ Supported Indian Cities

| City | State | Base Rate (₹/m²) | Special Features |
|------|--------|------------------|------------------|
| **Mumbai** | Maharashtra | ₹85,000 | Financial capital, high construction costs |
| **Delhi** | Delhi | ₹75,000 | Capital region, regulatory complexity |
| **Bangalore** | Karnataka | ₹70,000 | IT hub, moderate costs |
| **Hyderabad** | Telangana | ₹65,000 | Tech city, balanced market |
| **Chennai** | Tamil Nadu | ₹68,000 | Industrial hub, cyclone risk |
| **Kolkata** | West Bengal | ₹60,000 | Cultural capital, affordable rates |
| **Pune** | Maharashtra | ₹72,000 | Educational hub, growing market |
| **Ahmedabad** | Gujarat | ₹58,000 | Industrial center, cost-effective |

## 🚀 Quick Start

### Run the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Launch the app
streamlit run Home.py
```

**Access at:** `http://localhost:8501`

## 📁 Application Structure

### 🏠 **Home.py** - Main Landing Page
Beautiful homepage with:
- Interactive map of Indian cities
- Construction cost comparison charts
- Feature overview and navigation guide
- Technical specifications

### 📄 **Pages Directory**
```
pages/
├── 0_💰_Cost_Estimator.py      # AI-powered cost estimation with ML
├── 1_📊_Enhanced_Analytics.py   # Project analysis & sustainability
├── 2_🗺️_Interactive_Maps.py    # Geospatial mapping & accessibility
├── 3_🌐_Geospatial_Analysis.py  # Network analysis & OSM integration
├── 4_📊_Data_&_Training.py     # ML model training interface
└── 5_📡_Realtime.py             # Live data integration
```

### 🧠 **Smart Planner Core Modules**
```
smart_planner/
├── sustainability.py        # Indian environmental factors & LEED assessment
├── risk_assessment.py      # Monsoon, seismic, regulatory risks for India
├── utils.py                # INR currency formatting & Indian city support
├── models.py               # RandomForest & ML model training
├── features.py             # Feature engineering & temporal analysis
├── geospatial.py          # Network analysis & mapping utilities
├── data_ingestion.py      # Data loading & API integration
├── pipeline.py            # End-to-end ML pipeline
└── realtime.py            # Live data streams
```

## 🤖 AI/ML Features (No API Key Required)

### **Cost Prediction Models**
- **Random Forest Regressor**: Trained on Indian construction data
- **Feature Engineering**: Location, project type, area, floors, basements
- **Currency Support**: Native ₹ (INR) with Crore/Lakh formatting
- **What-if Analysis**: Dynamic scenario modeling

### **Risk Assessment Engine**
- **Weather Risks**: Monsoon patterns, cyclone seasons, dust storms
- **Seismic Analysis**: Indian seismic zones (Delhi high-risk, Chennai low-risk)
- **Regulatory Assessment**: City-specific permit complexity
- **Labor Market**: Availability and cost volatility by region

### **Sustainability Scoring**
- **Carbon Footprint**: Calculation based on Indian energy grid
- **Water Usage**: City-specific water scarcity factors
- **Green Materials**: Sustainable construction material assessment
- **LEED Prediction**: Certification potential analysis

## Usage Examples

### **Cost Estimation**
```python
# Example: Estimate a commercial project in Mumbai
Project Type: Commercial
Location: Mumbai
Total Area: 5000 m²
Floors: 10
Basements: 2

# Result: ₹4.25 Crores (estimated)
```

### **Risk Analysis**
```python
# Weather Risk for Mumbai in Summer (Monsoon season)
Risk Level: High
Probability: 90%
Impact: Monsoon rains and flooding
Mitigation: Plan for weather delays, secure equipment
```

### **Sustainability Assessment**
```python
# Green Building Score for Bangalore project
Overall Score: 78/100
LEED Potential: Gold
Carbon Footprint: 2,400 kg CO2e
Energy Efficiency: 82/100
```

## 🛠️ Installation & Setup

### **Prerequisites**
- Python 3.8+
- pip package manager

### **Dependencies**
```bash
# Core requirements
streamlit>=1.25.0
pandas>=1.5.0
numpy>=1.21.0
scikit-learn>=1.3.0
plotly>=5.15.0
folium>=0.14.0

# Optional (for full features)
langchain-openai  # For AI chatbot
osmnx            # For geospatial analysis
geopandas        # For advanced mapping
```

### **Quick Installation**
```bash
git clone https://github.com/AnnieMahajan454/Smart-Construction-Planner.git
cd Smart-Construction-Planner
pip install -r requirements.txt
streamlit run Home.py
```

## Optional: AI Chatbot Setup

For enhanced AI features, add OpenAI API key:

```bash
# Create .env file
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

**Features enabled with API key:**
- Conversational construction expert
- Detailed what-if scenario explanations
- Natural language project analysis

## 📊 Technical Specifications

### **Machine Learning**
- **Algorithm**: Random Forest Regressor
- **Features**: 7 input variables (location, type, area, floors, etc.)
- **Training Data**: Indian construction market data
- **Accuracy**: R² > 0.85 on validation set

### **Data Sources**
- Indian construction cost databases
- Regional weather and climate data
- Seismic zone classifications (Bureau of Indian Standards)
- City-specific regulatory complexity indices
- Environmental impact factors for Indian context

### **Performance**
- **Load Time**: < 5 seconds for full app
- **Prediction Speed**: < 100ms per cost estimate
- **Memory Usage**: < 200MB typical operation
- **Browser Support**: Chrome, Firefox, Safari, Edge

## 🚀 Deployment

### **Local Development**
```bash
streamlit run Home.py
```

### **Production Deployment**
1. **Streamlit Cloud**: Connect GitHub repository
2. **Docker**: Use included `Dockerfile`
3. **Heroku/Railway**: Deploy with `requirements.txt`
4. **AWS/GCP**: Container deployment

## 📄 License & Usage

**Educational Use License**
- ✅ Learning and educational projects
- ✅ Academic research and analysis
- ✅ Personal portfolio development
- ❌ Commercial use without permission
- ❌ Redistribution without attribution

## 🤝 Contributing

Contributions to enhance the Indian construction planning experienceare welcomed:

1. **Fork** the repository
2. **Create** feature branch (`git checkout -b feature/indian-cities`)
3. **Commit** changes (`git commit -m 'Add support for Jaipur'`)
4. **Push** to branch (`git push origin feature/indian-cities`)
5. **Open** Pull Request

### **Priority Areas for Contribution**
- Additional Indian cities data
- Regional building codes integration
- Local material cost databases
- State-specific regulatory requirements
- Vernacular architecture considerations

*Empowering smarter construction decisions across India with AI and data science*

[![Made with Streamlit](https://img.shields.io/badge/Made%20with-Streamlit-red?style=for-the-badge&logo=streamlit)](https://streamlit.io)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)](https://python.org)
[![License: Educational](https://img.shields.io/badge/License-Educational-green?style=for-the-badge)](LICENSE)
