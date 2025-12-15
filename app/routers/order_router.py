from fastapi import APIRouter
from app.models.order_create import OrderCreate
from app.services.order_service import *

order_router = APIRouter(prefix="/orders")


@order_router.post("/")
async def create_order(order: OrderCreate):
    """Create a new order."""
    return await create_order_service(order)


@order_router.get("/{order_id}")
async def get_order(order_id: int):
    """Retrieve an order by its ID, including client, payment, and products."""
    data = await get_order_service(order_id)
    print(data)
    return data


@order_router.delete("/{order_id}")
async def delete_order(order_id: int):
    """Delete an order by its ID."""
    deleted_order = await delete_order_service(order_id)
    return deleted_order


@order_router.put("/{order_id}")
async def update_order(order_id: int, order_data: OrderCreate):
    """Update an existing order by its ID."""
    updated_order = await update_order_service(order_id, order_data)
    return updated_order
