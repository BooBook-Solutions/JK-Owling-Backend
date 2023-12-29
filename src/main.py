import logging

from fastapi import FastAPI, Request, Depends
from starlette.middleware.cors import CORSMiddleware

from app.base import router as app_router
from app.middlewares.authentication import authentication_middleware

logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level
    format="%(asctime)s - %(levelname)s - %(message)s"
)


app = FastAPI()

origins = [
    "http://localhost:3000",  # replace with your frontend domain
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
