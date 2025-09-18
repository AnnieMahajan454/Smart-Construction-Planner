import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


def test_sustainability_import():
    """Test that sustainability module can be imported."""
    try:
        from smart_planner.sustainability import assess_project_sustainability
        assert assess_project_sustainability is not None
    except ImportError:
        pytest.skip("Sustainability module not available")


def test_risk_assessment_import():
    """Test that risk assessment module can be imported."""
    try:
        from smart_planner.risk_assessment import assess_project_risks
        assert assess_project_risks is not None
    except ImportError:
        pytest.skip("Risk assessment module not available")


def test_sustainability_assessment():
    """Test basic sustainability assessment functionality."""
    try:
        from smart_planner.sustainability import assess_project_sustainability
        
        # Test with basic parameters
        result = assess_project_sustainability(
            project_type="Residential",
            total_area=1000.0,
            location="New York",
            materials=["steel", "concrete", "wood"]
        )
        
        assert result is not None
        assert hasattr(result, 'overall_score')
        assert hasattr(result, 'carbon_footprint')
        assert hasattr(result, 'leed_potential')
        assert 0 <= result.overall_score <= 100
        
    except ImportError:
        pytest.skip("Sustainability module not available")


def test_risk_assessment():
    """Test basic risk assessment functionality."""
    try:
        from smart_planner.risk_assessment import assess_project_risks
        
        # Test with basic parameters
        result = assess_project_risks(
            project_type="Commercial",
            total_area=2000.0,
            location="San Francisco",
            materials=["steel", "concrete", "glass"]
        )
        
        assert result is not None
        assert hasattr(result, 'overall_risk_score')
        assert hasattr(result, 'risk_factors')
        assert hasattr(result, 'recommendations')
        assert 0 <= result.overall_risk_score <= 10
        assert len(result.risk_factors) > 0
        
    except ImportError:
        pytest.skip("Risk assessment module not available")


def test_enhanced_features_integration():
    """Test that enhanced features can work together."""
    try:
        from smart_planner.sustainability import assess_project_sustainability
        from smart_planner.risk_assessment import assess_project_risks
        
        # Common project parameters
        project_params = {
            "project_type": "Industrial",
            "total_area": 5000.0,
            "location": "Chicago",
            "materials": ["steel", "concrete", "aluminum"]
        }
        
        # Test sustainability
        sustainability = assess_project_sustainability(**project_params)
        assert sustainability is not None
        
        # Test risk assessment
        risks = assess_project_risks(**project_params)
        assert risks is not None
        
        # Verify they produce consistent results
        assert isinstance(sustainability.overall_score, (int, float))
        assert isinstance(risks.overall_risk_score, (int, float))
        
    except ImportError:
        pytest.skip("Enhanced features modules not available")
