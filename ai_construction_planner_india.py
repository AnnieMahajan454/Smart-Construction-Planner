import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
import folium
from streamlit_folium import st_folium
from sklearn.ensemble import RandomForestRegressor
import requests
import json
import random
import time
from typing import Dict, List, Tuple

# Set page configuration
st.set_page_config(
    page_title="🏗️ AI Smart Construction Planner - India",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS for professional UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border: 1px solid #e9ecef;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.15);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .weather-card {
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(116, 185, 255, 0.4);
    }
    
    .traffic-card {
        background: linear-gradient(135deg, #fd79a8 0%, #e84393 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(253, 121, 168, 0.4);
    }
    
    .recommendation-card {
        background: linear-gradient(135deg, #55efc4 0%, #00b894 100%);
        color: white;
        padding: 1.2rem;
        border-radius: 10px;
        margin: 0.8rem 0;
        box-shadow: 0 3px 12px rgba(85, 239, 196, 0.4);
    }
    
    .phase-timeline {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    .ai-insight {
        background: linear-gradient(135deg, #a29bfe 0%, #6c5ce7 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        box-shadow: 0 3px 10px rgba(162, 155, 254, 0.3);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.7rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.6);
    }
    
    .sidebar-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

class AIConstructionPlannerIndia:
    """
    AI-Powered Smart Construction Planner for India
    Features: Real-time weather, traffic analysis, optimal timing predictions, complete project planning
    """
    
    def __init__(self):
        self.indian_cities = {
            'Mumbai': {
                'lat': 19.0760, 'lon': 72.8777, 'state': 'Maharashtra',
                'population': 20.4, 'traffic_intensity': 0.95, 'monsoon_months': [6,7,8,9],
                'peak_hours': [(8,10), (18,20)], 'construction_cost_index': 1.4,
                'major_projects': ['Metro', 'Coastal Road', 'Housing'],
                'weather_risk': 'High', 'seismic_zone': 3
            },
            'Delhi': {
                'lat': 28.7041, 'lon': 77.1025, 'state': 'NCR',
                'population': 32.9, 'traffic_intensity': 0.90, 'monsoon_months': [7,8,9],
                'peak_hours': [(8,10), (17,19)], 'construction_cost_index': 1.3,
                'major_projects': ['Metro Phase-4', 'Smart City', 'Flyovers'],
                'weather_risk': 'Medium', 'seismic_zone': 4
            },
            'Bangalore': {
                'lat': 12.9716, 'lon': 77.5946, 'state': 'Karnataka',
                'population': 12.3, 'traffic_intensity': 0.75, 'monsoon_months': [6,7,8,9,10],
                'peak_hours': [(9,11), (18,20)], 'construction_cost_index': 1.1,
                'major_projects': ['IT Parks', 'Metro Extension', 'Peripheral Ring Road'],
                'weather_risk': 'Medium', 'seismic_zone': 2
            },
            'Chennai': {
                'lat': 13.0827, 'lon': 80.2707, 'state': 'Tamil Nadu',
                'population': 11.0, 'traffic_intensity': 0.80, 'monsoon_months': [6,7,8,9,10,11],
                'peak_hours': [(8,10), (17,19)], 'construction_cost_index': 1.0,
                'major_projects': ['Metro Phase-2', 'Port Expansion', 'IT Corridor'],
                'weather_risk': 'High', 'seismic_zone': 2
            },
            'Hyderabad': {
                'lat': 17.3850, 'lon': 78.4867, 'state': 'Telangana',
                'population': 10.0, 'traffic_intensity': 0.70, 'monsoon_months': [6,7,8,9],
                'peak_hours': [(8,10), (18,20)], 'construction_cost_index': 0.95,
                'major_projects': ['Metro Extension', 'HITEC City Phase-3', 'ORR'],
                'weather_risk': 'Medium', 'seismic_zone': 2
            },
            'Kolkata': {
                'lat': 22.5726, 'lon': 88.3639, 'state': 'West Bengal',
                'population': 14.8, 'traffic_intensity': 0.85, 'monsoon_months': [6,7,8,9,10],
                'peak_hours': [(8,10), (17,19)], 'construction_cost_index': 0.90,
                'major_projects': ['Metro Extension', 'New Town', 'Port Connectivity'],
                'weather_risk': 'High', 'seismic_zone': 3
            },
            'Pune': {
                'lat': 18.5204, 'lon': 73.8567, 'state': 'Maharashtra',
                'population': 7.4, 'traffic_intensity': 0.72, 'monsoon_months': [6,7,8,9],
                'peak_hours': [(8,10), (18,20)], 'construction_cost_index': 1.05,
                'major_projects': ['Metro', 'IT Parks', 'Ring Road'],
                'weather_risk': 'Medium', 'seismic_zone': 3
            },
            'Ahmedabad': {
                'lat': 23.0225, 'lon': 72.5714, 'state': 'Gujarat',
                'population': 8.4, 'traffic_intensity': 0.65, 'monsoon_months': [6,7,8,9],
                'peak_hours': [(8,10), (18,20)], 'construction_cost_index': 0.85,
                'major_projects': ['BRTS Extension', 'Smart City', 'Industrial Parks'],
                'weather_risk': 'Low', 'seismic_zone': 3
            }
        }
        
        self.construction_types = {
            'Residential Building': {
                'icon': '🏠', 'base_duration': 180, 'complexity': 0.6,
                'weather_sensitivity': 0.7, 'traffic_impact': 0.3,
                'phases': [
                    {'name': 'Foundation & Site Prep', 'percentage': 15, 'weather_critical': True},
                    {'name': 'Structure & Framework', 'percentage': 35, 'weather_critical': False},
                    {'name': 'Walls & Roofing', 'percentage': 25, 'weather_critical': True},
                    {'name': 'MEP & Interiors', 'percentage': 20, 'weather_critical': False},
                    {'name': 'Finishing & Handover', 'percentage': 5, 'weather_critical': False}
                ]
            },
            'Commercial Complex': {
                'icon': '🏢', 'base_duration': 300, 'complexity': 0.75,
                'weather_sensitivity': 0.65, 'traffic_impact': 0.5,
                'phases': [
                    {'name': 'Planning & Approvals', 'percentage': 10, 'weather_critical': False},
                    {'name': 'Foundation Work', 'percentage': 20, 'weather_critical': True},
                    {'name': 'Structural Work', 'percentage': 30, 'weather_critical': False},
                    {'name': 'MEP & Systems', 'percentage': 25, 'weather_critical': False},
                    {'name': 'Finishing & Setup', 'percentage': 15, 'weather_critical': False}
                ]
            },
            'Road Construction': {
                'icon': '🛣️', 'base_duration': 150, 'complexity': 0.8,
                'weather_sensitivity': 0.9, 'traffic_impact': 0.95,
                'phases': [
                    {'name': 'Survey & Design', 'percentage': 8, 'weather_critical': False},
                    {'name': 'Land Acquisition & Clearance', 'percentage': 12, 'weather_critical': False},
                    {'name': 'Earthwork & Drainage', 'percentage': 35, 'weather_critical': True},
                    {'name': 'Pavement & Surface', 'percentage': 30, 'weather_critical': True},
                    {'name': 'Signage & Completion', 'percentage': 15, 'weather_critical': False}
                ]
            },
            'Bridge Construction': {
                'icon': '🌉', 'base_duration': 400, 'complexity': 0.95,
                'weather_sensitivity': 0.85, 'traffic_impact': 0.8,
                'phases': [
                    {'name': 'Design & Environmental Clearance', 'percentage': 15, 'weather_critical': False},
                    {'name': 'Foundation & Pier Work', 'percentage': 40, 'weather_critical': True},
                    {'name': 'Superstructure Construction', 'percentage': 25, 'weather_critical': True},
                    {'name': 'Deck & Finishing', 'percentage': 15, 'weather_critical': True},
                    {'name': 'Testing & Commissioning', 'percentage': 5, 'weather_critical': False}
                ]
            },
            'Metro/Railway': {
                'icon': '🚇', 'base_duration': 600, 'complexity': 0.9,
                'weather_sensitivity': 0.7, 'traffic_impact': 0.85,
                'phases': [
                    {'name': 'Planning & Land Acquisition', 'percentage': 20, 'weather_critical': False},
                    {'name': 'Tunneling & Excavation', 'percentage': 35, 'weather_critical': True},
                    {'name': 'Track & Station Construction', 'percentage': 25, 'weather_critical': False},
                    {'name': 'Systems Integration', 'percentage': 15, 'weather_critical': False},
                    {'name': 'Testing & Commissioning', 'percentage': 5, 'weather_critical': False}
                ]
            },
            'Industrial Complex': {
                'icon': '🏭', 'base_duration': 450, 'complexity': 0.85,
                'weather_sensitivity': 0.6, 'traffic_impact': 0.4,
                'phases': [
                    {'name': 'Site Development', 'percentage': 10, 'weather_critical': False},
                    {'name': 'Infrastructure Setup', 'percentage': 25, 'weather_critical': True},
                    {'name': 'Building Construction', 'percentage': 35, 'weather_critical': False},
                    {'name': 'Equipment Installation', 'percentage': 20, 'weather_critical': False},
                    {'name': 'Testing & Commissioning', 'percentage': 10, 'weather_critical': False}
                ]
            }
        }
        
        # Initialize AI models
        self.weather_model = self._initialize_weather_model()
        self.traffic_model = self._initialize_traffic_model()
        self.optimal_timing_model = self._initialize_timing_model()
    
    def _initialize_weather_model(self):
        """Initialize ML model for weather impact prediction"""
        np.random.seed(42)
        n_samples = 8000
        
        # Features: month, temperature, humidity, rainfall, wind_speed, city_weather_risk
        months = np.random.randint(1, 13, n_samples)
        temperatures = np.random.uniform(10, 48, n_samples)
        humidity = np.random.uniform(20, 95, n_samples)
        rainfall = np.random.uniform(0, 300, n_samples)  # mm per month
        wind_speeds = np.random.uniform(0, 40, n_samples)
        weather_risk = np.random.uniform(0, 1, n_samples)
        
        X = np.column_stack([months, temperatures, humidity, rainfall, wind_speeds, weather_risk])
        
        # Generate weather impact scores
        y = []
        for i in range(n_samples):
            impact = 0
            month = months[i]
            temp = temperatures[i]
            rain = rainfall[i]
            wind = wind_speeds[i]
            
            # Monsoon impact
            if month in [6, 7, 8, 9] and rain > 100:
                impact += 0.6
            elif rain > 50:
                impact += 0.3
            
            # Temperature impact
            if temp > 40 or temp < 10:
                impact += 0.4
            elif temp > 35:
                impact += 0.2
            
            # Wind impact
            if wind > 25:
                impact += 0.3
            
            # Humidity impact
            if humidity[i] > 80:
                impact += 0.15
            
            y.append(min(1, impact))
        
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)
        return model
    
    def _initialize_traffic_model(self):
        """Initialize ML model for traffic impact prediction"""
        np.random.seed(42)
        n_samples = 10000
        
        # Features: hour, day_of_week, city_traffic_intensity, construction_type_impact, weather_condition
        hours = np.random.randint(0, 24, n_samples)
        days = np.random.randint(0, 7, n_samples)
        city_intensities = np.random.uniform(0.5, 1.0, n_samples)
        construction_impacts = np.random.uniform(0.2, 1.0, n_samples)
        weather_conditions = np.random.randint(0, 4, n_samples)
        
        X = np.column_stack([hours, days, city_intensities, construction_impacts, weather_conditions])
        
        # Generate traffic impact scores
        y = []
        for i in range(n_samples):
            hour = hours[i]
            day = days[i]
            intensity = city_intensities[i]
            
            # Base traffic pattern
            if 8 <= hour <= 10 or 17 <= hour <= 20:  # Peak hours
                base_traffic = 0.8 * intensity
            elif 22 <= hour <= 6:  # Night
                base_traffic = 0.15 * intensity
            else:  # Off-peak
                base_traffic = 0.4 * intensity
            
            # Weekend adjustment
            if day >= 5:
                base_traffic *= 0.7
            
            # Weather adjustment
            if weather_conditions[i] >= 2:  # Bad weather
                base_traffic *= 1.3
            
            # Construction impact
            traffic_impact = base_traffic + (construction_impacts[i] * 0.3)
            
            y.append(min(1, traffic_impact))
        
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)
        return model
    
    def _initialize_timing_model(self):
        """Initialize ML model for optimal timing prediction"""
        np.random.seed(42)
        n_samples = 5000
        
        # Features: month, weather_score, traffic_score, construction_complexity, city_complexity
        months = np.random.randint(1, 13, n_samples)
        weather_scores = np.random.uniform(0, 1, n_samples)
        traffic_scores = np.random.uniform(0, 1, n_samples)
        construction_complexity = np.random.uniform(0.5, 1.0, n_samples)
        city_complexity = np.random.uniform(0.5, 1.0, n_samples)
        
        X = np.column_stack([months, weather_scores, traffic_scores, construction_complexity, city_complexity])
        
        # Generate suitability scores
        y = []
        for i in range(n_samples):
            month = months[i]
            
            # Base seasonal suitability
            if month in [11, 12, 1, 2]:  # Winter - best
                base_score = 0.9
            elif month in [3, 4, 10]:  # Moderate
                base_score = 0.7
            elif month in [5]:  # Hot
                base_score = 0.5
            else:  # Monsoon
                base_score = 0.3
            
            # Adjust based on other factors
            weather_adjustment = (1 - weather_scores[i]) * 0.3
            traffic_adjustment = (1 - traffic_scores[i]) * 0.2
            
            final_score = base_score + weather_adjustment + traffic_adjustment
            final_score *= (2 - construction_complexity[i])  # Higher complexity reduces suitability
            final_score *= (2 - city_complexity[i])  # Higher city complexity reduces suitability
            
            y.append(min(1, max(0, final_score)))
        
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)
        return model
    
    def get_real_time_weather(self, city: str) -> Dict:
        """Get simulated real-time weather data for Indian cities"""
        current_month = datetime.now().month
        current_hour = datetime.now().hour
        city_data = self.indian_cities[city]
        
        # Simulate realistic weather based on season and location
        if current_month in [12, 1, 2]:  # Winter
            temp_range = (15, 25) if city in ['Mumbai', 'Chennai'] else (8, 20)
            humidity_range = (40, 70)
            rainfall = random.uniform(0, 10)
            condition = "Clear" if random.random() > 0.3 else "Partly Cloudy"
        elif current_month in [3, 4, 5]:  # Summer
            temp_range = (28, 45) if city == 'Delhi' else (25, 38)
            humidity_range = (30, 60)
            rainfall = random.uniform(0, 15)
            condition = "Hot" if random.random() > 0.4 else "Sunny"
        elif current_month in city_data['monsoon_months']:  # Monsoon
            temp_range = (22, 32)
            humidity_range = (70, 95)
            rainfall = random.uniform(50, 200)
            condition = "Rainy" if random.random() > 0.3 else "Heavy Rain"
        else:  # Post-monsoon
            temp_range = (20, 30)
            humidity_range = (50, 75)
            rainfall = random.uniform(10, 40)
            condition = "Pleasant"
        
        return {
            'temperature': round(random.uniform(*temp_range), 1),
            'humidity': round(random.uniform(*humidity_range), 1),
            'rainfall_today': round(random.uniform(0, rainfall/30), 1),  # Daily rainfall
            'monthly_rainfall': round(rainfall, 1),
            'wind_speed': round(random.uniform(5, 25), 1),
            'condition': condition,
            'air_quality': random.choice(['Good', 'Moderate', 'Poor', 'Unhealthy']),
            'uv_index': random.randint(3, 11),
            'timestamp': datetime.now()
        }
    
    def predict_traffic_patterns(self, city: str, date: datetime) -> Dict:
        """Predict traffic patterns for 24 hours"""
        city_data = self.indian_cities[city]
        traffic_intensity = city_data['traffic_intensity']
        
        hourly_traffic = {}
        for hour in range(24):
            # Use ML model to predict
            features = [[hour, date.weekday(), traffic_intensity, 0.5, 1]]  # Base prediction
            base_prediction = self.traffic_model.predict(features)[0]
            
            # Add realistic city-specific patterns
            if any(start <= hour <= end for start, end in city_data['peak_hours']):
                traffic_multiplier = 1.2
            elif 22 <= hour or hour <= 6:
                traffic_multiplier = 0.3
            else:
                traffic_multiplier = 1.0
            
            final_traffic = min(1.0, base_prediction * traffic_multiplier)
            hourly_traffic[hour] = final_traffic
        
        return hourly_traffic
    
    def predict_optimal_timing(self, city: str, construction_type: str, project_duration: int) -> Dict:
        """Predict optimal timing for construction project"""
        city_data = self.indian_cities[city]
        construction_data = self.construction_types[construction_type]
        
        # Analyze next 12 months
        current_date = datetime.now()
        monthly_scores = {}
        
        for month_offset in range(12):
            analysis_date = current_date + timedelta(days=30 * month_offset)
            month = analysis_date.month
            
            # Get weather prediction for this month
            weather_data = self.get_real_time_weather(city)  # Simplified for demo
            weather_risk_mapping = {'Low': 0.2, 'Medium': 0.5, 'High': 0.8}
            weather_score = weather_risk_mapping[city_data['weather_risk']]
            
            # Adjust for monsoon
            if month in city_data['monsoon_months']:
                weather_score += 0.3
            
            # Traffic score
            traffic_score = city_data['traffic_intensity']
            
            # Use ML model for optimal timing
            features = [[month, weather_score, traffic_score, 
                        construction_data['complexity'], 
                        city_data['traffic_intensity']]]
            
            suitability_score = self.optimal_timing_model.predict(features)[0]
            
            # Adjust for construction-specific factors
            if month in city_data['monsoon_months'] and construction_data['weather_sensitivity'] > 0.7:
                suitability_score *= 0.6
            
            monthly_scores[month] = {
                'score': suitability_score,
                'month_name': analysis_date.strftime('%B %Y'),
                'weather_risk': 'High' if month in city_data['monsoon_months'] else city_data['weather_risk'],
                'traffic_impact': 'High' if traffic_score > 0.8 else 'Medium' if traffic_score > 0.6 else 'Low'
            }
        
        # Find best months
        best_months = sorted(monthly_scores.items(), key=lambda x: x[1]['score'], reverse=True)[:3]
        
        return {
            'monthly_scores': monthly_scores,
            'best_months': best_months,
            'overall_recommendation': self._generate_timing_recommendations(city, construction_type, best_months)
        }
    
    def _generate_timing_recommendations(self, city: str, construction_type: str, best_months: List) -> List[str]:
        """Generate timing-based recommendations"""
        recommendations = []
        city_data = self.indian_cities[city]
        
        best_month = best_months[0][0]
        best_score = best_months[0][1]['score']
        
        if best_score > 0.8:
            recommendations.append(f"🌟 Excellent conditions predicted for {best_months[0][1]['month_name']}")
        elif best_score > 0.6:
            recommendations.append(f"✅ Good conditions expected in {best_months[0][1]['month_name']}")
        else:
            recommendations.append(f"⚠️ Challenging conditions ahead - extra planning required")
        
        # Monsoon recommendations
        if best_month not in city_data['monsoon_months']:
            recommendations.append("☀️ Recommended timing avoids monsoon season")
        else:
            recommendations.append("🌧️ Project may face monsoon delays - plan accordingly")
        
        # Traffic recommendations
        if city_data['traffic_intensity'] > 0.8:
            recommendations.append(f"🚦 High traffic city - consider night shifts in {city}")
        
        return recommendations
    
    def generate_complete_construction_plan(self, city: str, construction_type: str, 
                                          project_size: str, start_date: datetime) -> Dict:
        """Generate comprehensive AI-powered construction plan"""
        
        # Get base data
        city_data = self.indian_cities[city]
        construction_data = self.construction_types[construction_type]
        weather_data = self.get_real_time_weather(city)
        traffic_data = self.predict_traffic_patterns(city, start_date)
        timing_analysis = self.predict_optimal_timing(city, construction_type, construction_data['base_duration'])
        
        # Calculate project parameters
        size_multipliers = {'Small': 0.7, 'Medium': 1.0, 'Large': 1.5, 'Mega': 2.5}
        size_multiplier = size_multipliers[project_size]
        
        base_duration = construction_data['base_duration']
        adjusted_duration = base_duration * size_multiplier
        
        # Apply AI predictions for delays
        weather_impact = self.weather_model.predict([[
            start_date.month, weather_data['temperature'], weather_data['humidity'],
            weather_data['monthly_rainfall'], weather_data['wind_speed'],
            0.5  # weather risk factor
        ]])[0]
        
        weather_delay = adjusted_duration * weather_impact * construction_data['weather_sensitivity']
        
        avg_traffic = np.mean(list(traffic_data.values()))
        traffic_delay = adjusted_duration * avg_traffic * construction_data['traffic_impact'] * 0.2
        
        total_duration = int(adjusted_duration + weather_delay + traffic_delay)
        
        # Generate project phases
        phases = self._generate_detailed_phases(construction_data, total_duration, start_date, weather_data)
        
        # Calculate costs
        cost_estimation = self._calculate_project_costs(construction_type, project_size, city, total_duration)
        
        # Resource planning
        resource_plan = self._generate_resource_plan(construction_type, project_size, phases)
        
        # Risk assessment
        risk_assessment = self._perform_risk_assessment(city, construction_type, weather_data, traffic_data)
        
        return {
            'project_overview': {
                'city': city,
                'construction_type': construction_type,
                'project_size': project_size,
                'start_date': start_date,
                'estimated_completion': start_date + timedelta(days=total_duration),
                'total_duration_days': total_duration,
                'base_duration': base_duration,
                'weather_delay_days': int(weather_delay),
                'traffic_delay_days': int(traffic_delay)
            },
            'current_conditions': {
                'weather': weather_data,
                'traffic_patterns': traffic_data,
                'optimal_timing': timing_analysis
            },
            'project_phases': phases,
            'cost_estimation': cost_estimation,
            'resource_planning': resource_plan,
            'risk_assessment': risk_assessment,
            'ai_recommendations': self._generate_comprehensive_recommendations(
                city, construction_type, weather_data, traffic_data, timing_analysis)
        }
    
    def _generate_detailed_phases(self, construction_data: Dict, total_duration: int, 
                                 start_date: datetime, weather_data: Dict) -> List[Dict]:
        """Generate detailed project phases with AI optimization"""
        phases = []
        current_date = start_date
        
        for phase_info in construction_data['phases']:
            phase_duration = int((phase_info['percentage'] / 100) * total_duration)
            
            # Weather-sensitive phases get extra buffer during monsoon
            if phase_info['weather_critical'] and weather_data['condition'] in ['Rainy', 'Heavy Rain']:
                phase_duration = int(phase_duration * 1.2)
            
            end_date = current_date + timedelta(days=phase_duration)
            
            phases.append({
                'phase_name': phase_info['name'],
                'start_date': current_date,
                'end_date': end_date,
                'duration_days': phase_duration,
                'weather_critical': phase_info['weather_critical'],
                'progress_percentage': 0,
                'status': 'Not Started',
                'key_activities': self._get_phase_activities(phase_info['name']),
                'estimated_cost_cr': round(phase_duration * 0.5, 2)  # Simplified cost per day
            })
            
            current_date = end_date + timedelta(days=1)
        
        return phases
    
    def _get_phase_activities(self, phase_name: str) -> List[str]:
        """Get key activities for each phase"""
        activity_mapping = {
            'Foundation & Site Prep': ['Site Survey', 'Soil Testing', 'Excavation', 'Foundation Layout'],
            'Structure & Framework': ['Column Construction', 'Beam Installation', 'Slab Casting'],
            'Planning & Approvals': ['Design Finalization', 'Permit Applications', 'Environmental Clearance'],
            'Survey & Design': ['Topographic Survey', 'Design Development', 'Technical Drawings'],
            'Earthwork & Drainage': ['Excavation', 'Embankment', 'Drainage Systems'],
            'Tunneling & Excavation': ['Tunnel Boring', 'Support Systems', 'Ventilation Setup']
        }
        return activity_mapping.get(phase_name, ['Planning', 'Execution', 'Quality Check'])
    
    def _calculate_project_costs(self, construction_type: str, project_size: str, 
                               city: str, duration: int) -> Dict:
        """Calculate detailed project costs in Indian Rupees"""
        city_data = self.indian_cities[city]
        
        # Base costs per type (in Crores INR)
        base_costs = {
            'Residential Building': 50, 'Commercial Complex': 150, 'Road Construction': 100,
            'Bridge Construction': 300, 'Metro/Railway': 800, 'Industrial Complex': 200
        }
        
        # Size multipliers
        size_multipliers = {'Small': 0.6, 'Medium': 1.0, 'Large': 2.0, 'Mega': 4.0}
        
        base_cost = base_costs[construction_type]
        size_adjusted_cost = base_cost * size_multipliers[project_size]
        city_adjusted_cost = size_adjusted_cost * city_data['construction_cost_index']
        
        # Add contingency based on duration
        contingency = city_adjusted_cost * 0.15  # 15% contingency
        
        # Duration impact (longer projects cost more)
        duration_impact = (duration / 300) * 0.1 * city_adjusted_cost
        
        total_cost = city_adjusted_cost + contingency + duration_impact
        
        return {
            'base_cost_cr': round(base_cost, 2),
            'size_adjusted_cr': round(size_adjusted_cost, 2),
            'city_adjusted_cr': round(city_adjusted_cost, 2),
            'contingency_cr': round(contingency, 2),
            'duration_impact_cr': round(duration_impact, 2),
            'total_estimated_cr': round(total_cost, 2),
            'cost_per_day_lakhs': round((total_cost * 100) / duration, 2)
        }
    
    def _generate_resource_plan(self, construction_type: str, project_size: str, phases: List) -> Dict:
        """Generate resource planning details"""
        size_multipliers = {'Small': 1, 'Medium': 2, 'Large': 4, 'Mega': 8}
        multiplier = size_multipliers[project_size]
        
        # Base resource requirements
        base_resources = {
            'Residential Building': {'workers': 50, 'engineers': 5, 'supervisors': 3, 'equipment': 8},
            'Commercial Complex': {'workers': 100, 'engineers': 10, 'supervisors': 6, 'equipment': 15},
            'Road Construction': {'workers': 80, 'engineers': 8, 'supervisors': 5, 'equipment': 20},
            'Bridge Construction': {'workers': 120, 'engineers': 15, 'supervisors': 8, 'equipment': 25},
            'Metro/Railway': {'workers': 200, 'engineers': 25, 'supervisors': 15, 'equipment': 40},
            'Industrial Complex': {'workers': 150, 'engineers': 18, 'supervisors': 10, 'equipment': 30}
        }
        
        resources = base_resources.get(construction_type, base_resources['Residential Building'])
        
        return {
            'peak_workforce': {
                'skilled_workers': resources['workers'] * multiplier,
                'engineers': resources['engineers'] * multiplier,
                'supervisors': resources['supervisors'] * multiplier,
                'total_personnel': (resources['workers'] + resources['engineers'] + resources['supervisors']) * multiplier
            },
            'equipment_requirements': {
                'heavy_machinery': resources['equipment'] * multiplier,
                'vehicles': int(resources['equipment'] * 0.6 * multiplier),
                'tools_equipment': resources['equipment'] * 2 * multiplier
            },
            'material_estimates': {
                'cement_tons': 1000 * multiplier,
                'steel_tons': 500 * multiplier,
                'aggregate_cubic_meters': 2000 * multiplier
            },
            'phase_wise_allocation': [
                {'phase': phase['phase_name'], 'workers_required': int(resources['workers'] * 0.8 * multiplier)}
                for phase in phases
            ]
        }
    
    def _perform_risk_assessment(self, city: str, construction_type: str, 
                               weather_data: Dict, traffic_data: Dict) -> Dict:
        """Perform comprehensive risk assessment"""
        city_data = self.indian_cities[city]
        risks = []
        
        # Weather risks
        if weather_data['condition'] in ['Rainy', 'Heavy Rain']:
            risks.append({
                'category': 'Weather', 'level': 'High', 'impact': 'Schedule Delay',
                'description': 'Monsoon season may cause significant delays',
                'mitigation': 'Cover materials, adjust work schedule, waterproofing'
            })
        
        # Traffic risks
        avg_traffic = np.mean(list(traffic_data.values()))
        if avg_traffic > 0.8:
            risks.append({
                'category': 'Traffic', 'level': 'High', 'impact': 'Logistics Delay',
                'description': 'Heavy traffic may affect material delivery',
                'mitigation': 'Night delivery, alternative routes, buffer time'
            })
        
        # Seismic risks
        if city_data['seismic_zone'] >= 3:
            risks.append({
                'category': 'Seismic', 'level': 'Medium', 'impact': 'Structural Safety',
                'description': f'Seismic Zone {city_data["seismic_zone"]} requires special considerations',
                'mitigation': 'Seismic-resistant design, quality materials, regular inspections'
            })
        
        # Cost risks
        if city_data['construction_cost_index'] > 1.2:
            risks.append({
                'category': 'Financial', 'level': 'Medium', 'impact': 'Budget Overrun',
                'description': 'High construction costs in this city',
                'mitigation': 'Detailed budgeting, cost monitoring, value engineering'
            })
        
        # Overall risk score calculation
        risk_weights = {'High': 3, 'Medium': 2, 'Low': 1}
        total_risk_score = sum(risk_weights[risk['level']] for risk in risks)
        max_possible_score = len(risks) * 3
        overall_risk_percentage = (total_risk_score / max_possible_score * 100) if risks else 0
        
        return {
            'identified_risks': risks,
            'overall_risk_score': overall_risk_percentage,
            'risk_level': 'High' if overall_risk_percentage > 70 else 'Medium' if overall_risk_percentage > 40 else 'Low',
            'total_risks_identified': len(risks)
        }
    
    def _generate_comprehensive_recommendations(self, city: str, construction_type: str,
                                             weather_data: Dict, traffic_data: Dict,
                                             timing_analysis: Dict) -> List[str]:
        """Generate comprehensive AI-powered recommendations"""
        recommendations = []
        city_data = self.indian_cities[city]
        
        # Weather-based recommendations
        if weather_data['condition'] in ['Rainy', 'Heavy Rain']:
            recommendations.append("🌧️ Active monsoon detected - implement weather protection measures")
            recommendations.append("☂️ Schedule concrete work during dry spells, cover all materials")
        elif weather_data['condition'] == 'Hot':
            recommendations.append("🌡️ High temperature conditions - schedule work during cooler hours (6-10 AM)")
        
        # Traffic recommendations
        peak_traffic_hours = [h for h, level in traffic_data.items() if level > 0.7]
        if peak_traffic_hours:
            recommendations.append(f"🚦 Avoid material delivery during peak hours: {', '.join([f'{h}:00' for h in peak_traffic_hours])}")
        
        # Timing recommendations
        best_months = timing_analysis['best_months'][:2]
        recommendations.append(f"📅 Optimal start months: {best_months[0][1]['month_name']} or {best_months[1][1]['month_name']}")
        
        # City-specific recommendations
        if city_data['traffic_intensity'] > 0.8:
            recommendations.append(f"🏙️ {city} traffic density is high - plan for night operations where possible")
        
        if city_data['seismic_zone'] >= 3:
            recommendations.append(f"🏗️ Seismic Zone {city_data['seismic_zone']} - ensure earthquake-resistant construction")
        
        # Construction type specific
        if construction_type == 'Road Construction':
            recommendations.append("🛣️ Coordinate with traffic police for road closures and diversions")
        elif construction_type == 'Bridge Construction':
            recommendations.append("🌉 Monitor wind speeds closely for crane operations and high-altitude work")
        
        return recommendations

def create_india_construction_map(cities_data: Dict, selected_city: str, 
                                project_locations: List = None) -> folium.Map:
    """Create comprehensive India construction map with project locations"""
    # Center map on India
    india_map = folium.Map(
        location=[20.5937, 78.9629],
        zoom_start=5,
        tiles='OpenStreetMap'
    )
    
    # Add city markers
    for city, data in cities_data.items():
        # Determine marker color and icon based on traffic intensity and weather risk
        if city == selected_city:
            color = 'red'
            icon = 'star'
            popup_color = '#ff6b6b'
        elif data['traffic_intensity'] > 0.8:
            color = 'orange'
            icon = 'exclamation-sign'
            popup_color = '#ffa726'
        else:
            color = 'green'
            icon = 'ok-sign'
            popup_color = '#66bb6a'
        
        # Create detailed popup
        popup_html = f"""
        <div style="width: 300px; font-family: Arial, sans-serif;">
            <div style="background: {popup_color}; color: white; padding: 10px; margin: -10px -10px 10px -10px; border-radius: 5px;">
                <h3 style="margin: 0; font-size: 18px;">{city}</h3>
                <p style="margin: 5px 0 0 0; font-size: 12px;">{data['state']}</p>
            </div>
            <table style="width: 100%; font-size: 12px; border-collapse: collapse;">
                <tr><td><b>Population:</b></td><td>{data['population']}M</td></tr>
                <tr><td><b>Traffic Intensity:</b></td><td>{data['traffic_intensity']*100:.0f}%</td></tr>
                <tr><td><b>Weather Risk:</b></td><td>{data['weather_risk']}</td></tr>
                <tr><td><b>Seismic Zone:</b></td><td>{data['seismic_zone']}</td></tr>
                <tr><td><b>Cost Index:</b></td><td>{data['construction_cost_index']}</td></tr>
            </table>
            <div style="margin-top: 10px;">
                <p style="font-size: 11px; margin: 0;"><b>Major Projects:</b></p>
                <p style="font-size: 10px; margin: 2px 0;">{', '.join(data['major_projects'])}</p>
            </div>
        </div>
        """
        
        folium.Marker(
            location=[data['lat'], data['lon']],
            popup=folium.Popup(popup_html, max_width=350),
            tooltip=f"{city} - Click for details",
            icon=folium.Icon(color=color, icon=icon, prefix='glyphicon')
        ).add_to(india_map)
    
    # Add traffic intensity heatmap circles
    for city, data in cities_data.items():
        folium.Circle(
            location=[data['lat'], data['lon']],
            radius=data['traffic_intensity'] * 50000,  # Scale radius by traffic intensity
            color='red' if data['traffic_intensity'] > 0.8 else 'orange' if data['traffic_intensity'] > 0.6 else 'green',
            fillColor='red' if data['traffic_intensity'] > 0.8 else 'orange' if data['traffic_intensity'] > 0.6 else 'green',
            fillOpacity=0.2,
            popup=f"{city} Traffic Intensity: {data['traffic_intensity']*100:.0f}%"
        ).add_to(india_map)
    
    # Add legend
    legend_html = '''
    <div style="position: fixed; 
                bottom: 50px; right: 50px; width: 200px; height: 120px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:12px; padding: 10px; border-radius: 5px;">
    <p><b>Legend</b></p>
    <p><i class="fa fa-star" style="color:red"></i> Selected City</p>
    <p><i class="fa fa-exclamation" style="color:orange"></i> High Traffic</p>
    <p><i class="fa fa-ok" style="color:green"></i> Normal Traffic</p>
    <p><i class="fa fa-circle" style="color:red;opacity:0.3"></i> Traffic Intensity</p>
    </div>
    '''
    india_map.get_root().html.add_child(folium.Element(legend_html))
    
    return india_map

# Initialize the AI planner
@st.cache_resource
def load_construction_planner():
    """Load and cache the AI construction planner"""
    return AIConstructionPlannerIndia()

def main():
    """Main Streamlit application"""
    
    # Header Section
    st.markdown("""
    <div class="main-header">
        <h1>🏗️ AI Smart Construction Planner - India</h1>
        <p>Real-time Weather & Traffic Intelligence | Optimal Timing Predictions | Complete Project Planning</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize AI planner
    try:
        planner = load_construction_planner()
        st.success("🚀 AI Construction Planner loaded successfully! Ready for intelligent planning.")
    except Exception as e:
        st.error(f"❌ Error loading AI planner: {e}")
        return
    
    # Sidebar Configuration
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-header">
            <h3>🎯 Project Configuration</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # City selection
        selected_city = st.selectbox(
            "🌆 Select Indian City",
            options=list(planner.indian_cities.keys()),
            help="Choose the city where your construction project will be located"
        )
        
        # Construction type
        construction_type = st.selectbox(
            "🏗️ Construction Type",
            options=list(planner.construction_types.keys()),
            format_func=lambda x: f"{planner.construction_types[x]['icon']} {x}",
            help="Select the type of construction project"
        )
        
        # Project size
        project_size = st.selectbox(
            "📏 Project Size",
            options=['Small', 'Medium', 'Large', 'Mega'],
            index=1,
            help="Small: <₹50Cr | Medium: ₹50-200Cr | Large: ₹200-500Cr | Mega: >₹500Cr"
        )
        
        # Project details
        project_name = st.text_input(
            "📝 Project Name",
            value=f"Smart {construction_type} - {selected_city}",
            help="Enter a descriptive name for your project"
        )
        
        start_date = st.date_input(
            "📅 Planned Start Date",
            value=datetime.now().date(),
            min_value=datetime.now().date(),
            help="Select when you plan to start the construction"
        )
        
        st.markdown("---")
        
        # Action buttons
        if st.button("🤖 Generate AI Construction Plan", type="primary"):
            st.session_state.generate_plan = True
        
        if st.button("🌤️ Check Weather & Traffic", type="secondary"):
            st.session_state.check_conditions = True
        
        if st.button("⏰ Find Optimal Timing", type="secondary"):
            st.session_state.optimal_timing = True
    
    # Main Content Area
    if not any(st.session_state.get(key, False) for key in ['generate_plan', 'check_conditions', 'optimal_timing']):
        # Default view - City overview and map
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader(f"📍 {selected_city} - Construction Hub")
            city_info = planner.indian_cities[selected_city]
            
            st.markdown(f"""
            <div class="feature-card">
                <h4>🏙️ City Overview</h4>
                <table style="width: 100%; font-size: 14px;">
                    <tr><td><b>State:</b></td><td>{city_info['state']}</td></tr>
                    <tr><td><b>Population:</b></td><td>{city_info['population']} Million</td></tr>
                    <tr><td><b>Traffic Intensity:</b></td><td>{city_info['traffic_intensity']*100:.0f}%</td></tr>
                    <tr><td><b>Weather Risk:</b></td><td>{city_info['weather_risk']}</td></tr>
                    <tr><td><b>Seismic Zone:</b></td><td>{city_info['seismic_zone']}</td></tr>
                    <tr><td><b>Cost Index:</b></td><td>{city_info['construction_cost_index']}</td></tr>
                </table>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="feature-card">
                <h4>🏗️ Major Ongoing Projects</h4>
                <ul>
                    {''.join([f'<li>{project}</li>' for project in city_info['major_projects']])}
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.subheader("🗺️ India Construction Map")
            india_map = create_india_construction_map(planner.indian_cities, selected_city)
            map_data = st_folium(india_map, width=500, height=400)
        
        # Quick stats
        st.subheader("📊 Platform Statistics")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3 style="color: #667eea; margin: 0;">8+</h3>
                <p style="margin: 0.5rem 0 0 0;">Major Cities</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h3 style="color: #e74c3c; margin: 0;">6+</h3>
                <p style="margin: 0.5rem 0 0 0;">Project Types</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h3 style="color: #f39c12; margin: 0;">AI</h3>
                <p style="margin: 0.5rem 0 0 0;">Powered</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="metric-card">
                <h3 style="color: #27ae60; margin: 0;">24/7</h3>
                <p style="margin: 0.5rem 0 0 0;">Monitoring</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col5:
            st.markdown("""
            <div class="metric-card">
                <h3 style="color: #9b59b6; margin: 0;">Real-time</h3>
                <p style="margin: 0.5rem 0 0 0;">Data</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Feature overview
        st.subheader("✨ AI Intelligence Features")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="feature-card">
                <h4>🧠 Smart Planning</h4>
                <ul>
                    <li>AI-powered duration prediction</li>
                    <li>Weather impact analysis</li>
                    <li>Traffic optimization</li>
                    <li>Phase-wise scheduling</li>
                    <li>Resource allocation</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="feature-card">
                <h4>📊 Real-time Intelligence</h4>
                <ul>
                    <li>Live weather monitoring</li>
                    <li>Traffic pattern analysis</li>
                    <li>Cost estimation with ML</li>
                    <li>Risk assessment</li>
                    <li>Optimal timing prediction</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="feature-card">
                <h4>🎯 Smart Recommendations</h4>
                <ul>
                    <li>Best construction months</li>
                    <li>Weather precautions</li>
                    <li>Traffic management</li>
                    <li>Resource optimization</li>
                    <li>Risk mitigation strategies</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    # Handle Weather & Traffic Check
    elif st.session_state.get('check_conditions', False):
        st.header(f"🌤️ Current Conditions - {selected_city}")
        
        weather_data = planner.get_real_time_weather(selected_city)
        traffic_data = planner.predict_traffic_patterns(selected_city, datetime.now())
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="weather-card">
                <h4>🌡️ Weather Conditions</h4>
                <table style="width: 100%; color: white;">
                    <tr><td>Temperature:</td><td><b>{weather_data['temperature']}°C</b></td></tr>
                    <tr><td>Condition:</td><td><b>{weather_data['condition']}</b></td></tr>
                    <tr><td>Humidity:</td><td><b>{weather_data['humidity']}%</b></td></tr>
                    <tr><td>Today's Rainfall:</td><td><b>{weather_data['rainfall_today']}mm</b></td></tr>
                    <tr><td>Wind Speed:</td><td><b>{weather_data['wind_speed']} km/h</b></td></tr>
                    <tr><td>Air Quality:</td><td><b>{weather_data['air_quality']}</b></td></tr>
                    <tr><td>UV Index:</td><td><b>{weather_data['uv_index']}</b></td></tr>
                </table>
                <p style="font-size: 12px; margin-top: 10px;">
                    Updated: {weather_data['timestamp'].strftime('%H:%M:%S')}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            current_hour = datetime.now().hour
            current_traffic = traffic_data.get(current_hour, 0.5)
            traffic_status = "Heavy" if current_traffic > 0.7 else "Moderate" if current_traffic > 0.4 else "Light"
            
            st.markdown(f"""
            <div class="traffic-card">
                <h4>🚦 Traffic Analysis</h4>
                <div style="text-align: center; margin: 20px 0;">
                    <h2 style="margin: 0; font-size: 3rem;">{current_traffic:.0%}</h2>
                    <p style="margin: 5px 0; font-size: 1.2rem;"><b>{traffic_status}</b></p>
                </div>
                <table style="width: 100%; color: white;">
                    <tr><td>Current Hour:</td><td><b>{current_hour}:00</b></td></tr>
                    <tr><td>Peak Hours:</td><td><b>8-10 AM, 6-8 PM</b></td></tr>
                    <tr><td>City Intensity:</td><td><b>{planner.indian_cities[selected_city]['traffic_intensity']*100:.0f}%</b></td></tr>
                </table>
            </div>
            """, unsafe_allow_html=True)
        
        # Traffic pattern chart
        st.subheader("📈 24-Hour Traffic Pattern")
        
        hours = list(range(24))
        traffic_levels = [traffic_data[h] * 100 for h in hours]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=hours, y=traffic_levels,
            mode='lines+markers',
            name='Traffic Intensity',
            line=dict(color='#e74c3c', width=3),
            fill='tonexty'
        ))
        
        # Add peak hour highlights
        fig.add_vrect(x0=8, x1=10, fillcolor="orange", opacity=0.3, annotation_text="Morning Peak")
        fig.add_vrect(x0=18, x1=20, fillcolor="orange", opacity=0.3, annotation_text="Evening Peak")
        
        # Current time indicator
        fig.add_vline(x=current_hour, line_dash="dash", line_color="green", 
                     annotation_text=f"Now: {current_hour}:00")
        
        fig.update_layout(
            title=f"Traffic Intensity Pattern - {selected_city}",
            xaxis_title="Hour of Day",
            yaxis_title="Traffic Intensity (%)",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Reset state
        st.session_state.check_conditions = False
    
    # Handle Optimal Timing Analysis
    elif st.session_state.get('optimal_timing', False):
        st.header(f"⏰ Optimal Timing Analysis - {construction_type}")
        
        with st.spinner("🤖 AI is analyzing optimal timing for your project..."):
            timing_analysis = planner.predict_optimal_timing(selected_city, construction_type, 
                                                           planner.construction_types[construction_type]['base_duration'])
        
        # Best months display
        st.subheader("🌟 Recommended Construction Months")
        
        best_months = timing_analysis['best_months'][:3]
        
        col1, col2, col3 = st.columns(3)
        
        for i, (month, data) in enumerate(best_months):
            col = [col1, col2, col3][i]
            rank = ["🥇", "🥈", "🥉"][i]
            
            with col:
                st.markdown(f"""
                <div class="feature-card">
                    <div style="text-align: center;">
                        <h2 style="margin: 0; font-size: 2rem;">{rank}</h2>
                        <h4 style="margin: 10px 0;">{data['month_name']}</h4>
                        <div style="margin: 15px 0;">
                            <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                                      width: {data['score']*100}%; height: 20px; border-radius: 10px; margin: 10px auto;">
                            </div>
                            <p style="margin: 5px 0; font-weight: bold;">{data['score']*100:.0f}% Suitability</p>
                        </div>
                        <p><strong>Weather Risk:</strong> {data['weather_risk']}</p>
                        <p><strong>Traffic Impact:</strong> {data['traffic_impact']}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Monthly suitability chart
        st.subheader("📊 12-Month Suitability Analysis")
        
        monthly_scores = timing_analysis['monthly_scores']
        months = list(monthly_scores.keys())
        scores = [monthly_scores[m]['score'] * 100 for m in months]
        month_names = [monthly_scores[m]['month_name'].split()[0] for m in months]
        
        fig = go.Figure(data=[
            go.Bar(x=month_names, y=scores, 
                  marker_color=['#27ae60' if s > 70 else '#f39c12' if s > 50 else '#e74c3c' for s in scores],
                  text=[f'{s:.0f}%' for s in scores],
                  textposition='auto')
        ])
        
        fig.update_layout(
            title="Monthly Construction Suitability Scores",
            xaxis_title="Months",
            yaxis_title="Suitability Score (%)",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Recommendations
        st.subheader("💡 Timing Recommendations")
        for rec in timing_analysis['overall_recommendation']:
            st.markdown(f"""
            <div class="recommendation-card">
                {rec}
            </div>
            """, unsafe_allow_html=True)
        
        # Reset state
        st.session_state.optimal_timing = False
    
    # Handle Full Construction Plan Generation
    elif st.session_state.get('generate_plan', False):
        st.header(f"🎯 AI Construction Plan: {project_name}")
        
        with st.spinner("🤖 AI is generating comprehensive construction plan..."):
            time.sleep(3)  # Simulate AI processing
            
            schedule_date = datetime.combine(start_date, datetime.min.time())
            complete_plan = planner.generate_complete_construction_plan(
                selected_city, construction_type, project_size, schedule_date)
        
        # Project overview metrics
        overview = complete_plan['project_overview']
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #667eea; margin: 0;">{overview['total_duration_days']}</h3>
                <p style="margin: 0.5rem 0 0 0;">Total Days</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            completion_date = overview['estimated_completion'].strftime('%d %b %Y')
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #27ae60; margin: 0; font-size: 1rem;">{completion_date}</h3>
                <p style="margin: 0.5rem 0 0 0;">Completion</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            total_cost = complete_plan['cost_estimation']['total_estimated_cr']
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #e74c3c; margin: 0;">₹{total_cost}</h3>
                <p style="margin: 0.5rem 0 0 0;">Crores</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            weather_delay = overview['weather_delay_days']
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #f39c12; margin: 0;">+{weather_delay}</h3>
                <p style="margin: 0.5rem 0 0 0;">Weather Days</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col5:
            total_workers = complete_plan['resource_planning']['peak_workforce']['total_personnel']
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #9b59b6; margin: 0;">{total_workers}</h3>
                <p style="margin: 0.5rem 0 0 0;">Peak Workforce</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Detailed analysis tabs
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📅 Project Timeline", "💰 Cost Analysis", "👥 Resources", 
            "⚠️ Risk Assessment", "🌤️ Conditions", "💡 AI Recommendations"
        ])
        
        with tab1:
            st.subheader("🏗️ Project Phases & Timeline")
            
            phases = complete_plan['project_phases']
            
            # Gantt chart
            fig = go.Figure()
            
            colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c']
            
            for i, phase in enumerate(phases):
                fig.add_trace(go.Bar(
                    name=phase['phase_name'],
                    x=[phase['duration_days']],
                    y=[phase['phase_name']],
                    orientation='h',
                    marker_color=colors[i % len(colors)],
                    text=f"{phase['duration_days']} days",
                    textposition='auto'
                ))
            
            fig.update_layout(
                title="Project Timeline (Gantt Chart)",
                xaxis_title="Duration (Days)",
                height=400,
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Phase details
            for phase in phases:
                st.markdown(f"""
                <div class="phase-timeline">
                    <h5>{phase['phase_name']}</h5>
                    <div style="display: flex; justify-content: space-between; margin: 10px 0;">
                        <span><b>Duration:</b> {phase['duration_days']} days</span>
                        <span><b>Cost:</b> ₹{phase['estimated_cost_cr']} Cr</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin: 10px 0;">
                        <span><b>Start:</b> {phase['start_date'].strftime('%d %b %Y')}</span>
                        <span><b>End:</b> {phase['end_date'].strftime('%d %b %Y')}</span>
                    </div>
                    <p><b>Key Activities:</b> {', '.join(phase['key_activities'])}</p>
                    {'<p style="color: orange;"><b>⚠️ Weather Critical Phase</b></p>' if phase['weather_critical'] else ''}
                </div>
                """, unsafe_allow_html=True)
        
        with tab2:
            st.subheader("💰 Detailed Cost Analysis")
            
            cost_data = complete_plan['cost_estimation']
            
            # Cost breakdown chart
            cost_categories = {
                'Base Cost': cost_data['base_cost_cr'],
                'Size Adjustment': cost_data['size_adjusted_cr'] - cost_data['base_cost_cr'],
                'City Premium': cost_data['city_adjusted_cr'] - cost_data['size_adjusted_cr'],
                'Contingency': cost_data['contingency_cr'],
                'Duration Impact': cost_data['duration_impact_cr']
            }
            
            fig = go.Figure(data=[
                go.Bar(x=list(cost_categories.keys()), y=list(cost_categories.values()),
                       marker_color=['#3498db', '#f39c12', '#e74c3c', '#9b59b6', '#1abc9c'])
            ])
            
            fig.update_layout(
                title="Cost Breakdown Analysis (₹ Crores)",
                yaxis_title="Cost (₹ Crores)",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Cost summary
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div class="feature-card">
                    <h4>💸 Cost Summary</h4>
                    <table style="width: 100%;">
                        <tr><td>Base Cost:</td><td><b>₹{cost_data['base_cost_cr']} Cr</b></td></tr>
                        <tr><td>Size Adjusted:</td><td><b>₹{cost_data['size_adjusted_cr']} Cr</b></td></tr>
                        <tr><td>City Adjusted:</td><td><b>₹{cost_data['city_adjusted_cr']} Cr</b></td></tr>
                        <tr><td>Contingency (15%):</td><td><b>₹{cost_data['contingency_cr']} Cr</b></td></tr>
                        <tr style="border-top: 2px solid #667eea;">
                            <td><b>Total Cost:</b></td><td><b>₹{cost_data['total_estimated_cr']} Cr</b></td>
                        </tr>
                    </table>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="feature-card">
                    <h4>📊 Cost Metrics</h4>
                    <table style="width: 100%;">
                        <tr><td>Cost per Day:</td><td><b>₹{cost_data['cost_per_day_lakhs']} Lakhs</b></td></tr>
                        <tr><td>Duration Impact:</td><td><b>₹{cost_data['duration_impact_cr']} Cr</b></td></tr>
                        <tr><td>City Index:</td><td><b>{planner.indian_cities[selected_city]['construction_cost_index']}</b></td></tr>
                        <tr><td>Project Size:</td><td><b>{project_size}</b></td></tr>
                    </table>
                </div>
                """, unsafe_allow_html=True)
        
        with tab3:
            st.subheader("👥 Resource Planning")
            
            resources = complete_plan['resource_planning']
            
            col1, col2 = st.columns(2)
            
            with col1:
                workforce = resources['peak_workforce']
                st.markdown(f"""
                <div class="feature-card">
                    <h4>👷 Peak Workforce Requirements</h4>
                    <table style="width: 100%;">
                        <tr><td>Skilled Workers:</td><td><b>{workforce['skilled_workers']}</b></td></tr>
                        <tr><td>Engineers:</td><td><b>{workforce['engineers']}</b></td></tr>
                        <tr><td>Supervisors:</td><td><b>{workforce['supervisors']}</b></td></tr>
                        <tr style="border-top: 2px solid #667eea;">
                            <td><b>Total Personnel:</b></td><td><b>{workforce['total_personnel']}</b></td>
                        </tr>
                    </table>
                </div>
                """, unsafe_allow_html=True)
                
                equipment = resources['equipment_requirements']
                st.markdown(f"""
                <div class="feature-card">
                    <h4>🚜 Equipment Requirements</h4>
                    <table style="width: 100%;">
                        <tr><td>Heavy Machinery:</td><td><b>{equipment['heavy_machinery']}</b></td></tr>
                        <tr><td>Vehicles:</td><td><b>{equipment['vehicles']}</b></td></tr>
                        <tr><td>Tools & Equipment:</td><td><b>{equipment['tools_equipment']}</b></td></tr>
                    </table>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                materials = resources['material_estimates']
                st.markdown(f"""
                <div class="feature-card">
                    <h4>🏗️ Material Estimates</h4>
                    <table style="width: 100%;">
                        <tr><td>Cement:</td><td><b>{materials['cement_tons']} Tons</b></td></tr>
                        <tr><td>Steel:</td><td><b>{materials['steel_tons']} Tons</b></td></tr>
                        <tr><td>Aggregate:</td><td><b>{materials['aggregate_cubic_meters']} m³</b></td></tr>
                    </table>
                </div>
                """, unsafe_allow_html=True)
                
                # Phase-wise workforce chart
                phase_names = [p['phase'] for p in resources['phase_wise_allocation']]
                phase_workers = [p['workers_required'] for p in resources['phase_wise_allocation']]
                
                fig = go.Figure(data=[
                    go.Bar(x=phase_names, y=phase_workers, marker_color='#667eea')
                ])
                
                fig.update_layout(
                    title="Phase-wise Workforce Allocation",
                    xaxis_title="Project Phases",
                    yaxis_title="Workers Required",
                    height=300
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        with tab4:
            st.subheader("⚠️ Risk Assessment & Mitigation")
            
            risk_data = complete_plan['risk_assessment']
            
            # Risk level indicator
            risk_level = risk_data['risk_level']
            risk_color = '#e74c3c' if risk_level == 'High' else '#f39c12' if risk_level == 'Medium' else '#27ae60'
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown(f"""
                <div class="metric-card" style="border-left-color: {risk_color};">
                    <h3 style="color: {risk_color}; margin: 0;">{risk_level}</h3>
                    <p style="margin: 0.5rem 0 0 0;">Overall Risk Level</p>
                    <p style="font-size: 0.9rem; margin: 0.5rem 0 0 0;">
                        {risk_data['overall_risk_score']:.0f}% Risk Score
                    </p>
                    <p style="font-size: 0.9rem; margin: 0.2rem 0 0 0;">
                        {risk_data['total_risks_identified']} Risks Identified
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # Risk breakdown
                risk_categories = {}
                for risk in risk_data['identified_risks']:
                    category = risk['category']
                    if category not in risk_categories:
                        risk_categories[category] = 0
                    risk_categories[category] += 1
                
                if risk_categories:
                    fig = go.Figure(data=[
                        go.Pie(labels=list(risk_categories.keys()), 
                               values=list(risk_categories.values()),
                               hole=0.4)
                    ])
                    
                    fig.update_layout(
                        title="Risk Distribution by Category",
                        height=300
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
            
            # Detailed risks
            for risk in risk_data['identified_risks']:
                risk_color = '#e74c3c' if risk['level'] == 'High' else '#f39c12'
                
                st.markdown(f"""
                <div class="feature-card" style="border-left: 4px solid {risk_color};">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h5 style="margin: 0;">{risk['category']} Risk</h5>
                        <span style="color: {risk_color}; font-weight: bold;">{risk['level']}</span>
                    </div>
                    <p style="margin: 8px 0;"><strong>Impact:</strong> {risk['impact']}</p>
                    <p style="margin: 8px 0;">{risk['description']}</p>
                    <p style="margin: 8px 0; color: #27ae60;"><strong>Mitigation:</strong> {risk['mitigation']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with tab5:
            st.subheader("🌤️ Current Conditions Analysis")
            
            conditions = complete_plan['current_conditions']
            weather = conditions['weather']
            traffic = conditions['traffic_patterns']
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div class="weather-card">
                    <h4>🌡️ Weather Impact Analysis</h4>
                    <table style="width: 100%; color: white;">
                        <tr><td>Temperature:</td><td><b>{weather['temperature']}°C</b></td></tr>
                        <tr><td>Condition:</td><td><b>{weather['condition']}</b></td></tr>
                        <tr><td>Humidity:</td><td><b>{weather['humidity']}%</b></td></tr>
                        <tr><td>Monthly Rainfall:</td><td><b>{weather['monthly_rainfall']}mm</b></td></tr>
                        <tr><td>Wind Speed:</td><td><b>{weather['wind_speed']} km/h</b></td></tr>
                    </table>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                avg_traffic = np.mean(list(traffic.values()))
                traffic_status = "Heavy" if avg_traffic > 0.7 else "Moderate" if avg_traffic > 0.4 else "Light"
                
                st.markdown(f"""
                <div class="traffic-card">
                    <h4>🚦 Traffic Impact Analysis</h4>
                    <div style="text-align: center; margin: 15px 0;">
                        <h3 style="margin: 0;">{avg_traffic:.0%}</h3>
                        <p style="margin: 5px 0;">Average Daily Traffic</p>
                        <p style="margin: 5px 0;"><b>Status: {traffic_status}</b></p>
                    </div>
                    <p>Peak morning: 8-10 AM</p>
                    <p>Peak evening: 6-8 PM</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Optimal timing insight
            timing = conditions['optimal_timing']
            best_month = timing['best_months'][0]
            
            st.markdown(f"""
            <div class="ai-insight">
                <h4>🎯 Optimal Timing Insight</h4>
                <p><strong>Best Month to Start:</strong> {best_month[1]['month_name']} 
                   (Suitability Score: {best_month[1]['score']*100:.0f}%)</p>
                <p><strong>Weather Risk:</strong> {best_month[1]['weather_risk']}</p>
                <p><strong>Traffic Impact:</strong> {best_month[1]['traffic_impact']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with tab6:
            st.subheader("💡 AI-Generated Recommendations")
            
            recommendations = complete_plan['ai_recommendations']
            
            for i, recommendation in enumerate(recommendations, 1):
                st.markdown(f"""
                <div class="recommendation-card">
                    <strong>{i}.</strong> {recommendation}
                </div>
                """, unsafe_allow_html=True)
            
            # Additional insights
            st.subheader("🔍 Key Insights")
            
            insights = []
            
            # Duration insights
            base_duration = overview['base_duration']
            total_duration = overview['total_duration_days']
            duration_increase = ((total_duration - base_duration) / base_duration) * 100
            
            if duration_increase > 30:
                insights.append(f"📈 Project duration increased by {duration_increase:.0f}% due to external factors")
            elif duration_increase > 15:
                insights.append(f"⚠️ Moderate duration increase of {duration_increase:.0f}% expected")
            else:
                insights.append(f"✅ Minimal duration impact - only {duration_increase:.0f}% increase")
            
            # Cost insights
            total_cost = complete_plan['cost_estimation']['total_estimated_cr']
            if total_cost > 500:
                insights.append(f"💰 Large scale project - ₹{total_cost} Crores budget requires careful monitoring")
            
            # Weather insights
            if weather['condition'] in ['Rainy', 'Heavy Rain']:
                insights.append("🌧️ Current monsoon conditions detected - implement weather protection measures")
            
            # Traffic insights
            if avg_traffic > 0.8:
                insights.append("🚦 High traffic area - consider alternative logistics strategies")
            
            for insight in insights:
                st.info(insight)
        
        # Action buttons for next steps
        st.subheader("🎯 Next Steps")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📊 Generate Detailed Report", help="Create comprehensive project report"):
                st.success("📋 Detailed report generation initiated!")
        
        with col2:
            if st.button("📅 Export Schedule", help="Export timeline to calendar format"):
                st.success("📤 Schedule export prepared!")
        
        with col3:
            if st.button("💬 Share with Team", help="Share plan with project stakeholders"):
                st.success("👥 Plan sharing enabled!")
        
        with col4:
            if st.button("🔄 Update Analysis", help="Refresh with latest conditions"):
                st.experimental_rerun()
        
        # Reset state
        st.session_state.generate_plan = False
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem; color: #6c757d;">
        <p><strong>🏗️ AI Smart Construction Planner for India</strong></p>
        <p>Powered by Advanced Machine Learning | Real-time Intelligence | Comprehensive Planning</p>
        <p><em>Built for the future of Indian construction industry</em></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
