from sqlmodel import Relationship, SQLModel, Field
from typing import TYPE_CHECKING, List, Optional
from datetime import date
from app.models.order import Order

if TYPE_CHECKING:
    from app.models.order import Order

class Payment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    payment_date: date
    payment_method: str
    payment_status: bool
    
    orders: List["Order"] = Relationship(back_populates="payment")
    
