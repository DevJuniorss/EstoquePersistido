from app.db.database import get_session
from sqlmodel import func, select
from app.models.product import Product
from app.models.product_order import ProductOrder


async def get_all_products(size: int, offset: int):
    with get_session() as session:
        total = session.exec(
            select(func.count()).select_from(Product)
        ).one()

        products = session.exec(
            select(Product)
            .limit(size)
            .offset(offset)
        ).all()

    return products, total
    
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
    
async def count_orders_by_product_crud(product_id: int) -> int:
    with get_session() as session:
        statement = (
            select(func.count(func.distinct(ProductOrder.order_id)))
            .where(ProductOrder.product_id == product_id)
        )

        result = session.exec(statement).one()
        return result