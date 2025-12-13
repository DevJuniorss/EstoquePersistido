from sqlalchemy import Column, String, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import enum
import uuid


class TipoMovimentacao(enum.Enum):
    ENTRADA = "ENTRADA"
    SAIDA = "SAIDA"


class Pedido(Base):
    __tablename__ = "pedidos"

    id_pedido = Column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )

    data_pedido = Column(Date, nullable=False)

    tipo_movimentacao = Column(
        Enum(TipoMovimentacao), nullable=False
    )

    id_cliente = Column(
        String, ForeignKey("clientes.id_cliente"), nullable=True
    )

    id_fornecedor = Column(
        String, ForeignKey("fornecedores.id_fornecedor"), nullable=True
    )

    # RELACIONAMENTOS
    cliente = relationship("Cliente", back_populates="pedidos")
    fornecedor = relationship("Fornecedor", back_populates="pedidos")

    pagamento = relationship(
        "Pagamento",
        back_populates="pedido",
        uselist=False,
        cascade="all, delete-orphan"
    )

    lista_produtos = relationship(
        "ListaProdutos",
        back_populates="pedido",
        cascade="all, delete-orphan"
    )
