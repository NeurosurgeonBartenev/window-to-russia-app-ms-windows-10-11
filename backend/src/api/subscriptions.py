from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_db
from services.auth_service import AuthService
from services.subscription_service import SubscriptionService
from schemas.schemas import SubscriptionResponse, SubscriptionPlanResponse
from typing import List
from fastapi.security import HTTPBearer

router = APIRouter()
security = HTTPBearer()

@router.get("/me", response_model=SubscriptionResponse)
async def get_subscription(
    db: AsyncSession = Depends(get_db),
    credentials = Depends(security)
):
    """Get user's current subscription"""
    try:
        user = await AuthService.get_current_user(credentials, db)
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    subscription = await SubscriptionService.get_user_subscription(db, str(user.id))
    
    if not subscription:
        # Create free subscription if doesn't exist
        subscription = await SubscriptionService.create_subscription(
            db,
            str(user.id),
            "free"
        )
    
    return SubscriptionResponse(
        id=subscription.id,
        plan=subscription.plan,
        status=subscription.status,
        started_at=subscription.started_at,
        expires_at=subscription.expires_at,
        auto_renew=subscription.auto_renew
    )

@router.get("/plans", response_model=List[SubscriptionPlanResponse])
async def get_plans():
    """Get available subscription plans"""
    plans = SubscriptionService.get_all_plans()
    return plans

@router.post("/subscribe", response_model=SubscriptionResponse)
async def subscribe(
    plan_id: str,
    db: AsyncSession = Depends(get_db),
    credentials = Depends(security)
):
    """Subscribe to a plan"""
    try:
        user = await AuthService.get_current_user(credentials, db)
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    # Validate plan
    if plan_id not in SubscriptionService.PLANS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid plan: {plan_id}"
        )
    
    subscription = await SubscriptionService.upgrade_subscription(
        db,
        str(user.id),
        plan_id
    )
    
    return SubscriptionResponse(
        id=subscription.id,
        plan=subscription.plan,
        status=subscription.status,
        started_at=subscription.started_at,
        expires_at=subscription.expires_at,
        auto_renew=subscription.auto_renew
    )

@router.post("/cancel", response_model=SubscriptionResponse)
async def cancel_subscription(
    db: AsyncSession = Depends(get_db),
    credentials = Depends(security)
):
    """Cancel subscription"""
    try:
        user = await AuthService.get_current_user(credentials, db)
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    subscription = await SubscriptionService.cancel_subscription(db, str(user.id))
    
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription not found"
        )
    
    return SubscriptionResponse(
        id=subscription.id,
        plan=subscription.plan,
        status=subscription.status,
        started_at=subscription.started_at,
        expires_at=subscription.expires_at,
        auto_renew=subscription.auto_renew
    )
