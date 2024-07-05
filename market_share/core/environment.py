"""
Market Share.

A python-based FastAPI web API for calculating the market share for retails in an area.
"""

import os
from dotenv import load_dotenv

load_dotenv()

try:
    PORT = os.getenv("PORT")
    FAKE_TOKEN = os.getenv("FAKE_TOKEN")
except Exception as e:
    raise IOError(f"Failed to initialize HOST/PORT => {str(e)}")
