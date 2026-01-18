from app.models.client import Client
from beanie import PydanticObjectId
from beanie.operators import RegEx
from app.models.product import Product
from typing import List, Tuple

async def get_all_clients(size: int, offset: int) -> Tuple[List[Client], int]:
    total = await Client.count()
    
    clients = await Client.find_all().skip(offset).limit(size).to_list()
    
    return clients, total

async def get_clients_by_name(name: str, size: int, offset: int) -> Tuple[List[Client], int]:
    query = RegEx(Client.name, name, "i")   
    total = await Client.find(query).count()
    
    clients = await Client.find(query).skip(offset).limit(size).to_list()

    return clients, total
    
async def get_client_crud(client_id: PydanticObjectId) -> Client | None:
    return await Client.get(client_id)

async def get_clients_paginated(skip: int = 0, limit: int = 10, order_by: str = "name") -> List[Client]:
    """
    Lista clientes com paginação e ordenação.
    """
    return await Client.find_all().sort(order_by).skip(skip).limit(limit).to_list()

async def create_client_crud(client: Client) -> Client:
    await client.create()
    return client
    
async def update_client_crud(client_id: PydanticObjectId, client_data: Client) -> Client | None:
    client = await Client.get(client_id)
    if not client:
        return None
    
    data_dict = client_data.model_dump(exclude_unset=True, exclude={"id", "revision_id"})
    
    for key, value in data_dict.items():
        setattr(client, key, value)
    
    await client.save()
    return client

async def delete_client_crud(client_id: PydanticObjectId) -> Client | None:
    client = await Client.get(client_id)
    if not client:
        return None
    
    await client.delete()
    return client
