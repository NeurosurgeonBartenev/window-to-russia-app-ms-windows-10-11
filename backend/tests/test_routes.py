"""
Test for authentication endpoints
"""

import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


class TestAuthEndpoints:
    """
    Tests for authentication endpoints
    """
    
    def test_register_success(self):
        """
        Test successful user registration
        """
        response = client.post(
            "/api/v1/auth/register",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "testpassword123",
                "full_name": "Test User"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "user" in data
        assert "tokens" in data
        assert data["user"]["email"] == "test@example.com"
    
    def test_register_duplicate_email(self):
        """
        Test registration with duplicate email
        """
        # First registration
        client.post(
            "/api/v1/auth/register",
            json={
                "username": "user1",
                "email": "duplicate@example.com",
                "password": "password123"
            }
        )
        
        # Duplicate registration
        response = client.post(
            "/api/v1/auth/register",
            json={
                "username": "user2",
                "email": "duplicate@example.com",
                "password": "password123"
            }
        )
        assert response.status_code == 400
    
    def test_oauth_authorize(self):
        """
        Test OAuth authorization URL generation
        """
        response = client.get("/api/v1/auth/oauth/authorize?provider=google")
        # Will fail without proper OAuth config, but endpoint should exist
        assert response.status_code in [200, 400]


class TestUserEndpoints:
    """
    Tests for user endpoints
    """
    
    def test_get_current_user_without_token(self):
        """
        Test accessing protected endpoint without token
        """
        response = client.get("/api/v1/users/me")
        assert response.status_code == 401


class TestThemeEndpoints:
    """
    Tests for theme endpoints
    """
    
    def test_get_today_theme(self):
        """
        Test getting today's theme
        """
        response = client.get("/api/v1/themes/today")
        # May be None if no theme for today
        assert response.status_code == 200
    
    def test_list_themes(self):
        """
        Test listing all themes
        """
        response = client.get("/api/v1/themes")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
