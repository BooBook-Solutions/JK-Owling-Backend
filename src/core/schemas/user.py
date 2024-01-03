from __future__ import annotations

from enum import Enum

from pydantic import BaseModel

from app.settings import ADMIN_ROLE, USER_ROLE


class UserRole(Enum):
    ADMIN = ADMIN_ROLE
    USER = USER_ROLE

    def __str__(self):
        return str(self.value)

    def __eq__(self, other: str):
        return self.value == other

    def __ne__(self, other: str):
        return self.value != other


class UserRoleMapping(Enum):
    ADMIN = "Admin"
    USER = "User"

    @staticmethod
    def from_user_role(user_role: UserRole) -> UserRoleMapping:
        return UserRoleMapping[user_role.name.upper()]


class UserRoleGetResponse(BaseModel):
    name: UserRole
    name_translated: UserRoleMapping


class User(BaseModel):
    id: str | None = None
    name: str | None = None
    surname: str | None = None
    email: str | None = None
    picture: str | None = None
    role: UserRole | None = None


class UserGetResponse(BaseModel):
    id: str
    name: str | None = None
    surname: str | None = None
    email: str | None = None
    picture: str | None = None
    role: UserRoleGetResponse
