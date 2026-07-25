"""
Authentication schemas
"""

from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class TokenResponse(BaseModel):
    """
    JWT token response
    """
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    expires_in: int


class LoginRequest(BaseModel):
    """
    Login request schema
    """
    email: EmailStr
    password: str = Field(..., min_length=8)


class RegisterRequest(BaseModel):
    """
    User registration schema
    """
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None


class RefreshTokenRequest(BaseModel):
    """
    Refresh token request
    """
    refresh_token: str


class OAuthLoginRequest(BaseModel):
    """
    OAuth login request
    """
    provider: str = Field(..., description="OAuth provider: google, yandex, vk, etc.")
    code: str = Field(..., description="OAuth authorization code")
    state: Optional[str] = None


class OAuthCallbackRequest(BaseModel):
    """
    OAuth callback request
    """
    code: str
    state: Optional[str] = None
    error: Optional[str] = None
    error_description: Optional[str] = None
