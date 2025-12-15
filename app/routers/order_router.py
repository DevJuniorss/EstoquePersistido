from fastapi import APIRouter
from app.models.order_create import OrderCreate
from app.services.order_service import *
from app.schemas.read_order_schema import OrderRead

order_router = APIRouter(prefix="/orders")

@order_router.post("/")
async def create_order(order: OrderCreate):
    return await create_order_service(order)


@order_router.get("/{order_id}")
async def get_order(order_id: int):
    
    data = await get_order_service(order_id)
    print(data)
    return data