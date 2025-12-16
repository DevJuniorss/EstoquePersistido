from datetime import date
from sqlmodel import SQLModel
from typing import Optional


    

class ClientUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    
