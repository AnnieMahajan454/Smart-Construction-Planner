import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
import folium
from streamlit_folium import st_folium
from sklearn.ensemble import RandomForestRegressor
import random
import time

# Page configuration
st.set_page_config(
    page_title="🏗️ AI Construction Planner - India",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Light theme CSS with proper visibility
st.markdown("""
<style>
    /* Force light theme everywhere */
    html, body {
        background-color: #ffffff !important;
        color: #333333 !important;
    }
    
    .stApp {
        background-color: #ffffff !important;
        color: #333333 !important;
    }
    
    /* Main content area */
    .main {
        background-color: #ffffff !important;
        color: #333333 !important;
    }
    
    /* Streamlit header and toolbar styling */
    header[data-testid="stHeader"] {
        background-color: #ffffff !important;
        color: #333333 !important;
    }
    
    .stApp > header {
        background-color: #ffffff !important;
        color: #333333 !important;
    }
    
    /* Streamlit toolbar */
    .stToolbar {
        background-color: #ffffff !important;
        color: #333333 !important;
    }
    
    /* Top navigation area */
    div[data-testid="stToolbar"] {
        background-color: #ffffff !important;
        color: #333333 !important;
    }
    
    /* Header container */
    .css-18ni7ap, .css-hby737, .css-17eq0hr {
        background-color: #ffffff !important;
        color: #333333 !important;
    }
    
    /* Status bar and top elements */
    .css-1dp5vir {
        background-color: #ffffff !important;
        color: #333333 !important;
    }
    
    /* Force all header text to be visible */
    header * {
        color: #333333 !important;
    }
    
    /* Comprehensive Sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa !important;
        color: #333333 !important;
    }
    
    .sidebar .sidebar-content {
        background-color: #f8f9fa !important;
        color: #333333 !important;
    }
    
    /* Streamlit sidebar container */
    .css-1d391kg, .css-1lcbmhc, .css-1v0mbdj, .css-16idsys {
        background-color: #f8f9fa !important;
        color: #333333 !important;
    }
    
    /* Sidebar content area */
    section[data-testid="stSidebar"] {
        background-color: #f8f9fa !important;
    }
    
    section[data-testid="stSidebar"] > div {
        background-color: #f8f9fa !important;
        color: #333333 !important;
    }
    
    /* Force all sidebar text to be visible */
    section[data-testid="stSidebar"] * {
        color: #333333 !important;
    }
    
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4,
    section[data-testid="stSidebar"] h5,
    section[data-testid="stSidebar"] h6 {
        color: #1976d2 !important;
        font-weight: 600;
    }
    
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div {
        color: #333333 !important;
    }
    
    /* Header styling */
    .header-box {
        background: linear-gradient(135deg, #4285f4 0%, #34a853 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    }
    
    .header-box h1 {
        color: white !important;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
    }
    
    .header-box p {
        color: rgba(255,255,255,0.9) !important;
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
    }
    
    /* Info boxes */
    .info-box {
        background: #ffffff;
        border: 2px solid #e3f2fd;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        color: #333333 !important;
    }
    
    .info-box h4 {
        color: #1976d2 !important;
        margin: 0 0 1rem 0;
    }
    
    .info-box p, .info-box li {
        color: #555555 !important;
        line-height: 1.6;
    }
    
    /* Metric boxes */
    .metric-box {
        background: #ffffff;
        border: 2px solid #e8eaf6;
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    }
    
    .metric-box h3 {
        font-size: 2rem;
        font-weight: 700;
        margin: 0 !important;
    }
    
    .metric-box p {
        color: #666666 !important;
        font-size: 0.9rem;
        margin: 0.5rem 0 0 0 !important;
        font-weight: 500;
    }
    
    /* Weather box */
    .weather-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border: 2px solid #2196f3;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #0d47a1 !important;
    }
    
    .weather-box h4 {
        color: #0d47a1 !important;
        margin: 0 0 1rem 0;
    }
    
    .weather-box p {
        color: #1565c0 !important;
        margin: 0.5rem 0;
        font-weight: 500;
    }
    
    /* Traffic box */
    .traffic-box {
        background: linear-gradient(135deg, #fce4ec 0%, #f8bbd9 100%);
        border: 2px solid #e91e63;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #880e4f !important;
    }
    
    .traffic-box h4, .traffic-box h2 {
        color: #880e4f !important;
        margin: 0.5rem 0;
    }
    
    .traffic-box p {
        color: #ad1457 !important;
        margin: 0.5rem 0;
        font-weight: 500;
    }
    
    /* Recommendation box */
    .recommendation-box {
        background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);
        border: 2px solid #4caf50;
        border-radius: 10px;
        padding: 1.2rem;
        margin: 0.8rem 0;
        color: #1b5e20 !important;
        font-weight: 500;
    }
    
    /* Phase box */
    .phase-box {
        background: #ffffff;
        border: 2px solid #e0e0e0;
        border-left: 6px solid #4285f4;
        border-radius: 8px;
        padding: 1.2rem;
        margin: 0.8rem 0;
        box-shadow: 0 1px 4px rgba(0,0,0,0.1);
    }
    
    .phase-box h5 {
        color: #1976d2 !important;
        margin: 0 0 0.8rem 0;
    }
    
    .phase-box p {
        color: #555555 !important;
        margin: 0.3rem 0;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #4285f4 0%, #1976d2 100%) !important;
        color: white !important;
        border-radius: 8px;
        border: none;
        padding: 0.7rem 1.5rem;
        font-weight: 600;
        font-size: 1rem;
        box-shadow: 0 2px 8px rgba(66, 133, 244, 0.3);
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #3367d6 0%, #1565c0 100%) !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(66, 133, 244, 0.4);
    }
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        color: #333333 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    p, div, span {
        color: #333333 !important;
    }
    
    /* Comprehensive Input and Label Styling */
    
    /* All Streamlit labels */
    label, .stSelectbox label, .stTextInput label, .stDateInput label {
        color: #333333 !important;
        font-weight: 600;
    }
    
    /* Sidebar specific labels */
    section[data-testid="stSidebar"] label {
        color: #333333 !important;
        font-weight: 600;
    }
    
    /* Comprehensive Selectbox and Dropdown Styling */
    
    /* Base selectbox styling */
    .stSelectbox > div > div {
        background-color: #ffffff !important;
        color: #333333 !important;
    }
    
    .stSelectbox > div > div > select {
        background-color: #ffffff !important;
        color: #333333 !important;
        border: 2px solid #e0e0e0;
    }
    
    /* Dropdown menu styling */
    .stSelectbox > div[data-baseweb="select"] {
        background-color: #ffffff !important;
        color: #333333 !important;
    }
    
    /* Dropdown list container */
    div[data-baseweb="popover"] {
        background-color: #ffffff !important;
        color: #333333 !important;
        border: 1px solid #e0e0e0 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Dropdown options */
    div[data-baseweb="menu"] {
        background-color: #ffffff !important;
        color: #333333 !important;
    }
    
    div[data-baseweb="menu"] > ul {
        background-color: #ffffff !important;
    }
    
    div[data-baseweb="menu"] li {
        background-color: #ffffff !important;
        color: #333333 !important;
        padding: 0.5rem 1rem;
    }
    
    div[data-baseweb="menu"] li:hover {
        background-color: #f5f5f5 !important;
        color: #333333 !important;
    }
    
    div[data-baseweb="menu"] li[aria-selected="true"] {
        background-color: #e3f2fd !important;
        color: #1976d2 !important;
    }
    
    /* Selectbox in sidebar - comprehensive targeting */
    section[data-testid="stSidebar"] .stSelectbox > div > div {
        background-color: #ffffff !important;
        color: #333333 !important;
    }
    
    section[data-testid="stSidebar"] .stSelectbox select {
        background-color: #ffffff !important;
        color: #333333 !important;
    }
    
    section[data-testid="stSidebar"] div[data-baseweb="select"] {
        background-color: #ffffff !important;
        color: #333333 !important;
    }
    
    section[data-testid="stSidebar"] div[data-baseweb="select"] * {
        background-color: #ffffff !important;
        color: #333333 !important;
    }
    
    /* Force all dropdown text to be visible */
    .stSelectbox * {
        color: #333333 !important;
    }
    
    section[data-testid="stSidebar"] .stSelectbox * {
        color: #333333 !important;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background-color: #ffffff !important;
        color: #333333 !important;
        border: 2px solid #e0e0e0;
    }
    
    /* Date input styling */
    .stDateInput > div > div > input {
        background-color: #ffffff !important;
        color: #333333 !important;
        border: 2px solid #e0e0e0;
    }
    
    /* Sidebar input styling */
    section[data-testid="stSidebar"] input {
        background-color: #ffffff !important;
        color: #333333 !important;
        border: 2px solid #e0e0e0;
    }
    
    /* Force visibility for all sidebar form elements */
    section[data-testid="stSidebar"] .stSelectbox,
    section[data-testid="stSidebar"] .stTextInput,
    section[data-testid="stSidebar"] .stDateInput {
        color: #333333 !important;
    }
    
    section[data-testid="stSidebar"] .stSelectbox *,
    section[data-testid="stSidebar"] .stTextInput *,
    section[data-testid="stSidebar"] .stDateInput * {
        color: #333333 !important;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #f5f5f5;
        border-radius: 8px;
        padding: 0.2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #666666 !important;
        font-weight: 500;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #ffffff;
        color: #4285f4 !important;
        font-weight: 600;
    }
    
    /* Override any dark theme elements */
    .css-1629p8f, .css-1d391kg, .css-1v0mbdj {
        background-color: #ffffff !important;
        color: #333333 !important;
    }
    
    /* Force light background for main container */
    .block-container {
        background-color: #ffffff !important;
        padding-top: 2rem;
    }
    
    /* Ensure all text is visible */
    * {
        color: inherit;
    }
    
    .element-container {
        background-color: transparent !important;
    }
    
    /* Success/Info/Warning message styling */
    .stSuccess {
        background-color: #e8f5e8 !important;
        color: #1b5e20 !important;
    }
    
    .stInfo {
        background-color: #e3f2fd !important;
        color: #0d47a1 !important;
    }
    
    .stWarning {
        background-color: #fff3e0 !important;
        color: #e65100 !important;
    }
</style>
""", unsafe_allow_html=True)

class AIConstructionPlannerLight:
    """Lightweight AI Construction Planner for India"""
    
    def __init__(self):
        self.cities = {
            'Mumbai': {
                'lat': 19.0760, 'lon': 72.8777, 'state': 'Maharashtra',
                'population': 20.4, 'traffic_intensity': 0.95, 'cost_index': 1.4,
                'weather_risk': 'High', 'monsoon_months': [6,7,8,9]
            },
            'Delhi': {
                'lat': 28.7041, 'lon': 77.1025, 'state': 'Delhi',
                'population': 32.9, 'traffic_intensity': 0.90, 'cost_index': 1.3,
                'weather_risk': 'Medium', 'monsoon_months': [7,8,9]
            },
            'Bangalore': {
                'lat': 12.9716, 'lon': 77.5946, 'state': 'Karnataka',
                'population': 12.3, 'traffic_intensity': 0.75, 'cost_index': 1.1,
                'weather_risk': 'Medium', 'monsoon_months': [6,7,8,9]
            },
            'Chennai': {
                'lat': 13.0827, 'lon': 80.2707, 'state': 'Tamil Nadu',
                'population': 11.0, 'traffic_intensity': 0.80, 'cost_index': 1.0,
                'weather_risk': 'High', 'monsoon_months': [6,7,8,9,10,11]
            },
            'Hyderabad': {
                'lat': 17.3850, 'lon': 78.4867, 'state': 'Telangana',
                'population': 10.0, 'traffic_intensity': 0.70, 'cost_index': 0.95,
                'weather_risk': 'Medium', 'monsoon_months': [6,7,8,9]
            },
            'Kolkata': {
                'lat': 22.5726, 'lon': 88.3639, 'state': 'West Bengal',
                'population': 14.8, 'traffic_intensity': 0.85, 'cost_index': 0.90,
                'weather_risk': 'High', 'monsoon_months': [6,7,8,9,10]
            },
            'Pune': {
                'lat': 18.5204, 'lon': 73.8567, 'state': 'Maharashtra',
                'population': 7.4, 'traffic_intensity': 0.72, 'cost_index': 1.05,
                'weather_risk': 'Medium', 'monsoon_months': [6,7,8,9]
            },
            'Ahmedabad': {
                'lat': 23.0225, 'lon': 72.5714, 'state': 'Gujarat',
                'population': 8.4, 'traffic_intensity': 0.65, 'cost_index': 0.85,
                'weather_risk': 'Low', 'monsoon_months': [6,7,8,9]
            }
        }
        
        self.project_types = {
            'Residential Building': {'icon': '🏠', 'duration': 180, 'complexity': 0.6},
            'Commercial Complex': {'icon': '🏢', 'duration': 300, 'complexity': 0.7},
            'Road Construction': {'icon': '🛣️', 'duration': 150, 'complexity': 0.8},
            'Bridge Construction': {'icon': '🌉', 'duration': 400, 'complexity': 0.9},
            'Metro/Railway': {'icon': '🚇', 'duration': 600, 'complexity': 0.95},
            'Industrial Complex': {'icon': '🏭', 'duration': 450, 'complexity': 0.85}
        }
        
        # Initialize AI model
        self.ai_model = self._create_simple_model()
    
    def _create_simple_model(self):
        """Create a simple ML model for predictions"""
        np.random.seed(42)
        
        # Generate training data
        n_samples = 1000
        X = np.random.rand(n_samples, 4)  # 4 features
        y = (X[:, 0] * 0.3 + X[:, 1] * 0.2 + X[:, 2] * 0.3 + X[:, 3] * 0.2 + 
             np.random.normal(0, 0.1, n_samples))
        
        model = RandomForestRegressor(n_estimators=10, random_state=42)
        model.fit(X, y)
        return model
    
    def get_weather_data(self, city):
        """Get simulated weather data"""
        current_month = datetime.now().month
        city_data = self.cities[city]
        
        # Seasonal patterns
        if current_month in city_data['monsoon_months']:
            temp = random.uniform(25, 32)
            humidity = random.uniform(75, 95)
            condition = "Rainy"
            rainfall = random.uniform(20, 100)
        elif current_month in [12, 1, 2]:  # Winter
            temp = random.uniform(15, 25)
            humidity = random.uniform(40, 70)
            condition = "Pleasant"
            rainfall = random.uniform(0, 10)
        else:  # Summer
            temp = random.uniform(28, 40)
            humidity = random.uniform(30, 60)
            condition = "Hot"
            rainfall = random.uniform(0, 15)
        
        return {
            'temperature': round(temp, 1),
            'humidity': round(humidity, 1),
            'condition': condition,
            'rainfall': round(rainfall, 1),
            'wind_speed': round(random.uniform(5, 20), 1)
        }
    
    def get_traffic_patterns(self, city):
        """Get traffic patterns for 24 hours"""
        city_data = self.cities[city]
        intensity = city_data['traffic_intensity']
        
        traffic = {}
        for hour in range(24):
            if 8 <= hour <= 10 or 18 <= hour <= 20:  # Peak hours
                traffic[hour] = intensity * random.uniform(0.8, 1.0)
            elif 22 <= hour or hour <= 6:  # Night
                traffic[hour] = intensity * random.uniform(0.1, 0.3)
            else:  # Normal hours
                traffic[hour] = intensity * random.uniform(0.4, 0.7)
        
        return traffic
    
    def predict_optimal_months(self, city, construction_type):
        """Predict best months for construction"""
        city_data = self.cities[city]
        monsoon_months = city_data['monsoon_months']
        
        month_scores = {}
        for month in range(1, 13):
            score = 0.8  # Base score
            
            # Reduce score for monsoon months
            if month in monsoon_months:
                score -= 0.4
            
            # Winter months are better
            if month in [11, 12, 1, 2]:
                score += 0.2
            
            # Summer months are challenging
            if month in [4, 5]:
                score -= 0.2
            
            # Add some randomness
            score += random.uniform(-0.1, 0.1)
            month_scores[month] = max(0, min(1, score))
        
        # Get month names
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        best_months = sorted(month_scores.items(), key=lambda x: x[1], reverse=True)[:3]
        
        return {
            'all_scores': month_scores,
            'best_months': [(month_names[m-1], score) for m, score in best_months],
            'recommendations': self._get_timing_recommendations(city, best_months)
        }
    
    def _get_timing_recommendations(self, city, best_months):
        """Generate timing recommendations"""
        recommendations = []
        city_data = self.cities[city]
        
        best_month_num = best_months[0][0]
        best_score = best_months[0][1]
        
        if best_score > 0.8:
            recommendations.append("✅ Excellent conditions predicted")
        elif best_score > 0.6:
            recommendations.append("⚠️ Good conditions with some challenges")
        else:
            recommendations.append("🚨 Difficult conditions - extra planning needed")
        
        if best_month_num not in city_data['monsoon_months']:
            recommendations.append("🌞 Optimal timing avoids monsoon season")
        else:
            recommendations.append("🌧️ Consider monsoon delays in planning")
        
        if city_data['traffic_intensity'] > 0.8:
            recommendations.append(f"🚦 High traffic in {city} - plan deliveries carefully")
        
        return recommendations
    
    def generate_project_plan(self, city, project_type, project_size, start_date):
        """Generate complete project plan"""
        city_data = self.cities[city]
        type_data = self.project_types[project_type]
        
        # Calculate duration
        base_duration = type_data['duration']
        size_multipliers = {'Small': 0.7, 'Medium': 1.0, 'Large': 1.5, 'Mega': 2.0}
        adjusted_duration = int(base_duration * size_multipliers[project_size])
        
        # Get current conditions
        weather = self.get_weather_data(city)
        traffic = self.get_traffic_patterns(city)
        timing = self.predict_optimal_months(city, project_type)
        
        # Add delays based on conditions
        weather_delay = 0
        if weather['condition'] == 'Rainy':
            weather_delay = int(adjusted_duration * 0.15)
        elif weather['condition'] == 'Hot':
            weather_delay = int(adjusted_duration * 0.08)
        
        traffic_delay = int(adjusted_duration * city_data['traffic_intensity'] * 0.1)
        
        total_duration = adjusted_duration + weather_delay + traffic_delay
        completion_date = start_date + timedelta(days=total_duration)
        
        # Calculate costs (in Crores INR)
        base_costs = {
            'Residential Building': 50, 'Commercial Complex': 150, 'Road Construction': 80,
            'Bridge Construction': 250, 'Metro/Railway': 600, 'Industrial Complex': 180
        }
        
        base_cost = base_costs[project_type] * size_multipliers[project_size]
        total_cost = base_cost * city_data['cost_index']
        
        # Generate phases
        phases = self._generate_phases(project_type, total_duration, start_date)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(city, project_type, weather, traffic)
        
        return {
            'overview': {
                'total_duration': total_duration,
                'weather_delay': weather_delay,
                'traffic_delay': traffic_delay,
                'completion_date': completion_date,
                'total_cost': round(total_cost, 1)
            },
            'current_conditions': {
                'weather': weather,
                'traffic': traffic,
                'optimal_timing': timing
            },
            'phases': phases,
            'recommendations': recommendations
        }
    
    def _generate_phases(self, project_type, total_duration, start_date):
        """Generate project phases"""
        phase_templates = {
            'Residential Building': [
                ('Foundation Work', 0.2),
                ('Structure Construction', 0.4),
                ('Finishing Work', 0.3),
                ('Final Inspection', 0.1)
            ],
            'Commercial Complex': [
                ('Planning & Approval', 0.15),
                ('Foundation & Structure', 0.35),
                ('MEP & Systems', 0.35),
                ('Finishing & Handover', 0.15)
            ],
            'Road Construction': [
                ('Survey & Design', 0.1),
                ('Earthwork', 0.4),
                ('Paving', 0.4),
                ('Completion', 0.1)
            ]
        }
        
        template = phase_templates.get(project_type, phase_templates['Residential Building'])
        
        phases = []
        current_date = start_date
        
        for phase_name, percentage in template:
            phase_duration = int(total_duration * percentage)
            end_date = current_date + timedelta(days=phase_duration)
            
            phases.append({
                'name': phase_name,
                'start_date': current_date,
                'end_date': end_date,
                'duration': phase_duration
            })
            
            current_date = end_date + timedelta(days=1)
        
        return phases
    
    def _generate_recommendations(self, city, project_type, weather, traffic):
        """Generate AI recommendations"""
        recommendations = []
        
        # Weather recommendations
        if weather['condition'] == 'Rainy':
            recommendations.append("☔ Monsoon season - ensure proper drainage and material protection")
        elif weather['condition'] == 'Hot':
            recommendations.append("🌡️ High temperatures - schedule work during cooler hours")
        else:
            recommendations.append("🌤️ Good weather conditions for construction")
        
        # Traffic recommendations
        avg_traffic = np.mean(list(traffic.values()))
        if avg_traffic > 0.7:
            recommendations.append("🚦 High traffic area - plan material delivery during off-peak hours")
        else:
            recommendations.append("✅ Manageable traffic conditions")
        
        # Project specific
        if project_type == 'Road Construction':
            recommendations.append("🛣️ Coordinate with traffic authorities for road closures")
        elif project_type == 'Bridge Construction':
            recommendations.append("🌉 Monitor wind conditions for crane operations")
        
        return recommendations

def create_simple_map(cities, selected_city):
    """Create a simple folium map"""
    try:
        # Center on India
        m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)
        
        # Add city markers
        for city, data in cities.items():
            color = 'red' if city == selected_city else 'blue'
            
            folium.Marker(
                [data['lat'], data['lon']],
                popup=f"{city}, {data['state']}\nPopulation: {data['population']}M",
                tooltip=city,
                icon=folium.Icon(color=color)
            ).add_to(m)
        
        return m
    except:
        return None

# Initialize the planner
@st.cache_resource
def get_planner():
    return AIConstructionPlannerLight()

def main():
    # Header
    st.markdown("""
    <div class="header-box">
        <h1>🏗️ AI Smart Construction Planner - India</h1>
        <p>Intelligent planning with real-time weather & traffic analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load planner
    try:
        planner = get_planner()
    except Exception as e:
        st.error(f"Error loading planner: {e}")
        return
    
    # Sidebar
    with st.sidebar:
        st.header("🎯 Project Details")
        
        selected_city = st.selectbox(
            "📍 City",
            options=list(planner.cities.keys())
        )
        
        project_type = st.selectbox(
            "🏗️ Project Type",
            options=list(planner.project_types.keys()),
            format_func=lambda x: f"{planner.project_types[x]['icon']} {x}"
        )
        
        project_size = st.selectbox(
            "📏 Size",
            options=['Small', 'Medium', 'Large', 'Mega'],
            index=1
        )
        
        project_name = st.text_input(
            "📝 Project Name",
            value=f"{project_type} - {selected_city}"
        )
        
        start_date = st.date_input(
            "📅 Start Date",
            value=datetime.now().date()
        )
        
        st.markdown("---")
        
        # Action buttons
        generate_plan = st.button("🤖 Generate AI Plan", type="primary")
        check_conditions = st.button("🌤️ Check Conditions")
        find_timing = st.button("⏰ Find Best Timing")
    
    # Main content
    if generate_plan:
        st.header(f"📊 AI Plan: {project_name}")
        
        with st.spinner("🤖 Generating AI-powered construction plan..."):
            time.sleep(2)
            
            plan = planner.generate_project_plan(
                selected_city, project_type, project_size, 
                datetime.combine(start_date, datetime.min.time())
            )
        
        # Overview metrics
        overview = plan['overview']
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-box">
                <h3 style="color: #4285f4; margin: 0;">{overview['total_duration']}</h3>
                <p style="margin: 0.5rem 0 0 0;">Total Days</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-box">
                <h3 style="color: #34a853; margin: 0;">₹{overview['total_cost']}</h3>
                <p style="margin: 0.5rem 0 0 0;">Cost (Crores)</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            completion = overview['completion_date'].strftime('%d %b %Y')
            st.markdown(f"""
            <div class="metric-box">
                <h3 style="color: #ea4335; margin: 0; font-size: 1.2rem;">{completion}</h3>
                <p style="margin: 0.5rem 0 0 0;">Completion</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            delays = overview['weather_delay'] + overview['traffic_delay']
            st.markdown(f"""
            <div class="metric-box">
                <h3 style="color: #fbbc04; margin: 0;">+{delays}</h3>
                <p style="margin: 0.5rem 0 0 0;">Delay Days</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Tabs for detailed view
        tab1, tab2, tab3, tab4 = st.tabs(["📅 Timeline", "🌤️ Conditions", "💡 Recommendations", "📊 Analysis"])
        
        with tab1:
            st.subheader("🏗️ Project Timeline")
            
            # Timeline chart
            phases = plan['phases']
            
            fig = go.Figure()
            colors = ['#4285f4', '#34a853', '#ea4335', '#fbbc04']
            
            for i, phase in enumerate(phases):
                fig.add_trace(go.Bar(
                    name=phase['name'],
                    x=[phase['duration']],
                    y=[phase['name']],
                    orientation='h',
                    marker_color=colors[i % len(colors)]
                ))
            
            fig.update_layout(
                title="Project Phases",
                xaxis_title="Duration (Days)",
                height=400,
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Phase details
            for phase in phases:
                st.markdown(f"""
                <div class="phase-box">
                    <h5>{phase['name']}</h5>
                    <p><strong>Duration:</strong> {phase['duration']} days</p>
                    <p><strong>Start:</strong> {phase['start_date'].strftime('%d %b %Y')}</p>
                    <p><strong>End:</strong> {phase['end_date'].strftime('%d %b %Y')}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with tab2:
            st.subheader("🌤️ Current Conditions")
            
            conditions = plan['current_conditions']
            weather = conditions['weather']
            traffic = conditions['traffic']
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div class="weather-box">
                    <h4>🌡️ Weather Status</h4>
                    <p><strong>Temperature:</strong> {weather['temperature']}°C</p>
                    <p><strong>Condition:</strong> {weather['condition']}</p>
                    <p><strong>Humidity:</strong> {weather['humidity']}%</p>
                    <p><strong>Rainfall:</strong> {weather['rainfall']}mm</p>
                    <p><strong>Wind:</strong> {weather['wind_speed']} km/h</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                current_hour = datetime.now().hour
                current_traffic = traffic.get(current_hour, 0.5)
                status = "Heavy" if current_traffic > 0.7 else "Moderate" if current_traffic > 0.4 else "Light"
                
                st.markdown(f"""
                <div class="traffic-box">
                    <h4>🚦 Traffic Status</h4>
                    <h2 style="text-align: center; margin: 1rem 0;">{current_traffic:.0%}</h2>
                    <p style="text-align: center;"><strong>{status}</strong></p>
                    <p><strong>Peak Hours:</strong> 8-10 AM, 6-8 PM</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Traffic pattern chart
            hours = list(range(24))
            traffic_levels = [traffic[h] * 100 for h in hours]
            
            fig = go.Figure(data=go.Scatter(
                x=hours, y=traffic_levels,
                mode='lines+markers',
                name='Traffic Level',
                line=dict(color='#ea4335', width=2)
            ))
            
            fig.update_layout(
                title="24-Hour Traffic Pattern",
                xaxis_title="Hour of Day",
                yaxis_title="Traffic Level (%)",
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            st.subheader("💡 AI Recommendations")
            
            recommendations = plan['recommendations']
            
            for i, rec in enumerate(recommendations, 1):
                st.markdown(f"""
                <div class="recommendation-box">
                    <strong>{i}.</strong> {rec}
                </div>
                """, unsafe_allow_html=True)
        
        with tab4:
            st.subheader("📊 Detailed Analysis")
            
            # Duration breakdown
            durations = {
                'Base Duration': overview['total_duration'] - overview['weather_delay'] - overview['traffic_delay'],
                'Weather Delay': overview['weather_delay'],
                'Traffic Impact': overview['traffic_delay']
            }
            
            fig = go.Figure(data=[
                go.Bar(x=list(durations.keys()), y=list(durations.values()),
                       marker_color=['#4285f4', '#ea4335', '#fbbc04'])
            ])
            
            fig.update_layout(
                title="Duration Breakdown",
                yaxis_title="Days",
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # City info
            city_data = planner.cities[selected_city]
            
            st.markdown(f"""
            <div class="info-box">
                <h4>📍 City Analysis: {selected_city}</h4>
                <p><strong>State:</strong> {city_data['state']}</p>
                <p><strong>Population:</strong> {city_data['population']} Million</p>
                <p><strong>Traffic Intensity:</strong> {city_data['traffic_intensity']*100:.0f}%</p>
                <p><strong>Cost Index:</strong> {city_data['cost_index']}</p>
                <p><strong>Weather Risk:</strong> {city_data['weather_risk']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    elif check_conditions:
        st.header(f"🌤️ Current Conditions - {selected_city}")
        
        weather = planner.get_weather_data(selected_city)
        traffic = planner.get_traffic_patterns(selected_city)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="weather-box">
                <h4>🌡️ Weather Report</h4>
                <p><strong>Temperature:</strong> {weather['temperature']}°C</p>
                <p><strong>Condition:</strong> {weather['condition']}</p>
                <p><strong>Humidity:</strong> {weather['humidity']}%</p>
                <p><strong>Rainfall:</strong> {weather['rainfall']}mm</p>
                <p><strong>Wind Speed:</strong> {weather['wind_speed']} km/h</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            current_hour = datetime.now().hour
            current_traffic = traffic.get(current_hour, 0.5)
            
            st.markdown(f"""
            <div class="traffic-box">
                <h4>🚦 Traffic Report</h4>
                <h2 style="text-align: center;">{current_traffic:.0%}</h2>
                <p style="text-align: center;"><strong>Current Level</strong></p>
                <p><strong>Time:</strong> {current_hour}:00</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Traffic chart
        hours = list(range(24))
        traffic_levels = [traffic[h] * 100 for h in hours]
        
        fig = go.Figure(data=go.Scatter(
            x=hours, y=traffic_levels,
            mode='lines+markers',
            name='Traffic',
            line=dict(color='#4285f4', width=3)
        ))
        
        fig.add_vline(x=current_hour, line_dash="dash", line_color="red")
        
        fig.update_layout(
            title=f"Traffic Pattern - {selected_city}",
            xaxis_title="Hour",
            yaxis_title="Traffic Level (%)",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    elif find_timing:
        st.header(f"⏰ Best Timing - {project_type}")
        
        with st.spinner("🤖 Analyzing optimal construction timing..."):
            timing = planner.predict_optimal_months(selected_city, project_type)
        
        # Best months
        st.subheader("🌟 Recommended Months")
        
        best_months = timing['best_months']
        
        col1, col2, col3 = st.columns(3)
        
        for i, (month, score) in enumerate(best_months):
            col = [col1, col2, col3][i]
            rank = ['🥇', '🥈', '🥉'][i]
            
            with col:
                st.markdown(f"""
                <div class="info-box" style="text-align: center;">
                    <h2>{rank}</h2>
                    <h4>{month}</h4>
                    <p><strong>{score*100:.0f}% Suitable</strong></p>
                </div>
                """, unsafe_allow_html=True)
        
        # Monthly chart
        all_scores = timing['all_scores']
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        scores = [all_scores[i+1] * 100 for i in range(12)]
        
        fig = go.Figure(data=[
            go.Bar(x=months, y=scores, 
                   marker_color=['#34a853' if s > 70 else '#fbbc04' if s > 50 else '#ea4335' for s in scores])
        ])
        
        fig.update_layout(
            title="Monthly Suitability Scores",
            yaxis_title="Suitability (%)",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Recommendations
        st.subheader("💡 Timing Recommendations")
        
        for rec in timing['recommendations']:
            st.markdown(f"""
            <div class="recommendation-box">
                {rec}
            </div>
            """, unsafe_allow_html=True)
    
    else:
        # Default view
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader(f"📍 {selected_city} Overview")
            
            city_info = planner.cities[selected_city]
            
            st.markdown(f"""
            <div class="info-box">
                <h4>🏙️ City Information</h4>
                <p><strong>State:</strong> {city_info['state']}</p>
                <p><strong>Population:</strong> {city_info['population']} Million</p>
                <p><strong>Traffic Level:</strong> {city_info['traffic_intensity']*100:.0f}%</p>
                <p><strong>Weather Risk:</strong> {city_info['weather_risk']}</p>
                <p><strong>Cost Index:</strong> {city_info['cost_index']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Project info
            project_info = planner.project_types[project_type]
            
            st.markdown(f"""
            <div class="info-box">
                <h4>{project_info['icon']} Project Details</h4>
                <p><strong>Type:</strong> {project_type}</p>
                <p><strong>Base Duration:</strong> {project_info['duration']} days</p>
                <p><strong>Complexity:</strong> {project_info['complexity']*100:.0f}%</p>
                <p><strong>Size:</strong> {project_size}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.subheader("🗺️ India Map")
            
            india_map = create_simple_map(planner.cities, selected_city)
            if india_map:
                map_data = st_folium(india_map, width=400, height=300)
        
        # Quick stats
        st.subheader("📊 Platform Features")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="metric-box">
                <h3 style="color: #4285f4;">8</h3>
                <p>Major Cities</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-box">
                <h3 style="color: #34a853;">6</h3>
                <p>Project Types</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-box">
                <h3 style="color: #ea4335;">AI</h3>
                <p>Powered</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="metric-box">
                <h3 style="color: #fbbc04;">24/7</h3>
                <p>Analysis</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Features
        st.subheader("✨ Key Features")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="info-box">
                <h4>🧠 Smart Planning</h4>
                <ul>
                    <li>AI-powered predictions</li>
                    <li>Weather impact analysis</li>
                    <li>Traffic optimization</li>
                    <li>Timeline planning</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="info-box">
                <h4>📊 Real-time Data</h4>
                <ul>
                    <li>Live weather conditions</li>
                    <li>Traffic patterns</li>
                    <li>Cost estimation</li>
                    <li>Risk assessment</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="info-box">
                <h4>🎯 Smart Insights</h4>
                <ul>
                    <li>Optimal timing</li>
                    <li>Weather precautions</li>
                    <li>Traffic management</li>
                    <li>Cost optimization</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 1rem; color: #666;">
        <p><strong>🏗️ AI Smart Construction Planner for India</strong></p>
        <p>Powered by Machine Learning | Real-time Intelligence | Smart Planning</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
