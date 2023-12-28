import logging

from fastapi import FastAPI, Request

from app.base import router as app_router
from app.middlewares.authentication import authentication_middleware


logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level
    format="%(asctime)s - %(levelname)s - %(message)s"
)


app = FastAPI()


@app.middleware("http")
async def attach_authentication_middleware(request: Request, call_next):
    response = await authentication_middleware(request, call_next)
    return response

app.include_router(app_router, prefix="")
