"""
User model for database
"""

from sqlalchemy import Column, String, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid

from src.models.base import BaseModel


class User(BaseModel):
    """
    User model representing application users
    """
    
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=True)  # Nullable for OAuth users
    full_name = Column(String(255), nullable=True)
    avatar_url = Column(Text, nullable=True)
    language = Column(String(10), default="en", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    is_premium = Column(Boolean, default=False, nullable=False)
    bio = Column(Text, nullable=True)
    
    # OAuth provider IDs
    google_id = Column(String(255), unique=True, nullable=True, index=True)
    yandex_id = Column(String(255), unique=True, nullable=True, index=True)
    vk_id = Column(String(255), unique=True, nullable=True, index=True)
    microsoft_id = Column(String(255), unique=True, nullable=True, index=True)
    apple_id = Column(String(255), unique=True, nullable=True, index=True)
    x_id = Column(String(255), unique=True, nullable=True, index=True)
    wechat_id = Column(String(255), unique=True, nullable=True, index=True)
    qq_id = Column(String(255), unique=True, nullable=True, index=True)
    whatsapp_id = Column(String(255), unique=True, nullable=True, index=True)
    telegram_id = Column(String(255), unique=True, nullable=True, index=True)
    snapchat_id = Column(String(255), unique=True, nullable=True, index=True)
    instagram_id = Column(String(255), unique=True, nullable=True, index=True)
    line_id = Column(String(255), unique=True, nullable=True, index=True)
    kakao_id = Column(String(255), unique=True, nullable=True, index=True)
    facebook_id = Column(String(255), unique=True, nullable=True, index=True)
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"
