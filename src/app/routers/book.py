import json
import urllib.parse
from typing import List

import requests
from fastapi import APIRouter, Depends
from google.rpc.http_pb2 import HttpResponse

from app.authentication import authenticated_admin
from app.common import RequestException
from app.database import get_db
import logging
from starlette.requests import Request

from app.settings import RAPIDAPI_KEY, AMAZON_EXTRACTOR_URL, BOOK_INFO_URL
from core.schemas import Book
from core.schemas.book import BookListing, BookInfo

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

    book_title = book.title
    book_title = "Twilight"
    # {"title":"Twilight","rating":3.65,"first_publish_year":1990,"number_of_pages":498,"characters":["Edward Cullen","Bella Swan","Jacob Black","Carlisle Cullen","Esme Cullen","Alice Cullen","Emmett Cullen","Rosalie Hale","Jasper Hale","James","Victoria","Laurent","Billy Black"],"first_sentence":["MY MOTHER DROVE ME TO THE AIRPORT WITH THE windows rolled down.","I'd never given much thought to how I would die--though I had reason enough in the last few months--but even if I had, I would not have imagined it like this."],"languages":["eng","spa","chi","ger","pol","gre","por","fre","vie","ind","ara","rus"]}

    query_params = {
        "q": book_title,
        "limit": 1,
        "offset": 0
    }

    response = requests.get(BOOK_INFO_URL, params=query_params)
    response.encoding = "utf-8"
    print(response.text)
    json_response = json.loads(response.text)

    num_found = json_response["num_found"]
    result = {"found": False, "title": book_title}
    if num_found > 0:
        result = {
            "found": True,
            "first_publish_year": json_response["docs"][0]["first_publish_year"],
            "title": json_response["docs"][0]["title"],
            "number_of_pages": json_response["docs"][0]["number_of_pages_median"],
            "rating": json_response["docs"][0]["ratings_average"],
            "characters": json_response["docs"][0]["person"],
            "first_sentence": json_response["docs"][0]["first_sentence"],
            "languages": json_response["docs"][0]["language"],
        }

    print(result)

    return result


@router.get("/{book_id}/listings", response_model=List[BookListing])
async def get_book_listings(book_id: str, db=Depends(get_db)):
    book = await db.get_collection("book").get(book_id)
    if book is None:
        raise RequestException("Book not found")

    book_title = book.title
    book_title = "Twilight"
    url = AMAZON_EXTRACTOR_URL + urllib.parse.quote("Book " + book_title)

    querystring = {"api_key": RAPIDAPI_KEY}

    headers = {
        "X-RapidAPI-Key": "8e4d03a16emsh4c574cf7fcd0921p15d969jsn090c76ac9db1",
        "X-RapidAPI-Host": "amazon_data_extractor.p.rapidapi.com"
    }

    print(url)
    response = requests.get(url, headers=headers, params=querystring)

    print(response.json())

    results = [{
        "image": result["image"],
        "stars": result["stars"],
        "price": result["price_string"],
        "url": result["url"]
    } for result in response.json()["results"][:5]]

    print(results)

    return results


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
