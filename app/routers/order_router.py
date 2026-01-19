from fastapi import APIRouter, Query
from app.services.order_service import *

order_router = APIRouter(prefix="/orders")




@order_router.post("/")
async def create_order(order: OrderCreate):
    return await create_order_service(order)

@order_router.get("/")
async def get_orders(
    size: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """Retrieve a paginated list of orders."""
    return await list_orders(size=size, offset=offset)

@order_router.get("/{order_id}")
async def get_order(order_id: str):
    """Retrieve an order by its ID, including client, payment, and products."""
    data = await get_order_service(order_id)
    print(data)
    return data


@order_router.delete("/{order_id}")
async def delete_order(order_id: str):
    """Delete an order by its ID."""
    deleted_order = await delete_order_service(order_id)
    return deleted_order


@order_router.put("/{order_id}")
async def update_order(order_id: str, order_data: Order):
    """Update an existing order by its ID."""
    updated_order = await update_order_service(order_id, order_data)
    return updated_order

@order_router.get("/reports/stats")
async def get_order_stats():
    """Retorna estatísticas agregadas do sistema."""
    return await get_general_stats()

@order_router.get("/reports/year/{year}")
async def get_by_year(year: int):
    """Lista pedidos filtrados por ano."""
    return await get_orders_report_by_year(year)

@order_router.get("/search/all_client_orders")
async def all_client_orders(client_id: str):
    """Consulta todos os pedidos de um cliente específico detalhando os produtos.
    """
    orders = await Order.find(Order.client.id == PydanticObjectId(client_id), fetch_links=True).to_list()
    return {"client_id": client_id, "orders": orders}