from fastapi import APIRouter
from app.models.order_create import OrderCreate
from app.services.order_service import create_order_service

order_router = APIRouter(prefix="/orders")

@order_router.post("/")
async def create_order(order: OrderCreate):
    return await create_order_service(order)
