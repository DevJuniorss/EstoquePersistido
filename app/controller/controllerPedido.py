from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.service.pedidoService import PedidoService
from app.model.pedido import TipoMovimentacao
from app.view.pedidoSchema import PedidoCreate, PedidoResponse

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


@router.post("/", response_model=PedidoResponse)
def criar_pedido(
    payload: PedidoCreate,
    db: Session = Depends(get_db)
):
    try:
        service = PedidoService(db)
        pedido = service.criar_pedido(
            tipo_movimentacao=payload.tipo_movimentacao,
            id_cliente=payload.id_cliente,
            id_fornecedor=payload.id_fornecedor
        )
        return pedido

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{pedido_id}", response_model=PedidoResponse)
def buscar_pedido(
    pedido_id: str,
    db: Session = Depends(get_db)
):
    try:
        service = PedidoService(db)
        return service.buscar_pedido(pedido_id)

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
