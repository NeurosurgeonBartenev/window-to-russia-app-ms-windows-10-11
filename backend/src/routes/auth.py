"""
Authentication routes
"""

import logging
from typing import Optional
import secrets

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import get_db
from src.schemas.user import UserCreate, UserResponse
from src.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    RefreshTokenRequest,
    OAuthLoginRequest,
)
from src.services.auth_service import AuthService
from src.utils.auth import decode_token

logger = logging.getLogger(__name__)

router = APIRouter(tags=["auth"])


@router.post("/register", response_model=dict)
async def register(
    request: RegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user
    """
    user_data = UserCreate(
        username=request.username,
        email=request.email,
        password=request.password,
        full_name=request.full_name,
    )
    
    user = await AuthService.register_user(db, user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists or registration failed"
        )
    
    tokens = AuthService.create_tokens(user.id)
    return {
        "user": UserResponse.from_orm(user),
        "tokens": tokens,
        "message": "User registered successfully"
    }


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Login with email and password
    """
    user = await AuthService.authenticate_user(db, request.email, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    tokens = AuthService.create_tokens(user.id)
    return TokenResponse(
        access_token=tokens["access_token"],
        refresh_token=tokens["refresh_token"],
        expires_in=30 * 60  # 30 minutes in seconds
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(request: RefreshTokenRequest):
    """
    Refresh access token
    """
    payload = decode_token(request.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    user_id = payload.get("sub")
    tokens = AuthService.create_tokens(user_id)
    
    return TokenResponse(
        access_token=tokens["access_token"],
        refresh_token=tokens["refresh_token"],
        expires_in=30 * 60
    )


@router.get("/oauth/authorize")
async def oauth_authorize(provider: str, state: Optional[str] = None):
    """
    Get OAuth authorization URL
    """
    from src.utils.oauth import get_oauth_provider
    
    if not state:
        state = secrets.token_urlsafe(32)
    
    oauth_provider = get_oauth_provider(provider)
    if not oauth_provider:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"OAuth provider '{provider}' not supported"
        )
    
    auth_url = await oauth_provider.get_authorization_url(state)
    
    return {
        "provider": provider,
        "authorization_url": auth_url,
        "state": state
    }


@router.post("/oauth/callback", response_model=TokenResponse)
async def oauth_callback(
    request: OAuthLoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    OAuth callback endpoint
    """
    if request.error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"OAuth error: {request.error_description}"
        )
    
    result = await AuthService.oauth_login(db, request.provider, request.code)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="OAuth authentication failed"
        )
    
    user = result["user"]
    tokens = AuthService.create_tokens(user.id)
    
    return TokenResponse(
        access_token=tokens["access_token"],
        refresh_token=tokens["refresh_token"],
        expires_in=30 * 60
    )


@router.post("/oauth/login", response_model=TokenResponse)
async def oauth_login(
    request: OAuthLoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    OAuth login endpoint (alternative to callback)
    """
    result = await AuthService.oauth_login(db, request.provider, request.code)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="OAuth authentication failed"
        )
    
    user = result["user"]
    tokens = AuthService.create_tokens(user.id)
    
    return TokenResponse(
        access_token=tokens["access_token"],
        refresh_token=tokens["refresh_token"],
        expires_in=30 * 60
    )
