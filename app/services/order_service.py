from fastapi import HTTPException
from app.schemas.order_create import OrderCreate
from app.crud.order_crud import *
from app.crud.product_crud import get_product_crud


async def get_all_orders_service(size: int, offset: int):
    """
    Retrieves a paginated list of orders, including related client, payment, and products.

    Returns:
        dict: Orders list and total count.
    """
    orders, total = await get_all_orders(size, offset)

    data = []
    for order in orders:
        order_data = order.model_dump()
        order_data['client'] = order.client
        order_data['payment'] = order.payment
        order_data['product_orders'] = [
            {
                "product": po.product,
                "quantity": po.quantity
            }
            for po in order.product_orders
        ]
        data.append(order_data)

    return {
        "message": "Orders found",
        "total": total,
        "data": data
    }



async def get_order_service(order_id: int):
    """
    Retrieves an order by its ID, including related client, payment, and products.

    Parameters:
        order_id (int): The ID of the order to retrieve.

    Returns:
        dict: Order data with client, payment, and product details.

    Raises:
        HTTPException: If the order is not found.
    """
    order = await get_order_crud(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    data = order.model_dump()
    data['client'] = order.client
    data['payment'] = order.payment
    data['product_orders'] = [{"product": i.product, "quantity": i.quantity} for i in order.product_orders]

    return {"message": "Order found", "data": data}


async def create_order_service(order_data: OrderCreate):
    """
    Creates a new order with its associated products.

    Validates that the order has at least one product,
    that quantities are greater than zero, and that all products exist.

    Parameters:
        order_data (OrderCreate): Data required to create the order.

    Returns:
        dict: Created order data.

    Raises:
        HTTPException: If validation fails or a product is not found.
    """
    if not order_data.items:
        raise HTTPException(
            status_code=400,
            detail="Order must have at least one product"
        )

    for item in order_data.items:
        if item.quantity <= 0:
            raise HTTPException(
                status_code=400,
                detail="Quantity must be greater than zero"
            )

        product = await get_product_crud(item.product_id)
        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Product {item.product_id} not found"
            )

    return await create_order_crud(order_data)


async def delete_order_service(order_id: int):
    """
    Deletes an order by its ID, including associated product orders.

    Parameters:
        order_id (int): ID of the order to delete.

    Returns:
        dict: Confirmation message and deleted order data.

    Raises:
        HTTPException: If the order is not found.
    """
    deleted_order = await delete_order_crud(order_id)
    if not deleted_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order deleted successfully"}


async def update_order_service(order_id: int, order_data: OrderCreate):
    """
    Updates an existing order and its associated products.

    Parameters:
        order_id (int): ID of the order to update.
        order_data (OrderCreate): Updated data for the order.

    Returns:
        dict: Confirmation message and updated order data.

    Raises:
        HTTPException: If the order is not found.
    """
    updated_order = await update_order_crud(order_id, order_data)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order updated successfully", "data": updated_order}
