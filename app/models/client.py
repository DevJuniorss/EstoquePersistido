from sqlmodel import Relationship, SQLModel, Field
from typing import List, Optional, TYPE_CHECKING
if TYPE_CHECKING:

    from app.models.order import Order

class Client(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    address: str
    
    orders: List['Order'] = Relationship(back_populates="client", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
