from __future__ import annotations

import logging

from fastapi import HTTPException, Depends, Request
from google.auth.transport import requests
from google.oauth2 import id_token

from app.database import get_db
from app.settings import GOOGLE_CLIENT_ID
from core.schemas import User

logger = logging.getLogger("app.authentication")


def verify_google_token(token: str) -> dict | None:
    try:
        # Verify the token with Google
        id_info = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)

        # Extract relevant user information from the verified token
        user_info = {
            "sub": id_info.get("sub"),  # Subject (user ID)
            "email": id_info.get("email"),
            "name": id_info.get("name"),
            "family_name": id_info.get("family_name"),
            "picture": id_info.get("picture"),
            # Add more fields as needed
        }

        return user_info

    except ValueError as e:
        # Token verification failed
        logger.info(f"Token verification failed: {e}")
        return None


async def authenticated_user(request: Request, db=Depends(get_db)) -> User:
    user_is_authenticated = request.state.is_authenticated
    if not user_is_authenticated:
        raise HTTPException(status_code=401, detail="Authentication is required to access this resource")
    authenticated_token = request.state.authenticated_token
    user_collection = db.get_collection("user")
    user_id = authenticated_token.get("sub")
    user = user_collection.get(user_id)

    if user is None:
        raise HTTPException(status_code=401, detail="Credentials are invalid")
    return user


async def authenticated_admin(user: User = Depends(authenticated_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="You do not have permission to access this resource")
    return user
