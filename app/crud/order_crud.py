from datetime import datetime
from app.models.order import Order
from app.models.product import Product
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


async def get_orders_by_year(year: int):
    start_date = datetime(year, 1, 1)
    end_date = datetime(year + 1, 1, 1)
    
    orders = await Order.find(
        Order.order_date >= start_date,
        Order.order_date < end_date
    , fetch_links=True).to_list()
    return orders

async def count_orders_by_client():
    pipeline = [
        {"$group": {"_id": "$client.$id", "total_orders": {"$sum": 1}}},
    ]
    result = await Order.aggregate(pipeline).to_list()
    return result

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

async def get_orders_by_year_crud(year: int):
    """Filtros por data/ano utilizando operadores do MongoDB"""
    start_date = datetime(year, 1, 1)
    end_date = datetime(year + 1, 1, 1)
    return await Order.find(
        Order.order_date >= start_date,
        Order.order_date < end_date,
        fetch_links=True
    ).to_list()

async def get_total_products_count_crud():
    """Mostrar a quantidade total de produtos cadastrados"""
    return await Product.count()

async def get_order_stats_agg():
    """Agregações: Quantidade de itens por pedido"""
    pipeline = [
        {"$project": {"items_count": {"$size": "$items"}}},
        {"$group": {"_id": None, "avg_items": {"$avg": "$items_count"}, "total_items": {"$sum": "$items_count"}}}
    ]
    return await Order.aggregate(pipeline).to_list()

async def list_products_sorted(size: int, offset: int, sort_field: str = "name"):
    """Classificações e ordenações"""
    return await Product.find_all().sort(sort_field).skip(offset).limit(size).to_list()