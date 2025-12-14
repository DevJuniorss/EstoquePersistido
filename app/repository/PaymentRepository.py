from typing import List, Optional
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.models.payment_model import Payment # Importa o modelo Payment

class PaymentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_payment(self, paymentDate: date, paymentMethod: str,  paymentStatus: bool) -> Payment:
        new_payment = Payment(
            paymentDate=paymentDate,
            paymentMethod=paymentMethod,
            paymentStatus=paymentStatus
        )
        self.session.add(new_payment)
        await self.session.commit()
        await self.session.refresh(new_payment)
        return new_payment

    async def get_payment_by_id(self, payment_id: int) -> Optional[Payment]:
        stmt = select(Payment).where(Payment.id == payment_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_payments_by_method(self, method: str) -> List[Payment]:
        stmt = select(Payment).where(Payment.paymentMethod.ilike(f"%{method}%"))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_payments_by_status(self, status: bool) -> List[Payment]:
        stmt = select(Payment).where(Payment.paymentStatus == status)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_all_payments(self) -> List[Payment]:
        stmt = select(Payment)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update_payment_status(self, payment_id: int, new_status: bool) -> Optional[Payment]:
        stmt = (
            update(Payment)
            .where(Payment.id == payment_id)
            .values(paymentStatus=new_status)
            .returning(Payment) 
        )
        
        result = await self.session.execute(stmt)
        updated_payment = result.scalar_one_or_none()
        
        if updated_payment:
            await self.session.commit()
            await self.session.refresh(updated_payment)
        
        return updated_payment

    async def delete_payment(self, payment_id: int) -> bool:
        stmt = delete(Payment).where(Payment.id == payment_id)
        result = await self.session.execute(stmt)
        
        if result.rowcount > 0:
            await self.session.commit()
            return True
        return False
