from app.models.order import Order
from beanie import PydanticObjectId
from typing import List, Optional

async def get_order_crud(order_id: PydanticObjectId) -> Optional[Order]:
    """
    Retrieve an order by ID, fetching related links (Client, Products).
    """
    return await Order.get(order_id, fetch_links=True)

async def create_order_crud(order: Order) -> Order:
    """
    Save a new order to the database.
    """
    await order.create()
    return order

async def delete_order_crud(order_id: PydanticObjectId) -> Optional[Order]:
    """
    Delete an order by ID.
    """
    order = await Order.get(order_id)
    if not order:
        return None
    await order.delete()
    return order

async def update_order_crud(order_id: PydanticObjectId, order_data: dict) -> Optional[Order]:
    """
    Update an order with new data.
    """
    order = await Order.get(order_id)
    if not order:
        return None
    
    for key, value in order_data.items():
        if value is not None:
            setattr(order, key, value)
            
    await order.save()
    return order