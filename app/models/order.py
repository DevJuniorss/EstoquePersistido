from datetime import datetime
from typing import List, Optional
from beanie import Document, Link
from pydantic import BaseModel
from app.models.client import Client
from app.models.product import Product

class Payment(BaseModel):
    payment_method: str
    payment_date: datetime = datetime.now()
    status: str = "PENDING"

class OrderItem(BaseModel):
    product: Link[Product]
    quantity: int

class Order(Document):
    order_date: datetime
    movement_type: str
    client: Link[Client]

    payment: Payment 
    
    items: List[OrderItem]

    class Settings:
        name = "orders"