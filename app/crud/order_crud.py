from sqlmodel import func, select
from app.db.database import get_session
from app.models import order
from app.models.client import Client
from app.models.order import Order
from app.models.payment import Payment
from app.models.product_order import ProductOrder
from app.schemas.order_create import OrderCreate
from sqlalchemy.orm import selectinload




async def get_all_orders(size: int, offset: int):
    with get_session() as session:

        total = session.exec(
            select(func.count()).select_from(Order)
        ).one()

        statement = (
            select(Order)
            .options(
                selectinload(Order.client),
                selectinload(Order.payment),
                selectinload(Order.product_orders)
                    .selectinload(ProductOrder.product),
            )
            .limit(size)
            .offset(offset)
        )

        orders = session.exec(statement).all()

    return orders, total

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
    
async def delete_order_crud(order_id: int):
    with get_session() as session:
        order = session.get(Order, order_id)
        if not order:
            return None
        session.delete(order)
        session.commit()
        return order
    
async def update_order_crud(order_id: int, order_data: OrderCreate):
    with get_session() as session:
        order = session.get(Order, order_id)
        if not order:
            return None
        for key, value in order_data.model_dump(exclude_unset=True, exclude={"items"}).items():
            setattr(order, key, value)
        session.add(order)
        session.commit()
        session.refresh(order)
        return order
