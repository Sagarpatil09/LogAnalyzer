"""
Database model for log entries."""

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class LogEntry(Base):
    """
    Model representing a single log entry."""
    __tablename__ = "log_entries"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False)
    level = Column(String, index=True)
    component = Column(String, index=True)
    message = Column(String)

    file_id = Column(Integer, ForeignKey("log_files.id"))
    file = relationship("LogFile", back_populates="logs")
