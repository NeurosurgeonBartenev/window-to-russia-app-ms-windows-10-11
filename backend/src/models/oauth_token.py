"""
OAuth token model for database
"""

from sqlalchemy import Column, String, Text, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
import uuid

from src.models.base import BaseModel


class OAuthToken(BaseModel):
    """
    OAuth tokens for user authentication
    """
    
    __tablename__ = "oauth_tokens"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Token info
    provider = Column(String(50), nullable=False, index=True)  # google, yandex, vk, etc.
    access_token = Column(Text, nullable=False)
    refresh_token = Column(Text, nullable=True)
    id_token = Column(Text, nullable=True)
    
    # Expiration
    expires_at = Column(DateTime, nullable=True)
    refresh_expires_at = Column(DateTime, nullable=True)
    
    # Scope
    scope = Column(String(500), nullable=True)
    
    # Relationships
    user = relationship("User")
    
    def is_expired(self) -> bool:
        """
        Check if token is expired
        """
        if not self.expires_at:
            return False
        return datetime.utcnow() > self.expires_at
    
    def is_refresh_expired(self) -> bool:
        """
        Check if refresh token is expired
        """
        if not self.refresh_expires_at:
            return False
        return datetime.utcnow() > self.refresh_expires_at
    
    def __repr__(self) -> str:
        return f"<OAuthToken(user_id={self.user_id}, provider={self.provider})>"
