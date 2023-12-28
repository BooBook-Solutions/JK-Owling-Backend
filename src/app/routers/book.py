from typing import List

from fastapi import APIRouter, Depends

from app.authentication import authenticated_user, authenticated_admin
from app.database import get_db
import logging

from core.schemas import Book

logger = logging.getLogger("app.routers.book")

router = APIRouter(
    tags=["book"]
)


@router.get("", response_model=List[Book])
async def get_books(name: str = "", db=Depends(get_db)):
    books = await db.get_collection("book").filter()
    return books


@router.get("/{book_id}", response_model=Book)
async def get_books(book_id: str, db=Depends(get_db)):
    book = await db.get_collection("book").get(book_id)
    return book


@router.post("/{book_id}/order", response_model=Book)
async def get_books(book_id: str, user=Depends(authenticated_user), db=Depends(get_db)):
    book = await db.get_collection("book").get(book_id)
    logger.info("User " + str(user.id) + " ordered book: " + str(book))
    return {"message": "Book ordered successfully"}


@router.post("", response_model=Book)
async def create_book(user=Depends(authenticated_admin), db=Depends(get_db)):
    logger.info("Admin " + str(user.id) + " created book: ")
    return {"message": "Book created successfully"}
