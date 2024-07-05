"""
Market Share.

A python-based FastAPI web API for calculating the market share for retails in an area.
"""

from pydantic import BaseModel, Field


class ResponseTemplateForPOSTRequest_MarketShare(BaseModel):
    """Response template for [POST] /market/share."""

    market_share: float = Field(
        title="Market Share",
        description="Market share calculated for retail locations.")

    model_config = {
        "json_schema_extra": {
            "title": "Response Template of Calculating Market Share",
            "example": {
                "market_share": 100.00,
            }
        }
    }
