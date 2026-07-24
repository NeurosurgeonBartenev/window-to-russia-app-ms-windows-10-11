from sqlalchemy import Column, String, DateTime, UUID, Boolean, Integer, Float, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from config.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    display_name = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    language = Column(String, default="en")
    theme = Column(String, default="dark")  # dark/light
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    social_logins = relationship("SocialLogin", back_populates="user")
    favorites = relationship("UserFavorite", back_populates="user")
    places = relationship("PlaceWishlist", back_populates="user")
    subscriptions = relationship("Subscription", back_populates="user")

class SocialLogin(Base):
    __tablename__ = "social_logins"
    
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    provider = Column(String, nullable=False)  # google, yandex, etc
    provider_id = Column(String, nullable=False)
    access_token = Column(String, nullable=True)
    refresh_token = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="social_logins")

class DailyTheme(Base):
    __tablename__ = "daily_themes"
    
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    date = Column(DateTime, unique=True, nullable=False, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String, nullable=True)  # Cities, Heritage, Nature, etc
    region = Column(String, nullable=True)  # Region of Russia
    featured_image_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    published_at = Column(DateTime, nullable=True)
    
    # Relationships
    wallpapers = relationship("Wallpaper", back_populates="theme")

class Wallpaper(Base):
    __tablename__ = "wallpapers"
    
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    theme_id = Column(UUID, ForeignKey("daily_themes.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String, nullable=False)
    thumbnail_url = Column(String, nullable=True)
    image_4k_url = Column(String, nullable=True)
    image_2k_url = Column(String, nullable=True)
    image_1440p_url = Column(String, nullable=True)
    location_name = Column(String, nullable=True)
    location_description = Column(Text, nullable=True)
    location_latitude = Column(Float, nullable=True)
    location_longitude = Column(Float, nullable=True)
    google_maps_url = Column(String, nullable=True)
    order_index = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    theme = relationship("DailyTheme", back_populates="wallpapers")
    favorites = relationship("UserFavorite", back_populates="wallpaper")

class UserFavorite(Base):
    __tablename__ = "user_favorites"
    
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    wallpaper_id = Column(UUID, ForeignKey("wallpapers.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="favorites")
    wallpaper = relationship("Wallpaper", back_populates="favorites")

class PlaceWishlist(Base):
    __tablename__ = "places_wishlist"
    
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    location_name = Column(String, nullable=False)
    location_latitude = Column(Float, nullable=True)
    location_longitude = Column(Float, nullable=True)
    theme_id = Column(UUID, ForeignKey("daily_themes.id"), nullable=True)
    visited = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="places")

class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False, unique=True)
    plan = Column(String, default="free")  # free, premium, pro
    status = Column(String, default="active")  # active, expired, cancelled
    started_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    auto_renew = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="subscriptions")
