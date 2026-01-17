from fastapi import HTTPException, status
from app.crud.product_crud import *
from app.models.product import Product
from beanie import PydanticObjectId

async def list_products(size: int, offset: int):
    """
    Retrieves a paginated list of products.
    """
    products, total = await get_all_products(size, offset)
    return {
        "message": "List of products",
        "data": products,
        "size": size,
        "offset": offset,
        "total": total
    }

async def search_products_by_name(name: str, size: int, offset: int):
    """
    Searches products by name (partial match).
    """
    products, total = await get_products_by_name(name, size, offset)
    return {
        "message": f"Products containing '{name}'",
        "data": products,
        "size": size,
        "offset": offset,
        "total": total
    }

async def get_product_by_id_service(product_id: str):
    """
    Retrieves a product by its unique identifier.
    """
    if not PydanticObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid Product ID format")

    product = await get_product_crud(PydanticObjectId(product_id))
    
    if product:
        return {"message": "Product found", "data": product}
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Product not found"
    )

async def create_product_service(product: Product):
    """
    Creates a new product in the system.
    """
    if product.unit_price < 0 or product.quantity < 0:
        raise HTTPException(status_code=400, detail="Price and Quantity must be non-negative")

    try:
        created = await create_product_crud(product)
        return {"message": "Product created", "data": created}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating product: {str(e)}"
        )

async def update_product_service(product_id: str, product_data: Product):
    """
    Updates an existing product by ID.
    """
    if not PydanticObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid Product ID format")

    try:
        updated_product = await update_product_crud(PydanticObjectId(product_id), product_data)
        if updated_product:
            return {
                "message": "Product updated successfully",
                "data": updated_product
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating product: {str(e)}"
        )

async def delete_product_service(product_id: str):
    """
    Deletes a product by its ID.
    """
    if not PydanticObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid Product ID format")

    try:
        deleted_product = await delete_product_crud(PydanticObjectId(product_id))
        if deleted_product:
            return {
                "message": "Product deleted successfully",
                "data": deleted_product
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting product: {str(e)}"
        )