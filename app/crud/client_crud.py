from app.db.database import get_session
from sqlmodel import select
from app.models.client import Client


async def get_all_clients():
    with get_session() as session:
        return session.exec(select(Client)).all()
    
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