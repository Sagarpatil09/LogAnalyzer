"""
Database model for log files.
"""
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class LogFile(Base):
    __tablename__ = "log_files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    directory_id = Column(Integer, ForeignKey("directories.id"))
    processed_at = Column(DateTime, server_default=func.now())

    directory = relationship("Directory", back_populates="files")
    logs = relationship("LogEntry", back_populates="file")
