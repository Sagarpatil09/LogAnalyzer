"""Schema for directory input data."""

from pydantic import BaseModel


class DirectoryIn(BaseModel):
    path: str
