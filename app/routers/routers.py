from fastapi import APIRouter


from .product_router import product_router
from .home_router import home_router
from .client_router import client_router
from .order_router import order_router
from .payment_router import payment_router

api_router = APIRouter()

api_router.include_router(home_router, prefix='', tags=['home'])
api_router.include_router(client_router, tags=['Clients'])
api_router.include_router(product_router, tags=['Products'])
api_router.include_router(order_router, tags=['Orders'])
api_router.include_router(payment_router, tags=['Payments'])