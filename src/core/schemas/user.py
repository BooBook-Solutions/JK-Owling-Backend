from __future__ import annotations

from pydantic import BaseModel


class User(BaseModel):
    id: int
    email: str | None = None
    full_name: str | None = None
    disabled: bool = False
    is_admin: bool = False
