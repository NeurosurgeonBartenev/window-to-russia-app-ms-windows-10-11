from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_db
from services.auth_service import AuthService, OAuthService
from services.oauth_providers import get_oauth_provider
from schemas.schemas import TokenResponse, LoginResponse, UserResponse, RefreshTokenRequest
from datetime import timedelta
import secrets
import httpx

router = APIRouter()

# Store for state tokens (in production, use Redis)
state_store = {}

@router.get("/login/{provider}", response_model=dict)
async def login(provider: str, redirect_uri: str = Query(...)):
    """Initiate social login"""
    oauth_provider = get_oauth_provider(provider, redirect_uri)
    
    if not oauth_provider:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"OAuth provider '{provider}' not supported"
        )
    
    state = secrets.token_urlsafe(32)
    state_store[state] = {
        "provider": provider,
        "redirect_uri": redirect_uri
    }
    
    auth_url = await oauth_provider.get_auth_url(state)
    
    return {
        "auth_url": auth_url,
        "state": state
    }

@router.post("/callback/{provider}", response_model=LoginResponse)
async def callback(
    provider: str,
    code: str = Query(...),
    state: str = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """OAuth callback handler"""
    # Verify state
    if state not in state_store:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid state parameter"
        )
    
    state_data = state_store.pop(state)
    oauth_provider = get_oauth_provider(provider, state_data["redirect_uri"])
    
    try:
        # Get tokens from provider
        tokens = await oauth_provider.get_tokens(code)
        access_token = tokens.get("access_token")
        
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to get access token"
            )
        
        # Get user info from provider
        user_info = await oauth_provider.get_user_info(access_token)
        
        # Extract provider-specific fields
        provider_id = user_info.get("id") or user_info.get("sub") or user_info.get("uid")
        email = user_info.get("email") or user_info.get("default_email")
        display_name = user_info.get("name") or user_info.get("display_name") or email.split('@')[0]
        avatar_url = user_info.get("picture") or user_info.get("photo_max_url")
        
        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email not provided by OAuth provider"
            )
        
        # Get or create user
        user, created = await OAuthService.get_or_create_user(
            db,
            provider,
            str(provider_id),
            email,
            display_name,
            avatar_url
        )
        
        # Create JWT tokens
        access_token_expires = timedelta(minutes=30)
        jwt_access_token = AuthService.create_access_token(
            data={"sub": str(user.id)},
            expires_delta=access_token_expires
        )
        jwt_refresh_token = AuthService.create_refresh_token(
            data={"sub": str(user.id)}
        )
        
        return LoginResponse(
            access_token=jwt_access_token,
            refresh_token=jwt_refresh_token,
            expires_in=30 * 60,
            user=UserResponse(
                id=user.id,
                email=user.email,
                username=user.username,
                display_name=user.display_name,
                avatar_url=user.avatar_url,
                bio=user.bio,
                language=user.language,
                theme=user.theme,
                is_active=user.is_active,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
        )
    
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"OAuth provider request failed: {str(e)}"
        )

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(request: RefreshTokenRequest):
    """Refresh access token"""
    try:
        from jose import jwt
        from config.settings import settings
        
        payload = jwt.decode(
            request.refresh_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token type"
            )
        
        user_id = payload.get("sub")
        
        # Create new access token
        access_token_expires = timedelta(minutes=30)
        new_access_token = AuthService.create_access_token(
            data={"sub": user_id},
            expires_delta=access_token_expires
        )
        
        return TokenResponse(
            access_token=new_access_token,
            expires_in=30 * 60
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

@router.post("/logout", response_model=dict)
async def logout():
    """Logout user (token invalidation handled by client)"""
    return {"message": "Successfully logged out"}
