from fastapi import FastAPI

from core.database import Database
from v1.base import router as v1_router

app = FastAPI()

database = Database()
app.database = database

app.include_router(v1_router, prefix="/v1")
