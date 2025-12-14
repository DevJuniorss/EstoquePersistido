from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date

class Payment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    payment_date: date
    payment_method: str
    payment_status: bool
