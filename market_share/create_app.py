"""
Market Share.

A python-based FastAPI web API for calculating the market share for retails in an area.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from market_share.routes.api import api_router

APP_NAME = "Market Share Calculator API"
APP_DESC = "A python-based FastAPI web API for calculating the market share for retails in an area."
APP_VERSION = "0.0.1"
APP_TERMS = "No information"
APP_DOC_NAME = "market_share"

CONTACT_NAME = "WHATALOCATION"
CONTACT_LINK = "https://en.whatalocation.ai/"
CONTACT_MAIL = "sales@whatalocation.ai"

LICENSE_NAME = "No information"

docs_url = '/docs'
redoc_url = '/redoc'
openapi_url = f'/{APP_DOC_NAME}.json'

fastapi_app = FastAPI(
    title=APP_NAME,
    description=APP_DESC,
    version=APP_VERSION,
    terms_of_service=APP_TERMS,
    contact={
        "name": CONTACT_NAME,
        "url": CONTACT_LINK,
        "email": CONTACT_MAIL,
    },
    license_info={
        "name": LICENSE_NAME,
    },
    docs_url=docs_url,
    redoc_url=redoc_url,
    openapi_url=openapi_url)

fastapi_app.include_router(api_router)


fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app = fastapi_app
