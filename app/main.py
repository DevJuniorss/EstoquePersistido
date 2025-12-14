from fastapi import FastAPI
from datetime import datetime
from app.db.database import engine
from app.routers.routers import api_router

app = FastAPI()

app.include_router(api_router)

