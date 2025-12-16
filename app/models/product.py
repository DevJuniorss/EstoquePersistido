from sqlmodel import Relationship, SQLModel, Field
from typing import List, Optional

from app.models.order import Order
from app.models.product_order import ProductOrder

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    unit_price: float

    product_orders: List["ProductOrder"] = Relationship(back_populates="product", 
                                                        sa_relationship_kwargs={"cascade": "all, delete-orphan"})