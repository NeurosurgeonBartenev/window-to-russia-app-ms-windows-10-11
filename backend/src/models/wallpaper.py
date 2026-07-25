"""
Wallpaper model for database
"""

from sqlalchemy import Column, String, Text, Float, ForeignKey, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import relationship
import uuid

from src.models.base import BaseModel


class Wallpaper(BaseModel):
    """
    Individual wallpaper representing a single image in a daily theme
    """
    
    __tablename__ = "wallpapers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    theme_id = Column(UUID(as_uuid=True), ForeignKey("daily_themes.id"), nullable=False, index=True)
    
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Image details
    image_url = Column(Text, nullable=False)
    image_key = Column(String(255), nullable=False, unique=True)  # S3 key
    image_width = Column(Integer, nullable=True)
    image_height = Column(Integer, nullable=True)
    image_size_mb = Column(Float, nullable=True)  # Size in MB
    format = Column(String(10), default="JPEG", nullable=False)  # JPEG, PNG, WEBP
    
    # Location information
    location_name = Column(String(255), nullable=True)
    location_description = Column(Text, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    address = Column(Text, nullable=True)
    
    # Metadata
    photographer_name = Column(String(255), nullable=True)
    photographer_credit = Column(Text, nullable=True)
    copyright_info = Column(Text, nullable=True)
    taken_date = Column(String(50), nullable=True)  # May be approximate
    
    # Additional info
    tags = Column(String(500), nullable=True)  # Comma-separated or JSON
    is_landscape = Column(Boolean, default=True, nullable=False)
    aspect_ratio = Column(String(20), nullable=True)  # "16:9", "4:3", etc.
    resolution = Column(String(50), nullable=True)  # "4K", "8K", etc.
    
    # Statistics
    view_count = Column(Integer, default=0, nullable=False)
    like_count = Column(Integer, default=0, nullable=False)
    favorite_count = Column(Integer, default=0, nullable=False)
    
    # Relationships
    theme = relationship("DailyTheme", back_populates="wallpapers")
    favorites = relationship("Favorite", back_populates="wallpaper", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Wallpaper(id={self.id}, title={self.title}, theme_id={self.theme_id})>"
