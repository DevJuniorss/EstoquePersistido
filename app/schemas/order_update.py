from typing import List, Optional
from sqlmodel import SQLModel
class ProductOrderPayload(SQLModel):
    product_id: int
    quantity: int
    amount: float

class OrderUpdate(SQLModel):
    order_date: Optional[str] = None
    movement_type: Optional[str] = None
    client_id: Optional[int] = None
    payment_id: Optional[int] = None
    
    items: Optional[List[ProductOrderPayload]] = None