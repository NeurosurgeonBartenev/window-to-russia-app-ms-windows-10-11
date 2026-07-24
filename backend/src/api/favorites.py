from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_db
from services.auth_service import AuthService
from services.user_service import UserService
from schemas.schemas import FavoriteCreate, PaginatedResponse
from fastapi.security import HTTPBearer

router = APIRouter()
security = HTTPBearer()

@router.get("/", response_model=PaginatedResponse)
async def get_favorites(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    credentials = Depends(security)
):
    """Get user's favorite wallpapers"""
    try:
        user = await AuthService.get_current_user(credentials, db)
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    favorites, total = await UserService.get_user_favorites(
        db,
        str(user.id),
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
                "id": str(fav.id),
                "wallpaper_id": str(fav.wallpaper_id),
                "created_at": fav.created_at
            }
            for fav in favorites
        ]
    )

@router.post("/", response_model=dict)
async def add_favorite(
    favorite: FavoriteCreate,
    db: AsyncSession = Depends(get_db),
    credentials = Depends(security)
):
    """Add wallpaper to favorites"""
    try:
        user = await AuthService.get_current_user(credentials, db)
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    # Check if already favorited
    is_favorited = await UserService.is_wallpaper_favorited(
        db,
        str(user.id),
        str(favorite.wallpaper_id)
    )
    
    if is_favorited:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wallpaper already in favorites"
        )
    
    new_favorite = await UserService.add_favorite(
        db,
        str(user.id),
        str(favorite.wallpaper_id)
    )
    
    if not new_favorite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallpaper not found"
        )
    
    return {
        "id": str(new_favorite.id),
        "wallpaper_id": str(new_favorite.wallpaper_id),
        "created_at": new_favorite.created_at
    }

@router.delete("/{favorite_id}", response_model=dict)
async def remove_favorite(
    favorite_id: str,
    db: AsyncSession = Depends(get_db),
    credentials = Depends(security)
):
    """Remove from favorites"""
    try:
        user = await AuthService.get_current_user(credentials, db)
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    success = await UserService.remove_favorite(db, favorite_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Favorite not found"
        )
    
    return {"message": "Removed from favorites"}
