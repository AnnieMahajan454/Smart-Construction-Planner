# Smart Construction Planner

An AI‑assisted toolkit for data‑driven site design. It fuses pedestrian flow, geospatial context, utilities, traffic, and weather to forecast demand, assess accessibility, and surface risks. Planners get fast, practical recommendations and what‑if analysis to design safer, more inclusive public spaces with confidence.

## Key Features
- Pedestrian & Accessibility Insights: Optimizes layouts for safe and inclusive movement.
- Geospatial Data Integration: Leverages maps, mobility data, and urban utility patterns.
- AI & ML Algorithms: Predicts demand, flow, and optimal structural layouts.
- Real-Time Data Awareness: Considers live traffic and weather data to ensure safety and efficiency.
- Faster Decision-Making: Helps stakeholders plan and execute construction more effectively.

## What's Included

### Streamlit Cost Estimator
- Interactive cost estimation with Random Forest model
- What-if scenario simulation
- Data visualization and analysis
- Run with: `streamlit run costestimator.py`

### Smart Planner Package
- `smart_planner/data_ingestion.py`: Load CSV/GeoJSON data and fetch APIs
- `smart_planner/geospatial.py`: Network analysis and isochrone calculations
- `smart_planner/features.py`: Temporal feature engineering
- `smart_planner/models.py`: ML model training and inference
- `smart_planner/realtime.py`: Async data streams for traffic/weather
- `smart_planner/pipeline.py`: End-to-end workflow orchestration

## 🚀 Live Demo

**Try the application online:** [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://smart-construction-planner.streamlit.app)

*Note: The live demo works without API keys. For full AI chatbot functionality, set up your own deployment with OpenAI API key.*

## Quick Start

### Option 1: Use Online (Recommended)
Visit the live demo link above to try all features immediately.

### Option 2: Run Locally
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the Streamlit app:
   ```bash
   streamlit run costestimator.py
   ```

3. Use the planner package:
   ```python
   from smart_planner.pipeline import build_training_table, train_models
   
   features = build_training_table("ped_counts.csv")
   model, metrics = train_models(features)
   ```

### Option 3: Deploy Your Own
1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Set main file to `costestimator.py`
5. Add environment variables for API keys (optional)
6. Deploy!

## Requirements
- Python 3.8+
- See `requirements.txt` for full dependency list

## License
For educational use only.
