"""
Wallpaper routes
"""

import logging
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from src.database.database import get_db
from src.models.wallpaper import Wallpaper
from src.models.theme import DailyTheme
from src.schemas.theme import WallpaperResponse

logger = logging.getLogger(__name__)

router = APIRouter(tags=["wallpapers"])


@router.get("/theme/{theme_id}", response_model=List[WallpaperResponse])
async def get_theme_wallpapers(
    theme_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Get all wallpapers for a specific theme
    """
    # Check if theme exists
    result = await db.execute(
        select(DailyTheme).where(DailyTheme.id == theme_id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Theme not found"
        )
    
    result = await db.execute(
        select(Wallpaper).where(Wallpaper.theme_id == theme_id)
    )
    wallpapers = result.scalars().all()
    
    return [WallpaperResponse.from_orm(wp) for wp in wallpapers]


@router.get("/{wallpaper_id}", response_model=WallpaperResponse)
async def get_wallpaper(
    wallpaper_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific wallpaper
    """
    result = await db.execute(
        select(Wallpaper).where(Wallpaper.id == wallpaper_id)
    )
    wallpaper = result.scalar_one_or_none()
    
    if not wallpaper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallpaper not found"
        )
    
    # Increment view count
    wallpaper.view_count += 1
    db.add(wallpaper)
    await db.commit()
    
    return WallpaperResponse.from_orm(wallpaper)


@router.post("/{wallpaper_id}/like")
async def like_wallpaper(
    wallpaper_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Like a wallpaper
    """
    result = await db.execute(
        select(Wallpaper).where(Wallpaper.id == wallpaper_id)
    )
    wallpaper = result.scalar_one_or_none()
    
    if not wallpaper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallpaper not found"
        )
    
    wallpaper.like_count += 1
    db.add(wallpaper)
    await db.commit()
    await db.refresh(wallpaper)
    
    logger.info(f"Wallpaper liked: {wallpaper_id}")
    return {"like_count": wallpaper.like_count}


@router.post("/search/by-location")
async def search_wallpapers_by_location(
    location_name: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Search wallpapers by location name
    """
    result = await db.execute(
        select(Wallpaper).where(
            Wallpaper.location_name.ilike(f"%{location_name}%")
        )
    )
    wallpapers = result.scalars().all()
    
    return [WallpaperResponse.from_orm(wp) for wp in wallpapers]
