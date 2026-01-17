from typing import Optional
from beanie import Document
from pydantic import BaseModel

class Client(Document):
    name: str
    email: str
    address: str

    class Settings:
        name = "clients"

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Lucas Torres",
                "email": "lucas@email.com",
                "address": "Rua das Flores, 123"
            }
        }