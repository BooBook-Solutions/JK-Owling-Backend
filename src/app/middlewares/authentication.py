from fastapi import HTTPException, Request, Depends
from jose import jwt, JWTError

from app.database import get_db
from app.settings import HASH_SECRET_KEY, HASH_ALGORITHM


async def authentication_middleware(request: Request, call_next, db=Depends(get_db)):
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
            payload = jwt.decode(token, HASH_SECRET_KEY, algorithms=[HASH_ALGORITHM])
            if payload is None:
                raise credentials_exception
            else:
                user = db.get_collection("user").get(payload.get("sub"))
                if user is None:
                    raise credentials_exception
                request.state.is_authenticated = True
                request.state.authenticated_token = payload
        except JWTError:
            raise credentials_exception

    response = await call_next(request)
    return response
