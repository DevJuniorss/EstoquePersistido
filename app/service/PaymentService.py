from typing import List, Optional
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.payment_repository import PaymentRepository 
from app.models.payment_model import Payment 

class PaymentService:
    def __init__(self, session: AsyncSession):
        self.repository = PaymentRepository(session)


    async def create_payment(self, payment_data) -> Payment:
        #TODO remover se não for necessário o seguinte if:
        if payment_data.paymentDate > date.today():
            raise ValueError("A data de pagamento não pode ser futura.")
       #TODO formatos de pagamento 
        if payment_data.paymentMethod.lower() in ["pix", "cartão"]:
            initial_status = True
        else:
            initial_status = payment_data.paymentStatus
            
        return await self.repository.create_payment(
            paymentDate=payment_data.paymentDate,
            paymentMethod=payment_data.paymentMethod,
            paymentStatus=initial_status 
        )

    async def get_payment_by_id(self, payment_id: int) -> Optional[Payment]:
        return await self.repository.get_payment_by_id(payment_id)

    async def get_all_payments(self) -> List[Payment]:
        return await self.repository.get_all_payments()
    
    async def get_paid_payments(self) -> List[Payment]:
        return await self.repository.get_payments_by_status(status=True)

    async def update_payment_status(self, payment_id: int, new_status: bool) -> Optional[Payment]:
        current_payment = await self.repository.get_payment_by_id(payment_id)
        if current_payment and current_payment.paymentStatus is True and new_status is False:
             pass 

        return await self.repository.update_payment_status(payment_id, new_status)
