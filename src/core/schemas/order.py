from __future__ import annotations

from enum import Enum

from pydantic import BaseModel

from core.schemas import Book, User


class Status(Enum):
    PENDING = "pending"
    APPROVED = "confirmed"
    REJECTED = "rejected"

    def __str__(self):
        return self.value

class StatusMapping(Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"

    @staticmethod
    def from_status(status: Status) -> StatusMapping:
        return StatusMapping[status.name.upper()]


class StatusGetResponse(BaseModel):
    name: Status
    name_translated: StatusMapping


class Order(BaseModel):
    id: int | None = None
    user: int | None = None
    book: int | None = None
    quantity: int | None = None
    status: Status | None = None


class OrderPost(BaseModel):
    user_id: int
    book_id: int
    quantity: int


class OrderGetResponse(BaseModel):
    id: int
    user: User | None = None
    book: Book | None = None
    quantity: int
    status: StatusGetResponse
