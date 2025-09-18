import asyncio
from typing import AsyncIterator, Dict

import aiohttp
import pandas as pd


async def poll_json(api_url: str, interval_s: int = 30, **params) -> AsyncIterator[Dict]:
    """Polling helper that yields JSON payloads at a fixed interval."""
    async with aiohttp.ClientSession() as session:
        while True:
            async with session.get(api_url, params=params, timeout=30) as resp:
                resp.raise_for_status()
                yield await resp.json()
            await asyncio.sleep(interval_s)


async def traffic_stream(api_url: str, interval_s: int = 30, **params) -> AsyncIterator[pd.DataFrame]:
    """Yield normalized traffic DataFrames from an API that returns segments/incidents."""
    async for payload in poll_json(api_url, interval_s=interval_s, **params):
        df = pd.json_normalize(payload)
        df["timestamp"] = pd.Timestamp.utcnow()
        yield df


async def weather_stream(
    api_url: str,
    lat: float,
    lon: float,
    interval_s: int = 300,
    api_key: str = "",
) -> AsyncIterator[pd.DataFrame]:
    """Yield weather snapshots for a coordinate as a one-row DataFrame."""
    async with aiohttp.ClientSession() as session:
        while True:
            params = {"lat": lat, "lon": lon, "appid": api_key, "units": "metric"}
            async with session.get(api_url, params=params, timeout=30) as resp:
                resp.raise_for_status()
                raw = await resp.json()
            row = {
                "timestamp": pd.Timestamp.utcnow(),
                "temp_c": raw.get("main", {}).get("temp"),
                "humidity": raw.get("main", {}).get("humidity"),
                "wind_ms": raw.get("wind", {}).get("speed"),
                "conditions": (raw.get("weather", [{}])[0] or {}).get("main"),
            }
            yield pd.DataFrame([row])
            await asyncio.sleep(interval_s)

