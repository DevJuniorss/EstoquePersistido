from datetime import datetime
from typing import List
from fastapi import HTTPException, status
from beanie import PydanticObjectId

from app.models.order import Order, OrderItem
from app.models.client import Client
from app.models.product import Product
from app.crud import order_crud
from app.models.order import Payment 
from pydantic import BaseModel

class OrderItemCreate(BaseModel):
    product: str # 
    quantity: int

class OrderCreate(BaseModel):
    client: str 
    order_date: datetime
    movement_type: str
    payment: Payment
    items: List[OrderItemCreate]

async def get_order_service(order_id: str):
    """
    Retrieves an order by ID with all details.
    """
    if not PydanticObjectId.is_valid(order_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")

    order = await order_crud.get_order_crud(PydanticObjectId(order_id))
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return {"message": "Order found", "data": order}

async def create_order_service(order_data: OrderCreate):
    """
    Creates a new order using DTO pattern.
    """
    if not PydanticObjectId.is_valid(order_data.client):
        raise HTTPException(status_code=400, detail="Invalid Client ID format")
        
    client = await Client.get(PydanticObjectId(order_data.client))
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    if not order_data.items:
        raise HTTPException(status_code=400, detail="Order must have at least one product")

    order_items = []
    
    for item in order_data.items:
        if item.quantity <= 0:
            raise HTTPException(status_code=400, detail="Quantity must be greater than zero")

        if not PydanticObjectId.is_valid(item.product):
             raise HTTPException(status_code=400, detail=f"Invalid Product ID: {item.product}")

        product_obj = await Product.get(PydanticObjectId(item.product))
        if not product_obj:
            raise HTTPException(status_code=404, detail=f"Product {item.product} not found")
            
        order_items.append(OrderItem(product=product_obj, quantity=item.quantity))

    new_order = Order(
        order_date=order_data.order_date,
        movement_type=order_data.movement_type,
        client=client,
        payment=order_data.payment,
        items=order_items
    )

    return await order_crud.create_order_crud(new_order)

async def delete_order_service(order_id: str):
    """
    Deletes an order by ID.
    """
    if not PydanticObjectId.is_valid(order_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")

    deleted = await order_crud.delete_order_crud(PydanticObjectId(order_id))
    if not deleted:
        raise HTTPException(status_code=404, detail="Order not found")
        
    return {"message": "Order deleted successfully"}

async def update_order_service(order_id: str, order_data: Order):
    if not PydanticObjectId.is_valid(order_id):
        raise HTTPException(status_code=400, detail="Invalid Order ID format")
    
    order = await Order.get(PydanticObjectId(order_id), fetch_links=True)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order_data.items is not None:
        new_order_items = []
        for item in order_data.items:
            p_id = item.product.to_ref().id
            
            product = await Product.get(PydanticObjectId(p_id))
            if not product:
                raise HTTPException(status_code=404, detail=f"Product {p_id} not found")
            
            new_order_items.append(OrderItem(product=product, quantity=item.quantity))
        order.items = new_order_items

    data_dict = order_data.model_dump(exclude={"items"}, exclude_unset=True)
    
    if "client" in data_dict:
        c_val = data_dict.pop("client")
        c_id = c_val.to_ref().id if hasattr(c_val, "to_ref") else c_val
        new_client = await Client.get(PydanticObjectId(c_id))
        if new_client:
            order.client = new_client

    for key, value in data_dict.items():
        setattr(order, key, value)

    await order.save()
    return {"message": "Order updated successfully", "data": order}

async def get_orders_report_by_year(year: int):
    orders = await order_crud.get_orders_by_year_crud(year)
    if not orders:
        raise HTTPException(status_code=404, detail=f"No orders found for {year}")
    return {"year": year, "total": len(orders), "orders": orders}

async def get_general_stats():
    """Aggregations and counts using aggregation pipeline"""
    total_products = await Product.count()
    client_stats = await order_crud.count_orders_by_client()
    return {
        "total_products_in_catalog": total_products,
        "orders_per_client": client_stats
    }
    

async def list_orders(size: int, offset: int):
    """
    Retrieves a paginated list of orders.
    """
    orders, total = await order_crud.get_all_orders(size, offset)
    
    return {
        "message": "List of orders",
        "data": orders,
        "size": size,
        "offset": offset,
        "total": total
    }
