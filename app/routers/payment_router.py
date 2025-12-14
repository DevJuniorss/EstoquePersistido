from fastapi import APIRouter
from app.services.payment_service import *
from app.models.payment import Payment

payment_router = APIRouter(prefix = '/payments')

@payment_router.get('/')
async def get_payments():
    return await list_payments()

@payment_router.get('/{payment_id}')
async def get_payment(payment_id: int):
    return await get_payment_by_id_service(payment_id)

@payment_router.post('/')
async def create_payment(payment: Payment):
    created_payment = await create_payment_service(payment)
    return created_payment

@payment_router.put('/')
async def update_payment(payment_id: int, payment_data: Payment):
    updated_payment = await update_payment_service(payment_id, payment_data)
    return updated_payment

@payment_router.delete('/{payment_id}')
async def delete_payment(payment_id: int):
    deleted_payment = await delete_payment_service(payment_id)
    return deleted_payment