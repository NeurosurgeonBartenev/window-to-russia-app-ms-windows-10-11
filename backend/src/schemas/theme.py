"""
Theme and wallpaper schemas for API
"""

from datetime import date, datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field


class LocationInfo(BaseModel):
    """
    Location information schema
    """
    location_name: Optional[str] = None
    location_description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: Optional[str] = None


class WallpaperBase(BaseModel):
    """
    Base wallpaper schema
    """
    title: str
    description: Optional[str] = None
    location: Optional[LocationInfo] = None
    photographer_name: Optional[str] = None
    photographer_credit: Optional[str] = None
    resolution: Optional[str] = None


class WallpaperResponse(WallpaperBase):
    """
    Wallpaper response schema
    """
    id: UUID
    image_url: str
    theme_id: UUID
    view_count: int
    like_count: int
    favorite_count: int
    is_landscape: bool
    aspect_ratio: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class DailyThemeBase(BaseModel):
    """
    Base daily theme schema
    """
    title: str = Field(..., min_length=1, max_length=255)
    description: str
    short_description: Optional[str] = None
    category: str
    historical_narrative: Optional[str] = None
    cultural_significance: Optional[str] = None


class DailyThemeCreate(DailyThemeBase):
    """
    Schema for creating a daily theme
    """
    theme_date: date
    tags: Optional[List[str]] = None


class DailyThemeResponse(DailyThemeBase):
    """
    Daily theme response schema
    """
    id: UUID
    theme_date: date
    cover_image_url: Optional[str] = None
    is_published: bool
    is_featured: bool
    image_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class DailyThemeDetailResponse(DailyThemeResponse):
    """
    Detailed daily theme response with wallpapers
    """
    wallpapers: List[WallpaperResponse] = []


class FavoriteResponse(BaseModel):
    """
    Favorite wallpaper response
    """
    id: UUID
    wallpaper: WallpaperResponse
    created_at: datetime
    
    class Config:
        from_attributes = True


class PlaceToVisitBase(BaseModel):
    """
    Base place to visit schema
    """
    location_name: str
    location_description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: Optional[str] = None
    priority: str = "medium"
    notes: Optional[str] = None


class PlaceToVisitCreate(PlaceToVisitBase):
    """
    Schema for adding a place to visit
    """
    wallpaper_id: Optional[UUID] = None


class PlaceToVisitResponse(PlaceToVisitBase):
    """
    Place to visit response schema
    """
    id: UUID
    visited: bool
    visit_date: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
