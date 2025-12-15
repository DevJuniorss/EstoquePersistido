from fastapi import HTTPException
from app.crud.product_crud import *
from app.models.product import Product


async def list_products(size: int, offset: int):
    products, total = await get_all_products(size, offset)
    return {
        "message": "List of products",
        "data": products,
        "size": size,
        "offset": offset,
        "total": total
    }


async def get_product_by_id_service(product_id: int):
    product = await get_product_crud(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product found", "data": product}


async def create_product_service(product: Product):
    try:
        created_product = await create_product_crud(product)
        return {"message": "Product created successfully", "data": created_product}
    except Exception:
        raise HTTPException(status_code=500, detail="Error creating product")


async def update_product_service(product_id: int, product_data: Product):
    updated_product = await update_product_crud(product_id, product_data)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product updated successfully", "data": updated_product}


async def delete_product_service(product_id: int):
    deleted_product = await delete_product_crud(product_id)
    if not deleted_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully", "data": deleted_product}
