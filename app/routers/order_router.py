from fastapi import APIRouter
from app.models.order_create import OrderCreate
from app.services.order_service import *

order_router = APIRouter(prefix="/orders")

@order_router.post("/")
async def create_order(order: OrderCreate):
    return await create_order_service(order)


@order_router.get("/{order_id}")
async def get_order(order_id: int):
    
    data = await get_order_service(order_id)
    print(data)
    return data

@order_router.delete("/{order_id}")
async def delete_order(order_id: int):
    deleted_order = await delete_order_service(order_id)
    return deleted_order

@order_router.put("/{order_id}")
async def update_order(order_id: int, order_data: OrderCreate):
    updated_order = await update_order_service(order_id, order_data)
    return updated_order