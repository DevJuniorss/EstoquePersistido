from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.supplier_repository import SupplierRepository
from app.models.client_supplier_model import Supplier

class SupplierService:
    def __init__(self, session: AsyncSession):
        self.repository = SupplierRepository(session)

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