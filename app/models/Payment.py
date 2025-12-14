from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date
from sqlalchemy import String, Integer, Boolean
from app.base import Base

class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    paymentDate: Mapped[date] = mapped_column(Date)
    paymentMethod: Mapped[str] = mapped_column(String)
    paymentStatus: Mapped[bool] = mapped_column(Boolean)

    def __repr__(self) -> str:
        return (
            f"Payment(id={self.id!r}, "
           )
