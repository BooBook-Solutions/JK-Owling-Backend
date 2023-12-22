from fastapi import APIRouter
from v1.routers.authentication.username_password import router as authentication_router
from v1.routers.authentication.google import router as google_router

router = APIRouter(
    tags=["v1"],
    responses={404: {"description": "Release not found"}},
)

router.include_router(authentication_router, prefix="/authentication")
router.include_router(google_router, prefix="/google")
