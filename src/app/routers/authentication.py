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
from core.schemas.user import UserRole, UserGetResponse, UserRoleGetResponse, UserRoleMapping

logger = logging.getLogger("app.routers.authentication")

router = APIRouter(
    tags=["book"]
)


@router.post("/login")
async def login_user(request: Request, response: Response, db=Depends(get_db)):
    data = await request.json()
    google_token = data.get("google_token")
    if google_token is None:
        raise Exception("Invalid google token")
    try:
        info = verify_google_token(google_token)

        if info:
            user = await db.get_collection("user").get(email=info.get("email"))
            if user is None:
                role = data.get("role")
                if role is None or role not in [v.value for v in UserRole.__members__.values()]:
                    raise Exception("Invalid role")
                new_user = User(**{"name": info.get("given_name"),
                                   "surname": info.get("family_name"),
                                   "picture": info.get("picture"),
                                   "email": info.get("email"),
                                   "role": UserRole(role)})
                user_collection = db.get_collection("user")
                user = await user_collection.create(new_user)
                logger.info("User created: " + str(user))

            response_dict = {k: v for k, v in user.model_dump().items() if k is not "role"}
            response_dict["role"] = {
                "name": user.role.value,
                "name_translated": UserRoleMapping.from_user_role(user.role).value
            }
            payload = {
                "user": response_dict,
                "expires": time.time() + (60 * 60 * 24)  # 24h
            }
            print(payload)

            token = jwt.encode(payload, HASH_SECRET_KEY, algorithm=HASH_ALGORITHM)

            response.status_code = status.HTTP_200_OK
            return {"token": token}

    except Exception as e:
        print(e)
        # print stack trace
        import traceback
        traceback.print_exc()

    response.status_code = status.HTTP_400_BAD_REQUEST
    return {"message": "Invalid login credentials"}
