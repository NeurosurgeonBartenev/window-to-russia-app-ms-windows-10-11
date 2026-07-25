"""
Authentication service containing business logic
"""

import logging
from typing import Optional, Dict, Any
from datetime import timedelta
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models.user import User
from src.models.oauth_token import OAuthToken
from src.schemas.user import UserCreate, UserResponse
from src.utils.auth import hash_password, verify_password, create_access_token, create_refresh_token
from src.utils.oauth import get_oauth_provider

logger = logging.getLogger(__name__)


class AuthService:
    """
    Service for handling authentication operations
    """
    
    @staticmethod
    async def register_user(
        db: AsyncSession,
        user_data: UserCreate
    ) -> Optional[User]:
        """
        Register a new user
        """
        try:
            # Check if user already exists
            result = await db.execute(
                select(User).where(
                    (User.email == user_data.email) | (User.username == user_data.username)
                )
            )
            if result.scalar_one_or_none():
                logger.warning(f"User already exists: {user_data.email}")
                return None
            
            # Create new user
            new_user = User(
                username=user_data.username,
                email=user_data.email,
                password_hash=hash_password(user_data.password),
                full_name=user_data.full_name,
            )
            
            db.add(new_user)
            await db.commit()
            await db.refresh(new_user)
            
            logger.info(f"User registered: {new_user.email}")
            return new_user
        
        except Exception as e:
            await db.rollback()
            logger.error(f"Error registering user: {str(e)}")
            return None
    
    @staticmethod
    async def authenticate_user(
        db: AsyncSession,
        email: str,
        password: str
    ) -> Optional[User]:
        """
        Authenticate user with email and password
        """
        result = await db.execute(
            select(User).where(User.email == email)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            logger.warning(f"User not found: {email}")
            return None
        
        if not verify_password(password, user.password_hash):
            logger.warning(f"Invalid password for user: {email}")
            return None
        
        if not user.is_active:
            logger.warning(f"User account is inactive: {email}")
            return None
        
        logger.info(f"User authenticated: {email}")
        return user
    
    @staticmethod
    async def oauth_login(
        db: AsyncSession,
        provider: str,
        code: str
    ) -> Optional[Dict[str, Any]]:
        """
        Authenticate user via OAuth provider
        """
        try:
            # Get OAuth provider
            oauth_provider = get_oauth_provider(provider)
            if not oauth_provider:
                logger.error(f"OAuth provider not configured: {provider}")
                return None
            
            # Exchange code for token
            token_data = await oauth_provider.exchange_code_for_token(code)
            if not token_data:
                logger.error(f"Failed to exchange code for {provider}")
                return None
            
            access_token = token_data.get("access_token")
            if not access_token:
                logger.error(f"No access token in response from {provider}")
                return None
            
            # Get user info from provider
            user_info = await oauth_provider.get_user_info(access_token)
            if not user_info:
                logger.error(f"Failed to get user info from {provider}")
                return None
            
            # Find or create user
            provider_id_field = f"{provider.lower()}_id"
            provider_id = user_info.get("id") or user_info.get("sub")
            
            # Try to find user by OAuth ID
            result = await db.execute(
                select(User).where(
                    getattr(User, provider_id_field) == provider_id
                )
            )
            user = result.scalar_one_or_none()
            
            # If not found, try to find by email and link account
            if not user and "email" in user_info:
                result = await db.execute(
                    select(User).where(User.email == user_info["email"])
                )
                user = result.scalar_one_or_none()
                
                if user:
                    # Link OAuth account to existing user
                    setattr(user, provider_id_field, provider_id)
            
            # Create new user if not found
            if not user:
                user = User(
                    username=user_info.get("name", user_info.get("email", f"user_{provider_id}")).replace(" ", "_"),
                    email=user_info.get("email", f"{provider}_{provider_id}@oauth.local"),
                    full_name=user_info.get("name"),
                    avatar_url=user_info.get("picture"),
                    is_verified=True,  # OAuth users are verified by provider
                )
                setattr(user, provider_id_field, provider_id)
                db.add(user)
            
            await db.commit()
            await db.refresh(user)
            
            # Save OAuth token
            oauth_token = OAuthToken(
                user_id=user.id,
                provider=provider,
                access_token=access_token,
                refresh_token=token_data.get("refresh_token"),
                id_token=token_data.get("id_token"),
                scope=token_data.get("scope"),
            )
            db.add(oauth_token)
            await db.commit()
            
            logger.info(f"User authenticated via {provider}: {user.email}")
            return {"user": user, "token_data": token_data}
        
        except Exception as e:
            await db.rollback()
            logger.error(f"Error in OAuth login: {str(e)}")
            return None
    
    @staticmethod
    def create_tokens(user_id: UUID) -> Dict[str, str]:
        """
        Create access and refresh tokens
        """
        access_token = create_access_token(data={"sub": str(user_id)})
        refresh_token = create_refresh_token(data={"sub": str(user_id)})
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }
