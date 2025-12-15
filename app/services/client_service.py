from fastapi import HTTPException, status
from app.crud.client_crud import *
from app.models.client import Client


async def list_clients(size: int, offset: int):
    """
    Retrieves a paginated list of clients.

    Parameters:
        size (int): Number of clients to return.
        offset (int): Offset for pagination.

    Returns:
        dict: Paginated list of clients with total count.
    """
    clients, total = await get_all_clients(size, offset)
    return {
        "message": "List of clients",
        "data": clients,
        "size": size,
        "offset": offset,
        "total": total
    }


async def search_clients_by_name(name: str, size: int, offset: int):
    """
    Searches clients by name using a partial match.

    Parameters:
        name (str): Name or substring to search for.
        size (int): Number of clients to return.
        offset (int): Offset for pagination.

    Returns:
        dict: Paginated list of matching clients.
    """
    clients, total = await get_clients_by_name(name, size, offset)

    return {
        "message": f"Clients containing '{name}'",
        "data": clients,
        "size": size,
        "offset": offset,
        "total": total
    }


async def get_client_by_id_service(client_id: int):
    """
    Retrieves a client by its unique identifier.

    Parameters:
        client_id (int): Client ID.

    Returns:
        dict: Client data if found.

    Raises:
        HTTPException: If client is not found or an error occurs.
    """
    try:
        client = await get_client_crud(client_id)
        if client:
            return {"message": "Client found", "data": client}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found"
            )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving client"
        )


async def create_client_service(client: Client):
    """
    Creates a new client in the system.

    Parameters:
        client (Client): Client data.

    Returns:
        dict: Created client data.

    Raises:
        HTTPException: If an error occurs during creation.
    """
    try:
        created = await create_client_crud(client)
        return {"message": "Client created", "data": created}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating client"
        )


async def update_client_service(client_id: int, client_data: Client):
    """
    Updates an existing client by ID.

    Parameters:
        client_id (int): Client ID.
        client_data (Client): Updated client data.

    Returns:
        dict: Updated client data.

    Raises:
        HTTPException: If client is not found or update fails.
    """
    try:
        updated_client = await update_client_crud(client_id, client_data)
        if updated_client:
            return {
                "message": "Client updated successfully",
                "data": updated_client
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found"
            )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating client"
        )


async def delete_client_service(client_id: int):
    """
    Deletes a client by its ID.

    Parameters:
        client_id (int): Client ID.

    Returns:
        dict: Deleted client data.

    Raises:
        HTTPException: If client is not found or deletion fails.
    """
    try:
        deleted_client = await delete_client_crud(client_id)
        if deleted_client:
            return {
                "message": "Client deleted successfully",
                "data": deleted_client
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found"
            )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting client"
        )
