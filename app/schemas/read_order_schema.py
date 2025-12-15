from datetime import date
from typing import List
from sqlmodel import SQLModel


class ProductRead(SQLModel):
    id: int
    name: str
    unit_price: float

class ProductOrderRead(SQLModel):
    id: int
    quantity: int
    product: ProductRead

class ClientRead(SQLModel):
    id: int
    name: str
    email: str
    address: str

class PaymentRead(SQLModel):
    id: int
    method: str

class OrderRead(SQLModel):
    id: int
    order_date: date
    movement_type: str

    client: ClientRead
    payment: PaymentRead
    product_orders: List[ProductOrderRead]
