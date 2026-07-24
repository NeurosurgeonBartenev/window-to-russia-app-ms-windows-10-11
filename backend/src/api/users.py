from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_db
from services.auth_service import AuthService
from services.user_service import UserService
from services.subscription_service import SubscriptionService
from schemas.schemas import UserResponse, UserUpdate
from fastapi.security import HTTPBearer

router = APIRouter()
security = HTTPBearer()

@router.get("/me", response_model=UserResponse)
async def get_current_user(
    db: AsyncSession = Depends(get_db),
    credentials = Depends(security)
):
    """Get current authenticated user"""
    try:
        user = await AuthService.get_current_user(credentials, db)
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    return UserResponse(
        id=user.id,
        email=user.email,
        username=user.username,
        display_name=user.display_name,
        avatar_url=user.avatar_url,
        bio=user.bio,
        language=user.language,
        theme=user.theme,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at
    )

@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    credentials = Depends(security)
):
    """Update current user profile"""
    try:
        user = await AuthService.get_current_user(credentials, db)
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    updated_user = await UserService.update_user(
        db,
        str(user.id),
        display_name=user_update.display_name,
        bio=user_update.bio,
        language=user_update.language,
        theme=user_update.theme
    )
    
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse(
        id=updated_user.id,
        email=updated_user.email,
        username=updated_user.username,
        display_name=updated_user.display_name,
        avatar_url=updated_user.avatar_url,
        bio=updated_user.bio,
        language=updated_user.language,
        theme=updated_user.theme,
        is_active=updated_user.is_active,
        created_at=updated_user.created_at,
        updated_at=updated_user.updated_at
    )

@router.delete("/me", response_model=dict)
async def delete_current_user(
    db: AsyncSession = Depends(get_db),
    credentials = Depends(security)
):
    """Delete current user account"""
    try:
        user = await AuthService.get_current_user(credentials, db)
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    success = await UserService.delete_user(db, str(user.id))
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"message": "User deleted successfully"}
