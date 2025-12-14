from app.crud.client_crud import *
from app.models.client import Client



async def list_clients():
    clients = await get_all_clients()
    return {"message": "List of clients", "data": clients}

async def create_client_service(client: Client):
    try:
        return await create_client_crud(client)
    except Exception as e:
        return {"message": "Error creating client"}
    
async def update_client_service(client_id: int, client_data: Client):
    try:
        updated_client = await update_client_crud(client_id, client_data)
        if updated_client:
            return {"message": "Client updated successfully", "data": updated_client}
        else:
            return {"message": "Client not found"}
    except Exception as e:
        return {"message": "Error updating client"}
async def delete_client_service(client_id: int):
    try:
        deleted_client = await delete_client_crud(client_id)
        if deleted_client:
            return {"message": "Client deleted successfully", "data": deleted_client}
        else:
            return {"message": "Client not found"}
    except Exception as e:
        return {"message": "Error deleting client"}