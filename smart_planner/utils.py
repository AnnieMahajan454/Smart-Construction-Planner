"""Utility functions for the Smart Construction Planner."""

import logging
import os
import sys
from typing import Any, Dict, Optional

try:
    import streamlit as st
    import pandas as pd
except ImportError:
    st = None
    pd = None


def setup_logging(level: str = "INFO") -> logging.Logger:
    """Set up logging configuration for the application."""
    
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger("smart_planner")
    return logger


def safe_execute(func, *args, default_return=None, error_message="An error occurred", **kwargs):
    """Safely execute a function with error handling."""
    
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger = logging.getLogger("smart_planner")
        logger.error(f"{error_message}: {str(e)}")
        
        if 'st' in sys.modules:  # Check if Streamlit is available
            st.error(f"{error_message}. Please check your inputs and try again.")
        
        return default_return


def validate_inputs(**kwargs) -> Dict[str, Any]:
    """Validate common input parameters for construction projects."""
    
    errors = []
    validated = {}
    
    # Validate project type
    if 'project_type' in kwargs:
        valid_types = ['Residential', 'Commercial', 'Industrial', 'Institutional']
        if kwargs['project_type'] not in valid_types:
            errors.append(f"Invalid project type. Must be one of: {valid_types}")
        else:
            validated['project_type'] = kwargs['project_type']
    
    # Validate location
    if 'location' in kwargs:
        if not kwargs['location'] or not isinstance(kwargs['location'], str):
            errors.append("Location must be a non-empty string")
        else:
            validated['location'] = kwargs['location']
    
    # Validate total area
    if 'total_area' in kwargs:
        try:
            area = float(kwargs['total_area'])
            if area <= 0:
                errors.append("Total area must be greater than 0")
            elif area > 1000000:  # 1 million m² limit
                errors.append("Total area seems unreasonably large (>1M m²)")
            else:
                validated['total_area'] = area
        except (ValueError, TypeError):
            errors.append("Total area must be a valid number")
    
    # Validate number of floors
    if 'number_of_floors' in kwargs:
        try:
            floors = int(kwargs['number_of_floors'])
            if floors < 1:
                errors.append("Number of floors must be at least 1")
            elif floors > 200:  # Reasonable upper limit
                errors.append("Number of floors seems unreasonably high (>200)")
            else:
                validated['number_of_floors'] = floors
        except (ValueError, TypeError):
            errors.append("Number of floors must be a valid integer")
    
    # Validate number of basements
    if 'number_of_basements' in kwargs:
        try:
            basements = int(kwargs['number_of_basements'])
            if basements < 0:
                errors.append("Number of basements cannot be negative")
            elif basements > 20:  # Reasonable upper limit
                errors.append("Number of basements seems unreasonably high (>20)")
            else:
                validated['number_of_basements'] = basements
        except (ValueError, TypeError):
            errors.append("Number of basements must be a valid integer")
    
    # Validate materials list
    if 'materials' in kwargs:
        materials = kwargs['materials']
        if not isinstance(materials, list):
            errors.append("Materials must be provided as a list")
        elif not materials:
            validated['materials'] = ['steel', 'concrete']  # Default materials
        else:
            validated['materials'] = [str(m).strip() for m in materials if str(m).strip()]
    
    return {
        'validated': validated,
        'errors': errors,
        'is_valid': len(errors) == 0
    }


def format_currency(amount: float, currency: str = "USD") -> str:
    """Format currency amounts consistently."""
    
    if currency == "USD":
        if amount >= 1_000_000:
            return f"${amount/1_000_000:.1f}M"
        elif amount >= 1_000:
            return f"${amount/1_000:.0f}K"
        else:
            return f"${amount:,.0f}"
    
    return f"{amount:,.2f} {currency}"


def format_percentage(value: float, decimal_places: int = 1) -> str:
    """Format percentage values consistently."""
    
    return f"{value:.{decimal_places}f}%"


def get_env_var(var_name: str, default: Optional[str] = None, required: bool = False) -> Optional[str]:
    """Get environment variable with optional default and required validation."""
    
    value = os.getenv(var_name, default)
    
    if required and value is None:
        logger = logging.getLogger("smart_planner")
        logger.error(f"Required environment variable {var_name} is not set")
        raise ValueError(f"Required environment variable {var_name} is not set")
    
    return value


def cache_result(func):
    """Simple decorator for caching function results in Streamlit."""
    
    def wrapper(*args, **kwargs):
        if 'st' in sys.modules:
            # Use Streamlit's caching if available
            return st.cache_data(func)(*args, **kwargs)
        else:
            # Fallback to regular function call
            return func(*args, **kwargs)
    
    return wrapper


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


class CalculationError(Exception):
    """Custom exception for calculation errors."""
    pass


def create_progress_tracker(total_steps: int, description: str = "Processing..."):
    """Create a progress tracker for long-running operations."""
    
    if 'st' in sys.modules:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        def update_progress(current_step: int, step_description: str = ""):
            progress = current_step / total_steps
            progress_bar.progress(progress)
            if step_description:
                status_text.text(f"{description} {step_description} ({current_step}/{total_steps})")
            else:
                status_text.text(f"{description} {current_step}/{total_steps}")
        
        def complete_progress():
            progress_bar.progress(1.0)
            status_text.text(f"{description} Complete!")
        
        return update_progress, complete_progress
    else:
        # Fallback for non-Streamlit environments
        def update_progress(current_step: int, step_description: str = ""):
            print(f"{description} {current_step}/{total_steps}: {step_description}")
        
        def complete_progress():
            print(f"{description} Complete!")
        
        return update_progress, complete_progress


def display_dataframe_with_styling(df, title: str = None, height: int = 400):
    """Display a DataFrame with consistent styling."""
    
    if 'st' in sys.modules and df is not None and not df.empty:
        if title:
            st.subheader(title)
        
        # Apply styling based on DataFrame content
        if 'Score' in df.columns:
            def color_scores(val):
                if pd and pd.isna(val):
                    return ''
                try:
                    numeric_val = float(str(val).replace('%', '').replace('/100', ''))
                    if numeric_val >= 80:
                        return 'background-color: lightgreen'
                    elif numeric_val >= 60:
                        return 'background-color: lightyellow'
                    else:
                        return 'background-color: lightcoral'
                except (ValueError, TypeError, AttributeError):
                    return ''
            
            styled_df = df.style.applymap(color_scores, subset=['Score'])
            st.dataframe(styled_df, height=height, use_container_width=True)
        else:
            st.dataframe(df, height=height, use_container_width=True)
    elif df is None or df.empty:
        if 'st' in sys.modules:
            st.info("No data available to display")


# Constants for the application
DEFAULT_MATERIALS = ['steel', 'concrete', 'lumber']
SUPPORTED_LOCATIONS = [
    'New York', 'San Francisco', 'Los Angeles', 'Chicago',
    'Miami', 'Dallas', 'Houston', 'Atlanta'
]
PROJECT_TYPES = ['Residential', 'Commercial', 'Industrial', 'Institutional']
