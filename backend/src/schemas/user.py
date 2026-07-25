"""
User schemas for API requests and responses
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """
    Base user schema with common fields
    """
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = None
    language: str = "en"


class UserCreate(UserBase):
    """
    Schema for creating a new user
    """
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    """
    Schema for updating user information
    """
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    language: Optional[str] = None
    bio: Optional[str] = None


class UserResponse(UserBase):
    """
    Schema for user API response
    """
    id: UUID
    avatar_url: Optional[str] = None
    is_active: bool
    is_verified: bool
    is_premium: bool
    bio: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserDetailResponse(UserResponse):
    """
    Detailed user response including subscription info
    """
    subscription_level: Optional[str] = None
    subscription_expires_at: Optional[datetime] = None
