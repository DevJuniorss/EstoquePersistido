from beanie import Document
from pydantic import BaseModel, Field

class Product(Document):
    name: str
    quantity: int
    unit_price: float = Field(..., alias="unitPrice")

    class Settings:
        name = "products"

    