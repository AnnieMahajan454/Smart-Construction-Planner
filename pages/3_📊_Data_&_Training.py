import streamlit as st
import pandas as pd
from smart_planner.pipeline import build_training_table, train_models

st.title("📊 Data & Training")

st.markdown("""
Build a supervised learning table from pedestrian, traffic, and weather data,
then train a demand prediction model.
""")

footfall_file = st.text_input("Footfall CSV path", value="ped_counts.csv")
traffic_api = st.text_input("Traffic API URL (optional)", value="")
weather_api = st.text_input("Weather API URL (optional)", value="")
lat = st.number_input("Latitude", value=37.7749)
lon = st.number_input("Longitude", value=-122.4194)
api_key = st.text_input("API Key (optional)", value="", type="password")

if st.button("Build Feature Table"):
    try:
        features = build_training_table(
            footfall_csv=footfall_file,
            traffic_api_url=traffic_api or None,
            weather_api_url=weather_api or None,
            lat=lat if weather_api else None,
            lon=lon if weather_api else None,
            api_key=api_key or None,
        )
        st.session_state['features_tbl'] = features
        st.success(f"✅ Built feature table with {len(features)} rows and {len(features.columns)} columns")
        st.dataframe(features.head(10))
    except Exception as e:
        st.error(f"Error building features: {str(e)}")

if 'features_tbl' in st.session_state:
    if st.button("Train Model"):
        try:
            model, metrics = train_models(st.session_state['features_tbl'])
            st.session_state['trained_model'] = model
            st.success("✅ Model trained successfully")
            st.json(metrics)
        except Exception as e:
            st.error(f"Error training model: {str(e)}")