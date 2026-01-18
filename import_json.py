import asyncio
import json
import os
from datetime import datetime
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.models.client import Client
from app.models.product import Product
from app.models.order import Order, OrderItem, Payment

load_dotenv()

async def main():
    db_url = os.getenv("DATABASE_URL")
    print(f" Conectando em: {db_url}")
    client = AsyncIOMotorClient(db_url)
    database = client.get_database("estoque_db")
    
    await init_beanie(database=database, document_models=[Client, Product, Order])

    print("📂 Reading dados_antigos.json file...")
    with open("dados_antigos.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    print("--- 🗑️  Cleaning current database... ---")
    await Order.delete_all()
    await Product.delete_all()
    await Client.delete_all()

    map_clients = {}
    map_products = {}

    print("--- 👤 Importing Clients... ---")
    for c_data in data["clients"]:
        new_client = await Client(
            name=c_data["name"],
            email=c_data["email"],
            address=c_data["address"]
        ).create()
        
        map_clients[c_data["id"]] = new_client

    print("--- 📦 Importing Products... ---")
    for p_data in data["products"]:
        new_product = await Product(
            name=p_data["name"],
            quantity=p_data["quantity"],
            unitPrice=p_data["unitPrice"]
        ).create()
        
        map_products[p_data["id"]] = new_product

    print("--- 🛒 Importing Orders and Payments... ---")
    for o_data in data["orders"]:
        
        real_client = map_clients.get(o_data["clientId"])
        
        order_items = []
        for p_id in o_data["productIds"]:
            prod = map_products.get(p_id)
            if prod:
                item = OrderItem(product=prod, quantity=1)
                order_items.append(item)

        pay_data = next((p for p in data["payments"] if p["orderId"] == o_data["id"]), None)
        
        payment_obj = None
        if pay_data:
            payment_obj = Payment(
                payment_method=pay_data["paymentMethod"],
                payment_date=datetime.fromisoformat(pay_data["paymentDate"]),
                status="PAID" if pay_data["paymentStatus"] else "PENDING"
            )

        await Order(
            order_date=datetime.fromisoformat(o_data["orderDate"]),
            movement_type=o_data["movementType"].upper(),
            client=real_client,
            payment=payment_obj,
            items=order_items
        ).create()

    print("Import completed successfully!")

if __name__ == "__main__":
    asyncio.run(main())