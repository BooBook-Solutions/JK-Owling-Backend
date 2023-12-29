from __future__ import annotations

from pydantic import BaseModel


class Book(BaseModel):
    id: str
    title: str
    description: str | None = None
    author: str | None = None
