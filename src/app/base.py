from fastapi import APIRouter
from app.routers.book import router as book_router
from app.routers.authentication import router as authentication_router

router = APIRouter(
    tags=["app"],
    responses={404: {"description": "Release not found"}},
)

router.include_router(book_router, prefix="/books")
router.include_router(authentication_router, prefix="/authentication")
