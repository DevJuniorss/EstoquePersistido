# app/api/payments.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

# Assumimos que estas importações estão disponíveis
from app.base import get_db
from app.services.payment_service import PaymentService # Classe de Serviço a ser criada
from app.models.payment_model import Payment # Modelo SQLAlchemy
from app.schemas.payment_schema import PaymentCreate, PaymentOut, PaymentUpdateStatus # Schemas Pydantic

router = APIRouter(
    prefix="/payments",
    tags=["Pagamentos"],
)

async def get_payment_service(session: AsyncSession = Depends(get_db)) -> PaymentService:
    return PaymentService(session)


@router.post("/", response_model=PaymentOut, status_code=status.HTTP_201_CREATED)
async def create_new_payment(payment_data: PaymentCreate, service: PaymentService = Depends(get_payment_service)):
    return await service.create_payment(payment_data)


@router.get("/", response_model=List[PaymentOut])
async def get_all_payments_endpoint(service: PaymentService = Depends(get_payment_service)):
    return await service.get_all_payments()


@router.get("/{payment_id}", response_model=PaymentOut)
async def get_payment_by_id_endpoint(payment_id: int, service: PaymentService = Depends(get_payment_service)):
    payment = await service.get_payment_by_id(payment_id)
    if payment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pagamento com ID {payment_id} não encontrado."
        )
    return payment


@router.patch("/{payment_id}/status", response_model=PaymentOut)
async def update_payment_status_endpoint(payment_id: int, status_update: PaymentUpdateStatus, service: PaymentService = Depends(get_payment_service)):  
    updated_payment = await service.update_payment_status(
        payment_id=payment_id,
        new_status=status_update.paymentStatus
    )
    
    if updated_payment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pagamento com ID {payment_id} não encontrado para atualização."
        )
    return updated_payment
