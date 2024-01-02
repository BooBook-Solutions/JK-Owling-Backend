from typing import List

from fastapi import APIRouter, Depends

from app.authentication import authenticated_admin
from app.common import RequestException
from app.database import get_db
import logging
from starlette.requests import Request

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


@router.post("", response_model=Book)
async def create_book(book: Book, user=Depends(authenticated_admin), db=Depends(get_db)):
    book = await db.get_collection("book").create(book)
    logger.info("Admin " + str(user.id) + " created book: " + str(book))
    return book


@router.put("/{book_id}", response_model=Book)
async def update_book(book_id: str, request: Request, user=Depends(authenticated_admin), db=Depends(get_db)):
    book = await db.get_collection("book").get(book_id)
    if book is None:
        raise RequestException("Book not found")

    data = await request.json()
    book_data = book.model_copy(update=data)
    updated_book = await db.get_collection("book").update(book_data)
    logger.info("Admin " + str(user.id) + " updated book: " + str(updated_book))
    return updated_book


@router.delete("/{book_id}", response_model=Book)
async def delete_book(book_id: str, user=Depends(authenticated_admin), db=Depends(get_db)):
    book = await db.get_collection("book").get(book_id)
    if book is None:
        raise RequestException("Book not found")
    print(book)
    print(book_id)
    result = await db.get_collection("book").delete(book_id)
    if result:
        logger.info("User " + str(user.id) + " deleted book: " + str(book))
    else:
        raise RequestException("Could not delete book")
    return book
