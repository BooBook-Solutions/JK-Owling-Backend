from fastapi import APIRouter
from app.routers.book import router as book_router

router = APIRouter(
    tags=["app"],
    responses={404: {"description": "Release not found"}},
)

router.include_router(book_router, prefix="/book")
