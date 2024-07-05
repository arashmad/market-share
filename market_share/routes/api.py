"""
Market Share.

A python-based FastAPI web API for calculating the market share for retails in an area.
"""

from fastapi import APIRouter
from market_share.routes.endpoints import market_share

api_router = APIRouter()

api_router.include_router(market_share.router, prefix="/market")
