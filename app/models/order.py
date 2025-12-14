from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date

class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_date: date
    movement_type: str
    client_id: int = Field(foreign_key="client.id")
    payment_id: int = Field(foreign_key="payment.id")
