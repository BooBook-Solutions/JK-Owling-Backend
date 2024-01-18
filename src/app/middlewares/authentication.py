from fastapi import HTTPException, Request
from jose import jwt, JWTError

from app.settings import HASH_SECRET_KEY, HASH_ALGORITHM
from core.schemas import User


async def authentication_middleware(request: Request, call_next):
    # Retrieve the token from the request headers
    token = request.headers.get("Authorization")
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    request.state.is_authenticated = False
    request.state.authenticated_user = None
    request.state.authenticated_token = None
    if token:
        try:
            token = token.split("Bearer ")[1]
            payload = jwt.decode(token, HASH_SECRET_KEY, algorithms=[HASH_ALGORITHM])
            if payload is None:
                raise credentials_exception
            request.state.is_authenticated = True
            request.state.authenticated_token = payload
            user_dict = payload.get("user")
            user_dict["role"] = user_dict["role"]["name"]
            request.state.authenticated_user = User(**payload.get("user"))

        except JWTError:
            raise credentials_exception

    response = await call_next(request)
    return response
