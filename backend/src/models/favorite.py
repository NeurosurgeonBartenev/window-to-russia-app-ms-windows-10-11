"""
Favorite and wishlist models
"""

from sqlalchemy import Column, String, Text, Float, ForeignKey, UniqueConstraint, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from src.models.base import BaseModel


class Favorite(BaseModel):
    """
    User's favorite wallpapers
    """
    
    __tablename__ = "favorites"
    __table_args__ = (UniqueConstraint("user_id", "wallpaper_id", name="uq_user_wallpaper"),)
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    wallpaper_id = Column(UUID(as_uuid=True), ForeignKey("wallpapers.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Relationships
    user = relationship("User")
    wallpaper = relationship("Wallpaper", back_populates="favorites")
    
    def __repr__(self) -> str:
        return f"<Favorite(user_id={self.user_id}, wallpaper_id={self.wallpaper_id})>"


class PlaceToVisit(BaseModel):
    """
    User's wishlist of places to visit (from wallpaper locations)
    """
    
    __tablename__ = "places_to_visit"
    __table_args__ = (UniqueConstraint("user_id", "location_id", name="uq_user_location"),)
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    wallpaper_id = Column(UUID(as_uuid=True), ForeignKey("wallpapers.id"), nullable=True, index=True)
    
    # Location details (denormalized from wallpaper for convenience)
    location_name = Column(String(255), nullable=False)
    location_description = Column(Text, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    address = Column(Text, nullable=True)
    
    # Status tracking
    visited = Column(Boolean, default=False, nullable=False)
    visit_date = Column(String(50), nullable=True)
    notes = Column(Text, nullable=True)
    
    # Priority
    priority = Column(String(20), default="medium", nullable=False)  # low, medium, high
    
    # Relationships
    user = relationship("User")
    wallpaper = relationship("Wallpaper")
    
    def __repr__(self) -> str:
        return f"<PlaceToVisit(user_id={self.user_id}, location={self.location_name})>"
