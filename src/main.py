import logging
import traceback

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import Response, JSONResponse

from app.base import router as app_router
from app.common import RequestException
from app.middlewares.authentication import authentication_middleware
from app.settings import FRONTEND_URL
from core.schemas.common import ExceptionResponse

logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level
    format="%(asctime)s - %(levelname)s - %(message)s"
)


app = FastAPI()


@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except RequestException as e:
        traceback.print_exc()
        exception_response = ExceptionResponse(message=str(e))
        return JSONResponse(content=jsonable_encoder(exception_response), status_code=400)

origins = [
    FRONTEND_URL,  # replace with your frontend domain
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # specify allowed HTTP methods
    allow_headers=["*"],  # allow all headers, adjust as needed
    expose_headers=["Content-Disposition"],  # expose specific headers, if required
)


@app.middleware("http")
async def attach_authentication_middleware(request: Request, call_next):
    response = await authentication_middleware(request, call_next)
    return response


app.include_router(app_router, prefix="")
