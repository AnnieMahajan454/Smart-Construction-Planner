import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page config
st.set_page_config(
    page_title="Smart Construction Planner - India",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #1f77b4;
    }
    .footer {
        text-align: center;
        padding: 2rem;
        color: #7f8c8d;
        margin-top: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<div class="main-header">🏗️ Smart Construction Planner - India 🇮🇳</div>', unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; font-size: 1.2rem; color: #34495e; margin-bottom: 2rem;">
    <strong>AI-Powered Construction Planning & Cost Estimation for Indian Cities</strong><br>
    Leverage advanced analytics, ML models, and risk assessment for smarter construction decisions
</div>
""", unsafe_allow_html=True)

# Key Metrics Dashboard
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <h3 style="color: #1f77b4; margin: 0;">8+</h3>
        <p style="margin: 0.5rem 0 0 0;">Major Indian Cities</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <h3 style="color: #27ae60; margin: 0;">5+</h3>
        <p style="margin: 0.5rem 0 0 0;">AI/ML Models</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <h3 style="color: #e74c3c; margin: 0;">15+</h3>
        <p style="margin: 0.5rem 0 0 0;">Risk Factors</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <h3 style="color: #f39c12; margin: 0;">₹</h3>
        <p style="margin: 0.5rem 0 0 0;">Indian Currency</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Features Overview
st.markdown('<div class="sub-header">🚀 Key Features</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h4>💰 AI-Powered Cost Estimation</h4>
        <ul>
            <li>Random Forest ML model for accurate predictions</li>
            <li>Indian city-specific rates in INR</li>
            <li>What-if scenario analysis</li>
            <li>Real-time cost comparisons</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-card">
        <h4>🌱 Sustainability Assessment</h4>
        <ul>
            <li>Carbon footprint calculation</li>
            <li>Energy efficiency scoring</li>
            <li>Water usage optimization</li>
            <li>LEED certification prediction</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-card">
        <h4>🗺️ Geospatial Analysis</h4>
        <ul>
            <li>Interactive maps with Indian cities</li>
            <li>Accessibility analysis</li>
            <li>Location-based insights</li>
            <li>Network analysis capabilities</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h4>⚠️ Risk Assessment</h4>
        <ul>
            <li>Weather risks (monsoons, cyclones)</li>
            <li>Seismic risk analysis</li>
            <li>Regulatory compliance</li>
            <li>Labor market conditions</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-card">
        <h4>📊 Enhanced Analytics</h4>
        <ul>
            <li>Project timeline estimation</li>
            <li>Interactive visualizations</li>
            <li>Performance dashboards</li>
            <li>Comparative analysis</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-card">
        <h4>🤖 Machine Learning</h4>
        <ul>
            <li>Demand forecasting models</li>
            <li>Feature engineering pipeline</li>
            <li>Predictive analytics</li>
            <li>Model training interface</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Indian Cities Coverage
st.markdown('<div class="sub-header">🏙️ Supported Indian Cities</div>', unsafe_allow_html=True)

# Create a map visualization
indian_cities = {
    'City': ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune', 'Ahmedabad'],
    'State': ['Maharashtra', 'Delhi', 'Karnataka', 'Telangana', 'Tamil Nadu', 'West Bengal', 'Maharashtra', 'Gujarat'],
    'Latitude': [19.0760, 28.7041, 12.9716, 17.3850, 13.0827, 22.5726, 18.5204, 23.0225],
    'Longitude': [72.8777, 77.1025, 77.5946, 78.4867, 80.2707, 88.3639, 73.8567, 72.5714],
    'Base_Rate_INR': [85000, 75000, 70000, 65000, 68000, 60000, 72000, 58000],
    'Population': [20.4, 32.9, 12.3, 10.0, 11.0, 14.9, 7.2, 8.4]  # in millions
}

cities_df = pd.DataFrame(indian_cities)

# Create map
fig_map = px.scatter_mapbox(
    cities_df,
    lat="Latitude",
    lon="Longitude",
    hover_name="City",
    hover_data={"State": True, "Base_Rate_INR": ":,.0f", "Population": ":.1f M"},
    color="Base_Rate_INR",
    size="Population",
    color_continuous_scale="Viridis",
    size_max=30,
    zoom=4,
    height=500,
    title="Construction Cost Rates Across Indian Cities"
)

fig_map.update_layout(
    mapbox_style="open-street-map",
    mapbox=dict(center=dict(lat=20.5937, lon=78.9629)),
    coloraxis_colorbar=dict(title="Base Rate (₹/m²)")
)

st.plotly_chart(fig_map, use_container_width=True)

# Cost comparison chart
st.markdown('<div class="sub-header">💹 City-wise Construction Cost Comparison</div>', unsafe_allow_html=True)

fig_cost = px.bar(
    cities_df,
    x="City",
    y="Base_Rate_INR",
    color="Base_Rate_INR",
    color_continuous_scale="Blues",
    title="Base Construction Rates by City (INR per m²)",
    labels={"Base_Rate_INR": "Rate (₹/m²)"}
)

fig_cost.update_layout(
    xaxis_tickangle=-45,
    height=400,
    showlegend=False
)

fig_cost.update_traces(
    texttemplate='₹%{y:,.0f}',
    textposition='outside'
)

st.plotly_chart(fig_cost, use_container_width=True)

st.markdown("---")

# How to Get Started
st.markdown('<div class="sub-header">🚀 Get Started</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **1️⃣ Cost Estimation**

    Start with our AI-powered cost estimation tool to get accurate project costs for any Indian city.
    """)

with col2:
    st.markdown("""
    **2️⃣ Analyze Risks**

    Assess potential risks including weather, seismic, and regulatory factors specific to your location.
    """)

with col3:
    st.markdown("""
    **3️⃣ Optimize Sustainability**

    Evaluate and improve your project's environmental impact and sustainability score.
    """)

# Navigation Guide
st.markdown("---")
st.markdown('<div class="sub-header">🧭 Navigation Guide</div>', unsafe_allow_html=True)

navigation_info = """
| 📄 **Page** | 🎯 **Purpose** | ⚡ **Key Features** |
|-------------|----------------|-------------------|
| 💰 **Cost Estimator** | Primary cost estimation interface | ML predictions, What-if scenarios, Indian cities |
| 📊 **Enhanced Analytics** | Advanced project analysis | Timeline estimation, Sustainability, Risk assessment |
| 🗺️ **Interactive Maps** | Geospatial analysis and mapping | City coordinates, Accessibility analysis |
| 🗺️ **Geospatial Analysis** | Network and spatial analysis | OSM data, H3 hexagons, Isochrones |
| 📊 **Data & Training** | ML model training interface | Feature engineering, Model training |
| 📡 **Realtime** | Live data integration | API connections, Real-time updates |
"""

st.markdown(navigation_info)

# Technical Specifications
st.markdown("---")
with st.expander("🔧 Technical Specifications"):
    st.markdown("""
    **AI/ML Models:**
    - Random Forest Regressor for cost prediction
    - Scikit-learn pipeline for data processing
    - Feature engineering with temporal components
    - Risk assessment algorithms

    **Supported Cities:**
    Mumbai, Delhi, Bangalore, Hyderabad, Chennai, Kolkata, Pune, Ahmedabad

    **Data Sources:**
    - Indian construction market data
    - Weather patterns and seasonal risks
    - Seismic zone classifications
    - Regional regulatory complexity

    **Technologies:**
    - Streamlit for web interface
    - Plotly for interactive visualizations
    - Pandas/NumPy for data processing
    - OpenAI integration (optional)
    """)

# Footer
st.markdown("""
<div class="footer">
    <h4>🏗️ Smart Construction Planner - India</h4>
    <p>Built with ❤️ for the Indian construction industry</p>
    <p>Powered by AI/ML • Localized for India • Open Source</p>
</div>
""", unsafe_allow_html=True)
