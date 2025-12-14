from fastapi import APIRouter
from .home_router import home_router
from .client_router import client_router

api_router = APIRouter()

api_router.include_router(home_router, prefix='', tags=['home'])
api_router.include_router(client_router, tags=['Clients'])