from beanie import Document
from pydantic import BaseModel, Field

class Product(Document):
    name: str
    quantity: int
    unit_price: float = Field(..., alias="unitPrice")

    class Settings:
        name = "products"
    class Config:
        json_schema_extra = {
            "example": {
                "name": "string",
                "quantity": 0,
                "unitPrice": 0.0
            }
        }

    