"""
Daily theme model for database
"""

from sqlalchemy import Column, String, Text, Integer, Date, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSON
from sqlalchemy.orm import relationship
import uuid
from datetime import date

from src.models.base import BaseModel


class DailyTheme(BaseModel):
    """
    Daily theme representing the daily wallpaper collection
    """
    
    __tablename__ = "daily_themes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    short_description = Column(String(500), nullable=True)
    theme_date = Column(Date, nullable=False, unique=True, index=True)
    category = Column(String(100), nullable=False)  # region, heritage, landmark, etc.
    image_count = Column(Integer, default=10, nullable=False)
    
    # Content
    historical_narrative = Column(Text, nullable=True)
    cultural_significance = Column(Text, nullable=True)
    tags = Column(ARRAY(String), nullable=True)  # ["Moscow", "Architecture", "Historical"]
    metadata = Column(JSON, nullable=True)  # Additional metadata
    
    # Media
    cover_image_url = Column(Text, nullable=True)
    cover_image_key = Column(String(255), nullable=True)  # S3 key
    
    # Status
    is_published = Column(String, default=False, nullable=False)
    is_featured = Column(String, default=False, nullable=False)
    
    # Relationships
    wallpapers = relationship("Wallpaper", back_populates="theme", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<DailyTheme(id={self.id}, title={self.title}, date={self.theme_date})>"
