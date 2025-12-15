from fastapi import APIRouter
from fastapi.params import Query
from app.services.client_service import *
from app.models.client import Client

client_router = APIRouter(prefix='/clients')


@client_router.get('/')
async def get_clients(size: int = Query(10, ge=1, le=100),
                      offset: int = Query(0, ge=0)):
    """Retrieve a paginated list of clients."""
    return await list_clients(size=size, offset=offset)


@client_router.get("/search")
async def get_client_by_name(
    name: str = Query(..., min_length=1),
    size: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """Search clients by name with pagination."""
    return await search_clients_by_name(name, size, offset)


@client_router.get('/{client_id}')
async def get_client(client_id: int):
    """Retrieve a client by ID."""
    return await get_client_by_id_service(client_id)


@client_router.post('/')
async def create_client(client: Client):
    """Create a new client."""
    create_clientd = await create_client_service(client)
    return create_clientd


@client_router.put('/')
async def update_client(client_id: int, client_data: Client):
    """Update an existing client."""
    updated_client = await update_client_service(client_id, client_data)
    return updated_client


@client_router.delete('/')
async def delete_client(client_id: int):
    """Delete a client by ID."""
    deleted_client = await delete_client_service(client_id)
    return deleted_client
