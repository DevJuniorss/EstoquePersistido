from sqlalchemy.orm import Session
from app.model.pedido import Pedido


class PedidoRepository:

    def __init__(self, db: Session):
        self.db = db

    def save(self, pedido: Pedido) -> Pedido:
        self.db.add(pedido)
        self.db.commit()
        self.db.refresh(pedido)
        return pedido

    def find_by_id(self, pedido_id: str) -> Pedido | None:
        return (
            self.db
            .query(Pedido)
            .filter(Pedido.id_pedido == pedido_id)
            .first()
        )

    def find_all(self) -> list[Pedido]:
        return self.db.query(Pedido).all()

    def delete(self, pedido: Pedido) -> None:
        self.db.delete(pedido)
        self.db.commit()
