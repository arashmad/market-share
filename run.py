"""
Market Share.

A python-based FastAPI web API for calculating the market share for retails in an area.
"""


import uvicorn

from market_share.core import environment

PORT = int(environment.PORT)

if __name__ == "__main__":
    try:
        uvicorn.run(
            "market_share.create_app:app",
            host="0.0.0.0",
            port=PORT,
            reload=True,
            log_level="debug")
    except Exception as e:
        raise Exception(f"Failed to start the API => {str(e)}.")
