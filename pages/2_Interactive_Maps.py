"""Interactive Maps Page - Site location analysis and visualization."""

import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


def get_coordinates(city_name: str) -> tuple:
    """Get latitude and longitude for a city."""

    # Predefined coordinates for major cities
    city_coords = {
        'New York': (40.7128, -74.0060),
        'San Francisco': (37.7749, -122.4194),
        'Los Angeles': (34.0522, -118.2437),
        'Chicago': (41.8781, -87.6298),
        'Miami': (25.7617, -80.1918),
        'Dallas': (32.7767, -96.7970),
        'Houston': (29.7604, -95.3698),
        'Atlanta': (33.7490, -84.3880)
    }

    if city_name in city_coords:
        return city_coords[city_name]

    try:
        geolocator = Nominatim(user_agent="construction_planner")
        location = geolocator.geocode(city_name)
        if location:
            return (location.latitude, location.longitude)
    except Exception:
        pass

    # Default to New York if geocoding fails
    return (40.7128, -74.0060)


def create_site_map(location: str, project_sites: list = None) -> folium.Map:
    """Create an interactive map showing project site and nearby amenities."""

    lat, lon = get_coordinates(location)

    # Create base map
    m = folium.Map(location=[lat, lon], zoom_start=12)

    # Add main project location
    folium.Marker(
        [lat, lon],
        popup=f"Project Site - {location}",
        tooltip="Main Project Site",
        icon=folium.Icon(color='red', icon='building', prefix='fa')
    ).add_to(m)

    # Add nearby infrastructure points of interest
    amenities = [
        {"name": "Hospital", "offset": (0.02, 0.01), "icon": "plus", "color": "blue"},
        {"name": "School", "offset": (-0.015, 0.02), "icon": "graduation-cap", "color": "green"},
        {"name": "Fire Station", "offset": (0.01, -0.018), "icon": "fire", "color": "red"},
        {"name": "Shopping Center", "offset": (-0.025, -0.015), "icon": "shopping-cart", "color": "purple"},
        {"name": "Public Transport", "offset": (0.005, 0.025), "icon": "bus", "color": "orange"},
        {"name": "Park", "offset": (-0.01, 0.015), "icon": "tree", "color": "green"}
    ]

    for amenity in amenities:
        amenity_lat = lat + amenity["offset"][0]
        amenity_lon = lon + amenity["offset"][1]

        folium.Marker(
            [amenity_lat, amenity_lon],
            popup=amenity["name"],
            tooltip=amenity["name"],
            icon=folium.Icon(color=amenity["color"], icon=amenity["icon"], prefix='fa')
        ).add_to(m)

    # Add traffic/congestion layer simulation
    traffic_points = []
    for i in range(10):
        traffic_lat = lat + np.random.normal(0, 0.02)
        traffic_lon = lon + np.random.normal(0, 0.02)
        congestion_level = np.random.choice(['low', 'medium', 'high'])

        color_map = {'low': 'green', 'medium': 'orange', 'high': 'red'}

        folium.CircleMarker(
            [traffic_lat, traffic_lon],
            radius=5,
            color=color_map[congestion_level],
            fillColor=color_map[congestion_level],
            fillOpacity=0.6,
            popup=f"Traffic: {congestion_level}",
            tooltip=f"Congestion: {congestion_level}"
        ).add_to(m)

        traffic_points.append({
            'lat': traffic_lat,
            'lon': traffic_lon,
            'congestion': congestion_level,
            'distance_km': geodesic((lat, lon), (traffic_lat, traffic_lon)).kilometers
        })

    # Add radius circles
    folium.Circle(
        location=[lat, lon],
        radius=1000,  # 1km
        color='blue',
        fill=True,
        fillOpacity=0.1,
        popup="1km radius"
    ).add_to(m)

    folium.Circle(
        location=[lat, lon],
        radius=2000,  # 2km
        color='green',
        fill=True,
        fillOpacity=0.1,
        popup="2km radius"
    ).add_to(m)

    return m, traffic_points


def analyze_site_accessibility(location: str) -> dict:
    """Analyze site accessibility metrics."""

    # Simulated accessibility data based on city characteristics
    accessibility_data = {
        'New York': {
            'public_transport_score': 95,
            'walkability_score': 85,
            'bicycle_infrastructure': 78,
            'parking_availability': 40,
            'traffic_congestion': 85,
            'emergency_services_distance': 0.5
        },
        'San Francisco': {
            'public_transport_score': 88,
            'walkability_score': 82,
            'bicycle_infrastructure': 90,
            'parking_availability': 35,
            'traffic_congestion': 80,
            'emergency_services_distance': 0.7
        },
        'Los Angeles': {
            'public_transport_score': 65,
            'walkability_score': 60,
            'bicycle_infrastructure': 55,
            'parking_availability': 70,
            'traffic_congestion': 90,
            'emergency_services_distance': 1.2
        },
        'Chicago': {
            'public_transport_score': 85,
            'walkability_score': 75,
            'bicycle_infrastructure': 70,
            'parking_availability': 55,
            'traffic_congestion': 75,
            'emergency_services_distance': 0.8
        },
        'Miami': {
            'public_transport_score': 60,
            'walkability_score': 65,
            'bicycle_infrastructure': 45,
            'parking_availability': 75,
            'traffic_congestion': 70,
            'emergency_services_distance': 1.0
        },
        'Dallas': {
            'public_transport_score': 55,
            'walkability_score': 50,
            'bicycle_infrastructure': 40,
            'parking_availability': 85,
            'traffic_congestion': 65,
            'emergency_services_distance': 1.5
        },
        'Houston': {
            'public_transport_score': 50,
            'walkability_score': 45,
            'bicycle_infrastructure': 35,
            'parking_availability': 90,
            'traffic_congestion': 70,
            'emergency_services_distance': 1.8
        },
        'Atlanta': {
            'public_transport_score': 70,
            'walkability_score': 55,
            'bicycle_infrastructure': 50,
            'parking_availability': 80,
            'traffic_congestion': 75,
            'emergency_services_distance': 1.3
        }
    }

    return accessibility_data.get(location, accessibility_data['Chicago'])  # Default to Chicago


def create_accessibility_chart(accessibility_data: dict) -> go.Figure:
    """Create accessibility radar chart."""

    categories = [
        'Public Transport',
        'Walkability',
        'Bicycle Infrastructure',
        'Parking Availability',
        'Traffic Flow (inverted)',
        'Emergency Services'
    ]

    values = [
        accessibility_data['public_transport_score'],
        accessibility_data['walkability_score'],
        accessibility_data['bicycle_infrastructure'],
        accessibility_data['parking_availability'],
        100 - accessibility_data['traffic_congestion'],  # Invert traffic congestion
        max(0, 100 - accessibility_data['emergency_services_distance'] * 30)  # Convert distance to score
    ]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Accessibility Metrics',
        line_color='blue'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="Site Accessibility Assessment",
        height=500
    )

    return fig


def calculate_site_suitability(
    location: str,
    project_type: str,
    total_area: float,
    accessibility_data: dict
) -> dict:
    """Calculate overall site suitability score."""

    # Base suitability factors by project type
    type_weights = {
        'Residential': {
            'accessibility': 0.3,
            'safety': 0.25,
            'amenities': 0.25,
            'environment': 0.2
        },
        'Commercial': {
            'accessibility': 0.4,
            'safety': 0.2,
            'amenities': 0.15,
            'environment': 0.25
        },
        'Industrial': {
            'accessibility': 0.2,
            'safety': 0.3,
            'amenities': 0.1,
            'environment': 0.4
        },
        'Institutional': {
            'accessibility': 0.35,
            'safety': 0.3,
            'amenities': 0.2,
            'environment': 0.15
        }
    }

    weights = type_weights.get(project_type, type_weights['Commercial'])

    # Calculate component scores
    accessibility_score = (
        accessibility_data['public_transport_score'] * 0.4 +
        accessibility_data['walkability_score'] * 0.3 +
        accessibility_data['parking_availability'] * 0.3
    )

    safety_score = (
        max(0, 100 - accessibility_data['emergency_services_distance'] * 20) * 0.6 +
        (100 - accessibility_data['traffic_congestion']) * 0.4
    )

    amenities_score = (
        accessibility_data['public_transport_score'] * 0.5 +
        accessibility_data['bicycle_infrastructure'] * 0.3 +
        accessibility_data['walkability_score'] * 0.2
    )

    # Environmental score (simplified)
    environmental_score = 75  # Base environmental score

    # Calculate weighted overall score
    overall_score = (
        accessibility_score * weights['accessibility'] +
        safety_score * weights['safety'] +
        amenities_score * weights['amenities'] +
        environmental_score * weights['environment']
    )

    return {
        'overall_score': overall_score,
        'accessibility_score': accessibility_score,
        'safety_score': safety_score,
        'amenities_score': amenities_score,
        'environmental_score': environmental_score,
        'recommendation': get_suitability_recommendation(overall_score)
    }


def get_suitability_recommendation(score: float) -> str:
    """Get site suitability recommendation based on score."""

    if score >= 85:
        return "Excellent - Highly recommended site with optimal conditions"
    elif score >= 75:
        return "Very Good - Site meets most requirements with minor considerations"
    elif score >= 65:
        return "Good - Suitable site with some areas for improvement"
    elif score >= 50:
        return "Fair - Site may require additional planning and mitigation measures"
    else:
        return "Poor - Consider alternative sites or significant modifications"


def main():
    """Main interactive maps page."""

    st.title("🗺️ Interactive Site Analysis")
    st.markdown("Comprehensive site analysis with interactive mapping and accessibility assessment")

    # Sidebar inputs
    st.sidebar.header("Site Configuration")

    project_types = ['Residential', 'Commercial', 'Industrial', 'Institutional']
    locations = ['New York', 'San Francisco', 'Los Angeles', 'Chicago', 'Miami', 'Dallas', 'Houston', 'Atlanta']

    location = st.sidebar.selectbox("Primary Location", locations)
    project_type = st.sidebar.selectbox("Project Type", project_types)
    total_area = st.sidebar.number_input("Total Area (m²)", min_value=50.0, value=1000.0, step=50.0)

    # Custom location option
    custom_location = st.sidebar.text_input("Or enter custom location:")
    if custom_location:
        location = custom_location

    # Create tabs
    tab1, tab2, tab3 = st.tabs(["🗺️ Interactive Map", "📊 Accessibility Analysis", "🏗️ Site Suitability"])

    with tab1:
        st.header("Project Site Map")
        st.markdown(f"**Location:** {location} | **Project Type:** {project_type}")

        # Create and display map
        site_map, traffic_data = create_site_map(location)
        st_folium(site_map, width=700, height=500)

        # Display traffic analysis
        st.subheader("Traffic Analysis")

        if traffic_data:
            traffic_df = pd.DataFrame(traffic_data)

            col1, col2, col3 = st.columns(3)

            with col1:
                avg_congestion = traffic_df['congestion'].value_counts()
                st.write("**Traffic Congestion Distribution:**")
                for level, count in avg_congestion.items():
                    st.write(f"• {level.title()}: {count} points")

            with col2:
                avg_distance = traffic_df['distance_km'].mean()
                st.metric("Average Distance to Traffic Points", f"{avg_distance:.1f} km")

            with col3:
                high_congestion = len(traffic_df[traffic_df['congestion'] == 'high'])
                st.metric("High Congestion Areas", f"{high_congestion} within 2km")

        # Map legend
        with st.expander("Map Legend"):
            st.write("""
            **Icons:**
            - 🏢 Red Building: Project Site
            - 🏥 Blue Plus: Hospital
            - 🎓 Green Graduation Cap: School
            - 🔥 Red Fire: Fire Station
            - 🛒 Purple Shopping Cart: Shopping Center
            - 🚌 Orange Bus: Public Transport
            - 🌳 Green Tree: Park

            **Traffic Indicators:**
            - 🟢 Green Circle: Low Traffic
            - 🟡 Orange Circle: Medium Traffic
            - 🔴 Red Circle: High Traffic

            **Radius Circles:**
            - Blue: 1km radius
            - Green: 2km radius
            """)

    with tab2:
        st.header("Accessibility Analysis")

        # Get accessibility data
        accessibility_data = analyze_site_accessibility(location)

        # Display key metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Public Transport", f"{accessibility_data['public_transport_score']}/100")

        with col2:
            st.metric("Walkability", f"{accessibility_data['walkability_score']}/100")

        with col3:
            st.metric("Bicycle Infrastructure", f"{accessibility_data['bicycle_infrastructure']}/100")

        with col4:
            st.metric("Emergency Services", f"{accessibility_data['emergency_services_distance']:.1f} km")

        # Accessibility radar chart
        accessibility_chart = create_accessibility_chart(accessibility_data)
        st.plotly_chart(accessibility_chart, use_container_width=True)

        # Detailed breakdown
        st.subheader("Accessibility Breakdown")

        accessibility_df = pd.DataFrame({
            'Metric': [
                'Public Transport Access',
                'Walkability Score',
                'Bicycle Infrastructure',
                'Parking Availability',
                'Traffic Congestion (inverted)',
                'Emergency Services Distance'
            ],
            'Score/Value': [
                f"{accessibility_data['public_transport_score']}/100",
                f"{accessibility_data['walkability_score']}/100",
                f"{accessibility_data['bicycle_infrastructure']}/100",
                f"{accessibility_data['parking_availability']}/100",
                f"{accessibility_data['traffic_congestion']}/100",
                f"{accessibility_data['emergency_services_distance']} km"
            ],
            'Rating': [
                'Excellent' if accessibility_data['public_transport_score'] >= 80 else 'Good' if accessibility_data['public_transport_score'] >= 60 else 'Fair',
                'Excellent' if accessibility_data['walkability_score'] >= 80 else 'Good' if accessibility_data['walkability_score'] >= 60 else 'Fair',
                'Excellent' if accessibility_data['bicycle_infrastructure'] >= 80 else 'Good' if accessibility_data['bicycle_infrastructure'] >= 60 else 'Fair',
                'Excellent' if accessibility_data['parking_availability'] >= 80 else 'Good' if accessibility_data['parking_availability'] >= 60 else 'Fair',
                'Excellent' if accessibility_data['traffic_congestion'] <= 60 else 'Good' if accessibility_data['traffic_congestion'] <= 80 else 'Fair',
                'Excellent' if accessibility_data['emergency_services_distance'] <= 0.5 else 'Good' if accessibility_data['emergency_services_distance'] <= 1.0 else 'Fair'
            ]
        })

        st.dataframe(accessibility_df, use_container_width=True)

    with tab3:
        st.header("Site Suitability Assessment")

        # Calculate suitability
        suitability = calculate_site_suitability(location, project_type, total_area, accessibility_data)

        # Overall suitability display
        col1, col2 = st.columns(2)

        with col1:
            st.metric("Overall Suitability Score", f"{suitability['overall_score']:.0f}/100")

            # Color-coded recommendation
            score = suitability['overall_score']
            if score >= 85:
                color = "green"
            elif score >= 75:
                color = "blue"
            elif score >= 65:
                color = "orange"
            else:
                color = "red"

            st.markdown(f"**Recommendation:** <span style='color: {color}'>{suitability['recommendation']}</span>",
                       unsafe_allow_html=True)

        with col2:
            st.write("**Component Scores:**")
            st.write(f"• Accessibility: {suitability['accessibility_score']:.0f}/100")
            st.write(f"• Safety: {suitability['safety_score']:.0f}/100")
            st.write(f"• Amenities: {suitability['amenities_score']:.0f}/100")
            st.write(f"• Environment: {suitability['environmental_score']:.0f}/100")

        # Suitability breakdown chart
        fig = go.Figure(data=go.Bar(
            x=['Accessibility', 'Safety', 'Amenities', 'Environment'],
            y=[
                suitability['accessibility_score'],
                suitability['safety_score'],
                suitability['amenities_score'],
                suitability['environmental_score']
            ],
            marker_color=['blue', 'red', 'green', 'orange']
        ))

        fig.update_layout(
            title="Site Suitability Component Scores",
            xaxis_title="Assessment Categories",
            yaxis_title="Score (0-100)",
            yaxis=dict(range=[0, 100]),
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

        # Site improvement recommendations
        st.subheader("Site Improvement Recommendations")

        recommendations = []

        if suitability['accessibility_score'] < 70:
            recommendations.append("Consider improving public transport connections or shuttle services")

        if suitability['safety_score'] < 70:
            recommendations.append("Implement additional security measures and emergency response plans")

        if suitability['amenities_score'] < 70:
            recommendations.append("Plan for additional amenities or partnerships with nearby facilities")

        if suitability['environmental_score'] < 70:
            recommendations.append("Include environmental remediation or enhancement measures")

        if not recommendations:
            recommendations.append("Site shows good suitability across all assessment categories")

        for i, recommendation in enumerate(recommendations, 1):
            st.write(f"{i}. {recommendation}")


if __name__ == "__main__":
    main()
