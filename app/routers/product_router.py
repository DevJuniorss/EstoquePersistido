from fastapi import APIRouter
from fastapi.params import Query
from app.services.product_service import *
from app.models.product import Product

product_router = APIRouter(prefix='/products', tags=["Products"])

@product_router.get('/')
async def get_products(
    size: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """Retrieve a paginated list of products."""
    return await list_products(size=size, offset=offset)

@product_router.get("/search")
async def get_product_by_name(
    name: str = Query(..., min_length=1),
    size: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """Search products by name with pagination."""
    return await search_products_by_name(name, size, offset)

@product_router.get('/{product_id}')
async def get_product(product_id: str):
    """Retrieve a product by ID."""
    return await get_product_by_id_service(product_id)

@product_router.post('/', status_code=201)
async def create_product(product: Product):
    """Create a new product."""
    return await create_product_service(product)

@product_router.put('/{product_id}')
async def update_product(product_id: str, product_data: Product):
    """Update an existing product."""
    return await update_product_service(product_id, product_data)

@product_router.delete('/{product_id}')
async def delete_product(product_id: str):
    """Delete a product by ID."""
    return await delete_product_service(product_id)

@product_router.get('/')
async def get_products(
    size: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    sort_by: str = Query("name")
):
    """Retrieve a list of products sorted by specific field."""
    products = await Product.find_all().sort(sort_by).skip(offset).limit(size).to_list()
    return {"data": products}