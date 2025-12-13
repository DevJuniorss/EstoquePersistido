from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.models.client_model import Client, Supplier

class ClientRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    # --- Client Operations ---

    async def create_client(self, name: str, tipo_documento: str, email: Optional[str], telefone: Optional[str], endereco: Optional[str], nascimento: Optional[str]) -> Client:
        new_client = Client(
            name=name,
            tipo_documento=tipo_documento,
            email=email,
            telefone=telefone,
            endereco=endereco,
            nascimento=nascimento
        )
        self.session.add(new_client)
        await self.session.commit()
        await self.session.refresh(new_client)
        return new_client

    async def get_client_by_id(self, client_id: int) -> Optional[Client]:
        stmt = select(Client).where(Client.id == client_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_client_by_name(self, name: str) -> List[Client]:
        stmt = select(Client).where(Client.name.ilike(f"%{name}%"))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_client_by_document(self, tipo_documento: str) -> Optional[Client]:
        stmt = select(Client).where(Client.tipo_documento == tipo_documento)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all_clients(self) -> List[Client]:
        stmt = select(Client).where(Client.is_active == True)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    # --- Supplier Operations ---

    async def create_supplier(self, name: str, tipo_documento: str, email: Optional[str], telefone: Optional[str], endereco: Optional[str]) -> Supplier:
        new_supplier = Supplier(
            name=name,
            tipo_documento=tipo_documento,
            email=email,
            telefone=telefone,
            endereco=endereco
        )
        self.session.add(new_supplier)
        await self.session.commit()
        await self.session.refresh(new_supplier)
        return new_supplier

    async def get_supplier_by_id(self, supplier_id: int) -> Optional[Supplier]:
        stmt = select(Supplier).where(Supplier.id == supplier_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_supplier_by_name(self, name: str) -> List[Supplier]:
        stmt = select(Supplier).where(Supplier.name.ilike(f"%{name}%"))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_supplier_by_document(self, tipo_documento: str) -> Optional[Supplier]:
        stmt = select(Supplier).where(Supplier.tipo_documento == tipo_documento)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all_suppliers(self) -> List[Supplier]:
        stmt = select(Supplier).where(Supplier.is_active == True)
        result = await self.session.execute(stmt)
        return result.scalars().all()