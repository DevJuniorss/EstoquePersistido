from app.db.database import get_session
from sqlmodel import func, select
from app.models.client import Client
from app.models.order import Order
from sqlalchemy.orm import selectinload

from app.models.product_order import ProductOrder


async def get_all_clients(size: int, offset: int):
    with get_session() as session:
        total = session.exec(
            select(func.count()).select_from(Client)
        ).one()

        clients = session.exec(
            select(Client)
            .limit(size)
            .offset(offset)
        ).all()

    return clients, total




async def get_orders_by_client_crud(
    client_id: int,
    size: int,
    offset: int
):
    with get_session() as session:

        total = session.exec(
            select(func.count())
            .select_from(Order)
            .where(Order.client_id == client_id)
        ).one()

        statement = (
            select(Order)
            .where(Order.client_id == client_id)
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


async def get_clients_by_name(name: str, size: int, offset: int):
    pattern = f"%{name}%"

    with get_session() as session:
        total = session.exec(
            select(func.count())
            .select_from(Client)
            .where(Client.name.ilike(pattern))
        ).one()

        clients = session.exec(
            select(Client)
            .where(Client.name.ilike(pattern))
            .limit(size)
            .offset(offset)
        ).all()

    return clients, total
    
async def get_client_crud(client_id: int):
    with get_session() as session:
        client = session.get(Client, client_id)
        return client

async def create_client_crud(client: Client):
    with get_session() as session:
        session.add(client)
        session.commit()
        session.refresh(client)
        return client
    
async def update_client_crud(client_id: int, client_data: Client):
    with get_session() as session:
        client = session.get(Client, client_id)
        if not client:
            return None
        for key, value in client_data.model_dump(exclude_unset=True).items():
            setattr(client, key, value)
        session.add(client)
        session.commit()
        session.refresh(client)
        return client

async def delete_client_crud(client_id: int):
    with get_session() as session:
        client = session.get(Client, client_id)
        if not client:
            return None
        session.delete(client)
        session.commit()
        return client