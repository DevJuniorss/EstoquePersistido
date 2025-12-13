from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Boolean
from app.base import Base

class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    tipo_documento: Mapped[str] = mapped_column(String(4), nullable=False) # CPF | CNPJ
    email: Mapped[Optional[str]] = mapped_column(String, unique=True, nullable=True)
    telefone: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    endereco: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    nascimento: Mapped[Optional[str]] = mapped_column(String, nullable=True) # Assuming string for simplicity, could be Date
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    def __repr__(self) -> str:
        return f"Client(id={self.id!r}, name={self.name!r})"

class Supplier(Base):
    __tablename__ = "suppliers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    tipo_documento: Mapped[str] = mapped_column(String(4), nullable=False) # CPF | CNPJ
    email: Mapped[Optional[str]] = mapped_column(String, unique=True, nullable=True)
    telefone: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    endereco: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    def __repr__(self) -> str:
        return f"Supplier(id={self.id!r}, name={self.name!r})"