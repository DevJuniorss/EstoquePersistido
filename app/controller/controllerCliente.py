from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.base import get_db
from app.services.client_service import ClientService
from app.models.client_model import Client, Supplier # For return types

# Pydantic Schemas (Controller/View Layer) - To be created later
# For now, we will use the SQLAlchemy models directly for simplicity.

router = APIRouter(
    prefix="/clients",
    tags=["Clients and Suppliers"],
)

# Dependency to get the ClientService instance
async def get_client_service(session: AsyncSession = Depends(get_db)) -> ClientService:
    return ClientService(session)

@router.get("/", response_model=List[Client])
async def get_all_clients(service: ClientService = Depends(get_client_service)):
    """
    Retrieve a list of all active clients.
    """
    return await service.get_all_active_clients()

@router.get("/suppliers", response_model=List[Supplier])
async def get_all_suppliers(service: ClientService = Depends(get_client_service)):
    """
    Retrieve a list of all active suppliers.
    """
    return await service.get_all_active_suppliers()