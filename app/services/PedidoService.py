from datetime import date
from sqlalchemy.orm import Session
from app.model.pedido import Pedido, TipoMovimentacao
from app.repository.pedidoRepository import PedidoRepository


class PedidoService:

    def __init__(self, db: Session):
        self.repository = PedidoRepository(db)

    def criar_pedido(
        self,
        tipo_movimentacao: TipoMovimentacao,
        id_cliente: str | None,
        id_fornecedor: str | None
    ) -> Pedido:

        if tipo_movimentacao == TipoMovimentacao.SAIDA and not id_cliente:
            raise ValueError("Pedido de SAÍDA exige um cliente")

        if tipo_movimentacao == TipoMovimentacao.ENTRADA and not id_fornecedor:
            raise ValueError("Pedido de ENTRADA exige um fornecedor")

        pedido = Pedido(
            data_pedido=date.today(),
            tipo_movimentacao=tipo_movimentacao,
            id_cliente=id_cliente,
            id_fornecedor=id_fornecedor
        )

        return self.repository.save(pedido)

    def buscar_pedido(self, pedido_id: str) -> Pedido:
        pedido = self.repository.find_by_id(pedido_id)

        if not pedido:
            raise ValueError("Pedido não encontrado")

        return pedido

    def listar_pedidos(self) -> list[Pedido]:
        return self.repository.find_all()
