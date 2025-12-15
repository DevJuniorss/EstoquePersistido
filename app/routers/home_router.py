from fastapi import APIRouter

home_router = APIRouter()


@home_router.get("/")
async def read_home():
    """Return a welcome message for the home page."""
    return {"message": "Welcome to the Home Page"}
