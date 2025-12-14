from app.crud.client_crud import get_all_clients



async def list_clients():
    clients = await get_all_clients()
    return {"message": "List of clients", "data": clients}