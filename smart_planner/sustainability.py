"""Sustainability scoring and environmental impact assessment for construction projects."""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class SustainabilityMetrics:
    """Container for sustainability assessment results."""
    overall_score: float
    carbon_footprint: float
    energy_efficiency: float
    water_usage: float
    waste_reduction: float
    green_materials: float
    leed_potential: str
    recommendations: List[str]


def calculate_carbon_footprint(
    project_type: str,
    total_area: float,
    materials: Dict[str, float],
    location: str
) -> float:
    """Calculate estimated carbon footprint based on project parameters."""
    
    # Base carbon intensity (kg CO2e/m²) by project type
    base_intensity = {
        'Residential': 400,
        'Commercial': 350,
        'Industrial': 500,
        'Institutional': 300
    }
    
    # Location multipliers for local energy grid carbon intensity
    location_multipliers = {
        'New York': 0.9,
        'San Francisco': 0.7,  # Cleaner grid
        'Los Angeles': 0.85,
        'Chicago': 1.0,
        'Miami': 1.1,
        'Dallas': 1.2,
        'Houston': 1.3,  # Heavy fossil fuel reliance
        'Atlanta': 1.15
    }
    
    base_footprint = total_area * base_intensity.get(project_type, 400)
    location_factor = location_multipliers.get(location, 1.0)
    
    # Material impact factors
    material_factors = {
        'steel': 1.8,
        'concrete': 0.15,
        'wood': -0.5,  # Carbon sequestration
        'aluminum': 2.5,
        'glass': 0.8,
        'insulation': -0.3  # Energy savings
    }
    
    material_impact = 0
    for material, quantity in materials.items():
        factor = material_factors.get(material.lower(), 1.0)
        material_impact += quantity * factor
    
    return base_footprint * location_factor + material_impact


def assess_energy_efficiency(
    building_design: Dict[str, any],
    location: str,
    project_type: str
) -> float:
    """Assess energy efficiency potential (0-100 scale)."""
    
    base_score = 50  # Baseline
    
    # Climate zone adjustments
    climate_zones = {
        'New York': 'cold',
        'San Francisco': 'mild',
        'Los Angeles': 'warm',
        'Chicago': 'cold',
        'Miami': 'hot',
        'Dallas': 'hot',
        'Houston': 'hot',
        'Atlanta': 'warm'
    }
    
    climate = climate_zones.get(location, 'mild')
    
    # Building design features impact
    if building_design.get('solar_panels', False):
        base_score += 15
    if building_design.get('green_roof', False):
        base_score += 10
    if building_design.get('high_performance_windows', False):
        base_score += 8
    if building_design.get('led_lighting', True):
        base_score += 5
    if building_design.get('smart_hvac', False):
        base_score += 12
    if building_design.get('insulation_rating', 'standard') == 'high':
        base_score += 10
    
    # Climate-specific adjustments
    if climate == 'hot' and building_design.get('cooling_efficiency', 'standard') == 'high':
        base_score += 8
    elif climate == 'cold' and building_design.get('heating_efficiency', 'standard') == 'high':
        base_score += 8
    
    # Project type considerations
    type_multipliers = {
        'Institutional': 1.1,  # Often have higher efficiency standards
        'Commercial': 1.0,
        'Residential': 0.95,
        'Industrial': 0.9
    }
    
    final_score = base_score * type_multipliers.get(project_type, 1.0)
    return min(100, max(0, final_score))


def calculate_water_usage_score(
    project_type: str,
    total_area: float,
    water_features: Dict[str, any],
    location: str
) -> float:
    """Calculate water usage efficiency score (0-100)."""
    
    # Base water consumption (liters/m²/year) by project type
    base_consumption = {
        'Residential': 1000,
        'Commercial': 800,
        'Industrial': 2000,
        'Institutional': 600
    }
    
    # Water scarcity by location (higher = more scarce)
    water_scarcity = {
        'New York': 0.3,
        'San Francisco': 0.8,
        'Los Angeles': 0.9,
        'Chicago': 0.2,
        'Miami': 0.4,
        'Dallas': 0.7,
        'Houston': 0.6,
        'Atlanta': 0.5
    }
    
    base_usage = total_area * base_consumption.get(project_type, 1000)
    scarcity_factor = water_scarcity.get(location, 0.5)
    
    # Water-saving features
    savings = 0
    if water_features.get('rainwater_harvesting', False):
        savings += 20
    if water_features.get('greywater_recycling', False):
        savings += 15
    if water_features.get('low_flow_fixtures', True):
        savings += 10
    if water_features.get('drought_resistant_landscaping', False):
        savings += 12
    if water_features.get('permeable_surfaces', False):
        savings += 8
    
    # Score calculation (inverted - lower usage = higher score)
    efficiency_score = 100 - (base_usage * (1 - savings/100) * scarcity_factor * 0.001)
    return max(0, min(100, efficiency_score))


def evaluate_green_materials(materials_list: List[str]) -> Tuple[float, List[str]]:
    """Evaluate the sustainability of construction materials."""
    
    green_materials = {
        'bamboo': 10,
        'recycled_steel': 9,
        'cork': 8,
        'hemp_insulation': 9,
        'reclaimed_wood': 8,
        'recycled_concrete': 7,
        'low_voc_paint': 6,
        'sustainable_timber': 8,
        'recycled_plastic': 7,
        'bio_insulation': 9
    }
    
    standard_materials = {
        'steel': 3,
        'concrete': 2,
        'aluminum': 4,
        'vinyl': 2,
        'traditional_wood': 5,
        'fiberglass': 3,
        'asphalt': 1
    }
    
    total_score = 0
    material_count = len(materials_list)
    recommendations = []
    
    for material in materials_list:
        material_clean = material.lower().replace(' ', '_')
        
        if material_clean in green_materials:
            total_score += green_materials[material_clean]
        elif material_clean in standard_materials:
            total_score += standard_materials[material_clean]
            # Suggest green alternatives
            if material_clean == 'steel':
                recommendations.append("Consider recycled steel instead of virgin steel")
            elif material_clean == 'concrete':
                recommendations.append("Consider recycled concrete or alternative materials like hemp-crete")
            elif material_clean == 'traditional_wood':
                recommendations.append("Consider certified sustainable timber or reclaimed wood")
        else:
            total_score += 5  # Neutral score for unknown materials
    
    if material_count == 0:
        return 50, ["No materials specified for evaluation"]
    
    average_score = (total_score / material_count) * 10  # Scale to 0-100
    
    if not recommendations:
        recommendations.append("Great material choices for sustainability!")
    
    return min(100, average_score), recommendations


def predict_leed_potential(sustainability_metrics: Dict[str, float]) -> str:
    """Predict potential LEED certification level."""
    
    # LEED scoring thresholds (simplified)
    total_score = (
        sustainability_metrics.get('energy_efficiency', 0) * 0.3 +
        sustainability_metrics.get('water_usage', 0) * 0.2 +
        sustainability_metrics.get('green_materials', 0) * 0.2 +
        sustainability_metrics.get('waste_reduction', 0) * 0.15 +
        (100 - min(100, sustainability_metrics.get('carbon_footprint', 50000) / 500)) * 0.15
    )
    
    if total_score >= 80:
        return "Platinum"
    elif total_score >= 70:
        return "Gold"
    elif total_score >= 60:
        return "Silver"
    elif total_score >= 50:
        return "Certified"
    else:
        return "Below Certification"


def generate_sustainability_recommendations(metrics: SustainabilityMetrics) -> List[str]:
    """Generate specific recommendations based on sustainability assessment."""
    
    recommendations = []
    
    if metrics.energy_efficiency < 70:
        recommendations.extend([
            "Consider adding solar panels to reduce energy consumption",
            "Implement smart HVAC systems for better energy management",
            "Use high-performance windows to improve insulation"
        ])
    
    if metrics.water_usage < 60:
        recommendations.extend([
            "Install rainwater harvesting system",
            "Implement greywater recycling for irrigation",
            "Use drought-resistant landscaping"
        ])
    
    if metrics.green_materials < 70:
        recommendations.extend([
            "Increase use of recycled and sustainable materials",
            "Consider bamboo or cork for flooring alternatives",
            "Use low-VOC paints and finishes"
        ])
    
    if metrics.carbon_footprint > 100000:  # High footprint
        recommendations.extend([
            "Optimize building design for reduced material usage",
            "Consider prefabricated construction methods",
            "Plan for carbon offset programs"
        ])
    
    return recommendations


def assess_project_sustainability(
    project_type: str,
    total_area: float,
    location: str,
    materials: List[str],
    building_design: Dict[str, any] = None,
    water_features: Dict[str, any] = None
) -> SustainabilityMetrics:
    """Comprehensive sustainability assessment for a construction project."""
    
    if building_design is None:
        building_design = {}
    if water_features is None:
        water_features = {}
    
    # Convert materials list to dict for carbon footprint calculation
    materials_dict = {material: total_area * 0.1 for material in materials}  # Simplified estimation
    
    # Calculate individual metrics
    carbon_footprint = calculate_carbon_footprint(project_type, total_area, materials_dict, location)
    energy_efficiency = assess_energy_efficiency(building_design, location, project_type)
    water_usage = calculate_water_usage_score(project_type, total_area, water_features, location)
    green_materials_score, material_recommendations = evaluate_green_materials(materials)
    
    # Waste reduction score (simplified - based on material choices and design)
    waste_reduction = 70  # Base score
    if building_design.get('modular_design', False):
        waste_reduction += 15
    if 'recycled' in ' '.join(materials).lower():
        waste_reduction += 10
    waste_reduction = min(100, waste_reduction)
    
    # Overall score calculation
    overall_score = (
        energy_efficiency * 0.25 +
        water_usage * 0.2 +
        green_materials_score * 0.2 +
        waste_reduction * 0.15 +
        max(0, 100 - carbon_footprint/1000) * 0.2  # Carbon footprint contribution (inverted)
    )
    
    # LEED potential assessment
    sustainability_dict = {
        'energy_efficiency': energy_efficiency,
        'water_usage': water_usage,
        'green_materials': green_materials_score,
        'waste_reduction': waste_reduction,
        'carbon_footprint': carbon_footprint
    }
    leed_potential = predict_leed_potential(sustainability_dict)
    
    # Generate comprehensive recommendations
    metrics = SustainabilityMetrics(
        overall_score=overall_score,
        carbon_footprint=carbon_footprint,
        energy_efficiency=energy_efficiency,
        water_usage=water_usage,
        waste_reduction=waste_reduction,
        green_materials=green_materials_score,
        leed_potential=leed_potential,
        recommendations=material_recommendations
    )
    
    additional_recommendations = generate_sustainability_recommendations(metrics)
    metrics.recommendations.extend(additional_recommendations)
    
    return metrics
