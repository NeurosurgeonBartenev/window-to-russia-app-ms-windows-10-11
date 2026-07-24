from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from uuid import UUID

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    display_name: Optional[str] = None
    language: str = "en"
    theme: str = "dark"

class UserCreate(UserBase):
    username: str

class UserUpdate(BaseModel):
    display_name: Optional[str] = None
    bio: Optional[str] = None
    language: Optional[str] = None
    theme: Optional[str] = None

class UserResponse(UserBase):
    id: UUID
    username: str
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

# Auth Schemas
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    expires_in: int
    token_type: str = "bearer"

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    expires_in: int
    user: UserResponse

class RefreshTokenRequest(BaseModel):
    refresh_token: str

# Wallpaper Schemas
class LocationInfo(BaseModel):
    name: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    description: Optional[str] = None
    google_maps_url: Optional[str] = None

class WallpaperResponse(BaseModel):
    id: UUID
    title: str
    description: Optional[str] = None
    image_url: str
    thumbnail_url: Optional[str] = None
    location: Optional[LocationInfo] = None
    order_index: int
    created_at: datetime

class WallpaperDetailResponse(WallpaperResponse):
    image_4k_url: Optional[str] = None
    image_2k_url: Optional[str] = None
    image_1440p_url: Optional[str] = None

# Daily Theme Schemas
class DailyThemeResponse(BaseModel):
    id: UUID
    date: datetime
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    region: Optional[str] = None
    featured_image_url: Optional[str] = None
    wallpapers_count: int = 0
    wallpapers: List[WallpaperResponse] = []

# Favorite Schemas
class FavoriteCreate(BaseModel):
    wallpaper_id: UUID

class FavoriteResponse(BaseModel):
    id: UUID
    wallpaper_id: UUID
    created_at: datetime

# Place Schemas
class PlaceCreate(BaseModel):
    location_name: str
    location_latitude: Optional[float] = None
    location_longitude: Optional[float] = None
    theme_id: Optional[UUID] = None

class PlaceUpdate(BaseModel):
    visited: Optional[bool] = None

class PlaceResponse(BaseModel):
    id: UUID
    location_name: str
    location_latitude: Optional[float] = None
    location_longitude: Optional[float] = None
    visited: bool
    created_at: datetime

# Subscription Schemas
class SubscriptionResponse(BaseModel):
    id: UUID
    plan: str
    status: str
    started_at: datetime
    expires_at: Optional[datetime] = None
    auto_renew: bool

class SubscriptionPlanResponse(BaseModel):
    id: str
    name: str
    price: float
    currency: str
    billing_period: str  # month, year
    features: List[str]

# Pagination
class PaginationParams(BaseModel):
    page: int = 1
    per_page: int = 20
    
    @property
    def skip(self) -> int:
        return (self.page - 1) * self.per_page
    
    @property
    def limit(self) -> int:
        return self.per_page

class PaginatedResponse(BaseModel):
    total: int
    page: int
    per_page: int
    total_pages: int
    has_next: bool
    has_previous: bool
    data: List[dict]
