from __future__ import annotations

from typing import Annotated

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
