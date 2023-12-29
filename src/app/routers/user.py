from typing import List

from fastapi import APIRouter, Depends

from app.authentication import authenticated_user
from app.common import RequestException
from app.database import get_db
import logging

from app.settings import ADMIN_ROLE
from core.schemas import User

logger = logging.getLogger("app.routers.user")

router = APIRouter(
    tags=["user"]
)


@router.get("", response_model=List[User])
async def get_users(db=Depends(get_db)):
    users = await db.get_collection("user").filter()
    return users


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: str, db=Depends(get_db)):
    user = await db.get_collection("user").get(user_id)
    return user


@router.put("/{user_id}", response_model=User)
async def update_user(user_id: str, user=Depends(authenticated_user), db=Depends(get_db)):
    request_user = await db.get_collection("user").get(user_id)
    if request_user is None:
        raise RequestException("User not found")
    if user.role != ADMIN_ROLE and user_id != user.id:
        raise RequestException("You are not allowed to update this user")
    updated_user = await db.get_collection("user").update(request_user)

    if user.role == ADMIN_ROLE:
        logger.info("Admin " + str(user.id) + " updated user: " + str(updated_user))
    else:
        logger.info("User " + str(user.id) + " updated to: " + str(updated_user))
    return updated_user


@router.delete("/{user_id}", response_model=User)
async def delete_user(user_id: str, user=Depends(authenticated_user), db=Depends(get_db)):
    request_user = await db.get_collection("user").get(user_id)
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
    return user

# MISSING METHODS: create_user
