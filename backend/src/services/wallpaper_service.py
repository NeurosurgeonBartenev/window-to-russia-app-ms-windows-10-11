from typing import Optional, List
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func
from datetime import datetime
from models.models import DailyTheme, Wallpaper
from schemas.schemas import DailyThemeResponse, WallpaperResponse

class WallpaperService:
    @staticmethod
    async def get_today_theme(db: AsyncSession, language: str = "en") -> Optional[DailyThemeResponse]:
        """Get today's daily theme with wallpapers"""
        today = datetime.utcnow().date()
        
        result = await db.execute(
            select(DailyTheme)
            .where(DailyTheme.published_at.isnot(None))
            .order_by(desc(DailyTheme.date))
            .limit(1)
        )
        theme = result.scalar_one_or_none()
        
        if not theme:
            return None
        
        # Get wallpapers for this theme
        wallpapers_result = await db.execute(
            select(Wallpaper)
            .where(Wallpaper.theme_id == theme.id)
            .order_by(Wallpaper.order_index)
        )
        wallpapers = wallpapers_result.scalars().all()
        
        return DailyThemeResponse(
            id=theme.id,
            date=theme.date,
            title=theme.title,
            description=theme.description,
            category=theme.category,
            region=theme.region,
            featured_image_url=theme.featured_image_url,
            wallpapers_count=len(wallpapers),
            wallpapers=[WallpaperResponse(
                id=w.id,
                title=w.title,
                description=w.description,
                image_url=w.image_url,
                thumbnail_url=w.thumbnail_url,
                location={
                    "name": w.location_name,
                    "latitude": w.location_latitude,
                    "longitude": w.location_longitude,
                    "description": w.location_description,
                    "google_maps_url": w.google_maps_url
                } if w.location_name else None,
                order_index=w.order_index,
                created_at=w.created_at
            ) for w in wallpapers]
        )
    
    @staticmethod
    async def get_wallpaper_by_id(db: AsyncSession, wallpaper_id: str) -> Optional[Wallpaper]:
        """Get wallpaper by ID"""
        result = await db.execute(
            select(Wallpaper).where(Wallpaper.id == wallpaper_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_archive(
        db: AsyncSession,
        page: int = 1,
        per_page: int = 20,
        month: Optional[str] = None,
        region: Optional[str] = None,
        category: Optional[str] = None
    ) -> tuple[List[DailyTheme], int]:
        """Get wallpaper archive with pagination and filters"""
        query = select(DailyTheme).where(DailyTheme.published_at.isnot(None))
        
        if month:
            # Filter by month (format: 2026-07)
            year, month_num = month.split('-')
            query = query.where(
                func.extract('year', DailyTheme.date) == int(year),
                func.extract('month', DailyTheme.date) == int(month_num)
            )
        
        if region:
            query = query.where(DailyTheme.region == region)
        
        if category:
            query = query.where(DailyTheme.category == category)
        
        # Count total
        count_result = await db.execute(
            select(func.count()).select_from(DailyTheme).select_entity_from(query)
        )
        total = count_result.scalar()
        
        # Apply ordering and pagination
        query = query.order_by(desc(DailyTheme.date))
        query = query.offset((page - 1) * per_page).limit(per_page)
        
        result = await db.execute(query)
        themes = result.scalars().all()
        
        return themes, total
    
    @staticmethod
    async def search_wallpapers(
        db: AsyncSession,
        q: str,
        page: int = 1,
        per_page: int = 20
    ) -> tuple[List[Wallpaper], int]:
        """Search wallpapers by title or description"""
        from sqlalchemy import or_
        
        query = select(Wallpaper).where(
            or_(
                Wallpaper.title.ilike(f"%{q}%"),
                Wallpaper.description.ilike(f"%{q}%"),
                Wallpaper.location_name.ilike(f"%{q}%")
            )
        )
        
        # Count total
        count_result = await db.execute(
            select(func.count()).select_from(Wallpaper).select_entity_from(query)
        )
        total = count_result.scalar()
        
        # Apply pagination
        query = query.order_by(desc(Wallpaper.created_at))
        query = query.offset((page - 1) * per_page).limit(per_page)
        
        result = await db.execute(query)
        wallpapers = result.scalars().all()
        
        return wallpapers, total
