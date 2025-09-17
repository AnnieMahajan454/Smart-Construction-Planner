import importlib
import pytest


def test_core_imports():
    core_modules = [
        "smart_planner",
        "smart_planner.data_ingestion",
        "smart_planner.features",
        "smart_planner.models",
        "smart_planner.realtime",
        "smart_planner.pipeline",
    ]
    for name in core_modules:
        assert importlib.import_module(name)


def test_geospatial_optional():
    # Skip if heavy geo deps are not available in CI
    pytest.importorskip("geopandas")
    pytest.importorskip("osmnx")
    assert importlib.import_module("smart_planner.geospatial")


