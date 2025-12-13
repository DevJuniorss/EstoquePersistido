from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.client_repository import ClientRepository
from app.models.client_model import Client, Supplier

class ClientService:
    def __init__(self, session: AsyncSession):
        self.repository = ClientRepository(session)

    # --- Client Operations ---

    async def register_client(self, name: str, tipo_documento: str, email: Optional[str], telefone: Optional[str], endereco: Optional[str], nascimento: Optional[str]) -> Client:
        # Business logic for validation can go here
        if not name or not tipo_documento:
            raise ValueError("Name and document type are required.")
        
        # Check for existing client by document or email (example business rule)
        existing_client = await self.repository.get_client_by_document(tipo_documento)
        if existing_client:
            raise ValueError(f"Client with document {tipo_documento} already exists.")

        return await self.repository.create_client(name, tipo_documento, email, telefone, endereco, nascimento)

    async def get_client_details(self, client_id: int) -> Optional[Client]:
        return await self.repository.get_client_by_id(client_id)

    async def search_clients_by_name(self, name: str) -> List[Client]:
        return await self.repository.get_client_by_name(name)

    async def search_client_by_document(self, tipo_documento: str) -> Optional[Client]:
        return await self.repository.get_client_by_document(tipo_documento)

    async def get_all_active_clients(self) -> List[Client]:
        return await self.repository.get_all_clients()

    # --- Supplier Operations ---

    async def register_supplier(self, name: str, tipo_documento: str, email: Optional[str], telefone: Optional[str], endereco: Optional[str]) -> Supplier:
        # Business logic for validation can go here
        if not name or not tipo_documento:
            raise ValueError("Name and document type are required.")
        
        # Check for existing supplier by document or email (example business rule)
        existing_supplier = await self.repository.get_supplier_by_document(tipo_documento)
        if existing_supplier:
            raise ValueError(f"Supplier with document {tipo_documento} already exists.")

        return await self.repository.create_supplier(name, tipo_documento, email, telefone, endereco)

    async def get_supplier_details(self, supplier_id: int) -> Optional[Supplier]:
        return await self.repository.get_supplier_by_id(supplier_id)

    async def search_suppliers_by_name(self, name: str) -> List[Supplier]:
        return await self.repository.get_supplier_by_name(name)

    async def search_supplier_by_document(self, tipo_documento: str) -> Optional[Supplier]:
        return await self.repository.get_supplier_by_document(tipo_documento)

    async def get_all_active_suppliers(self) -> List[Supplier]:
        return await self.repository.get_all_suppliers()