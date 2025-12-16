from fastapi import APIRouter, Query
from app.schemas.payment_update import PaymentUpdate
from app.services.payment_service import *
from app.models.payment import Payment

payment_router = APIRouter(prefix='/payments')


@payment_router.get('/')
async def get_payments(size: int = Query(10, ge=1, le=100), offset: int = Query(0, ge=0)):
    """Retrieve a paginated list of payments."""
    return await list_payments(size=size, offset=offset)


@payment_router.get('/{payment_id}')
async def get_payment(payment_id: int):
    """Retrieve a payment by its ID."""
    return await get_payment_by_id_service(payment_id)


@payment_router.post('/')
async def create_payment(payment: Payment):
    """Create a new payment."""
    created_payment = await create_payment_service(payment)
    return created_payment


@payment_router.put('/')
async def update_payment(payment_id: int, payment_data: PaymentUpdate):
    """Update an existing payment by its ID."""
    updated_payment = await update_payment_service(payment_id, payment_data)
    return updated_payment


@payment_router.delete('/{payment_id}')
async def delete_payment(payment_id: int):
    """Delete a payment by its ID."""
    deleted_payment = await delete_payment_service(payment_id)
    return deleted_payment
