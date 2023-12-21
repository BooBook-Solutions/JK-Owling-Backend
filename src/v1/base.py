from fastapi import APIRouter
from v1.routers.authentication.username_password import router as authentication_router

router = APIRouter(
    tags=["v1"],
    responses={404: {"description": "Release not found"}},
)

router.include_router(authentication_router, prefix="/authentication")
