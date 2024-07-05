"""
Market Share.

A python-based FastAPI web API for calculating the market share for retails in an area.
"""

from fastapi import APIRouter, HTTPException, Security, UploadFile, File, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse

from market_share.utils.auth import is_user
from market_share.utils.main import MarketShare

import market_share.schemas.general as schema_general
import market_share.schemas.market_share as market_share_general

router = APIRouter()
security = HTTPBearer()

TAG = ['Market Share']


@router.post('/share', tags=TAG,
             summary="Request to calculate the market share for retail locations.",
             response_model=market_share_general.ResponseTemplateForPOSTRequest_MarketShare,
             responses={
                 400: {"model": schema_general.Message},
                 401: {"model": schema_general.Message},
                 403: {"model": schema_general.Message},
                 404: {"model": schema_general.Message},
                 500: {"model": schema_general.Message}})
def compute_market_share(
        boundary: UploadFile = File(
            title="City Boundary",
            description="City boundary where user wants to calculate the share percentage.\n\n"
            "Only `.geojson` are supported.\n\n"
            "Supported CRS is `EPSG:4326.`"),
        retails: UploadFile = File(
            title="Retails List",
            description="List of locations indicating retails.\n\n"
            "Only `.csv` are supported.\n\n"
            "Supported CRS is `EPSG:4326.`"),
        distance: float = Form(
            500,
            title="Distance",
            description="Distance around each retail location in meter used for calculation.",
            ge=250,
            json_schema_extra={"example": 500}),
        skip_merge: bool = Form(
            False,
            title="Skip Merge",
            description="Ignore the common areas covered by more than one location by setting to `False`."),
        credentials: HTTPAuthorizationCredentials = Security(security)):
    """Request to calculate the market share for retail locations."""
    try:
        if not credentials or not credentials.credentials:
            raise HTTPException(
                status_code=403,
                detail="Invalid header!")

        access_token = credentials.credentials

        if not is_user(token=access_token):
            raise HTTPException(
                status_code=401,
                detail="Unauthorized user!")

        boundary_file = boundary
        retails_file = retails

        market_share = MarketShare(
            boundary=boundary_file,
            locations=retails_file,
            distance=distance,
            skip_merge=skip_merge).calculate()

        return JSONResponse(
            status_code=200,
            content={"market_share": market_share})

    except Exception as e:
        status_code = e.status_code if isinstance(e, HTTPException) else 500
        message = e.detail if isinstance(
            e, HTTPException) else f"Internal Server Error => {str(e)}"

        return JSONResponse(
            status_code=status_code,
            content={"msg": message})
