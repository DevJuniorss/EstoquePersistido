from app.db.database import get_session
from sqlmodel import select
from app.models.payment import Payment


async def get_all_payments():
    with get_session() as session:
        return session.exec(select(Payment)).all()
    
async def get_payment_crud(payment_id: int):
    with get_session() as session:
        payment = session.get(Payment, payment_id)
        return payment

async def create_payment_crud(payment: Payment):
    with get_session() as session:
        session.add(payment)
        session.commit()
        session.refresh(payment)
        return payment
    
async def update_payment_crud(payment_id: int, payment_data: Payment):
    with get_session() as session:
        payment = session.get(Payment, payment_id)
        if not payment:
            return None
        for key, value in payment_data.model_dump(exclude_unset=True).items():
            setattr(payment, key, value)
        session.add(payment)
        session.commit()
        session.refresh(payment)
        return payment

async def delete_payment_crud(payment_id: int):
    with get_session() as session:
        payment = session.get(Payment, payment_id)
        if not payment:
            return None
        session.delete(payment)
        session.commit()
        return payment