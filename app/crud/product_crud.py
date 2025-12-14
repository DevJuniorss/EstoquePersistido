from app.db.database import get_session
from sqlmodel import select
from app.models.product import Product


async def get_all_products():
    with get_session() as session:
        return session.exec(select(Product)).all()
    
async def get_product_crud(product_id: int):
    with get_session() as session:
        product = session.get(Product, product_id)
        return product

async def create_product_crud(product: Product):
    with get_session() as session:
        session.add(product)
        session.commit()
        session.refresh(product)
        return product
    
async def update_product_crud(product_id: int, product_data: Product):
    with get_session() as session:
        product = session.get(Product, product_id)
        if not product:
            return None
        for key, value in product_data.model_dump(exclude_unset=True).items():
            setattr(product, key, value)
        session.add(product)
        session.commit()
        session.refresh(product)
        return product

async def delete_product_crud(product_id: int):
    with get_session() as session:
        product = session.get(Product, product_id)
        if not product:
            return None
        session.delete(product)
        session.commit()
        return product