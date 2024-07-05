"""
Market Share.

A python-based FastAPI web API for calculating the market share for retails in an area.
"""

from fastapi import HTTPException

from market_share.core import environment

FAKE_TOKEN = environment.FAKE_TOKEN


def is_user(token: str) -> bool:
    """
    Check if user is authorized to access the resource.

    Parameters
    ----------
    token: str
        JWT token used to verified user.

    Returns
    ----------
    `True` if user is authorized, otherwise `False`.
    """
    try:
        return FAKE_TOKEN == token

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f'Failed to validate the request. => {str(e)}')
