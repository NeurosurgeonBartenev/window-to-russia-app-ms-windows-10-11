"""
Theme routes
"""

import logging
from datetime import date
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload

from src.database.database import get_db
from src.models.theme import DailyTheme
from src.models.wallpaper import Wallpaper
from src.schemas.theme import (
    DailyThemeResponse,
    DailyThemeDetailResponse,
    DailyThemeCreate,
    WallpaperResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(tags=["themes"])


@router.get("/today", response_model=Optional[DailyThemeDetailResponse])
async def get_today_theme(db: AsyncSession = Depends(get_db)):
    """
    Get today's theme with all wallpapers
    """
    from datetime import date
    
    today = date.today()
    result = await db.execute(
        select(DailyTheme)
        .where(DailyTheme.theme_date == today)
        .options(selectinload(DailyTheme.wallpapers))
    )
    theme = result.scalar_one_or_none()
    
    if not theme:
        logger.warning(f"No theme found for today: {today}")
        return None
    
    return DailyThemeDetailResponse.from_orm(theme)


@router.get("/{theme_id}", response_model=DailyThemeDetailResponse)
async def get_theme(
    theme_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Get theme by ID with all wallpapers
    """
    result = await db.execute(
        select(DailyTheme)
        .where(DailyTheme.id == theme_id)
        .options(selectinload(DailyTheme.wallpapers))
    )
    theme = result.scalar_one_or_none()
    
    if not theme:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Theme not found"
        )
    
    return DailyThemeDetailResponse.from_orm(theme)


@router.get("", response_model=List[DailyThemeResponse])
async def list_themes(
    skip: int = 0,
    limit: int = 30,
    category: Optional[str] = None,
    featured_only: bool = False,
    db: AsyncSession = Depends(get_db)
):
    """
    List all published themes with pagination
    """
    query = select(DailyTheme).where(DailyTheme.is_published == True)
    
    if category:
        query = query.where(DailyTheme.category == category)
    
    if featured_only:
        query = query.where(DailyTheme.is_featured == True)
    
    query = query.order_by(desc(DailyTheme.theme_date)).offset(skip).limit(limit)
    
    result = await db.execute(query)
    themes = result.scalars().all()
    
    return [DailyThemeResponse.from_orm(theme) for theme in themes]


@router.get("/search/by-date")
async def search_themes_by_date(
    date_from: date,
    date_to: Optional[date] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Search themes by date range
    """
    if not date_to:
        date_to = date_from
    
    result = await db.execute(
        select(DailyTheme)
        .where(
            (DailyTheme.theme_date >= date_from) &
            (DailyTheme.theme_date <= date_to) &
            (DailyTheme.is_published == True)
        )
        .order_by(desc(DailyTheme.theme_date))
    )
    themes = result.scalars().all()
    
    return [DailyThemeResponse.from_orm(theme) for theme in themes]


@router.post("", response_model=DailyThemeDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_theme(
    theme_data: DailyThemeCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new daily theme (admin only)
    """
    # Check if theme already exists for this date
    result = await db.execute(
        select(DailyTheme).where(DailyTheme.theme_date == theme_data.theme_date)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Theme already exists for this date"
        )
    
    new_theme = DailyTheme(
        title=theme_data.title,
        description=theme_data.description,
        short_description=theme_data.short_description,
        theme_date=theme_data.theme_date,
        category=theme_data.category,
        historical_narrative=theme_data.historical_narrative,
        cultural_significance=theme_data.cultural_significance,
        tags=theme_data.tags,
    )
    
    db.add(new_theme)
    await db.commit()
    await db.refresh(new_theme)
    
    logger.info(f"Theme created: {new_theme.id}")
    return DailyThemeDetailResponse.from_orm(new_theme)
