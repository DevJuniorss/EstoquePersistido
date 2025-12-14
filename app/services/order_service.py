from fastapi import HTTPException
from app.models.order_create import OrderCreate
from app.crud.order_crud import create_order_crud
from app.crud.product_crud import get_product_crud


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
