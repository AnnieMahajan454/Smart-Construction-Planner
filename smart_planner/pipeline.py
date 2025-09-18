from typing import Optional

import pandas as pd

from . import data_ingestion as di
from . import features as fx
from . import models as mdl


def build_training_table(
    footfall_csv: str,
    traffic_api_url: Optional[str] = None,
    weather_api_url: Optional[str] = None,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    api_key: Optional[str] = None,
) -> pd.DataFrame:
    footfall = di.load_static_pedestrian_counts(footfall_csv)
    traffic = None
    weather = None
    if traffic_api_url:
        try:
            traffic = di.fetch_realtime_traffic(traffic_api_url, params=None, api_key=api_key)
        except Exception:
            traffic = None
    if weather_api_url and lat is not None and lon is not None:
        try:
            w = di.fetch_weather_now(weather_api_url, lat=lat, lon=lon, api_key=api_key)
            weather = pd.DataFrame([w])
        except Exception:
            weather = None
    return fx.build_feature_table(footfall, traffic, weather)


def train_models(features: pd.DataFrame):
    trained, metrics = mdl.train_demand_predictor(features)
    return trained, metrics


