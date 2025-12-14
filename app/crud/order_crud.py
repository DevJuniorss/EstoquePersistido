from sqlmodel import select
from app.db.database import get_session
from app.models.order import Order
from app.models.product_order import ProductOrder
from app.models.order_create import OrderCreate




async def get_order_crud(order_id: int):
    pass

async def create_order_crud(order_data: OrderCreate):
    with get_session() as session:
        order = Order(
            order_date=order_data.order_date,
            movement_type=order_data.movement_type,
            client_id=order_data.client_id,
            payment_id=order_data.payment_id
        )

        session.add(order)
        session.commit()
        session.refresh(order)

        for item in order_data.items:
            product_order = ProductOrder(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity
                )
            session.add(product_order)

        session.commit()
        session.refresh(order)
        return order
