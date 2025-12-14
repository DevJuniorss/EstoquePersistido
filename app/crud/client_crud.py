from app.db.database import get_session
from fastapi import Depends
from sqlmodel import Session, select
from app.models.client import Client


async def get_all_clients():
    with get_session() as session:
        return session.exec(select(Client)).all()