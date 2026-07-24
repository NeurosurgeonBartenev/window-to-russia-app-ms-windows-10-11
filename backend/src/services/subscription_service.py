from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import uuid4
from datetime import datetime, timedelta
from models.models import Subscription

class SubscriptionService:
    PLANS = {
        "free": {
            "name": "Free",
            "price": 0,
            "currency": "USD",
            "billing_period": "month",
            "features": [
                "daily_wallpapers",
                "720p_resolution",
                "5_favorites"
            ]
        },
        "premium": {
            "name": "Premium",
            "price": 4.99,
            "currency": "USD",
            "billing_period": "month",
            "features": [
                "daily_wallpapers",
                "4k_resolution",
                "unlimited_favorites",
                "priority_support",
                "ad_free"
            ]
        },
        "pro": {
            "name": "Pro",
            "price": 9.99,
            "currency": "USD",
            "billing_period": "month",
            "features": [
                "daily_wallpapers",
                "8k_resolution",
                "unlimited_favorites",
                "priority_support",
                "ad_free",
                "custom_themes",
                "early_access"
            ]
        }
    }
    
    @staticmethod
    async def get_user_subscription(db: AsyncSession, user_id: str) -> Optional[Subscription]:
        """Get user's current subscription"""
        result = await db.execute(
            select(Subscription).where(Subscription.user_id == user_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def create_subscription(
        db: AsyncSession,
        user_id: str,
        plan: str = "free"
    ) -> Subscription:
        """Create a new subscription for user"""
        subscription = Subscription(
            id=str(uuid4()),
            user_id=user_id,
            plan=plan,
            status="active",
            started_at=datetime.utcnow(),
            expires_at=None if plan == "free" else datetime.utcnow() + timedelta(days=30),
            auto_renew=True if plan != "free" else False
        )
        
        db.add(subscription)
        await db.commit()
        await db.refresh(subscription)
        return subscription
    
    @staticmethod
    async def upgrade_subscription(
        db: AsyncSession,
        user_id: str,
        new_plan: str
    ) -> Optional[Subscription]:
        """Upgrade user's subscription"""
        subscription = await SubscriptionService.get_user_subscription(db, user_id)
        
        if not subscription:
            return await SubscriptionService.create_subscription(db, user_id, new_plan)
        
        subscription.plan = new_plan
        subscription.status = "active"
        subscription.started_at = datetime.utcnow()
        subscription.expires_at = datetime.utcnow() + timedelta(days=30) if new_plan != "free" else None
        subscription.auto_renew = True if new_plan != "free" else False
        
        await db.commit()
        await db.refresh(subscription)
        return subscription
    
    @staticmethod
    async def cancel_subscription(db: AsyncSession, user_id: str) -> Optional[Subscription]:
        """Cancel user's subscription"""
        subscription = await SubscriptionService.get_user_subscription(db, user_id)
        
        if not subscription:
            return None
        
        subscription.status = "cancelled"
        subscription.auto_renew = False
        
        await db.commit()
        await db.refresh(subscription)
        return subscription
    
    @staticmethod
    def get_plan_details(plan: str) -> dict:
        """Get plan details"""
        return SubscriptionService.PLANS.get(plan, SubscriptionService.PLANS["free"])
    
    @staticmethod
    def get_all_plans() -> List[dict]:
        """Get all available plans"""
        plans = []
        for plan_id, plan_data in SubscriptionService.PLANS.items():
            plans.append({
                "id": plan_id,
                **plan_data
            })
        return plans
