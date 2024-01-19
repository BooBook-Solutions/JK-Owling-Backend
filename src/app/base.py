from fastapi import APIRouter
from app.routers.book import router as book_router
from app.routers.user import router as user_router
from app.routers.order import router as order_router
from app.routers.authentication import router as authentication_router

router = APIRouter(
    tags=["app"],
)

router.include_router(book_router, prefix="/books")
router.include_router(user_router, prefix="/users")
router.include_router(order_router, prefix="/orders")
router.include_router(authentication_router, prefix="/authentication")
