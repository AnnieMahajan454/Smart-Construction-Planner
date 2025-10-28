@echo off
echo ====================================
echo Smart Construction Planner Setup
echo ====================================
echo.

echo [1/4] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)
python --version
echo.

echo [2/4] Upgrading pip...
python -m pip install --upgrade pip
echo.

echo [3/4] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo WARNING: Some packages failed to install
    echo Trying individual installation...
    pip install streamlit
    pip install pandas numpy
    pip install plotly
    pip install folium streamlit-folium
    pip install scikit-learn
)
echo.

echo [4/4] Verifying installation...
python -c "import streamlit, pandas, numpy, plotly, folium, sklearn; print('All packages installed successfully!')"
if errorlevel 1 (
    echo ERROR: Some packages are missing
    echo Please check the error messages above
    pause
    exit /b 1
)
echo.

echo ====================================
echo Setup Complete!
echo ====================================
echo.
echo To run the application:
echo   streamlit run ai_planner_light.py
echo.
echo The app will open in your default browser at http://localhost:8501
echo.
pause
