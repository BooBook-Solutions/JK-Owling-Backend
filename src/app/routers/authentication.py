import time

from fastapi import APIRouter, Depends, Response
from jose import jwt
from starlette import status
from starlette.requests import Request

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
async def login_user(request: Request, response: Response, db=Depends(get_db)):
    data = await request.json()
    google_token = data.get("google_token")
    try:
        info = verify_google_token(google_token)

        if info:
            user = await db.get_collection("user").get(email=info.get("email"))
            if user is None:
                new_user = User(**{"name": info.get("name"),
                                   "email": info.get("email"),
                                   "password": "", "role": "user"})
                user_collection = db.get_collection("user")
                user = await user_collection.create(new_user)
                logger.info("User created: " + str(user))

            payload = {
                "user": user.dict(),
                "expires": time.time() + (60 * 60 * 24)  # 24h
            }

            token = jwt.encode(payload, HASH_SECRET_KEY, algorithm=HASH_ALGORITHM)

            response.status_code = status.HTTP_200_OK
            return {"token": token}

    except Exception as e:
        print(e)

    response.status_code = status.HTTP_400_BAD_REQUEST
    return {"message": "Invalid login credentials"}
