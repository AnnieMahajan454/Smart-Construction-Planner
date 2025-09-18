"""Enhanced Analytics Page - Advanced features for construction planning."""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os

# Add parent directory to path to import smart_planner
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

try:
    from smart_planner.sustainability import assess_project_sustainability, SustainabilityMetrics
    from smart_planner.risk_assessment import assess_project_risks, RiskLevel
    ADVANCED_FEATURES_AVAILABLE = True
except ImportError as e:
    st.error(f"Advanced features not available: {e}")
    ADVANCED_FEATURES_AVAILABLE = False


def estimate_project_timeline(
    project_type: str,
    total_area: float,
    number_of_floors: int,
    location: str,
    complexity_factors: dict = None
) -> dict:
    """Estimate project timeline based on various factors."""
    
    if complexity_factors is None:
        complexity_factors = {}
    
    # Base construction rates (days per m²) by project type
    base_rates = {
        'Residential': 0.8,
        'Commercial': 1.2,
        'Industrial': 1.0,
        'Institutional': 1.5
    }
    
    # Location multipliers (permitting and labor availability)
    location_multipliers = {
        'New York': 1.3,
        'San Francisco': 1.4,
        'Los Angeles': 1.2,
        'Chicago': 1.1,
        'Miami': 1.0,
        'Dallas': 0.9,
        'Houston': 0.9,
        'Atlanta': 1.0
    }
    
    base_construction_days = total_area * base_rates.get(project_type, 1.0)
    location_factor = location_multipliers.get(location, 1.0)
    
    # Floor complexity
    floor_factor = 1 + (number_of_floors - 1) * 0.15
    
    # Design and permitting phase (typically 15-25% of total timeline)
    design_permitting_days = base_construction_days * 0.2 * location_factor
    
    # Construction phase
    construction_days = base_construction_days * location_factor * floor_factor
    
    # Complexity factors
    if complexity_factors.get('complex_design', False):
        construction_days *= 1.2
    if complexity_factors.get('sustainable_features', False):
        construction_days *= 1.1
    if complexity_factors.get('historic_renovation', False):
        construction_days *= 1.4
    
    # Closeout phase
    closeout_days = construction_days * 0.1
    
    total_days = design_permitting_days + construction_days + closeout_days
    
    return {
        'total_days': int(total_days),
        'design_permitting_days': int(design_permitting_days),
        'construction_days': int(construction_days),
        'closeout_days': int(closeout_days),
        'total_weeks': int(total_days / 7),
        'total_months': int(total_days / 30)
    }


def create_gantt_chart(timeline_dict: dict) -> go.Figure:
    """Create a Gantt chart for project timeline."""
    
    phases = [
        {'Task': 'Design & Permitting', 'Start': 0, 'Duration': timeline_dict['design_permitting_days']},
        {'Task': 'Construction', 'Start': timeline_dict['design_permitting_days'], 
         'Duration': timeline_dict['construction_days']},
        {'Task': 'Closeout & Handover', 
         'Start': timeline_dict['design_permitting_days'] + timeline_dict['construction_days'],
         'Duration': timeline_dict['closeout_days']}
    ]
    
    fig = go.Figure()
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    
    for i, phase in enumerate(phases):
        fig.add_trace(go.Bar(
            name=phase['Task'],
            x=[phase['Duration']],
            y=[phase['Task']],
            orientation='h',
            base=phase['Start'],
            marker_color=colors[i],
            text=f"{phase['Duration']} days",
            textposition='inside'
        ))
    
    fig.update_layout(
        title="Project Timeline Gantt Chart",
        xaxis_title="Days",
        yaxis_title="Project Phase",
        barmode='overlay',
        height=300,
        margin=dict(l=150)
    )
    
    return fig


def create_sustainability_radar(metrics: SustainabilityMetrics) -> go.Figure:
    """Create a radar chart for sustainability metrics."""
    
    categories = [
        'Energy Efficiency',
        'Water Usage',
        'Green Materials',
        'Waste Reduction',
        'Overall Score'
    ]
    
    values = [
        metrics.energy_efficiency,
        metrics.water_usage,
        metrics.green_materials,
        metrics.waste_reduction,
        metrics.overall_score
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Sustainability Metrics',
        line_color='green'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="Project Sustainability Assessment",
        height=400
    )
    
    return fig


def create_risk_heatmap(risk_assessment) -> go.Figure:
    """Create a risk assessment heatmap."""
    
    risk_categories = [
        'Timeline Risk',
        'Budget Risk', 
        'Safety Risk',
        'Environmental Risk',
        'Regulatory Risk'
    ]
    
    risk_values = [
        risk_assessment.timeline_risk,
        risk_assessment.budget_risk,
        risk_assessment.safety_risk,
        risk_assessment.environmental_risk,
        risk_assessment.regulatory_risk
    ]
    
    # Create color scale based on risk levels
    colors = []
    for value in risk_values:
        if value >= 7:
            colors.append('red')
        elif value >= 5:
            colors.append('orange')
        elif value >= 3:
            colors.append('yellow')
        else:
            colors.append('green')
    
    fig = go.Figure(data=go.Bar(
        x=risk_categories,
        y=risk_values,
        marker_color=colors,
        text=[f"{v:.1f}" for v in risk_values],
        textposition='auto'
    ))
    
    fig.update_layout(
        title="Project Risk Assessment by Category",
        xaxis_title="Risk Categories",
        yaxis_title="Risk Score (0-10)",
        yaxis=dict(range=[0, 10]),
        height=400
    )
    
    return fig


def main():
    """Main enhanced analytics page."""
    
    st.title("🏗️ Enhanced Construction Analytics")
    st.markdown("Advanced analytics and insights for your construction project")
    
    if not ADVANCED_FEATURES_AVAILABLE:
        st.error("Advanced features are not available. Please check your installation.")
        return
    
    # Sidebar inputs
    st.sidebar.header("Project Configuration")
    
    project_types = ['Residential', 'Commercial', 'Industrial', 'Institutional']
    locations = ['New York', 'San Francisco', 'Los Angeles', 'Chicago', 'Miami', 'Dallas', 'Houston', 'Atlanta']
    
    project_type = st.sidebar.selectbox("Project Type", project_types)
    location = st.sidebar.selectbox("Location", locations)
    total_area = st.sidebar.number_input("Total Area (m²)", min_value=50.0, value=1000.0, step=50.0)
    number_of_floors = st.sidebar.number_input("Number of Floors", min_value=1, max_value=50, value=2)
    number_of_basements = st.sidebar.number_input("Number of Basements", min_value=0, max_value=5, value=0)
    
    # Advanced options
    with st.sidebar.expander("Advanced Options"):
        project_start_month = st.selectbox("Project Start Month", 
                                         range(1, 13), 
                                         format_func=lambda x: [
                                             'January', 'February', 'March', 'April', 'May', 'June',
                                             'July', 'August', 'September', 'October', 'November', 'December'
                                         ][x-1])
        
        materials = st.multiselect("Primary Materials",
                                 ['Steel', 'Concrete', 'Lumber', 'Aluminum', 'Glass', 'Insulation'],
                                 default=['Steel', 'Concrete', 'Lumber'])
        
        # Sustainability features
        st.subheader("Sustainability Features")
        solar_panels = st.checkbox("Solar Panels")
        green_roof = st.checkbox("Green Roof")
        rainwater_harvesting = st.checkbox("Rainwater Harvesting")
        smart_hvac = st.checkbox("Smart HVAC")
        
        # Complexity factors
        st.subheader("Project Complexity")
        complex_design = st.checkbox("Complex Design")
        sustainable_features = st.checkbox("Enhanced Sustainability Features")
        historic_renovation = st.checkbox("Historic Renovation")
    
    # Create tabs for different analyses
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Timeline Analysis", "🌱 Sustainability Assessment", 
                                      "⚠️ Risk Assessment", "💰 Enhanced Cost Analysis"])
    
    with tab1:
        st.header("Project Timeline Analysis")
        
        complexity_factors = {
            'complex_design': complex_design,
            'sustainable_features': sustainable_features,
            'historic_renovation': historic_renovation
        }
        
        timeline = estimate_project_timeline(
            project_type, total_area, number_of_floors, location, complexity_factors
        )
        
        # Display timeline summary
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Duration", f"{timeline['total_months']} months", 
                     f"{timeline['total_days']} days")
        
        with col2:
            st.metric("Construction Phase", f"{timeline['construction_days']} days",
                     f"{timeline['construction_days']/timeline['total_days']*100:.0f}% of total")
        
        with col3:
            st.metric("Design & Permitting", f"{timeline['design_permitting_days']} days",
                     f"{timeline['design_permitting_days']/timeline['total_days']*100:.0f}% of total")
        
        # Gantt Chart
        gantt_fig = create_gantt_chart(timeline)
        st.plotly_chart(gantt_fig, use_container_width=True)
        
        # Timeline breakdown
        st.subheader("Phase Breakdown")
        phase_data = pd.DataFrame({
            'Phase': ['Design & Permitting', 'Construction', 'Closeout & Handover'],
            'Duration (Days)': [timeline['design_permitting_days'], 
                              timeline['construction_days'], 
                              timeline['closeout_days']],
            'Percentage': [
                timeline['design_permitting_days']/timeline['total_days']*100,
                timeline['construction_days']/timeline['total_days']*100,
                timeline['closeout_days']/timeline['total_days']*100
            ]
        })
        
        st.dataframe(phase_data, use_container_width=True)
    
    with tab2:
        st.header("Sustainability Assessment")
        
        # Prepare building design features
        building_design = {
            'solar_panels': solar_panels,
            'green_roof': green_roof,
            'smart_hvac': smart_hvac,
            'led_lighting': True,  # Default
            'high_performance_windows': False
        }
        
        # Water features
        water_features = {
            'rainwater_harvesting': rainwater_harvesting,
            'low_flow_fixtures': True,  # Default
            'greywater_recycling': False,
            'drought_resistant_landscaping': False
        }
        
        # Perform sustainability assessment
        sustainability = assess_project_sustainability(
            project_type, total_area, location, materials, building_design, water_features
        )
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Overall Score", f"{sustainability.overall_score:.0f}/100")
        
        with col2:
            st.metric("Carbon Footprint", f"{sustainability.carbon_footprint/1000:.1f} tons CO2e")
        
        with col3:
            st.metric("Energy Efficiency", f"{sustainability.energy_efficiency:.0f}/100")
        
        with col4:
            st.metric("LEED Potential", sustainability.leed_potential)
        
        # Sustainability radar chart
        radar_fig = create_sustainability_radar(sustainability)
        st.plotly_chart(radar_fig, use_container_width=True)
        
        # Detailed breakdown
        st.subheader("Sustainability Breakdown")
        sustainability_df = pd.DataFrame({
            'Metric': ['Energy Efficiency', 'Water Usage', 'Green Materials', 'Waste Reduction'],
            'Score': [sustainability.energy_efficiency, sustainability.water_usage,
                     sustainability.green_materials, sustainability.waste_reduction],
            'Rating': [
                'Excellent' if sustainability.energy_efficiency >= 80 else 'Good' if sustainability.energy_efficiency >= 60 else 'Fair',
                'Excellent' if sustainability.water_usage >= 80 else 'Good' if sustainability.water_usage >= 60 else 'Fair',
                'Excellent' if sustainability.green_materials >= 80 else 'Good' if sustainability.green_materials >= 60 else 'Fair',
                'Excellent' if sustainability.waste_reduction >= 80 else 'Good' if sustainability.waste_reduction >= 60 else 'Fair'
            ]
        })
        
        st.dataframe(sustainability_df, use_container_width=True)
        
        # Recommendations
        st.subheader("Sustainability Recommendations")
        for i, recommendation in enumerate(sustainability.recommendations[:5], 1):
            st.write(f"{i}. {recommendation}")
    
    with tab3:
        st.header("Risk Assessment")
        
        # Perform risk assessment
        risk_assessment = assess_project_risks(
            project_type, total_area, location, materials, project_start_month
        )
        
        # Overall risk display
        col1, col2, col3 = st.columns(3)
        
        with col1:
            risk_color = {
                RiskLevel.LOW: "green",
                RiskLevel.MEDIUM: "orange", 
                RiskLevel.HIGH: "red",
                RiskLevel.CRITICAL: "darkred"
            }[risk_assessment.risk_level]
            
            st.markdown(f"**Overall Risk Level:** <span style='color: {risk_color}'>{risk_assessment.risk_level.value}</span>", 
                       unsafe_allow_html=True)
        
        with col2:
            st.metric("Risk Score", f"{risk_assessment.overall_risk_score:.1f}/10")
        
        with col3:
            st.metric("High-Risk Factors", 
                     len([f for f in risk_assessment.risk_factors if f.level in [RiskLevel.HIGH, RiskLevel.CRITICAL]]))
        
        # Risk heatmap
        risk_heatmap = create_risk_heatmap(risk_assessment)
        st.plotly_chart(risk_heatmap, use_container_width=True)
        
        # Individual risk factors
        st.subheader("Risk Factor Details")
        
        for factor in risk_assessment.risk_factors:
            with st.expander(f"{factor.name} - {factor.level.value} Risk"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Description:** {factor.description}")
                    st.write(f"**Probability:** {factor.probability:.0%}")
                    st.write(f"**Impact:** {factor.impact:.1f}/10")
                
                with col2:
                    st.write("**Mitigation Strategies:**")
                    for strategy in factor.mitigation_strategies[:3]:
                        st.write(f"• {strategy}")
        
        # Overall recommendations
        st.subheader("Risk Management Recommendations")
        for i, recommendation in enumerate(risk_assessment.recommendations, 1):
            st.write(f"{i}. {recommendation}")
    
    with tab4:
        st.header("Enhanced Cost Analysis")
        
        # Basic cost calculation (simplified for demo)
        base_rates = {
            'New York': 3500,
            'San Francisco': 3400,
            'Los Angeles': 3000,
            'Chicago': 2600,
            'Miami': 2500,
            'Dallas': 2400,
            'Houston': 2300,
            'Atlanta': 2200
        }
        
        base_rate = base_rates.get(location, 2500)
        base_cost = total_area * base_rate
        
        # Apply multipliers
        floor_multiplier = 1 + (number_of_floors - 1) * 0.1
        basement_multiplier = 1 + number_of_basements * 0.15
        
        total_cost = base_cost * floor_multiplier * basement_multiplier
        
        # Add sustainability premium/discount
        if sustainability.overall_score > 80:
            sustainability_impact = 1.05  # 5% premium for high sustainability
        elif sustainability.overall_score > 60:
            sustainability_impact = 1.02  # 2% premium
        else:
            sustainability_impact = 1.0
        
        # Add risk premium
        risk_multiplier = 1 + (risk_assessment.overall_risk_score / 100)
        
        adjusted_cost = total_cost * sustainability_impact * risk_multiplier
        
        # Cost breakdown
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Base Cost", f"${total_cost:,.0f}")
        
        with col2:
            st.metric("Risk-Adjusted", f"${adjusted_cost:,.0f}",
                     f"${adjusted_cost - total_cost:,.0f}")
        
        with col3:
            st.metric("Cost per m²", f"${adjusted_cost/total_area:,.0f}")
        
        with col4:
            contingency = adjusted_cost * 0.15
            st.metric("With 15% Contingency", f"${adjusted_cost + contingency:,.0f}")
        
        # Cost breakdown chart
        cost_breakdown = {
            'Materials': adjusted_cost * 0.4,
            'Labor': adjusted_cost * 0.3,
            'Equipment': adjusted_cost * 0.15,
            'Permits & Fees': adjusted_cost * 0.05,
            'Overhead': adjusted_cost * 0.1
        }
        
        fig = px.pie(values=list(cost_breakdown.values()), 
                    names=list(cost_breakdown.keys()),
                    title="Cost Breakdown by Category")
        st.plotly_chart(fig, use_container_width=True)
        
        # Cost comparison by location
        st.subheader("Cost Comparison by Location")
        location_costs = {}
        for loc, rate in base_rates.items():
            loc_cost = total_area * rate * floor_multiplier * basement_multiplier
            location_costs[loc] = loc_cost
        
        cost_comparison_df = pd.DataFrame({
            'Location': list(location_costs.keys()),
            'Estimated Cost': list(location_costs.values())
        }).sort_values('Estimated Cost')
        
        fig = px.bar(cost_comparison_df, x='Location', y='Estimated Cost',
                    title="Cost Comparison Across Locations")
        fig.update_xaxis(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
