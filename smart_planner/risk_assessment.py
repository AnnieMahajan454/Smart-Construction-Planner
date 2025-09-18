"""Risk assessment module for construction projects."""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import datetime


class RiskLevel(Enum):
    """Risk level enumeration."""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


@dataclass
class RiskFactor:
    """Individual risk factor."""
    name: str
    level: RiskLevel
    probability: float  # 0-1
    impact: float  # 0-10
    description: str
    mitigation_strategies: List[str]


@dataclass
class ProjectRiskAssessment:
    """Complete project risk assessment."""
    overall_risk_score: float
    risk_level: RiskLevel
    risk_factors: List[RiskFactor]
    timeline_risk: float
    budget_risk: float
    safety_risk: float
    environmental_risk: float
    regulatory_risk: float
    recommendations: List[str]


def assess_weather_risk(location: str, project_start_month: int) -> RiskFactor:
    """Assess weather-related construction risks."""
    
    # Weather risk data by location and season
    weather_risks = {
        'New York': {
            'winter': {'probability': 0.8, 'impact': 7, 'main_risk': 'snow and freezing'},
            'spring': {'probability': 0.4, 'impact': 4, 'main_risk': 'rain'},
            'summer': {'probability': 0.2, 'impact': 3, 'main_risk': 'thunderstorms'},
            'fall': {'probability': 0.3, 'impact': 4, 'main_risk': 'early cold weather'}
        },
        'San Francisco': {
            'winter': {'probability': 0.5, 'impact': 4, 'main_risk': 'rain and fog'},
            'spring': {'probability': 0.3, 'impact': 3, 'main_risk': 'fog'},
            'summer': {'probability': 0.1, 'impact': 2, 'main_risk': 'minimal weather impact'},
            'fall': {'probability': 0.2, 'impact': 3, 'main_risk': 'early rains'}
        },
        'Los Angeles': {
            'winter': {'probability': 0.3, 'impact': 3, 'main_risk': 'occasional rain'},
            'spring': {'probability': 0.1, 'impact': 2, 'main_risk': 'minimal weather impact'},
            'summer': {'probability': 0.2, 'impact': 4, 'main_risk': 'extreme heat'},
            'fall': {'probability': 0.4, 'impact': 5, 'main_risk': 'fire season and Santa Ana winds'}
        },
        'Chicago': {
            'winter': {'probability': 0.9, 'impact': 8, 'main_risk': 'severe cold and snow'},
            'spring': {'probability': 0.5, 'impact': 5, 'main_risk': 'severe storms'},
            'summer': {'probability': 0.3, 'impact': 4, 'main_risk': 'thunderstorms'},
            'fall': {'probability': 0.4, 'impact': 4, 'main_risk': 'early winter weather'}
        },
        'Miami': {
            'winter': {'probability': 0.1, 'impact': 2, 'main_risk': 'minimal weather impact'},
            'spring': {'probability': 0.2, 'impact': 3, 'main_risk': 'occasional storms'},
            'summer': {'probability': 0.8, 'impact': 7, 'main_risk': 'hurricane season'},
            'fall': {'probability': 0.7, 'impact': 6, 'main_risk': 'continued hurricane season'}
        },
        'Dallas': {
            'winter': {'probability': 0.4, 'impact': 5, 'main_risk': 'ice storms'},
            'spring': {'probability': 0.7, 'impact': 6, 'main_risk': 'severe storms and tornadoes'},
            'summer': {'probability': 0.5, 'impact': 6, 'main_risk': 'extreme heat'},
            'fall': {'probability': 0.2, 'impact': 3, 'main_risk': 'minimal weather impact'}
        },
        'Houston': {
            'winter': {'probability': 0.3, 'impact': 4, 'main_risk': 'occasional freezing'},
            'spring': {'probability': 0.6, 'impact': 5, 'main_risk': 'severe storms'},
            'summer': {'probability': 0.7, 'impact': 7, 'main_risk': 'hurricane season and flooding'},
            'fall': {'probability': 0.5, 'impact': 5, 'main_risk': 'hurricane season'}
        },
        'Atlanta': {
            'winter': {'probability': 0.5, 'impact': 5, 'main_risk': 'ice storms'},
            'spring': {'probability': 0.6, 'impact': 5, 'main_risk': 'severe storms'},
            'summer': {'probability': 0.4, 'impact': 4, 'main_risk': 'thunderstorms'},
            'fall': {'probability': 0.2, 'impact': 3, 'main_risk': 'minimal weather impact'}
        }
    }
    
    # Determine season
    season_map = {
        12: 'winter', 1: 'winter', 2: 'winter',
        3: 'spring', 4: 'spring', 5: 'spring',
        6: 'summer', 7: 'summer', 8: 'summer',
        9: 'fall', 10: 'fall', 11: 'fall'
    }
    
    season = season_map.get(project_start_month, 'spring')
    location_risks = weather_risks.get(location, weather_risks['Chicago'])  # Default to moderate risk
    risk_data = location_risks[season]
    
    # Determine risk level
    if risk_data['impact'] >= 7:
        level = RiskLevel.HIGH
    elif risk_data['impact'] >= 5:
        level = RiskLevel.MEDIUM
    else:
        level = RiskLevel.LOW
    
    mitigation_strategies = [
        "Plan for weather delays in timeline",
        "Secure weather-resistant equipment and materials",
        "Monitor weather forecasts closely",
        "Have backup plans for critical activities"
    ]
    
    if 'hurricane' in risk_data['main_risk']:
        mitigation_strategies.extend([
            "Purchase hurricane insurance coverage",
            "Plan construction shutdown procedures",
            "Secure all equipment and materials during storm season"
        ])
    
    if 'snow' in risk_data['main_risk'] or 'ice' in risk_data['main_risk']:
        mitigation_strategies.extend([
            "Plan for snow removal and de-icing",
            "Use cold-weather concrete mixes",
            "Protect work areas from freezing"
        ])
    
    return RiskFactor(
        name="Weather Risk",
        level=level,
        probability=risk_data['probability'],
        impact=risk_data['impact'],
        description=f"Risk from {risk_data['main_risk']} during {season} in {location}",
        mitigation_strategies=mitigation_strategies
    )


def assess_seismic_risk(location: str) -> RiskFactor:
    """Assess seismic risk based on location."""
    
    seismic_zones = {
        'New York': {'probability': 0.1, 'impact': 4, 'zone': 'Low'},
        'San Francisco': {'probability': 0.8, 'impact': 9, 'zone': 'Very High'},
        'Los Angeles': {'probability': 0.7, 'impact': 8, 'zone': 'High'},
        'Chicago': {'probability': 0.2, 'impact': 3, 'zone': 'Low'},
        'Miami': {'probability': 0.05, 'impact': 2, 'zone': 'Very Low'},
        'Dallas': {'probability': 0.1, 'impact': 3, 'zone': 'Low'},
        'Houston': {'probability': 0.1, 'impact': 3, 'zone': 'Low'},
        'Atlanta': {'probability': 0.15, 'impact': 4, 'zone': 'Low-Medium'}
    }
    
    risk_data = seismic_zones.get(location, {'probability': 0.3, 'impact': 5, 'zone': 'Medium'})
    
    if risk_data['impact'] >= 8:
        level = RiskLevel.HIGH
    elif risk_data['impact'] >= 5:
        level = RiskLevel.MEDIUM
    else:
        level = RiskLevel.LOW
    
    mitigation_strategies = [
        "Follow local seismic building codes",
        "Use appropriate structural design for seismic zones",
        "Consider seismic insurance",
        "Plan for post-earthquake inspections"
    ]
    
    if risk_data['impact'] >= 7:
        mitigation_strategies.extend([
            "Implement enhanced seismic design standards",
            "Use base isolation or damping systems",
            "Conduct detailed geotechnical surveys"
        ])
    
    return RiskFactor(
        name="Seismic Risk",
        level=level,
        probability=risk_data['probability'],
        impact=risk_data['impact'],
        description=f"Earthquake risk in {risk_data['zone']} seismic zone ({location})",
        mitigation_strategies=mitigation_strategies
    )


def assess_regulatory_risk(project_type: str, location: str, total_area: float) -> RiskFactor:
    """Assess regulatory and permitting risks."""
    
    # Base regulatory complexity by location
    regulatory_complexity = {
        'New York': {'base_risk': 8, 'permit_time': 16},
        'San Francisco': {'base_risk': 9, 'permit_time': 20},
        'Los Angeles': {'base_risk': 7, 'permit_time': 14},
        'Chicago': {'base_risk': 6, 'permit_time': 12},
        'Miami': {'base_risk': 5, 'permit_time': 10},
        'Dallas': {'base_risk': 4, 'permit_time': 8},
        'Houston': {'base_risk': 4, 'permit_time': 8},
        'Atlanta': {'base_risk': 5, 'permit_time': 10}
    }
    
    # Project type multipliers
    type_multipliers = {
        'Residential': 1.0,
        'Commercial': 1.2,
        'Industrial': 1.5,
        'Institutional': 1.3
    }
    
    # Size multipliers
    if total_area > 10000:  # Large projects
        size_multiplier = 1.4
    elif total_area > 5000:  # Medium projects
        size_multiplier = 1.2
    else:  # Small projects
        size_multiplier = 1.0
    
    base_data = regulatory_complexity.get(location, {'base_risk': 6, 'permit_time': 12})
    type_mult = type_multipliers.get(project_type, 1.0)
    
    adjusted_risk = min(10, base_data['base_risk'] * type_mult * size_multiplier)
    probability = min(1.0, (base_data['permit_time'] / 20) * type_mult)
    
    if adjusted_risk >= 8:
        level = RiskLevel.HIGH
    elif adjusted_risk >= 6:
        level = RiskLevel.MEDIUM
    else:
        level = RiskLevel.LOW
    
    mitigation_strategies = [
        "Engage with regulatory authorities early in the process",
        "Hire experienced local permit expeditors",
        "Prepare comprehensive documentation",
        "Build permit delays into project timeline",
        "Consider pre-approved design options where available"
    ]
    
    if adjusted_risk >= 8:
        mitigation_strategies.extend([
            "Engage specialized regulatory consultants",
            "Consider phased approval approach",
            "Plan for extended approval timelines"
        ])
    
    return RiskFactor(
        name="Regulatory Risk",
        level=level,
        probability=probability,
        impact=adjusted_risk,
        description=f"Permitting and regulatory compliance risk for {project_type} project in {location}",
        mitigation_strategies=mitigation_strategies
    )


def assess_labor_risk(location: str, project_type: str, total_area: float) -> RiskFactor:
    """Assess labor availability and cost risks."""
    
    # Labor market conditions by location
    labor_markets = {
        'New York': {'availability': 0.7, 'cost_volatility': 0.8, 'union_strength': 0.9},
        'San Francisco': {'availability': 0.5, 'cost_volatility': 0.9, 'union_strength': 0.7},
        'Los Angeles': {'availability': 0.6, 'cost_volatility': 0.7, 'union_strength': 0.8},
        'Chicago': {'availability': 0.8, 'cost_volatility': 0.6, 'union_strength': 0.8},
        'Miami': {'availability': 0.7, 'cost_volatility': 0.5, 'union_strength': 0.4},
        'Dallas': {'availability': 0.8, 'cost_volatility': 0.4, 'union_strength': 0.3},
        'Houston': {'availability': 0.9, 'cost_volatility': 0.5, 'union_strength': 0.4},
        'Atlanta': {'availability': 0.8, 'cost_volatility': 0.4, 'union_strength': 0.5}
    }
    
    market_data = labor_markets.get(location, {'availability': 0.7, 'cost_volatility': 0.6, 'union_strength': 0.6})
    
    # Calculate risk factors
    availability_risk = (1 - market_data['availability']) * 10
    cost_risk = market_data['cost_volatility'] * 8
    
    # Project size impact
    if total_area > 10000:  # Large projects need more workers
        size_impact = 1.3
    elif total_area > 5000:
        size_impact = 1.1
    else:
        size_impact = 1.0
    
    overall_risk = (availability_risk + cost_risk) / 2 * size_impact
    probability = 0.3 + (market_data['cost_volatility'] * 0.4)  # Base 30% chance
    
    if overall_risk >= 7:
        level = RiskLevel.HIGH
    elif overall_risk >= 4:
        level = RiskLevel.MEDIUM
    else:
        level = RiskLevel.LOW
    
    mitigation_strategies = [
        "Secure key contractors early with fixed-price contracts",
        "Build labor cost escalation into budget",
        "Develop relationships with multiple subcontractors",
        "Consider alternative construction methods (prefab, modular)"
    ]
    
    if market_data['union_strength'] > 0.7:
        mitigation_strategies.append("Engage with union representatives early")
    
    if overall_risk >= 6:
        mitigation_strategies.extend([
            "Consider hiring bonuses for critical trades",
            "Plan for extended construction timeline",
            "Explore non-local labor sources"
        ])
    
    return RiskFactor(
        name="Labor Risk",
        level=level,
        probability=probability,
        impact=overall_risk,
        description=f"Labor availability and cost risk in {location}",
        mitigation_strategies=mitigation_strategies
    )


def assess_material_risk(project_type: str, materials: List[str]) -> RiskFactor:
    """Assess material cost and availability risks."""
    
    # Material risk profiles
    material_risks = {
        'steel': {'volatility': 0.8, 'supply_risk': 0.6},
        'aluminum': {'volatility': 0.9, 'supply_risk': 0.7},
        'lumber': {'volatility': 0.9, 'supply_risk': 0.8},
        'concrete': {'volatility': 0.4, 'supply_risk': 0.3},
        'copper': {'volatility': 0.8, 'supply_risk': 0.5},
        'glass': {'volatility': 0.5, 'supply_risk': 0.4},
        'insulation': {'volatility': 0.6, 'supply_risk': 0.5}
    }
    
    if not materials:
        materials = ['steel', 'concrete', 'lumber']  # Default materials
    
    total_volatility = 0
    total_supply_risk = 0
    high_risk_materials = []
    
    for material in materials:
        material_clean = material.lower().replace(' ', '_')
        risk_data = material_risks.get(material_clean, {'volatility': 0.5, 'supply_risk': 0.4})
        
        total_volatility += risk_data['volatility']
        total_supply_risk += risk_data['supply_risk']
        
        if risk_data['volatility'] > 0.7 or risk_data['supply_risk'] > 0.6:
            high_risk_materials.append(material)
    
    avg_volatility = total_volatility / len(materials)
    avg_supply_risk = total_supply_risk / len(materials)
    
    overall_risk = (avg_volatility + avg_supply_risk) * 5  # Scale to 0-10
    probability = 0.4 + (avg_volatility * 0.4)  # 40-80% probability
    
    if overall_risk >= 7:
        level = RiskLevel.HIGH
    elif overall_risk >= 4:
        level = RiskLevel.MEDIUM
    else:
        level = RiskLevel.LOW
    
    mitigation_strategies = [
        "Lock in material prices with suppliers early",
        "Build material cost escalation into budget (10-20%)",
        "Identify alternative suppliers and materials",
        "Consider bulk purchasing for critical materials"
    ]
    
    if high_risk_materials:
        mitigation_strategies.extend([
            f"Pay special attention to {', '.join(high_risk_materials)} pricing and availability",
            "Consider material substitutions where possible",
            "Implement just-in-time delivery to reduce inventory risk"
        ])
    
    return RiskFactor(
        name="Material Risk",
        level=level,
        probability=probability,
        impact=overall_risk,
        description="Risk from material cost volatility and supply chain disruptions",
        mitigation_strategies=mitigation_strategies
    )


def calculate_overall_risk_score(risk_factors: List[RiskFactor]) -> Tuple[float, RiskLevel]:
    """Calculate overall project risk score and level."""
    
    if not risk_factors:
        return 0.0, RiskLevel.LOW
    
    # Weighted risk calculation
    total_weighted_risk = 0
    total_weight = 0
    
    for factor in risk_factors:
        # Weight = probability * impact
        weight = factor.probability * factor.impact
        total_weighted_risk += weight
        total_weight += factor.impact  # Normalize by max possible impact
    
    if total_weight == 0:
        overall_score = 0
    else:
        overall_score = total_weighted_risk / total_weight * 10  # Scale to 0-10
    
    # Determine overall risk level
    if overall_score >= 7.5:
        overall_level = RiskLevel.CRITICAL
    elif overall_score >= 6:
        overall_level = RiskLevel.HIGH
    elif overall_score >= 3:
        overall_level = RiskLevel.MEDIUM
    else:
        overall_level = RiskLevel.LOW
    
    return overall_score, overall_level


def generate_risk_recommendations(assessment: ProjectRiskAssessment) -> List[str]:
    """Generate high-level risk management recommendations."""
    
    recommendations = []
    
    # Overall risk level recommendations
    if assessment.overall_risk_score >= 7:
        recommendations.extend([
            "Consider comprehensive project insurance coverage",
            "Implement rigorous risk monitoring and reporting",
            "Establish contingency funds of 20-30% above baseline estimates",
            "Consider bringing in specialized risk management consultants"
        ])
    elif assessment.overall_risk_score >= 5:
        recommendations.extend([
            "Implement regular risk review meetings",
            "Establish contingency funds of 15-20% above baseline estimates",
            "Consider selective insurance coverage for high-risk areas"
        ])
    else:
        recommendations.extend([
            "Maintain standard project controls and monitoring",
            "Establish contingency funds of 10-15% above baseline estimates"
        ])
    
    # Specific risk area recommendations
    if assessment.timeline_risk >= 6:
        recommendations.append("Implement accelerated construction methods to mitigate schedule risks")
    
    if assessment.budget_risk >= 6:
        recommendations.append("Consider cost-plus contracts for uncertain work elements")
    
    if assessment.safety_risk >= 6:
        recommendations.append("Implement enhanced safety programs and training")
    
    return recommendations


def assess_project_risks(
    project_type: str,
    total_area: float,
    location: str,
    materials: List[str] = None,
    project_start_month: int = None
) -> ProjectRiskAssessment:
    """Comprehensive project risk assessment."""
    
    if materials is None:
        materials = ['steel', 'concrete', 'lumber']
    
    if project_start_month is None:
        project_start_month = datetime.datetime.now().month
    
    # Assess individual risk factors
    risk_factors = [
        assess_weather_risk(location, project_start_month),
        assess_seismic_risk(location),
        assess_regulatory_risk(project_type, location, total_area),
        assess_labor_risk(location, project_type, total_area),
        assess_material_risk(project_type, materials)
    ]
    
    # Calculate overall risk
    overall_score, overall_level = calculate_overall_risk_score(risk_factors)
    
    # Calculate category-specific risks
    timeline_risk = np.mean([f.impact for f in risk_factors if f.name in ['Weather Risk', 'Regulatory Risk', 'Labor Risk']])
    budget_risk = np.mean([f.impact for f in risk_factors if f.name in ['Material Risk', 'Labor Risk']])
    safety_risk = np.mean([f.impact for f in risk_factors if f.name in ['Weather Risk', 'Seismic Risk']])
    environmental_risk = np.mean([f.impact for f in risk_factors if f.name in ['Weather Risk', 'Seismic Risk']])
    regulatory_risk = next((f.impact for f in risk_factors if f.name == 'Regulatory Risk'), 0)
    
    # Create assessment
    assessment = ProjectRiskAssessment(
        overall_risk_score=overall_score,
        risk_level=overall_level,
        risk_factors=risk_factors,
        timeline_risk=timeline_risk,
        budget_risk=budget_risk,
        safety_risk=safety_risk,
        environmental_risk=environmental_risk,
        regulatory_risk=regulatory_risk,
        recommendations=[]
    )
    
    # Generate recommendations
    assessment.recommendations = generate_risk_recommendations(assessment)
    
    return assessment
