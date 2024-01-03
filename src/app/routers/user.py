from typing import List

from fastapi import APIRouter, Depends
from starlette.requests import Request

from app.authentication import authenticated_user
from app.common import RequestException
from app.database import get_db
import logging

from app.settings import ADMIN_ROLE
from core.schemas import User
from core.schemas.user import UserRole, UserRoleGetResponse, UserRoleMapping, UserGetResponse

logger = logging.getLogger("app.routers.user")

router = APIRouter(
    tags=["user"]
)


@router.get("/role", response_model=List[UserRoleGetResponse])
async def get_user_roles():
    user_roles = list(UserRole)
    response = [UserRoleGetResponse(name=role, name_translated=UserRoleMapping.from_user_role(role))
                for role in user_roles]
    return response


@router.get("", response_model=List[UserGetResponse])
async def get_users(db=Depends(get_db)):
    users = await db.get_collection("user").filter()
    users = [return_user(user) for user in users]
    return users


@router.get("/{user_id}", response_model=UserGetResponse)
async def get_user(user_id: str, db=Depends(get_db)):
    user = await db.get_collection("user").get(user_id)
    if user is None:
        raise RequestException("User not found")
    return return_user(user)


@router.put("/{user_id}", response_model=UserGetResponse)
async def update_user(user_id: str, request: Request, user=Depends(authenticated_user), db=Depends(get_db)):
    request_user = await db.get_collection("user").get(None, user_id=user_id)
    if request_user is None:
        raise RequestException("User not found")
    if user.role != ADMIN_ROLE and user_id != user.id:
        raise RequestException("You are not allowed to update this user")

    data = await request.json()
    updated_user = request_user.model_copy(update=data)
    updated_user = await db.get_collection("user").update(updated_user)

    if user.role == ADMIN_ROLE:
        logger.info("Admin " + str(user.id) + " updated user: " + str(updated_user))
    else:
        logger.info("User " + str(user.id) + " updated to: " + str(updated_user))
    updated_user = return_user(updated_user)
    return updated_user


@router.delete("/{user_id}", response_model=UserGetResponse)
async def delete_user(user_id: str, user=Depends(authenticated_user), db=Depends(get_db)):
    request_user = await db.get_collection("user").get(None, user_id=user_id)
    if request_user is None:
        raise RequestException("User not found")
    if user.role != ADMIN_ROLE and user_id != user.id:
        raise RequestException("You are not allowed to delete this user")
    result = await db.get_collection("user").delete(user_id)

    if result and user.role == ADMIN_ROLE:
        logger.info("Admin " + str(user.id) + " deleted user: " + str(request_user))
    elif result and user.role != ADMIN_ROLE:
        logger.info("User " + str(user.id) + " deleted user: " + str(request_user))
    else:
        raise RequestException("Could not delete user")
    user = return_user(request_user)
    return user


def return_user(user: User) -> UserGetResponse:
    return UserGetResponse(**{
        "id": user.id,
        "name": user.name,
        "surname": user.surname,
        "email": user.email,
        "picture": user.picture,
        "role": UserRoleGetResponse(name=user.role, name_translated=UserRoleMapping.from_user_role(user.role))
    })

# MISSING METHODS: create_user
