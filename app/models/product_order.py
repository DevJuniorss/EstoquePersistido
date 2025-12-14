from sqlmodel import Relationship, SQLModel, Field
from typing import Optional
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.product import Product
    from app.models.order import Order

class ProductOrder(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    order_id: int = Field(foreign_key="order.id")
    product_id: int = Field(foreign_key="product.id")

    quantity: int

    order: "Order" = Relationship(back_populates="product_orders")
    product: "Product" = Relationship(back_populates="product_orders")
