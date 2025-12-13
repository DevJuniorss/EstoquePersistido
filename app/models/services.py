from database import Database
import statistics

class ProductService:
    def __init__(self):
        self.db = Database()

    async def create_product(self, name, price):
        if price <= 0:
            return {"error": "Price must be positive"}
        return await self.db.add(name, price)

    async def get_products(self):
        return await self.db.get_all()

    async def get_highest_price(self):
        products = await self.db.get_all()
        if not products:
            return {"error": "No products"}
        return max(products, key=lambda x: x['price'])

    async def get_lowest_price(self):
        products = await self.db.get_all()
        if not products:
            return {"error": "No products"}
        return min(products, key=lambda x: x['price'])

    async def get_average_price(self):
        products = await self.db.get_all()
        if not products:
            return {"average": 0}
        prices = [p['price'] for p in products]
        return {"average": statistics.mean(prices)}

    async def get_above_average(self):
        products = await self.db.get_all()
        if not products:
            return []
        avg = statistics.mean(p['price'] for p in products)
        return [p for p in products if p['price'] >= avg]

    async def get_below_average(self):
        products = await self.db.get_all()
        if not products:
            return []
        avg = statistics.mean(p['price'] for p in products)
        return [p for p in products if p['price'] < avg]

    async def delete_product(self, product_id):
        success = await self.db.delete(product_id)
        if success:
            return {"message": "Product deleted"}
        return {"error": "Product not found"}
    

    # async def get_recent_products(self):
    #     """10 ultimos adicionados"""
    #     return self.products[-10:]

    # async def get_recently_deleted(self):
    #     """10 últimos excluídos"""
    #     return self.deleted_products[-10:]