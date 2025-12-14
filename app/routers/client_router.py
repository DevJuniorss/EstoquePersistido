from fastapi import APIRouter
from app.services.client_service import *
from app.models.client import Client

client_router = APIRouter(prefix = '/clients')

@client_router.get('/')
async def get_clients():
    return await list_clients()

@client_router.get('/{client_id}')
async def get_client(client_id: int):
    return await get_client_by_id_service(client_id)

@client_router.post('/')
async def create_client(client: Client):
    create_clientd = await create_client_service(client)
    return create_clientd

@client_router.put('/')
async def update_client(client_id: int, client_data: Client):
    updated_client = await update_client_service(client_id, client_data)
    return updated_client

@client_router.delete('/')
async def delete_client(client_id: int):
    deleted_client = await delete_client_service(client_id)
    return deleted_client