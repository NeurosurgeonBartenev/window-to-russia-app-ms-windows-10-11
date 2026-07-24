from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func
from uuid import uuid4
from datetime import datetime
from models.models import PlaceWishlist

class PlaceService:
    @staticmethod
    async def get_user_places(
        db: AsyncSession,
        user_id: str,
        visited: Optional[bool] = None,
        page: int = 1,
        per_page: int = 20
    ) -> tuple[List[PlaceWishlist], int]:
        """Get user's places wishlist"""
        query = select(PlaceWishlist).where(PlaceWishlist.user_id == user_id)
        
        if visited is not None:
            query = query.where(PlaceWishlist.visited == visited)
        
        # Count total
        count_query = select(func.count()).select_from(PlaceWishlist).where(PlaceWishlist.user_id == user_id)
        if visited is not None:
            count_query = count_query.where(PlaceWishlist.visited == visited)
        
        count_result = await db.execute(count_query)
        total = count_result.scalar()
        
        # Apply pagination
        query = query.order_by(desc(PlaceWishlist.created_at))
        query = query.offset((page - 1) * per_page).limit(per_page)
        
        result = await db.execute(query)
        places = result.scalars().all()
        
        return places, total
    
    @staticmethod
    async def add_place(
        db: AsyncSession,
        user_id: str,
        location_name: str,
        location_latitude: Optional[float] = None,
        location_longitude: Optional[float] = None,
        theme_id: Optional[str] = None
    ) -> PlaceWishlist:
        """Add place to wishlist"""
        place = PlaceWishlist(
            id=str(uuid4()),
            user_id=user_id,
            location_name=location_name,
            location_latitude=location_latitude,
            location_longitude=location_longitude,
            theme_id=theme_id,
            visited=False
        )
        
        db.add(place)
        await db.commit()
        await db.refresh(place)
        return place
    
    @staticmethod
    async def update_place(
        db: AsyncSession,
        place_id: str,
        visited: Optional[bool] = None
    ) -> Optional[PlaceWishlist]:
        """Update place status"""
        result = await db.execute(
            select(PlaceWishlist).where(PlaceWishlist.id == place_id)
        )
        place = result.scalar_one_or_none()
        
        if not place:
            return None
        
        if visited is not None:
            place.visited = visited
        
        place.updated_at = datetime.utcnow()
        
        await db.commit()
        await db.refresh(place)
        return place
    
    @staticmethod
    async def delete_place(db: AsyncSession, place_id: str) -> bool:
        """Delete place from wishlist"""
        result = await db.execute(
            select(PlaceWishlist).where(PlaceWishlist.id == place_id)
        )
        place = result.scalar_one_or_none()
        
        if not place:
            return False
        
        await db.delete(place)
        await db.commit()
        return True
