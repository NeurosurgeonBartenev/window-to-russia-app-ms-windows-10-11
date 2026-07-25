"""
Base model with common fields
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import declarative_base

from src.database.database import Base as DBBase


class BaseModel(DBBase):
    """
    Base model with common timestamp fields
    """
    
    __abstract__ = True
    
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
