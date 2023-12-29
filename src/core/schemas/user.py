from __future__ import annotations

from pydantic import BaseModel


class User(BaseModel):
    id: str | None = None
    name: str | None = None
    surname: str | None = None
    email: str | None = None
    picture: str | None = None
    role: str | None = None
