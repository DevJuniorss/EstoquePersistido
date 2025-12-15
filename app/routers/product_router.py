from fastapi import APIRouter, Query
from app.services.client_service import *
from app.models.product import Product
from app.services.product_service import *

product_router = APIRouter(prefix='/products')


@product_router.get('/')
async def get_products(size: int = Query(10, ge=1, le=100), offset: int = Query(0, ge=0)):
    """Retrieve a paginated list of products."""
    return await list_products(size=size, offset=offset)


@product_router.get('/{product_id}')
async def get_product(product_id: int):
    """Retrieve a product by its ID."""
    return await get_product_by_id_service(product_id)


@product_router.post('/')
async def create_product(product: Product):
    """Create a new product."""
    created_product = await create_product_service(product)
    return created_product


@product_router.put('/')
async def update_product(product_id: int, product_data: Product):
    """Update an existing product by its ID."""
    updated_product = await update_product_service(product_id, product_data)
    return updated_product


@product_router.delete('/')
async def delete_product(product_id: int):
    """Delete a product by its ID."""
    deleted_product = await delete_product_service(product_id)
    return deleted_product


@product_router.get("/{product_id}/orders/count")
async def count_orders_by_product(product_id: int):
    """Count the total number of orders for a specific product."""
    return await count_orders_by_product_service(product_id)
