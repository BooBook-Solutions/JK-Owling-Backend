from fastapi import APIRouter, Depends

from app.authentication import authenticated_user, authenticated_admin
from app.database import get_db
import logging

logger = logging.getLogger("app.routers.book")

router = APIRouter(
    tags=["book"]
)


@router.get("")
async def get_books(name: str = "",
                    user=Depends(authenticated_user), db=Depends(get_db)):
    books = db.get_collection("book")
    logger.info("List of books: " + str([b.id for b in books]))
    return await books.filter()


@router.post("")
async def create_book(name: str, isbn: str = "", author: str = "",
                      user=Depends(authenticated_admin), db=Depends(get_db)):
    books = db.get_collection("book")
    book = books.create({"name": name, "isbn": isbn, "author": author})
    logger.info("Admin "+str(user.id)+" created book: " + str(book))
    return {"book": book, "message": "Book created successfully"}
