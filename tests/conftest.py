"""
Pytest configuration and fixtures for FastAPI tests.
Provides test client and fresh activity data for each test.
"""

import pytest
from copy import deepcopy
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def activities_data():
    """
    Fixture providing a fresh copy of activities data for each test.
    Using deepcopy ensures no test pollution - modifications in one test
    don't affect other tests.
    
    Yields:
        dict: Fresh copy of activities database
    """
    return deepcopy(activities)


@pytest.fixture
def client(activities_data, monkeypatch):
    """
    Fixture providing a TestClient with isolated activities data.
    Uses monkeypatch to replace the global activities dict with fresh test data.
    
    Args:
        activities_data: Fresh activities fixture
        monkeypatch: pytest's monkeypatch fixture for safely modifying globals
        
    Yields:
        TestClient: FastAPI test client
    """
    # Replace the global activities dict with test data
    monkeypatch.setattr("src.app.activities", activities_data)
    
    # Return TestClient for making requests
    return TestClient(app)
