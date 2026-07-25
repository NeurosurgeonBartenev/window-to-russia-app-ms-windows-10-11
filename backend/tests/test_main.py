"""
Tests for main application
"""

import pytest
from fastapi.testclient import TestClient

from main import app


def test_health_check():
    """
    Test health check endpoint
    """
    client = TestClient(app)
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "app" in data
    assert "version" in data


def test_root_endpoint():
    """
    Test root endpoint
    """
    client = TestClient(app)
    response = client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert "docs" in data
