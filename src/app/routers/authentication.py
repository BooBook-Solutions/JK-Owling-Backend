import time

from fastapi import APIRouter, Depends
from fastapi.openapi.models import Response
from jose import jwt
from starlette import status

from app.authentication import verify_google_token
from app.database import get_db
import logging

from app.settings import HASH_ALGORITHM, HASH_SECRET_KEY
from core.schemas import User

logger = logging.getLogger("app.routers.authentication")

router = APIRouter(
    tags=["book"]
)


@router.post("/login")
async def login_user(google_token: str, response: Response, db=Depends(get_db)):

    try:
        info = verify_google_token(google_token)

        if info:
            user = db.get_collection("user").get(info.get("sub"))
            if user is None:
                new_user = User(**{"name": info.get("name") + " " + info.get("family_name"),
                                   "email": info.get("email"),
                                   "password": "", "role": "user"})
                user = db.get_collection("user").create(new_user)
                logger.info("User created: " + str(user))

            payload = {
                "user": user,
                "expires": time.time() + (60 * 60 * 24)  # 24h
            }

            token = jwt.encode(payload, HASH_SECRET_KEY, algorithm=HASH_ALGORITHM)

            response.status_code = status.HTTP_200_OK
            return {"token": token}

    except ValueError:
        pass

    response.status_code = status.HTTP_400_BAD_REQUEST
    return {"message": "Invalid login credentials"}
