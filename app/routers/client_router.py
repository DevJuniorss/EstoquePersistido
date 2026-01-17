from fastapi import APIRouter
from fastapi.params import Query
from app.services.client_service import *
from app.models.client import Client
from app.crud import client_crud
from beanie import PydanticObjectId 

client_router = APIRouter(prefix='/clients', tags=["Clients"])

@client_router.get('/')
async def get_clients(
    size: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
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

async def list_clients_crud(size: int, offset: int):
    """
    Lista clientes com ordenação e paginação.
    """
    return await Client.find_all().sort("name").skip(offset).limit(size).to_list()

@client_router.get('/{client_id}')
async def get_client(client_id: str): 
    """Retrieve a client by ID. (Use ID string do Mongo)"""
    return await get_client_by_id_service(client_id)

@client_router.post('/', status_code=201)
async def create_client(client: Client):
    """Create a new client."""
    return await create_client_service(client)

@client_router.put('/{client_id}')
async def update_client(client_id: str, client_data: Client):
    """Update an existing client."""
    return await update_client_service(client_id, client_data)

@client_router.delete('/{client_id}')
async def delete_client(client_id: str):
    """Delete a client by ID."""
    return await delete_client_service(client_id)