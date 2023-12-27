from __future__ import annotations

from pydantic import BaseModel


class Book(BaseModel):
    id: int
    name: str
    isbn: str | None = None
    author: str | None = None
