import os
from typing import Dict, Optional

import pandas as pd
import requests


def load_static_pedestrian_counts(csv_path: str) -> pd.DataFrame:
    """Load pedestrian counter data from a CSV with columns like
    [sensor_id, lat, lon, timestamp, count].
    """
    return pd.read_csv(csv_path, parse_dates=["timestamp"]) if os.path.exists(csv_path) else pd.DataFrame()


def load_utilities_geojson(geojson_path: str) -> Optional[dict]:
    """Load utilities network (water, power, comms) as GeoJSON for mapping constraints."""
    if not os.path.exists(geojson_path):
        return None
    import json

    with open(geojson_path, "r", encoding="utf-8") as f:
        return json.load(f)


def fetch_realtime_traffic(api_url: str, params: Optional[Dict] = None, api_key: Optional[str] = None) -> pd.DataFrame:
    """Fetch real-time traffic speeds/incidents from an API.

    Expected response shape is normalized to a DataFrame with columns like
    [segment_id, geometry_wkt, speed_kph, congestion_level, timestamp].
    """
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else None
    resp = requests.get(api_url, params=params, headers=headers, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return pd.json_normalize(data)


def fetch_weather_now(api_url: str, lat: float, lon: float, api_key: Optional[str] = None) -> Dict:
    """Fetch current weather for a coordinate. Normalize to a minimal dict."""
    params = {"lat": lat, "lon": lon, "appid": api_key, "units": "metric"}
    resp = requests.get(api_url, params=params, timeout=30)
    resp.raise_for_status()
    raw = resp.json()
    return {
        "temp_c": raw.get("main", {}).get("temp"),
        "humidity": raw.get("main", {}).get("humidity"),
        "wind_ms": raw.get("wind", {}).get("speed"),
        "conditions": raw.get("weather", [{}])[0].get("main"),
        "timestamp": pd.Timestamp.utcnow(),
    }


def fetch_gtfs_static(gtfs_zip_url: str, dest_dir: str) -> str:
    """Download GTFS static feed (transit) for accessibility analysis; returns path to ZIP."""
    os.makedirs(dest_dir, exist_ok=True)
    zip_path = os.path.join(dest_dir, "gtfs.zip")
    with requests.get(gtfs_zip_url, stream=True, timeout=60) as r:
        r.raise_for_status()
        with open(zip_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    return zip_path


