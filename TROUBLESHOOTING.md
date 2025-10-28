# Troubleshooting Guide - Smart Construction Planner

## Common Issues and Solutions

### 1. Installation Issues

#### Problem: Package installation fails
**Solution:**
```bash
# Upgrade pip first
pip install --upgrade pip

# Install packages one by one if batch install fails
pip install streamlit
pip install pandas numpy
pip install plotly
pip install folium streamlit-folium
pip install scikit-learn
```

#### Problem: Version conflicts
**Solution:**
```bash
# Create a virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Running the Application

#### Problem: Application won't start
**Solution:**
```bash
# Make sure you're in the correct directory
cd Smart-Construction-Planner

# Run with full path
streamlit run ai_planner_light.py

# If port 8501 is in use, specify a different port
streamlit run ai_planner_light.py --server.port 8502
```

#### Problem: "Module not found" error
**Solution:**
```bash
# Verify all packages are installed
pip list | grep -E "streamlit|pandas|numpy|plotly|folium|scikit-learn"

# Reinstall missing packages
pip install -r requirements.txt
```

### 3. Browser Issues

#### Problem: Browser doesn't open automatically
**Solution:**
1. Look for the URL in the terminal output (usually `http://localhost:8501`)
2. Manually open your browser and navigate to that URL
3. Try using `--server.headless false` flag:
   ```bash
   streamlit run ai_planner_light.py --server.headless false
   ```

#### Problem: "This site can't be reached" in browser
**Solution:**
1. Check if the application is actually running in the terminal
2. Try accessing `http://127.0.0.1:8501` instead of `localhost`
3. Check if your firewall is blocking the port

### 4. Runtime Errors

#### Problem: Map doesn't display
**Solution:**
- Check your internet connection (Folium maps require internet for tiles)
- Try refreshing the page
- Clear browser cache

#### Problem: Data not loading or showing errors
**Solution:**
```bash
# Check Python version (should be 3.8+)
python --version

# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### 5. Performance Issues

#### Problem: Application is slow
**Solution:**
- Close other Streamlit instances running on your machine
- Clear Streamlit cache: Delete `.streamlit` folder in your user directory
- Restart the application
- Use Chrome or Edge browser for better performance

#### Problem: High memory usage
**Solution:**
- Restart the Streamlit server
- Close unnecessary tabs in your browser
- Reduce the number of data points being displayed

### 6. Development Issues

#### Problem: Changes not reflecting
**Solution:**
- Streamlit has auto-reload. Click "Always rerun" in the top-right menu
- Manually refresh the page
- Stop and restart the server

#### Problem: Session state issues
**Solution:**
- Clear the browser cache
- Use the "Clear cache" option in Streamlit's hamburger menu
- Restart the application

### 7. Windows-Specific Issues

#### Problem: PowerShell execution policy error
**Solution:**
```powershell
# Run PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Problem: `&&` not recognized in PowerShell
**Solution:**
Use `;` instead of `&&` to chain commands:
```powershell
cd Smart-Construction-Planner; streamlit run ai_planner_light.py
```

### 8. Import Errors

#### Problem: "No module named 'pedestrian_paths'"
**Solution:**
- Ensure you're running the command from the `Smart-Construction-Planner` directory
- Check that `pedestrian_paths.py` exists in the same directory as `ai_planner_light.py`

### 9. Data/Display Issues

#### Problem: Dropdown menus not showing options
**Solution:**
- This is usually a CSS/theme issue
- Try using a different browser
- Clear browser cache and cookies
- The latest fix in the code should resolve this

#### Problem: Text not visible (white text on white background)
**Solution:**
- The application now forces a light theme
- If you still see issues, try:
  1. Clear browser cache
  2. Use Chrome or Edge in regular (non-incognito) mode
  3. Disable browser extensions temporarily

## Getting Help

If you're still experiencing issues:

1. **Check the terminal/console output** for error messages
2. **Take a screenshot** of the error
3. **Note your environment**:
   - Operating System and version
   - Python version (`python --version`)
   - Package versions (`pip list`)
4. **Check GitHub Issues** at https://github.com/AnnieMahajan454/Smart-Construction-Planner/issues
5. **Create a new issue** with:
   - Detailed description of the problem
   - Steps to reproduce
   - Error messages
   - Your environment details

## Quick Health Check

Run this to verify your setup:

```bash
# Check Python
python --version

# Check if all packages are installed
python -c "import streamlit, pandas, numpy, plotly, folium, sklearn; print('All packages imported successfully!')"

# Verify the application syntax
python -m py_compile ai_planner_light.py
python -m py_compile pedestrian_paths.py

# If all above succeed, run the app
streamlit run ai_planner_light.py
```

## System Requirements

- **Python**: 3.8 or higher
- **RAM**: Minimum 4GB (8GB recommended)
- **Internet**: Required for map tiles
- **Browser**: Chrome, Edge, Firefox, or Safari (latest versions)
- **Operating System**: Windows 10+, macOS 10.14+, or Linux

## Performance Tips

1. Use a modern browser (Chrome/Edge recommended)
2. Close unused browser tabs
3. Ensure stable internet connection for maps
4. Run only one instance of the application at a time
5. Restart the application if it becomes unresponsive
