from typing import Tuple, List, Optional

import geopandas as gpd
import networkx as nx
import osmnx as ox
from shapely.geometry import Point, LineString
import h3


def load_base_layers(place: str) -> Tuple[gpd.GeoDataFrame, nx.MultiDiGraph]:
    """Load base layers: buildings (footprints) and walkable street network."""
    buildings = ox.geometries_from_place(place, tags={"building": True})
    walk_graph = ox.graph_from_place(place, network_type="walk")
    return buildings, walk_graph


def snap_points_to_graph(points: gpd.GeoDataFrame, graph: nx.MultiDiGraph) -> List[int]:
    """Return nearest node IDs for input points."""
    nodes, _ = ox.graph_to_gdfs(graph)
    return [ox.distance.nearest_nodes(graph, x=pt.x, y=pt.y) for pt in points.geometry]


def shortest_path_length_m(graph: nx.MultiDiGraph, origin_node: int, dest_node: int) -> float:
    """Compute shortest path length in meters using edge length attribute."""
    length_m = nx.shortest_path_length(graph, origin_node, dest_node, weight="length")
    return float(length_m)


def compute_isochrone(graph: nx.MultiDiGraph, center_node: int, speed_m_s: float, minutes: int) -> gpd.GeoSeries:
    """Compute a simple isochrone polygon reachable within time budget, given a walking speed."""
    meters = speed_m_s * 60 * minutes
    subgraph = nx.ego_graph(graph, center_node, radius=meters, distance="length")
    nodes, edges = ox.graph_to_gdfs(subgraph)
    return edges.buffer(15).unary_union


def spatial_join_points_to_hex(points: gpd.GeoDataFrame, resolution: int) -> gpd.GeoDataFrame:
    """Aggregate point features into H3 hexagons at a given resolution."""
    def to_h3(row):
        lat, lon = row.geometry.y, row.geometry.x
        return h3.geo_to_h3(lat, lon, resolution)

    points = points.copy()
    points["h3"] = points.apply(to_h3, axis=1)
    grouped = points.groupby("h3").agg({"count": "sum"}).reset_index()
    grouped["geometry"] = grouped["h3"].apply(lambda h: LineString())  # placeholder geometry
    return gpd.GeoDataFrame(grouped, geometry="geometry", crs="EPSG:4326")


