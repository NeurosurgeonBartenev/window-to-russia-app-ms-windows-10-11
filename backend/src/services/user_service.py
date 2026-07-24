from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func
from uuid import uuid4
from models.models import User, UserFavorite, Wallpaper
from schemas.schemas import UserResponse

class UserService:
    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: str) -> Optional[User]:
        """Get user by ID"""
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
        """Get user by email"""
        result = await db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def update_user(db: AsyncSession, user_id: str, **kwargs) -> Optional[User]:
        """Update user profile"""
        user = await UserService.get_user_by_id(db, user_id)
        if not user:
            return None
        
        for key, value in kwargs.items():
            if hasattr(user, key) and value is not None:
                setattr(user, key, value)
        
        from datetime import datetime
        user.updated_at = datetime.utcnow()
        
        await db.commit()
        await db.refresh(user)
        return user
    
    @staticmethod
    async def delete_user(db: AsyncSession, user_id: str) -> bool:
        """Delete user account"""
        user = await UserService.get_user_by_id(db, user_id)
        if not user:
            return False
        
        await db.delete(user)
        await db.commit()
        return True
    
    @staticmethod
    async def get_user_favorites(
        db: AsyncSession,
        user_id: str,
        page: int = 1,
        per_page: int = 20
    ) -> tuple[list, int]:
        """Get user's favorite wallpapers"""
        query = select(UserFavorite).where(UserFavorite.user_id == user_id)
        
        # Count total
        count_result = await db.execute(
            select(func.count()).select_from(UserFavorite).where(UserFavorite.user_id == user_id)
        )
        total = count_result.scalar()
        
        # Apply pagination
        query = query.order_by(desc(UserFavorite.created_at))
        query = query.offset((page - 1) * per_page).limit(per_page)
        
        result = await db.execute(query)
        favorites = result.scalars().all()
        
        return favorites, total
    
    @staticmethod
    async def is_wallpaper_favorited(db: AsyncSession, user_id: str, wallpaper_id: str) -> bool:
        """Check if wallpaper is favorited by user"""
        result = await db.execute(
            select(UserFavorite).where(
                (UserFavorite.user_id == user_id) &
                (UserFavorite.wallpaper_id == wallpaper_id)
            )
        )
        return result.scalar_one_or_none() is not None
    
    @staticmethod
    async def add_favorite(db: AsyncSession, user_id: str, wallpaper_id: str) -> Optional[UserFavorite]:
        """Add wallpaper to favorites"""
        # Check if already favorited
        if await UserService.is_wallpaper_favorited(db, user_id, wallpaper_id):
            return None
        
        # Check if wallpaper exists
        wallpaper = await db.execute(
            select(Wallpaper).where(Wallpaper.id == wallpaper_id)
        )
        if not wallpaper.scalar_one_or_none():
            return None
        
        favorite = UserFavorite(
            id=str(uuid4()),
            user_id=user_id,
            wallpaper_id=wallpaper_id
        )
        
        db.add(favorite)
        await db.commit()
        await db.refresh(favorite)
        return favorite
    
    @staticmethod
    async def remove_favorite(db: AsyncSession, favorite_id: str) -> bool:
        """Remove from favorites"""
        result = await db.execute(
            select(UserFavorite).where(UserFavorite.id == favorite_id)
        )
        favorite = result.scalar_one_or_none()
        
        if not favorite:
            return False
        
        await db.delete(favorite)
        await db.commit()
        return True
