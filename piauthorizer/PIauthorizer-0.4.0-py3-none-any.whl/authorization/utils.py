import sys

import jwt
from fastapi import Depends, HTTPException, status

from . import ALGORITHM, AUDIENCE, jwks_client, oauth2_scheme
from .schemas import User


async def override():
    return True


def get_dependencies() -> list:
    """return the basic PI authorization dependencies for FastAPI

    Returns:
        [list]: basic dependency list
    """
    dependencies = []

    if "--reload" not in sys.argv:
        dependencies = [Depends(get_current_user)]

    return dependencies


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        payload = jwt.decode(
            token, signing_key.key, audience=AUDIENCE, algorithms=[ALGORITHM]
        )
    except Exception as _:
        raise credentials_exception
    user = User(username=payload.get("name"), email=payload.get("email"))

    return user
