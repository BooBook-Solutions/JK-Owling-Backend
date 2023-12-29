from fastapi import HTTPException, Request
from jose import jwt, JWTError

from app.settings import HASH_SECRET_KEY, HASH_ALGORITHM


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
    if token:
        try:
            token = token.split("Bearer ")[1]
            payload = jwt.decode(token, HASH_SECRET_KEY, algorithms=[HASH_ALGORITHM])
            if payload is None:
                raise credentials_exception

        except JWTError:
            raise credentials_exception

    response = await call_next(request)
    return response
