from fastapi import APIRouter, Query
from app.services.client_service import *
from app.models.product import Product
from app.services.product_service import *
product_router = APIRouter(prefix = '/products')

@product_router.get('/')
async def get_products(size: int = Query(10, ge=1, le=100), offset: int = Query(0, ge=0)):
    return await list_products(size=size, offset=offset)

@product_router.get('/{product_id}')
async def get_product(product_id: int):
    return await get_product_by_id_service(product_id)

@product_router.post('/')
async def create_product(product: Product):
    created_product = await create_product_service(product)
    return created_product

@product_router.put('/')
async def update_product(product_id: int, product_data: Product):
    updated_product = await update_product_service(product_id, product_data)
    return updated_product

@product_router.delete('/')
async def delete_product(product_id: int):
    deleted_product = await delete_product_service(product_id)
    return deleted_product