from sqlmodel import Session, create_engine
from dotenv import load_dotenv
import logging
import os

load_dotenv()

logging.basicConfig(level=logging.INFO)
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

engine = create_engine(os.getenv("DATABASE_URL"), echo=True)

def get_session():
    return Session(engine, expire_on_commit=False)