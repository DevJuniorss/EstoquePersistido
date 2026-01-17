from typing import List, Optional
from datetime import datetime
from beanie import Document, Link, PydanticObjectId
from pydantic import BaseModel

from app.models.client import Client
from app.models.product import Product 


class OrderItem(BaseModel):
    product: Link[Product]
    quantity: int

class Order(Document):
    order_date: datetime
    movement_type: str
    
    client: Link[Client]
    payment_id: str
    
    items: List[OrderItem]

    class Settings:
        name = "orders"

    class Config:
        json_schema_extra = {
            "example": {
                "order_date": "2026-01-17T10:00:00",
                "movement_type": "SAIDA",
                "client": "64f1a2b3...",
                "payment_id": "p123",
                "items": [
                    {"product": "64f1a2b3...", "quantity": 2}
                ]
            }
        }