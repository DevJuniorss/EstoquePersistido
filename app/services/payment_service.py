from fastapi import HTTPException
from app.crud.payment_crud import *
from app.models.payment import Payment
from datetime import date



async def list_payments():
    payments = await get_all_payments()
    return {"message": "List of payments", "data": payments}


async def get_payment_by_id_service(payment_id: int):
    payment = await get_payment_crud(payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return {"message": "Payment found", "data": payment}


async def create_payment_service(payment: Payment):
    try:
        payment = Payment(**payment.model_dump())
        payment.payment_date = date.fromisoformat(payment.payment_date)
        return await create_payment_crud(payment)
    except Exception:
        raise HTTPException(status_code=500, detail="Error creating payment")
        

async def update_payment_service(payment_id: int, payment_data: Payment):
    updated_payment = await update_payment_crud(payment_id, payment_data)
    if not updated_payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return {"message": "Payment updated successfully", "data": updated_payment}


async def delete_payment_service(payment_id: int):
    deleted_payment = await delete_payment_crud(payment_id)
    if not deleted_payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return {"message": "Payment deleted successfully", "data": deleted_payment}