from sqlmodel import Relationship, SQLModel, Field
from typing import List, Optional
from datetime import date


from typing import TYPE_CHECKING

from app.models.product_order import ProductOrder

if TYPE_CHECKING:
    from app.models.client import Client
    from app.models.payment import Payment
    from app.models.product_order import ProductOrder
    from app.models.product import Product



class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_date: date
    movement_type: str

    client_id: int = Field(foreign_key="client.id")
    payment_id: int = Field(foreign_key="payment.id")

    product_orders: List["ProductOrder"] = Relationship(back_populates="order", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    client: "Client" = Relationship(back_populates="orders")
    payment: "Payment" = Relationship(back_populates="orders")
