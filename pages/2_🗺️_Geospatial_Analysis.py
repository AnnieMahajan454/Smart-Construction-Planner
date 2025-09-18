import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import os

st.title("🗺️ Geospatial Analysis")

st.markdown("""
This page provides geospatial analysis capabilities including network analysis,
accessibility mapping, and isochrone calculations for construction planning.
""")

# Check if geospatial packages are available
try:
    import geopandas as gpd
    import networkx as nx
    import osmnx as ox
    from shapely.geometry import Point, LineString
    import h3
    geospatial_available = True
except ImportError:
    geospatial_available = False
    st.warning("⚠️ Geospatial packages not available. Install geopandas, osmnx, and h3 for full functionality.")

if geospatial_available:
    st.success("✅ Geospatial packages loaded successfully!")

    # Place selection
    st.header("📍 Location Selection")
    place = st.text_input(
        "Enter a place name (e.g., 'Mumbai, India', 'Bangalore, India')",
        value="Mumbai, India")

    if st.button("Load Location Data"):
        try:
            with st.spinner("Loading geospatial data..."):
                # Load base layers
                buildings, walk_graph = ox.geometries_from_place(place, tags={"building": True}), ox.graph_from_place(place, network_type="walk")

                st.session_state['buildings'] = buildings
                st.session_state['walk_graph'] = walk_graph
                st.session_state['place'] = place

                st.success(f"✅ Loaded data for {place}")

                # Display basic stats
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Buildings", len(buildings))
                with col2:
                    st.metric("Network Nodes", walk_graph.number_of_nodes())
                with col3:
                    st.metric("Network Edges", walk_graph.number_of_edges())

        except Exception as e:
            st.error(f"Error loading location data: {str(e)}")

    # Network Analysis
    if 'walk_graph' in st.session_state:
        st.header("🕸️ Network Analysis")

        walk_graph = st.session_state['walk_graph']

        # Get some sample nodes for analysis
        nodes, edges = ox.graph_to_gdfs(walk_graph)
        sample_nodes = nodes.sample(min(5, len(nodes)))

        st.subheader("Sample Network Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Network Statistics:**")
            st.write(f"- Total nodes: {walk_graph.number_of_nodes()}")
            st.write(f"- Total edges: {walk_graph.number_of_edges()}")
            st.write(f"- Average degree: {np.mean([d for n, d in walk_graph.degree()]):.2f}")

        with col2:
            st.write("**Sample Nodes:**")
            for idx, (node_id, node) in enumerate(sample_nodes.iterrows()):
                st.write(f"Node {node_id}: ({node.geometry.y:.4f}, {node.geometry.x:.4f})")

        # Isochrone Analysis
        st.subheader("⏱️ Isochrone Analysis")

        if len(sample_nodes) > 0:
            center_node = st.selectbox(
                "Select center node for isochrone",
                options=sample_nodes.index.tolist(),
                format_func=lambda x: f"Node {x}")

            speed_m_s = st.slider("Walking speed (m/s)", 0.5, 2.0, 1.4)
            minutes = st.slider("Time budget (minutes)", 5, 60, 15)

            if st.button("Calculate Isochrone"):
                try:
                    # Calculate isochrone
                    meters = speed_m_s * 60 * minutes
                    subgraph = nx.ego_graph(walk_graph, center_node, radius=meters, distance="length")
                    sub_nodes, sub_edges = ox.graph_to_gdfs(subgraph)
                    isochrone_geom = sub_edges.buffer(15).unary_union

                    st.success(f"✅ Isochrone calculated for {minutes} minutes at {speed_m_s} m/s")

                except Exception as e:
                    st.error(f"Error calculating isochrone: {str(e)}")

    # H3 Hexagon Analysis
    st.header("🔷 H3 Hexagon Analysis")

    st.markdown("""
    H3 is a hexagonal hierarchical geospatial indexing system.
    It's useful for aggregating point data into regular hexagonal grids.
    """)

    # Sample points for H3 analysis
    if st.button("Generate Sample Points"):
        # Create some sample points around Mumbai
        np.random.seed(42)
        n_points = 50
        lats = np.random.normal(19.0760, 0.1, n_points)  # Mumbai coordinates
        lons = np.random.normal(72.8777, 0.1, n_points)
        counts = np.random.poisson(10, n_points)

        sample_points = pd.DataFrame({
            'lat': lats,
            'lon': lons,
            'count': counts
        })

        st.session_state['sample_points'] = sample_points
        st.success(f"✅ Generated {n_points} sample points")

    if 'sample_points' in st.session_state:
        sample_points = st.session_state['sample_points']

        resolution = st.slider("H3 Resolution", 6, 12, 8)

        if st.button("Aggregate to H3 Hexagons"):
            try:
                # Convert to H3 hexagons
                def to_h3(row):
                    return h3.geo_to_h3(row['lat'], row['lon'], resolution)

                sample_points['h3'] = sample_points.apply(to_h3, axis=1)
                hex_aggregated = sample_points.groupby('h3').agg({'count': 'sum'}).reset_index()

                st.write(f"**Aggregated {len(sample_points)} points into {len(hex_aggregated)} hexagons**")

                # Display aggregated data
                st.dataframe(hex_aggregated.head(10))

                # Create visualization
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

                # Original points
                scatter = ax1.scatter(
                    sample_points['lon'], sample_points['lat'],
                    c=sample_points['count'], cmap='viridis', s=50)
                ax1.set_title('Original Points')
                ax1.set_xlabel('Longitude')
                ax1.set_ylabel('Latitude')
                plt.colorbar(scatter, ax=ax1)

                # Hexagon centers (simplified visualization)
                hex_lats = [h3.h3_to_geo(h)[0] for h in hex_aggregated['h3']]
                hex_lons = [h3.h3_to_geo(h)[1] for h in hex_aggregated['h3']]

                scatter2 = ax2.scatter(
                    hex_lons, hex_lats,
                    c=hex_aggregated['count'], cmap='viridis', s=100)
                ax2.set_title('H3 Hexagon Aggregation')
                ax2.set_xlabel('Longitude')
                ax2.set_ylabel('Latitude')
                plt.colorbar(scatter2, ax=ax2)

                st.pyplot(fig)

            except Exception as e:
                st.error(f"Error in H3 analysis: {str(e)}")

else:
    st.info("""
    **To enable geospatial analysis:**

    1. Install required packages:
    ```bash
    pip install geopandas osmnx h3 folium streamlit-folium
    ```

    2. For OSMnx, you may also need:
    ```bash
    pip install osmnx
    ```

    3. Refresh this page after installation.
    """)

# Data Upload Section
st.header("📁 Upload Geospatial Data")

uploaded_file = st.file_uploader("Upload GeoJSON file", type=['geojson', 'json'])

if uploaded_file is not None:
    try:
        data = json.load(uploaded_file)
        st.success("✅ File uploaded successfully!")

        # Display basic info
        if 'features' in data:
            st.write(f"**Number of features:** {len(data['features'])}")

            # Show first few features
            if len(data['features']) > 0:
                st.write("**Sample feature:**")
                st.json(data['features'][0])

    except Exception as e:
        st.error(f"Error reading file: {str(e)}")

# Instructions
st.header("📖 How to Use")

st.markdown("""
1. **Load Location Data**: Enter a place name to load buildings and street network data
2. **Network Analysis**: Explore the street network structure and connectivity
3. **Isochrone Analysis**: Calculate areas reachable within a time budget
4. **H3 Analysis**: Aggregate point data into hexagonal grids
5. **Upload Data**: Upload your own GeoJSON files for analysis

**Note**: Some features require internet connection to download OpenStreetMap data.
""")
