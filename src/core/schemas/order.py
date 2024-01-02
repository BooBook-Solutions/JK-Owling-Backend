from __future__ import annotations

from enum import Enum

from pydantic import BaseModel


class Status(Enum):
    PENDING = "pending"
    APPROVED = "confirmed"
    REJECTED = "rejected"


class Order(BaseModel):
    id: str | None = None
    user: str | None = None
    book: str | None = None
    status: Status | None = None
