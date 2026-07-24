import os
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from config.settings import settings
from models.models import User, SocialLogin
from sqlalchemy import select

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password"""
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, 
            settings.SECRET_KEY, 
            algorithm=settings.ALGORITHM
        )
        return encoded_jwt
    
    @staticmethod
    def create_refresh_token(data: dict) -> str:
        """Create a JWT refresh token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
        return encoded_jwt
    
    @staticmethod
    async def get_current_user(
        credentials: HTTPAuthCredentials = Depends(security),
        db: AsyncSession = None
    ) -> User:
        """Get current authenticated user from token"""
        token = credentials.credentials
        
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            user_id: str = payload.get("sub")
            if user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication credentials"
                )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
        
        if db is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database connection not available"
            )
        
        # Get user from database
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        return user

# OAuth Providers
class OAuthService:
    @staticmethod
    async def get_or_create_user(
        db: AsyncSession,
        provider: str,
        provider_id: str,
        email: str,
        display_name: Optional[str] = None,
        avatar_url: Optional[str] = None
    ) -> tuple[User, bool]:
        """Get or create user from OAuth provider"""
        from uuid import uuid4
        
        # Check if social login exists
        result = await db.execute(
            select(SocialLogin).where(
                (SocialLogin.provider == provider) &
                (SocialLogin.provider_id == provider_id)
            )
        )
        social_login = result.scalar_one_or_none()
        
        if social_login:
            # User already exists
            result = await db.execute(
                select(User).where(User.id == social_login.user_id)
            )
            user = result.scalar_one_or_none()
            return user, False
        
        # Create new user
        user_id = str(uuid4())
        username = email.split('@')[0] + '_' + str(uuid4())[:8]
        
        user = User(
            id=user_id,
            email=email,
            username=username,
            display_name=display_name or email.split('@')[0],
            avatar_url=avatar_url,
            language="en",
            theme="dark",
            is_active=True
        )
        
        # Create social login record
        social_login = SocialLogin(
            id=str(uuid4()),
            user_id=user_id,
            provider=provider,
            provider_id=provider_id
        )
        
        db.add(user)
        db.add(social_login)
        await db.commit()
        await db.refresh(user)
        
        return user, True
