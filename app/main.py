from fastapi import FastAPI
from datetime import datetime
from app.db.database import engine
from app.routers.routers import api_router
from contextlib import asynccontextmanager
from app.db.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(api_router)

