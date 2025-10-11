import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random
import folium
from typing import Dict, List, Tuple, Optional

class PedestrianPathsManager:
    """Manager class for pedestrian paths, blocked routes, and construction impact on walkways"""
    
    def __init__(self):
        self.cities = {
            'Mumbai': {
                'lat': 19.0760, 'lon': 72.8777, 'zoom': 11,
                'major_areas': ['Bandra', 'Andheri', 'Colaba', 'Worli', 'Powai', 'Juhu']
            },
            'Delhi': {
                'lat': 28.7041, 'lon': 77.1025, 'zoom': 11,
                'major_areas': ['CP', 'Karol Bagh', 'Lajpat Nagar', 'Dwarka', 'Rohini', 'Gurgaon']
            },
            'Bangalore': {
                'lat': 12.9716, 'lon': 77.5946, 'zoom': 11,
                'major_areas': ['Koramangala', 'Indiranagar', 'Whitefield', 'Electronic City', 'Marathahalli', 'HSR Layout']
            },
            'Chennai': {
                'lat': 13.0827, 'lon': 80.2707, 'zoom': 11,
                'major_areas': ['T Nagar', 'Anna Nagar', 'OMR', 'Velachery', 'Adyar', 'Mylapore']
            },
            'Hyderabad': {
                'lat': 17.3850, 'lon': 78.4867, 'zoom': 11,
                'major_areas': ['Banjara Hills', 'Jubilee Hills', 'Gachibowli', 'Kondapur', 'Secunderabad', 'Begumpet']
            },
            'Kolkata': {
                'lat': 22.5726, 'lon': 88.3639, 'zoom': 11,
                'major_areas': ['Park Street', 'Salt Lake', 'Howrah', 'Ballygunge', 'Gariahat', 'Esplanade']
            },
            'Pune': {
                'lat': 18.5204, 'lon': 73.8567, 'zoom': 11,
                'major_areas': ['Koregaon Park', 'Viman Nagar', 'Hinjewadi', 'Kothrud', 'Aundh', 'Camp']
            },
            'Ahmedabad': {
                'lat': 23.0225, 'lon': 72.5714, 'zoom': 11,
                'major_areas': ['Navrangpura', 'CG Road', 'SG Highway', 'Vastrapur', 'Bopal', 'Satellite']
            }
        }
        
        # Generate sample blocked paths and construction sites
        self.blocked_paths = self._generate_blocked_paths()
        self.construction_sites = self._generate_construction_sites()
    
    def _generate_blocked_paths(self) -> Dict:
        """Generate sample blocked paths for each city"""
        blocked_paths = {}
        
        for city, city_data in self.cities.items():
            city_blocked = []
            base_lat, base_lon = city_data['lat'], city_data['lon']
            
            # Generate 5-10 blocked paths per city
            num_paths = random.randint(5, 10)
            for i in range(num_paths):
                # Generate coordinates within city bounds
                lat_offset = random.uniform(-0.1, 0.1)
                lon_offset = random.uniform(-0.1, 0.1)
                
                start_lat = base_lat + lat_offset
                start_lon = base_lon + lon_offset
                end_lat = base_lat + lat_offset + random.uniform(-0.02, 0.02)
                end_lon = base_lon + lon_offset + random.uniform(-0.02, 0.02)
                
                # Random area from major areas
                area = random.choice(city_data['major_areas'])
                
                # Generate path data
                path = {
                    'id': f"{city}_{i+1}",
                    'name': f"{area} - Main Walkway {i+1}",
                    'area': area,
                    'start_coords': [start_lat, start_lon],
                    'end_coords': [end_lat, end_lon],
                    'block_reason': random.choice([
                        'Road Construction', 'Building Construction', 'Metro Work', 
                        'Utility Repair', 'Bridge Work', 'Sewage Work'
                    ]),
                    'severity': random.choice(['High', 'Medium', 'Low']),
                    'start_date': datetime.now() - timedelta(days=random.randint(1, 30)),
                    'expected_end': datetime.now() + timedelta(days=random.randint(10, 120)),
                    'alternative_available': random.choice([True, False]),
                    'pedestrian_impact': random.choice(['Complete Block', 'Partial Block', 'Detour Available']),
                    'estimated_delay': random.randint(5, 30)  # minutes
                }
                city_blocked.append(path)
            
            blocked_paths[city] = city_blocked
        
        return blocked_paths
    
    def _generate_construction_sites(self) -> Dict:
        """Generate construction sites that affect pedestrian movement"""
        construction_sites = {}
        
        for city, city_data in self.cities.items():
            city_sites = []
            base_lat, base_lon = city_data['lat'], city_data['lon']
            
            # Generate 3-7 construction sites per city
            num_sites = random.randint(3, 7)
            for i in range(num_sites):
                lat_offset = random.uniform(-0.08, 0.08)
                lon_offset = random.uniform(-0.08, 0.08)
                
                site_lat = base_lat + lat_offset
                site_lon = base_lon + lon_offset
                
                area = random.choice(city_data['major_areas'])
                
                site = {
                    'id': f"site_{city}_{i+1}",
                    'name': f"{area} Construction Project {i+1}",
                    'area': area,
                    'coords': [site_lat, site_lon],
                    'project_type': random.choice([
                        'Residential Building', 'Commercial Complex', 'Road Construction',
                        'Bridge Construction', 'Metro/Railway', 'Industrial Complex'
                    ]),
                    'size': random.choice(['Small', 'Medium', 'Large', 'Mega']),
                    'pedestrian_safety_level': random.choice(['Safe', 'Caution', 'Dangerous']),
                    'walkway_closure': random.choice([
                        'No Impact', 'Temporary Closure', 'Permanent Reroute'
                    ]),
                    'start_date': datetime.now() - timedelta(days=random.randint(1, 90)),
                    'expected_completion': datetime.now() + timedelta(days=random.randint(30, 365)),
                    'working_hours': '7 AM - 7 PM',
                    'safety_measures': random.choice([
                        'Protective Barriers', 'Safety Personnel', 'Warning Signs Only', 'Full Enclosure'
                    ])
                }
                city_sites.append(site)
            
            construction_sites[city] = city_sites
        
        return construction_sites
    
    def get_blocked_paths_for_city(self, city: str) -> List[Dict]:
        """Get all blocked paths for a specific city"""
        return self.blocked_paths.get(city, [])
    
    def get_construction_sites_for_city(self, city: str) -> List[Dict]:
        """Get all construction sites for a specific city"""
        return self.construction_sites.get(city, [])
    
    def get_pedestrian_impact_summary(self, city: str) -> Dict:
        """Get summary of pedestrian impact in the city"""
        blocked = self.get_blocked_paths_for_city(city)
        sites = self.get_construction_sites_for_city(city)
        
        # Calculate statistics
        total_blocked = len(blocked)
        high_impact = len([p for p in blocked if p['severity'] == 'High'])
        complete_blocks = len([p for p in blocked if p['pedestrian_impact'] == 'Complete Block'])
        
        dangerous_sites = len([s for s in sites if s['pedestrian_safety_level'] == 'Dangerous'])
        total_sites = len(sites)
        
        avg_delay = np.mean([p['estimated_delay'] for p in blocked]) if blocked else 0
        
        return {
            'total_blocked_paths': total_blocked,
            'high_impact_paths': high_impact,
            'complete_blocks': complete_blocks,
            'dangerous_construction_sites': dangerous_sites,
            'total_construction_sites': total_sites,
            'average_delay_minutes': round(avg_delay, 1),
            'areas_affected': len(set([p['area'] for p in blocked + sites]))
        }
    
    def find_alternative_routes(self, city: str, blocked_path_id: str) -> List[Dict]:
        """Find alternative routes for a blocked path"""
        alternatives = []
        
        # Simple algorithm to generate alternative routes
        for i in range(random.randint(1, 3)):
            alternative = {
                'route_id': f"alt_{blocked_path_id}_{i+1}",
                'name': f"Alternative Route {i+1}",
                'additional_distance': random.randint(100, 800),  # meters
                'additional_time': random.randint(2, 15),  # minutes
                'difficulty': random.choice(['Easy', 'Moderate', 'Difficult']),
                'safety_rating': random.choice(['Safe', 'Moderately Safe', 'Exercise Caution']),
                'description': random.choice([
                    "Via main road with designated walkway",
                    "Through nearby park path",
                    "Using underpass/overpass",
                    "Via secondary streets with sidewalks",
                    "Through shopping complex corridor"
                ])
            }
            alternatives.append(alternative)
        
        return alternatives
    
    def get_safety_alerts(self, city: str) -> List[Dict]:
        """Get current safety alerts for pedestrians"""
        blocked = self.get_blocked_paths_for_city(city)
        sites = self.get_construction_sites_for_city(city)
        
        alerts = []
        
        # High priority blocked paths
        for path in blocked:
            if path['severity'] == 'High' or path['pedestrian_impact'] == 'Complete Block':
                alert = {
                    'type': 'Path Blocked',
                    'priority': 'High' if path['severity'] == 'High' else 'Medium',
                    'area': path['area'],
                    'message': f"{path['name']} is {path['pedestrian_impact'].lower()}",
                    'expected_duration': (path['expected_end'] - datetime.now()).days,
                    'alternative_available': path['alternative_available']
                }
                alerts.append(alert)
        
        # Dangerous construction sites
        for site in sites:
            if site['pedestrian_safety_level'] == 'Dangerous':
                alert = {
                    'type': 'Construction Hazard',
                    'priority': 'High',
                    'area': site['area'],
                    'message': f"Exercise extreme caution near {site['name']}",
                    'expected_duration': (site['expected_completion'] - datetime.now()).days,
                    'safety_measures': site['safety_measures']
                }
                alerts.append(alert)
        
        # Sort by priority
        priority_order = {'High': 0, 'Medium': 1, 'Low': 2}
        alerts.sort(key=lambda x: priority_order.get(x['priority'], 3))
        
        return alerts[:10]  # Return top 10 alerts
    
    def create_pedestrian_map(self, city: str) -> folium.Map:
        """Create an interactive map showing blocked paths and construction sites"""
        if city not in self.cities:
            return None
        
        try:
            city_data = self.cities[city]
            
            # Create base map with better styling
            m = folium.Map(
                location=[city_data['lat'], city_data['lon']],
                zoom_start=city_data['zoom'],
                tiles='OpenStreetMap',
                width='100%',
                height='500px'
            )
            
            # Add blocked paths
            blocked_paths = self.get_blocked_paths_for_city(city)
            for path in blocked_paths:
                # Color based on severity
                color = {
                    'High': 'red',
                    'Medium': 'orange', 
                    'Low': 'yellow'
                }.get(path['severity'], 'gray')
                
                # Add path line
                folium.PolyLine(
                    locations=[path['start_coords'], path['end_coords']],
                    color=color,
                    weight=8,
                    opacity=0.8,
                    popup=folium.Popup(
                        f"""<b>{path['name']}</b><br>
                        Reason: {path['block_reason']}<br>
                        Impact: {path['pedestrian_impact']}<br>
                        Severity: {path['severity']}<br>
                        Expected End: {path['expected_end'].strftime('%Y-%m-%d')}<br>
                        Est. Delay: {path['estimated_delay']} min""",
                        max_width=300
                    )
                ).add_to(m)
                
                # Add start marker
                folium.Marker(
                    path['start_coords'],
                    popup=f"BLOCKED: {path['name']}",
                    icon=folium.Icon(color='red', icon='exclamation-sign')
                ).add_to(m)
            
            # Add construction sites
            construction_sites = self.get_construction_sites_for_city(city)
            for site in construction_sites:
                # Color based on safety level
                icon_color = {
                    'Safe': 'green',
                    'Caution': 'orange',
                    'Dangerous': 'red'
                }.get(site['pedestrian_safety_level'], 'blue')
                
                folium.Marker(
                    site['coords'],
                    popup=folium.Popup(
                        f"""<b>Construction: {site['name']}</b><br>
                        Type: {site['project_type']}<br>
                        Safety Level: {site['pedestrian_safety_level']}<br>
                        Walkway Status: {site['walkway_closure']}<br>
                        Expected Completion: {site['expected_completion'].strftime('%Y-%m-%d')}<br>
                        Safety Measures: {site['safety_measures']}""",
                        max_width=300
                    ),
                    icon=folium.Icon(color=icon_color, icon='cog')
                ).add_to(m)
        
            # Add a cleaner legend
            legend_html = '''
            <div style="position: fixed; 
                        bottom: 50px; left: 50px; width: 250px; height: 160px; 
                        background-color: white; border:1px solid #ccc; z-index:9999; 
                        font-size:12px; padding: 15px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.2);">
            <b style="font-size: 14px;">Map Legend</b><br><br>
            <div style="margin-bottom: 5px;"><span style="color:red; font-size: 16px;">●</span> High Impact Block</div>
            <div style="margin-bottom: 5px;"><span style="color:orange; font-size: 16px;">●</span> Medium Impact Block</div>
            <div style="margin-bottom: 5px;"><span style="color:gold; font-size: 16px;">●</span> Low Impact Block</div>
            <div style="margin-bottom: 5px;"><span style="color:red; font-size: 14px;">🏗️</span> Dangerous Site</div>
            <div style="margin-bottom: 5px;"><span style="color:orange; font-size: 14px;">🏗️</span> Caution Required</div>
            <div><span style="color:green; font-size: 14px;">🏗️</span> Safe Construction</div>
            </div>
            '''
            m.get_root().html.add_child(folium.Element(legend_html))
            
            return m
        except Exception as e:
            # Return a basic map if there are issues
            return folium.Map(
                location=[20.5937, 78.9629],
                zoom_start=5,
                width='100%',
                height='500px'
            )
    
    def get_area_wise_impact(self, city: str) -> Dict:
        """Get pedestrian impact statistics by area"""
        blocked = self.get_blocked_paths_for_city(city)
        sites = self.get_construction_sites_for_city(city)
        
        area_impact = {}
        
        # Process blocked paths
        for path in blocked:
            area = path['area']
            if area not in area_impact:
                area_impact[area] = {
                    'blocked_paths': 0,
                    'construction_sites': 0,
                    'high_impact_blocks': 0,
                    'dangerous_sites': 0,
                    'total_delay_minutes': 0
                }
            
            area_impact[area]['blocked_paths'] += 1
            area_impact[area]['total_delay_minutes'] += path['estimated_delay']
            
            if path['severity'] == 'High':
                area_impact[area]['high_impact_blocks'] += 1
        
        # Process construction sites
        for site in sites:
            area = site['area']
            if area not in area_impact:
                area_impact[area] = {
                    'blocked_paths': 0,
                    'construction_sites': 0,
                    'high_impact_blocks': 0,
                    'dangerous_sites': 0,
                    'total_delay_minutes': 0
                }
            
            area_impact[area]['construction_sites'] += 1
            
            if site['pedestrian_safety_level'] == 'Dangerous':
                area_impact[area]['dangerous_sites'] += 1
        
        return area_impact