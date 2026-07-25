"""
Favorites routes
"""

import logging
from typing import List
from uuid import UUID
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.database.database import get_db
from src.models.user import User
from src.models.favorite import Favorite, PlaceToVisit
from src.models.wallpaper import Wallpaper
from src.schemas.theme import FavoriteResponse, PlaceToVisitResponse, PlaceToVisitCreate
from src.routes.users import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(tags=["favorites"])


@router.get("/wallpapers", response_model=List[FavoriteResponse])
async def get_favorite_wallpapers(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get user's favorite wallpapers
    """
    result = await db.execute(
        select(Favorite)
        .where(Favorite.user_id == current_user.id)
        .options(selectinload(Favorite.wallpaper))
    )
    favorites = result.scalars().all()
    
    return [FavoriteResponse.from_orm(fav) for fav in favorites]


@router.post("/wallpapers/{wallpaper_id}")
async def add_to_favorites(
    wallpaper_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Add wallpaper to favorites
    """
    # Check if wallpaper exists
    result = await db.execute(
        select(Wallpaper).where(Wallpaper.id == wallpaper_id)
    )
    wallpaper = result.scalar_one_or_none()
    if not wallpaper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallpaper not found"
        )
    
    # Check if already favorited
    result = await db.execute(
        select(Favorite).where(
            (Favorite.user_id == current_user.id) &
            (Favorite.wallpaper_id == wallpaper_id)
        )
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Wallpaper already in favorites"
        )
    
    # Add to favorites
    favorite = Favorite(
        user_id=current_user.id,
        wallpaper_id=wallpaper_id
    )
    wallpaper.favorite_count += 1
    
    db.add(favorite)
    db.add(wallpaper)
    await db.commit()
    
    logger.info(f"Wallpaper added to favorites: {wallpaper_id} by {current_user.id}")
    return {"message": "Wallpaper added to favorites"}


@router.delete("/wallpapers/{wallpaper_id}")
async def remove_from_favorites(
    wallpaper_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Remove wallpaper from favorites
    """
    result = await db.execute(
        select(Favorite).where(
            (Favorite.user_id == current_user.id) &
            (Favorite.wallpaper_id == wallpaper_id)
        )
    )
    favorite = result.scalar_one_or_none()
    
    if not favorite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Favorite not found"
        )
    
    # Update wallpaper count
    result = await db.execute(
        select(Wallpaper).where(Wallpaper.id == wallpaper_id)
    )
    wallpaper = result.scalar_one_or_none()
    if wallpaper:
        wallpaper.favorite_count = max(0, wallpaper.favorite_count - 1)
        db.add(wallpaper)
    
    await db.delete(favorite)
    await db.commit()
    
    logger.info(f"Wallpaper removed from favorites: {wallpaper_id} by {current_user.id}")
    return {"message": "Wallpaper removed from favorites"}


@router.get("/places", response_model=List[PlaceToVisitResponse])
async def get_places_to_visit(
    visited: Optional[bool] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get user's places to visit wishlist
    """
    query = select(PlaceToVisit).where(PlaceToVisit.user_id == current_user.id)
    
    if visited is not None:
        query = query.where(PlaceToVisit.visited == visited)
    
    result = await db.execute(query)
    places = result.scalars().all()
    
    return [PlaceToVisitResponse.from_orm(place) for place in places]


@router.post("/places", status_code=status.HTTP_201_CREATED)
async def add_place_to_visit(
    place_data: PlaceToVisitCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Add a place to visit wishlist
    """
    # Check if location already in wishlist
    result = await db.execute(
        select(PlaceToVisit).where(
            (PlaceToVisit.user_id == current_user.id) &
            (PlaceToVisit.location_name == place_data.location_name)
        )
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Place already in wishlist"
        )
    
    place = PlaceToVisit(
        user_id=current_user.id,
        wallpaper_id=place_data.wallpaper_id,
        location_name=place_data.location_name,
        location_description=place_data.location_description,
        latitude=place_data.latitude,
        longitude=place_data.longitude,
        address=place_data.address,
        priority=place_data.priority,
        notes=place_data.notes,
    )
    
    db.add(place)
    await db.commit()
    await db.refresh(place)
    
    logger.info(f"Place added to wishlist: {place.location_name} by {current_user.id}")
    return PlaceToVisitResponse.from_orm(place)


@router.put("/places/{place_id}")
async def update_place_to_visit(
    place_id: UUID,
    place_data: PlaceToVisitCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update a place in wishlist
    """
    result = await db.execute(
        select(PlaceToVisit).where(
            (PlaceToVisit.id == place_id) &
            (PlaceToVisit.user_id == current_user.id)
        )
    )
    place = result.scalar_one_or_none()
    
    if not place:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Place not found"
        )
    
    place.location_name = place_data.location_name
    place.location_description = place_data.location_description
    place.latitude = place_data.latitude
    place.longitude = place_data.longitude
    place.address = place_data.address
    place.priority = place_data.priority
    place.notes = place_data.notes
    
    db.add(place)
    await db.commit()
    await db.refresh(place)
    
    return PlaceToVisitResponse.from_orm(place)


@router.post("/places/{place_id}/mark-visited")
async def mark_place_visited(
    place_id: UUID,
    visit_date: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Mark place as visited
    """
    result = await db.execute(
        select(PlaceToVisit).where(
            (PlaceToVisit.id == place_id) &
            (PlaceToVisit.user_id == current_user.id)
        )
    )
    place = result.scalar_one_or_none()
    
    if not place:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Place not found"
        )
    
    place.visited = True
    place.visit_date = visit_date
    
    db.add(place)
    await db.commit()
    
    logger.info(f"Place marked as visited: {place_id}")
    return {"message": "Place marked as visited"}


@router.delete("/places/{place_id}")
async def remove_place_to_visit(
    place_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Remove place from wishlist
    """
    result = await db.execute(
        select(PlaceToVisit).where(
            (PlaceToVisit.id == place_id) &
            (PlaceToVisit.user_id == current_user.id)
        )
    )
    place = result.scalar_one_or_none()
    
    if not place:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Place not found"
        )
    
    await db.delete(place)
    await db.commit()
    
    logger.info(f"Place removed from wishlist: {place_id}")
    return {"message": "Place removed from wishlist"}
