import streamlit as st
import asyncio
from smart_planner import realtime as rt

st.title("📡 Realtime Monitoring")

st.markdown("""
Monitor live traffic and weather data streams. This demo polls APIs at a fixed interval
and displays the latest snapshot. Requires internet and API endpoints.
""")

traffic_api = st.text_input("Traffic API URL", value="")
weather_api = st.text_input("Weather API URL", value="")
lat = st.number_input("Latitude", value=37.7749)
lon = st.number_input("Longitude", value=-122.4194)
api_key = st.text_input("API Key (optional)", value="", type="password")
interval = st.slider("Polling interval (seconds)", 10, 300, 60)

placeholder = st.empty()

async def monitor(traffic_api, weather_api, lat, lon, api_key, interval):
    tasks = []
    if traffic_api:
        async def run_traffic():
            async for df in rt.traffic_stream(traffic_api, interval_s=interval):
                with placeholder.container():
                    st.subheader("Traffic Snapshot")
                    st.dataframe(df.head(10))
        tasks.append(asyncio.create_task(run_traffic()))
    if weather_api:
        async def run_weather():
            async for df in rt.weather_stream(weather_api, lat=lat, lon=lon, interval_s=interval, api_key=api_key or ""):
                with placeholder.container():
                    st.subheader("Weather Snapshot")
                    st.dataframe(df)
        tasks.append(asyncio.create_task(run_weather()))
    if tasks:
        await asyncio.gather(*tasks)

if st.button("Start Monitoring"):
    if not traffic_api and not weather_api:
        st.warning("Provide at least one API URL to start.")
    else:
        try:
            asyncio.run(monitor(traffic_api, weather_api, lat, lon, api_key, interval))
        except RuntimeError:
            st.info("Monitoring already running in this session. Please refresh to restart.")
