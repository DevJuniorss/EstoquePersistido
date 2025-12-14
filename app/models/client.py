from sqlmodel import SQLModel, Field
from typing import Optional

class Client(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    address: str