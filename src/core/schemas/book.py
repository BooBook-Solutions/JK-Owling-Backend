from __future__ import annotations

from typing import Annotated, List

from pydantic import BaseModel, BeforeValidator


def convert_str_to_int(value: str) -> int:
    return int(value)


def convert_str_to_float(value: str) -> float:
    return float(value)


class Book(BaseModel):
    id: int | None = None
    title: str | None = None
    description: str | None = None
    author: str | None = None
    price: Annotated[float, BeforeValidator(convert_str_to_float)] | None = None
    cover: str | None = None
    quantity: Annotated[int, BeforeValidator(convert_str_to_int)] | None = None


class BookInfo(BaseModel):
    title: str | None = None
    rating: float | None = None
    first_publish_year: int | None = None
    number_of_pages: int | None = None
    characters: List[str] | None = None
    first_sentence: List[str] | None = None
    languages: List[str] | None = None


class BookListing(BaseModel):
    image: str | None = None
    price: str | None = None
    url: str | None = None
    stars: str | None = None
