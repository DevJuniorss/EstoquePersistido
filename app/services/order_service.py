from fastapi import HTTPException, status
from beanie import PydanticObjectId

from app.models.order import Order, OrderItem
from app.models.client import Client
from app.models.product import Product
from app.crud import order_crud

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

async def create_order_service(order_data: Order):
    """
    Creates a new order. Validates Client and Products existence before saving.
    """
    if not PydanticObjectId.is_valid(order_data.client_id):
        raise HTTPException(status_code=400, detail="Invalid Client ID")
        
    client = await Client.get(PydanticObjectId(order_data.client_id))
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    if not order_data.items:
        raise HTTPException(status_code=400, detail="Order must have at least one product")

    order_items = []
    
    for item in order_data.items:
        if item.quantity <= 0:
            raise HTTPException(status_code=400, detail="Quantity must be greater than zero")

        if not PydanticObjectId.is_valid(item.product_id):
             raise HTTPException(status_code=400, detail=f"Invalid Product ID: {item.product_id}")

        product = await Product.get(PydanticObjectId(item.product_id))
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
            
        order_items.append(OrderItem(product=product, quantity=item.quantity))

    new_order = Order(
        order_date=order_data.order_date,
        movement_type=order_data.movement_type,
        client=client,
        payment_id=str(order_data.payment_id),
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
            if item.quantity <= 0:
                raise HTTPException(status_code=400, detail="Quantity must be greater than zero")

            if not PydanticObjectId.is_valid(item.product_id):
                 raise HTTPException(status_code=400, detail=f"Invalid Product ID: {item.product_id}")
            product = await Product.get(PydanticObjectId(item.product_id))
            
            if not product:
                raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
            
            new_order_items.append(OrderItem(product=product, quantity=item.quantity))
        
        order.items = new_order_items


    data_dict = order_data.model_dump(exclude={"items"}, exclude_unset=True)
    
    if "client_id" in data_dict:
        cid = data_dict.pop("client_id")
        if PydanticObjectId.is_valid(cid):
            new_client = await Client.get(PydanticObjectId(cid))
            if new_client:
                order.client = new_client
            else:
                raise HTTPException(status_code=404, detail="Client not found")

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
    """Aggregations and counts using aggregation pipeline (Requirement e/g)"""
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