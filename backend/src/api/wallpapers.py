from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_db
from services.auth_service import AuthService
from services.wallpaper_service import WallpaperService
from schemas.schemas import DailyThemeResponse, WallpaperDetailResponse, PaginatedResponse
from models.models import Wallpaper
from sqlalchemy import select

router = APIRouter()

@router.get("/today", response_model=DailyThemeResponse)
async def get_today_theme(
    language: str = Query("en", min_length=2, max_length=2),
    db: AsyncSession = Depends(get_db)
):
    """Get today's wallpaper theme"""
    theme = await WallpaperService.get_today_theme(db, language)
    
    if not theme:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Today's theme not found"
        )
    
    return theme

@router.get("/{wallpaper_id}", response_model=WallpaperDetailResponse)
async def get_wallpaper(
    wallpaper_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get wallpaper by ID"""
    wallpaper = await WallpaperService.get_wallpaper_by_id(db, wallpaper_id)
    
    if not wallpaper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallpaper not found"
        )
    
    return WallpaperDetailResponse(
        id=wallpaper.id,
        title=wallpaper.title,
        description=wallpaper.description,
        image_url=wallpaper.image_url,
        thumbnail_url=wallpaper.thumbnail_url,
        image_4k_url=wallpaper.image_4k_url,
        image_2k_url=wallpaper.image_2k_url,
        image_1440p_url=wallpaper.image_1440p_url,
        location={
            "name": wallpaper.location_name,
            "latitude": wallpaper.location_latitude,
            "longitude": wallpaper.location_longitude,
            "description": wallpaper.location_description,
            "google_maps_url": wallpaper.google_maps_url
        } if wallpaper.location_name else None,
        order_index=wallpaper.order_index,
        created_at=wallpaper.created_at
    )

@router.get("/archive", response_model=PaginatedResponse)
async def get_archive(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    month: str = Query(None),
    region: str = Query(None),
    category: str = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """Get wallpaper archive"""
    themes, total = await WallpaperService.get_archive(
        db,
        page=page,
        per_page=per_page,
        month=month,
        region=region,
        category=category
    )
    
    total_pages = (total + per_page - 1) // per_page
    
    return PaginatedResponse(
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_previous=page > 1,
        data=[
            {
                "id": str(theme.id),
                "date": theme.date,
                "title": theme.title,
                "region": theme.region,
                "category": theme.category,
                "featured_image_url": theme.featured_image_url
            }
            for theme in themes
        ]
    )

@router.get("/search", response_model=PaginatedResponse)
async def search_wallpapers(
    q: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Search wallpapers"""
    wallpapers, total = await WallpaperService.search_wallpapers(
        db,
        q=q,
        page=page,
        per_page=per_page
    )
    
    total_pages = (total + per_page - 1) // per_page
    
    return PaginatedResponse(
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_previous=page > 1,
        data=[
            {
                "id": str(wallpaper.id),
                "title": wallpaper.title,
                "description": wallpaper.description,
                "image_url": wallpaper.image_url,
                "thumbnail_url": wallpaper.thumbnail_url,
                "location_name": wallpaper.location_name
            }
            for wallpaper in wallpapers
        ]
    )
