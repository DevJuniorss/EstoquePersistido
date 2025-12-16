from datetime import date
from typing import Optional
from sqlmodel import  SQLModel


class PaymentUpdate(SQLModel):
    id: Optional[int]
    payment_date: Optional[date] = None
    payment_method: Optional[str] = None
    payment_status: Optional[bool] = None