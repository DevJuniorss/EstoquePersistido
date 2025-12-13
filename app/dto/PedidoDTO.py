from pydantic import BaseModel
from datetime import date
from app.model.pedido import TipoMovimentacao


class PedidoCreate(BaseModel):
    tipo_movimentacao: TipoMovimentacao
    id_cliente: str | None = None
    id_fornecedor: str | None = None


class PedidoResponse(BaseModel):
    id_pedido: str
    data_pedido: date
    tipo_movimentacao: TipoMovimentacao

    class Config:
        from_attributes = True
