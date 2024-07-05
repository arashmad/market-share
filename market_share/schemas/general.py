"""
Market Share.

A python-based FastAPI web API for calculating the market share for retails in an area.
"""

from pydantic import BaseModel, Field
from typing import Optional


class Message(BaseModel):
    """Template for general response."""

    msg: Optional[str] = Field(
        title="Message",
        description="Response message from API.")

    model_config = {
        "json_schema_extra": {
            "title": "Template for general response.",
            "example": {
                "msg": "Response message from API.",
            }
        }
    }
