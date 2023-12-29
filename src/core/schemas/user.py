from __future__ import annotations

from pydantic import BaseModel


class User(BaseModel):
    id: str | None = None
    name: str | None = None
    email: str | None = None
    password: str | None = None
    role: str | None = None
