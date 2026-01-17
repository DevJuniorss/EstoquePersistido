import os
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models.client import Client
from app.models.order import Order
from app.models.product import Product


async def init_db():
    client = AsyncIOMotorClient(os.getenv("DATABASE_URL"))    
    database = client.get_database("stock_db")
    
    await init_beanie(database=database, document_models=[
        Client,
        Product,
        Order

    ])