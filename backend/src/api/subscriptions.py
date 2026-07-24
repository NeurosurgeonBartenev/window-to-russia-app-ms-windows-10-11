from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_db
from schemas.schemas import SubscriptionResponse, SubscriptionPlanResponse
from typing import List

router = APIRouter()

# Placeholder implementations

@router.get("/me", response_model=SubscriptionResponse)
async def get_subscription(db: AsyncSession = Depends(get_db)):
    """Get user subscription"""
    return {
        "id": "sub-uuid",
        "plan": "free",
        "status": "active",
        "started_at": "2026-07-24T00:00:00",
        "expires_at": None,
        "auto_renew": False
    }

@router.get("/plans", response_model=List[SubscriptionPlanResponse])
async def get_plans():
    """Get available subscription plans"""
    return [
        {
            "id": "free",
            "name": "Free",
            "price": 0,
            "currency": "USD",
            "billing_period": "month",
            "features": ["daily_wallpapers", "720p_resolution"]
        },
        {
            "id": "premium",
            "name": "Premium",
            "price": 4.99,
            "currency": "USD",
            "billing_period": "month",
            "features": ["daily_wallpapers", "4k_resolution", "unlimited_favorites"]
        }
    ]

@router.post("/subscribe")
async def subscribe(plan_id: str, db: AsyncSession = Depends(get_db)):
    """Subscribe to a plan"""
    return {"message": f"Subscribed to {plan_id}"}
