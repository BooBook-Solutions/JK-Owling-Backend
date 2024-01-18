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

    book_title = book.title + " " + book.author
    # book_title = "Twilight"
    # {"title":"Twilight","rating":3.65,"first_publish_year":1990,"number_of_pages":498,"characters":["Edward Cullen","Bella Swan","Jacob Black","Carlisle Cullen","Esme Cullen","Alice Cullen","Emmett Cullen","Rosalie Hale","Jasper Hale","James","Victoria","Laurent","Billy Black"],"first_sentence":["MY MOTHER DROVE ME TO THE AIRPORT WITH THE windows rolled down.","I'd never given much thought to how I would die--though I had reason enough in the last few months--but even if I had, I would not have imagined it like this."],"languages":["eng","spa","chi","ger","pol","gre","por","fre","vie","ind","ara","rus"]}

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
    # book_title = "Twilight"
    # return [{"image":"https://m.media-amazon.com/images/I/81hJRgAMa7L.jpg","price":"11.22€","url":"https://www.amazon.com/What-Expect-First-Heidi-Murkoff/dp/0761181504/ref=sr_1_1?dib=eyJ2IjoiMSJ9.WPbQSLDK8CFwR_eR2OIIdyLxUSZaZrRTijLIewN4iG7keP-JsC1YffcI6AN_tYIHJX5vtMCAJ9GYGNA4g2mTycqXXVz5JEciCS6O6vFR5dXxqhknmKBxxoaHcrZHA0g9Yk2uE4Mj8p705bQZENrMHg.1QxYxmQN-gx5clgkim2LaGR30vAqSat7byCC46C5VAY&dib_tag=se&keywords=Book+First+book&qid=1705245695&sr=8-1","stars":4.8},{"image":"https://m.media-amazon.com/images/I/71eUoeoSoBL.jpg","price":"13.95€","url":"https://www.amazon.com/First-Little-Readers-Parent-Pack/dp/0545231493/ref=sr_1_2?dib=eyJ2IjoiMSJ9.WPbQSLDK8CFwR_eR2OIIdyLxUSZaZrRTijLIewN4iG7keP-JsC1YffcI6AN_tYIHJX5vtMCAJ9GYGNA4g2mTycqXXVz5JEciCS6O6vFR5dXxqhknmKBxxoaHcrZHA0g9Yk2uE4Mj8p705bQZENrMHg.1QxYxmQN-gx5clgkim2LaGR30vAqSat7byCC46C5VAY&dib_tag=se&keywords=Book+First+book&qid=1705245695&sr=8-2","stars":4.7},{"image":"https://m.media-amazon.com/images/I/81vaq5oh1nL.jpg","price":"6.99€","url":"https://www.amazon.com/First-100-Animals-Sticker-Book/dp/0312520115/ref=sr_1_3?dib=eyJ2IjoiMSJ9.WPbQSLDK8CFwR_eR2OIIdyLxUSZaZrRTijLIewN4iG7keP-JsC1YffcI6AN_tYIHJX5vtMCAJ9GYGNA4g2mTycqXXVz5JEciCS6O6vFR5dXxqhknmKBxxoaHcrZHA0g9Yk2uE4Mj8p705bQZENrMHg.1QxYxmQN-gx5clgkim2LaGR30vAqSat7byCC46C5VAY&dib_tag=se&keywords=Book+First+book&qid=1705245695&sr=8-3","stars":4.8},{"image":"https://m.media-amazon.com/images/I/81g3WrvekaL.jpg","price":"11.99€","url":"https://aax-us-iad.amazon.com/x/c/RKdz2j3W8f6cGfuEpdQuMOAAAAGNCJBfawEAAAH2AQBvbm9fdHhuX2JpZDYgICBvbm9fdHhuX2ltcDEgICBgBVYh/https://www.amazon.com/Should-Darla-Featuring-Power-Choose/dp/173309461X/ref=sxin_14_sbv_search_btf?content-id=amzn1.sym.6ca944f8-539c-499e-a3a4-26a566d1de59%3Aamzn1.sym.6ca944f8-539c-499e-a3a4-26a566d1de59&cv_ct_cx=Book+First+book&dib=eyJ2IjoiMSJ9.XIylDFZYui7qI6KeKeabIg.FYqYSTESlAfYbDqLUD2Mcn0y3FAr7RLtrTfGLbutHp8&dib_tag=se&keywords=Book+First+book&pd_rd_i=173309461X&pd_rd_r=579622ad-8a89-420e-8d44-c5a36bb806ad&pd_rd_w=NhhEE&pd_rd_wg=49VLR&pf_rd_p=6ca944f8-539c-499e-a3a4-26a566d1de59&pf_rd_r=C4NXNQM6N7CNJEGVTQS7&qid=1705245695&sbo=RZvfv%2F%2FHxDF%2BO5021pAnSA%3D%3D&sr=1-1-5190daf0-67e3-427c-bea6-c72c1df98776","stars":4.8},{"image":"https://m.media-amazon.com/images/I/81lmTHZOD1L.jpg","price":"7.59€","url":"https://www.amazon.com/First-Numbers-Colors-Shapes-100/dp/0312520638/ref=sr_1_4?dib=eyJ2IjoiMSJ9.WPbQSLDK8CFwR_eR2OIIdyLxUSZaZrRTijLIewN4iG7keP-JsC1YffcI6AN_tYIHJX5vtMCAJ9GYGNA4g2mTycqXXVz5JEciCS6O6vFR5dXxqhknmKBxxoaHcrZHA0g9Yk2uE4Mj8p705bQZENrMHg.1QxYxmQN-gx5clgkim2LaGR30vAqSat7byCC46C5VAY&dib_tag=se&keywords=Book+First+book&qid=1705245695&sr=8-4","stars":4.8}]

    url = AMAZON_EXTRACTOR_URL + urllib.parse.quote("Book " + book_title + " " + book.author)

    querystring = {"api_key": AMAZON_EXTRACTOR_KEY}

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "amazon_data_extractor.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring, verify=False)

    parameters = ["name", "image", "stars", "url"]
    listings = []
    for result in response.json()["results"][:5]:
        listing = {parameter: (result[parameter] if parameter in result else "") for parameter in parameters}
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
