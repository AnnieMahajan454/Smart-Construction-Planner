#!/usr/bin/env python3
"""
Demo script showing the new pedestrian features of the Smart Construction Planner
"""

from pedestrian_paths import PedestrianPathsManager
import pandas as pd

def demo_pedestrian_features():
    """Demonstrate the pedestrian features"""
    print("🚶‍♀️ Smart Construction & Pedestrian Planner - Demo")
    print("=" * 60)
    
    # Initialize the pedestrian manager
    pedestrian_manager = PedestrianPathsManager()
    
    # Demo for Mumbai
    city = "Mumbai"
    print(f"\n📍 Demonstrating features for {city}")
    print("-" * 40)
    
    # 1. Get pedestrian impact summary
    print("\n1. 📊 Pedestrian Impact Summary:")
    impact = pedestrian_manager.get_pedestrian_impact_summary(city)
    for key, value in impact.items():
        print(f"   {key.replace('_', ' ').title()}: {value}")
    
    # 2. Show blocked paths
    print(f"\n2. 🚫 Blocked Paths in {city}:")
    blocked_paths = pedestrian_manager.get_blocked_paths_for_city(city)
    for i, path in enumerate(blocked_paths[:3], 1):  # Show first 3
        print(f"   {i}. {path['name']}")
        print(f"      Area: {path['area']}")
        print(f"      Reason: {path['block_reason']}")
        print(f"      Severity: {path['severity']}")
        print(f"      Impact: {path['pedestrian_impact']}")
        print(f"      Expected End: {path['expected_end'].strftime('%Y-%m-%d')}")
        print(f"      Estimated Delay: {path['estimated_delay']} minutes")
        print()
    
    # 3. Show construction sites
    print(f"\n3. 🏗️ Construction Sites affecting pedestrians in {city}:")
    sites = pedestrian_manager.get_construction_sites_for_city(city)
    for i, site in enumerate(sites[:3], 1):  # Show first 3
        print(f"   {i}. {site['name']}")
        print(f"      Area: {site['area']}")
        print(f"      Project Type: {site['project_type']}")
        print(f"      Safety Level: {site['pedestrian_safety_level']}")
        print(f"      Walkway Impact: {site['walkway_closure']}")
        print(f"      Expected Completion: {site['expected_completion'].strftime('%Y-%m-%d')}")
        print(f"      Working Hours: {site['working_hours']}")
        print()
    
    # 4. Show safety alerts
    print(f"\n4. ⚠️ Current Safety Alerts for {city}:")
    alerts = pedestrian_manager.get_safety_alerts(city)
    for i, alert in enumerate(alerts[:5], 1):  # Show first 5
        print(f"   {i}. {alert['type']} - {alert['priority']} Priority")
        print(f"      Area: {alert['area']}")
        print(f"      Message: {alert['message']}")
        print(f"      Duration: {alert['expected_duration']} more days")
        print()
    
    # 5. Show alternative routes for a blocked path
    if blocked_paths:
        example_path = blocked_paths[0]
        print(f"\n5. 🛐️ Alternative Routes for '{example_path['name']}':")
        alternatives = pedestrian_manager.find_alternative_routes(city, example_path['id'])
        
        for i, alt in enumerate(alternatives, 1):
            print(f"   Route {i}: {alt['name']}")
            print(f"      Description: {alt['description']}")
            print(f"      Additional Distance: {alt['additional_distance']}m")
            print(f"      Additional Time: {alt['additional_time']} minutes")
            print(f"      Difficulty: {alt['difficulty']}")
            print(f"      Safety Rating: {alt['safety_rating']}")
            print()
    
    # 6. Area-wise impact
    print(f"\n6. 🏠 Area-wise Impact in {city}:")
    area_impact = pedestrian_manager.get_area_wise_impact(city)
    
    area_df = pd.DataFrame([
        {
            'Area': area,
            'Blocked Paths': data['blocked_paths'],
            'Construction Sites': data['construction_sites'],
            'High Impact Blocks': data['high_impact_blocks'],
            'Dangerous Sites': data['dangerous_sites'],
            'Total Delay (min)': data['total_delay_minutes']
        }
        for area, data in area_impact.items()
    ])
    
    if not area_df.empty:
        print(area_df.to_string(index=False))
    else:
        print("   No area impact data available")
    
    print(f"\n✅ Demo completed for {city}!")
    print("\n💡 To view more cities and features, run the Streamlit app:")
    print("   streamlit run ai_planner_light.py")

if __name__ == "__main__":
    demo_pedestrian_features()