from fastapi import HTTPException
from app.models.order_create import OrderCreate
from app.crud.order_crud import *
from app.crud.product_crud import get_product_crud


async def get_order_service(order_id: int):
    order = await get_order_crud(order_id)
    print('service', order.client)
    data = order.model_dump()
    data['client'] = order.client
    data['payment'] = order.payment
    data['product_orders'] = [i.product for i in order.product_orders]
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order found", "data": data}

async def create_order_service(order_data: OrderCreate):
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
