from fastapi import HTTPException, status
from app.crud.client_crud import *
from app.models.client import Client

async def list_clients(size: int, offset: int):
    clients, total = await get_all_clients(size, offset)
    return {
        "message": "List of clients",
        "data": clients,
        "size": size,
        "offset": offset,
        "total": total
    }


async def get_client_by_id_service(client_id: int):
    try:
        client = await get_client_crud(client_id)
        if client:
            return {"message": "Client found", "data": client}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error retrieving client")

async def create_client_service(client: Client):
    try:
        created = await create_client_crud(client)
        return {"message": "Client created", "data": created}
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating client")
    
async def update_client_service(client_id: int, client_data: Client):
    try:
        updated_client = await update_client_crud(client_id, client_data)
        if updated_client:
            return {"message": "Client updated successfully", "data": updated_client}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error updating client")

async def delete_client_service(client_id: int):
    try:
        deleted_client = await delete_client_crud(client_id)
        if deleted_client:
            return {"message": "Client deleted successfully", "data": deleted_client}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error deleting client")