from fastapi import HTTPException
from app.crud.payment_crud import *
from app.models.payment import Payment
from datetime import date


async def list_payments(size: int, offset: int):
    """
    Retrieves a paginated list of payments.

    Parameters:
        size (int): Number of payments to return.
        offset (int): Offset for pagination.

    Returns:
        dict: Paginated list of payments with total count.
    """
    payments, total = await get_all_payments(size, offset)
    return {
        "message": "List of payments",
        "data": payments,
        "size": size,
        "offset": offset,
        "total": total
    }


async def get_payment_by_id_service(payment_id: int):
    """
    Retrieves a payment by its unique identifier.

    Parameters:
        payment_id (int): The ID of the payment to retrieve.

    Returns:
        dict: Payment data if found.

    Raises:
        HTTPException: If the payment is not found.
    """
    payment = await get_payment_crud(payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return {"message": "Payment found", "data": payment}


async def create_payment_service(payment: Payment):
    """
    Creates a new payment record.

    Converts payment_date to a date object and stores the payment in the database.

    Parameters:
        payment (Payment): Payment data to create.

    Returns:
        Payment: The created payment object.

    Raises:
        HTTPException: If an error occurs during creation.
    """
    try:
        payment = Payment(**payment.model_dump())
        payment.payment_date = date.fromisoformat(payment.payment_date)
        return await create_payment_crud(payment)
    except Exception:
        raise HTTPException(status_code=500, detail="Error creating payment")
        

async def update_payment_service(payment_id: int, payment_data: Payment):
    """
    Updates an existing payment by its ID.

    Parameters:
        payment_id (int): The ID of the payment to update.
        payment_data (Payment): Updated payment information.

    Returns:
        dict: Confirmation message and updated payment data.

    Raises:
        HTTPException: If the payment is not found.
    """
    updated_payment = await update_payment_crud(payment_id, payment_data)
    if not updated_payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return {"message": "Payment updated successfully", "data": updated_payment}


async def delete_payment_service(payment_id: int):
    """
    Deletes a payment by its ID.

    Parameters:
        payment_id (int): The ID of the payment to delete.

    Returns:
        dict: Confirmation message and deleted payment data.

    Raises:
        HTTPException: If the payment is not found.
    """
    deleted_payment = await delete_payment_crud(payment_id)
    if not deleted_payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return {"message": "Payment deleted successfully", "data": deleted_payment}
