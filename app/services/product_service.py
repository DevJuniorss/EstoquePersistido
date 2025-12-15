from fastapi import HTTPException
from app.crud.product_crud import *
from app.models.product import Product


async def list_products(size: int, offset: int):
    """
    Retrieves a paginated list of products.

    Parameters:
        size (int): Number of products to return.
        offset (int): Offset for pagination.

    Returns:
        dict: Paginated list of products with total count.
    """
    products, total = await get_all_products(size, offset)
    return {
        "message": "List of products",
        "data": products,
        "size": size,
        "offset": offset,
        "total": total
    }


async def get_product_by_id_service(product_id: int):
    """
    Retrieves a product by its unique identifier.

    Parameters:
        product_id (int): The ID of the product to retrieve.

    Returns:
        dict: Product data if found.

    Raises:
        HTTPException: If the product is not found.
    """
    product = await get_product_crud(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product found", "data": product}


async def create_product_service(product: Product):
    """
    Creates a new product record.

    Parameters:
        product (Product): Product data to create.

    Returns:
        dict: Created product data.

    Raises:
        HTTPException: If an error occurs during creation.
    """
    try:
        created_product = await create_product_crud(product)
        return {"message": "Product created successfully", "data": created_product}
    except Exception:
        raise HTTPException(status_code=500, detail="Error creating product")


async def update_product_service(product_id: int, product_data: Product):
    """
    Updates an existing product by its ID.

    Parameters:
        product_id (int): The ID of the product to update.
        product_data (Product): Updated product information.

    Returns:
        dict: Confirmation message and updated product data.

    Raises:
        HTTPException: If the product is not found.
    """
    updated_product = await update_product_crud(product_id, product_data)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product updated successfully", "data": updated_product}


async def delete_product_service(product_id: int):
    """
    Deletes a product by its ID.

    Parameters:
        product_id (int): The ID of the product to delete.

    Returns:
        dict: Confirmation message and deleted product data.

    Raises:
        HTTPException: If the product is not found.
    """
    deleted_product = await delete_product_crud(product_id)
    if not deleted_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully", "data": deleted_product}


async def count_orders_by_product_service(product_id: int):
    """
    Counts the total number of orders that include a specific product.

    Parameters:
        product_id (int): The ID of the product.

    Returns:
        dict: Total number of orders containing the product.

    Raises:
        HTTPException: If no orders are found for the product.
    """
    total = await count_orders_by_product_crud(product_id)

    if total == 0:
        raise HTTPException(
            status_code=404,
            detail="No orders found for this product"
        )

    return {
        "product_id": product_id,
        "total_orders": total
    }
