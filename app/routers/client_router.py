from fastapi import APIRouter
from sqlmodel import SQLModel, Field
from app.services.client_service import list_clients

client_router = APIRouter(prefix = '/clients')

@client_router.get('/')
async def get_clients():
    return await list_clients()
    