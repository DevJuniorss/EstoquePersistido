import pandas as pd
import os
import asyncio

class Database:
    def __init__(self, filename="products.csv"):
        self.filename = filename
        self.lock = asyncio.Lock()
        self.last_id_file = "last_id.txt"
        self.last_id = self._load_last_id()
        self._create_file()

    def _create_file(self):
        if not os.path.exists(self.filename):
            df = pd.DataFrame(columns=["id", "name", "price"])
            df.to_csv(self.filename, index=False)

    def _load_last_id(self):
        if os.path.exists(self.last_id_file):
            with open(self.last_id_file, "r") as f:
                return int(f.read().strip() or 0)
        return 0

    def _save_last_id(self):
        with open(self.last_id_file, "w") as f:
            f.write(str(self.last_id))

    async def get_all(self):
        if not os.path.exists(self.filename):
            return []
        df = pd.read_csv(self.filename)
        return df.to_dict(orient="records")

    async def add(self, name, price):
        async with self.lock:
            self.last_id += 1
            self._save_last_id()

            df = pd.DataFrame([[self.last_id, name, price]], columns=["id", "name", "price"])
            df.to_csv(self.filename, mode="a", header=not os.path.exists(self.filename) or os.stat(self.filename).st_size == 0, index=False)
            return {"id": self.last_id, "name": name, "price": price}

    async def delete(self, product_id):
        async with self.lock:
            if not os.path.exists(self.filename):
                return False
            df = pd.read_csv(self.filename)
            new_df = df[df["id"] != product_id]
            if len(new_df) == len(df):
                return False
            new_df.to_csv(self.filename, index=False)
            return True
