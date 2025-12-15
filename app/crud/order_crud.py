from sqlmodel import select
from app.db.database import get_session
from app.models import order
from app.models.client import Client
from app.models.order import Order
from app.models.payment import Payment
from app.models.product_order import ProductOrder
from app.models.order_create import OrderCreate
from sqlalchemy.orm import selectinload
from app.schemas.read_order_schema import OrderRead





async def get_order_crud(order_id: int):
    with get_session() as session:
        
        statement = (
    select(Order)
    .where(Order.id == order_id)
    .options(
        selectinload(Order.client),
        selectinload(Order.payment),
        selectinload(Order.product_orders)
            .selectinload(ProductOrder.product),
    )
)

    order = session.exec(statement).first()
    return order

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
