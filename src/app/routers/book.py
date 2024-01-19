import json
import urllib.parse
from typing import List

import requests
from fastapi import APIRouter, Depends

from app.authentication import authenticated_admin
from app.common import RequestException
from app.database import get_db
import logging
from starlette.requests import Request

from app.settings import RAPIDAPI_KEY, AMAZON_EXTRACTOR_URL, BOOK_INFO_URL, AMAZON_EXTRACTOR_KEY
from core.schemas import Book
from core.schemas.book import BookListing, BookInfo, BookPut

logger = logging.getLogger("app.routers.book")

router = APIRouter(
    tags=["book"]
)


@router.get("", response_model=List[Book])
async def get_books(name: str = "", db=Depends(get_db)):
    books = await db.get_collection("book").filter()
    return books


@router.get("/{book_id}", response_model=Book)
async def get_book(book_id: str, db=Depends(get_db)):
    book = await db.get_collection("book").get(book_id)
    if book is None:
        raise RequestException("Book not found")
    return book


@router.get("/{book_id}/info", response_model=BookInfo)
async def get_book_info(book_id: str, db=Depends(get_db)):
    book = await db.get_collection("book").get(book_id)
    if book is None:
        raise RequestException("Book not found")

    book_title = book.title + " " + book.author
    query_params = {
        "q": book_title,
        "limit": 1,
        "offset": 0
    }

    response = requests.get(BOOK_INFO_URL, params=query_params)
    response.encoding = "utf-8"
    json_response = json.loads(response.text)

    num_found = json_response["num_found"]
    result = {
        "found": False,
        "title": book_title,
        "rating": None,
        "first_publish_year": None,
        "number_of_pages": None,
        "characters": None,
        "first_sentence": None,
        "languages": None
    }
    mapping = {
        "found": "found",
        "title": "title",
        "rating": "ratings_average",
        "first_publish_year": "first_publish_year",
        "number_of_pages": "number_of_pages_median",
        "characters": "person",
        "first_sentence": "first_sentence",
        "languages": "language"
    }
    if num_found > 0:
        result["found"] = True
        for key in result.keys():
            if mapping[key] in json_response["docs"][0]:
                result[key] = json_response["docs"][0][mapping[key]]

    return result


@router.get("/{book_id}/listings", response_model=List[BookListing])
async def get_book_listings(book_id: str, db=Depends(get_db)):
    book = await db.get_collection("book").get(book_id)
    if book is None:
        raise RequestException("Book not found")

    book_title = book.title
    url = AMAZON_EXTRACTOR_URL + urllib.parse.quote(book_title + " " + book.author)

    querystring = {"api_key": AMAZON_EXTRACTOR_KEY}

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "amazon_data_extractor.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring, verify=False)

    parameters = {"name": "", "image": "", "stars": 0, "url": ""}
    listings = []
    for result in response.json()["results"][:5]:
        listing = {parameter: (result[parameter] if parameter in result else parameters[parameter])
                   for parameter in parameters}
        listing["price"] = ""
        if "price" in result:
            listing["price"] = str(result["price"]) + "€"
        listings.append(listing)

    return listings


@router.post("", response_model=Book)
async def create_book(book: Book, user=Depends(authenticated_admin), db=Depends(get_db)):
    book = await db.get_collection("book").create(book)
    logger.info("Admin " + str(user.id) + " created book: " + str(book))
    return book


@router.put("/{book_id}", response_model=Book)
async def update_book(book_id: str, input_book: BookPut, request: Request, user=Depends(authenticated_admin), db=Depends(get_db)):
    book = await db.get_collection("book").get(book_id)
    if book is None:
        raise RequestException("Book not found")

    data = await request.json()
    book_data = Book(**(book.model_copy(update=data).dict()))
    updated_book = await db.get_collection("book").update(book_data)
    logger.info("Admin " + str(user.id) + " updated book: " + str(updated_book))
    return updated_book


@router.delete("/{book_id}", response_model=Book)
async def delete_book(book_id: str, user=Depends(authenticated_admin), db=Depends(get_db)):
    book = await db.get_collection("book").get(book_id)
    if book is None:
        raise RequestException("Book not found")
    orders = await db.get_collection("order").filter(book_id=book_id)
    if len(orders) > 0:
        raise RequestException("Cannot delete book with orders")
    result = await db.get_collection("book").delete(book_id)
    if result:
        logger.info("User " + str(user.id) + " deleted book: " + str(book))
    else:
        raise RequestException("Could not delete book")
    return book
