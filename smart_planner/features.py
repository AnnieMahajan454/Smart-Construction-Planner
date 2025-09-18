from typing import Dict, Optional

import numpy as np
import pandas as pd


def engineer_temporal_features(df: pd.DataFrame, timestamp_col: str) -> pd.DataFrame:
    """Add hour-of-day, day-of-week, weekend, month seasonality features."""
    df = df.copy()
    ts = pd.to_datetime(df[timestamp_col])
    df["hour"] = ts.dt.hour
    df["dow"] = ts.dt.dayofweek
    df["is_weekend"] = (df["dow"] >= 5).astype(int)
    df["month"] = ts.dt.month
    df["sin_hour"] = np.sin(2 * np.pi * df["hour"] / 24)
    df["cos_hour"] = np.cos(2 * np.pi * df["hour"] / 24)
    return df


def merge_weather(df: pd.DataFrame, weather: pd.DataFrame, on: str = "timestamp") -> pd.DataFrame:
    """Join weather features to the primary time series."""
    return df.merge(weather, on=on, how="left")


def recent_footfall_features(counts: pd.DataFrame, window_h: int = 2) -> pd.DataFrame:
    """Compute rolling sums/means for pedestrian counts per sensor."""
    counts = counts.sort_values(["sensor_id", "timestamp"]).copy()
    counts["count_roll_mean"] = (
        counts.groupby("sensor_id")["count"].rolling(f"{window_h}H", on="timestamp").mean().reset_index(level=0, drop=True)
    )
    counts["count_roll_sum"] = (
        counts.groupby("sensor_id")["count"].rolling(f"{window_h}H", on="timestamp").sum().reset_index(level=0, drop=True)
    )
    return counts


def build_feature_table(
    footfall: pd.DataFrame,
    traffic: Optional[pd.DataFrame],
    weather: Optional[pd.DataFrame],
) -> pd.DataFrame:
    """Assemble a supervised learning table keyed by time and location.

    Target candidates: crowding risk, accessibility score, safety score, utility impact score.
    """
    base = engineer_temporal_features(footfall, "timestamp")
    base = recent_footfall_features(base)
    if weather is not None and not weather.empty:
        base = merge_weather(base, weather.rename(columns={"dt": "timestamp"}), on="timestamp")
    if traffic is not None and not traffic.empty:
        traffic_small = traffic[["timestamp", "speed_kph", "congestion_level"]].copy()
        base = base.merge(traffic_small, on="timestamp", how="left")

    # Placeholder target: use future 1-hour pedestrian count as proxy demand.
    base = base.sort_values(["sensor_id", "timestamp"])  # type: ignore
    base["target_demand_next_hour"] = (
        base.groupby("sensor_id")["count"].shift(-1)
    )
    base = base.dropna(subset=["target_demand_next_hour"]).reset_index(drop=True)
    return base


