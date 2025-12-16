from sqlmodel import SQLModel
from typing import List
from datetime import date

class ProductOrderCreate(SQLModel):
    product_id: int
    quantity: int

class OrderCreate(SQLModel):
    order_date: date
    movement_type: str
    client_id: int
    payment_id: int
    items: List[ProductOrderCreate]
