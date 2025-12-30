"""
Database model for directories.
"""

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Directory(Base):
    """
    Model representing a directory containing log files.
    """

    __tablename__ = "directories"

    id = Column(Integer, primary_key=True, index=True)
    path = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    files = relationship("LogFile", back_populates="directory")
