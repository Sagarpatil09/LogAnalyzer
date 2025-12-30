"""Schemas for log entry output and statistics."""
from datetime import datetime
from typing import Dict, List

from pydantic import BaseModel


class LogEntryOut(BaseModel):
    """
    Schema for log entry output data.
    """
    id: int
    timestamp: datetime
    level: str
    component: str
    message: str

    class Config:
        orm_mode = True


class PaginatedLogs(BaseModel):
    """
    Schema for paginated log entries."""
    total: int
    page: int
    page_size: int
    data: List[LogEntryOut]


class LogStatsOut(BaseModel):
    """
    Schema for log statistics output data."""
    total_logs: int
    logs_by_level: Dict[str, int]
    logs_by_component: Dict[str, int]
