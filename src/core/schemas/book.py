from __future__ import annotations

from pydantic import BaseModel


class Book(BaseModel):
    id: str | None = None
    title: str | None = None
    description: str | None = None
    author: str | None = None
    price: float | None = None
    cover: str | None = None
    quantity: int | None = None
