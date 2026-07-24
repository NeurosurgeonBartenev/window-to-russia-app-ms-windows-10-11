from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_db
from services.auth_service import AuthService
from services.place_service import PlaceService
from schemas.schemas import PlaceCreate, PlaceUpdate, PaginatedResponse
from fastapi.security import HTTPBearer

router = APIRouter()
security = HTTPBearer()

@router.get("/", response_model=PaginatedResponse)
async def get_places(
    visited: bool = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    credentials = Depends(security)
):
    """Get user's places wishlist"""
    try:
        user = await AuthService.get_current_user(credentials, db)
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    places, total = await PlaceService.get_user_places(
        db,
        str(user.id),
        visited=visited,
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
                "id": str(place.id),
                "location_name": place.location_name,
                "location_latitude": place.location_latitude,
                "location_longitude": place.location_longitude,
                "visited": place.visited,
                "created_at": place.created_at
            }
            for place in places
        ]
    )

@router.post("/", response_model=dict)
async def add_place(
    place: PlaceCreate,
    db: AsyncSession = Depends(get_db),
    credentials = Depends(security)
):
    """Add place to wishlist"""
    try:
        user = await AuthService.get_current_user(credentials, db)
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    new_place = await PlaceService.add_place(
        db,
        str(user.id),
        place.location_name,
        place.location_latitude,
        place.location_longitude,
        place.theme_id
    )
    
    return {
        "id": str(new_place.id),
        "location_name": new_place.location_name,
        "location_latitude": new_place.location_latitude,
        "location_longitude": new_place.location_longitude,
        "visited": new_place.visited,
        "created_at": new_place.created_at
    }

@router.put("/{place_id}", response_model=dict)
async def update_place(
    place_id: str,
    place_update: PlaceUpdate,
    db: AsyncSession = Depends(get_db),
    credentials = Depends(security)
):
    """Update place status"""
    try:
        user = await AuthService.get_current_user(credentials, db)
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    updated_place = await PlaceService.update_place(
        db,
        place_id,
        visited=place_update.visited
    )
    
    if not updated_place:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Place not found"
        )
    
    return {
        "id": str(updated_place.id),
        "location_name": updated_place.location_name,
        "visited": updated_place.visited,
        "updated_at": updated_place.updated_at
    }

@router.delete("/{place_id}", response_model=dict)
async def delete_place(
    place_id: str,
    db: AsyncSession = Depends(get_db),
    credentials = Depends(security)
):
    """Delete place from wishlist"""
    try:
        user = await AuthService.get_current_user(credentials, db)
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    success = await PlaceService.delete_place(db, place_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Place not found"
        )
    
    return {"message": "Deleted from wishlist"}
