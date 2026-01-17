from app.models.product import Product
from beanie import PydanticObjectId
from beanie.operators import RegEx
from typing import List, Tuple

async def get_all_products(size: int, offset: int) -> Tuple[List[Product], int]:
    """
    Retrieve all products with pagination.
    """
    total = await Product.count()
    products = await Product.find_all().skip(offset).limit(size).to_list()
    return products, total

async def get_products_by_name(name: str, size: int, offset: int) -> Tuple[List[Product], int]:
    """
    Search products by name using partial match (case-insensitive).
    """
    query = RegEx(Product.name, name, "i")
    total = await Product.find(query).count()
    products = await Product.find(query).skip(offset).limit(size).to_list()
    
    return products, total

async def get_product_crud(product_id: PydanticObjectId) -> Product | None:
    """
    Get a single product by ID.
    """
    return await Product.get(product_id)

async def create_product_crud(product: Product) -> Product:
    """
    Create a new product.
    """
    await product.create()
    return product

async def update_product_crud(product_id: PydanticObjectId, product_data: Product) -> Product | None:
    """
    Update a product.
    """
    product = await Product.get(product_id)
    if not product:
        return None
    
    data_dict = product_data.model_dump(exclude_unset=True, exclude={"id", "revision_id"})
    
    for key, value in data_dict.items():
        setattr(product, key, value)
    
    await product.save()
    return product

async def delete_product_crud(product_id: PydanticObjectId) -> Product | None:
    """
    Delete a product.
    """
    product = await Product.get(product_id)
    if not product:
        return None
    
    await product.delete()
    return product