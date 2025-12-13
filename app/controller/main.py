from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from services import ProductService

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

service = ProductService()

@app.get("/")
def read_root():
    return FileResponse('../front/index.html')

@app.post("/products")
async def create_product(name: str, price: float):
    return await service.create_product(name, price)

@app.get("/products")
async def get_products():
    return await service.get_products()

@app.get("/products/highest")
async def get_highest():
    return await service.get_highest_price()

@app.get("/products/lowest")
async def get_lowest():
    return await service.get_lowest_price()

@app.get("/products/average")
async def get_average():
    return await service.get_average_price()

@app.get("/products/above-average")
async def get_above_average():
    return await service.get_above_average()

@app.get("/products/below-average")
async def get_below_average():
    return await service.get_below_average()

@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    return await service.delete_product(product_id)



# N deu certo 

# @app.get("/products/recent")
# async def get_recent_products():
#     """Era para restornar os ultimos 10 produtos adicionados"""
#     return await service.get_recent_products()

# @app.get("/products/deleted")
# async def get_recently_deleted():
#     """Era para resotornar os ultimos 10 itens removidos do estoque"""
#     return await service.get_recently_deleted()