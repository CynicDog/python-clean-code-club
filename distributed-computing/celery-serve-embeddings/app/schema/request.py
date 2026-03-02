"""Pydantic schemas for AI Inference requests."""

from pydantic import BaseModel
from typing import List, Optional, Any


class TextRequest(BaseModel):
    """Schema for submitting text for embedding."""

    text: str


class TaskResponse(BaseModel):
    """Initial response after triggering a task."""

    task_id: str
    status: str


class ResultResponse(BaseModel):
    """Schema for the final embedding result."""

    task_id: str
    status: str
    data: Optional[Any] = None
    error: Optional[str] = None
