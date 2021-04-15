import os
import sys

import jwt
from fastapi import Depends, HTTPException, status
from jwt import PyJWKClient

from .forms import *
from .readiness import *

for env_variable in [
    "AUTH_STS_URL",
    "AUTH_ALGORITHM",
    "AUTH_AUDIENCE",
    "AUTH_SCOPE",
    "AUTH_LOGIN_URL",
    "AUTH_JWKS_URL",
]:
    if os.environ.get(env_variable) is None:
        raise KeyError(f"Environment variable {env_variable} missing")

STS_URL = os.environ.get("AUTH_STS_URL")
ALGORITHM = os.environ.get("AUTH_ALGORITHM")
AUDIENCE = os.environ.get("AUTH_AUDIENCE")
AUTH_SCOPE = os.environ.get("AUTH_SCOPE")
LOGIN_URL = os.environ.get("AUTH_LOGIN_URL")
oauth2_scheme = OAuth2ImplicitCodeBearer(
    authorizationUrl=LOGIN_URL,
    tokenUrl="token",
    scopes={AUTH_SCOPE: "Full Control"},
)
JWKS_URL = os.environ.get("AUTH_JWKS_URL")
jwks_client = PyJWKClient(JWKS_URL)


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
        jwt.decode(
            token, signing_key.key, audience=AUDIENCE, algorithms=[ALGORITHM]
        )
    except Exception as _:
        raise credentials_exception

    return True
