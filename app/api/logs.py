"""
API endpoints for log management: ingestion, retrieval, and statistics."""

import os
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.log_entry import LogEntry
from app.schemas.directory import DirectoryIn
from app.schemas.log_entry import LogEntryOut, LogStatsOut, PaginatedLogs
from app.services.log_ingestion import ingest_logs

router = APIRouter(prefix="/logs", tags=["Logs"])


def get_db():
    """
    Dependency to get DB session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/ingest")
def ingest_directory(payload: DirectoryIn, db: Session = Depends(get_db)):
    """
    Ingest logs from the specified directory
    """
    if not os.path.isdir(payload.path):
        raise HTTPException(status_code=400, detail="Invalid directory path")

    return ingest_logs(payload.path, db)


@router.get("", response_model=PaginatedLogs)
def get_logs(
    level: Optional[str] = Query(None),
    component: Optional[str] = Query(None),
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
):
    """
    Fetch logs with optional filters and pagination
    """
    query = db.query(LogEntry)

    if level:
        query = query.filter(LogEntry.level == level)

    if component:
        query = query.filter(LogEntry.component == component)

    if start_time:
        query = query.filter(LogEntry.timestamp >= start_time)

    if end_time:
        query = query.filter(LogEntry.timestamp <= end_time)

    total = query.count()

    offset = (page - 1) * page_size
    logs = query.order_by(LogEntry.timestamp).offset(offset).limit(page_size).all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "data": logs,
    }


@router.get("/stats", response_model=LogStatsOut)
def get_log_stats(db: Session = Depends(get_db)):
    """
    Get aggregated log statistics
    """

    total_logs = db.query(func.count(LogEntry.id)).scalar()

    level_counts = (
        db.query(LogEntry.level, func.count(LogEntry.id)).group_by(LogEntry.level).all()
    )

    component_counts = (
        db.query(LogEntry.component, func.count(LogEntry.id))
        .group_by(LogEntry.component)
        .all()
    )

    return {
        "total_logs": total_logs,
        "logs_by_level": {level: count for level, count in level_counts},
        "logs_by_component": {
            component: count for component, count in component_counts
        },
    }
