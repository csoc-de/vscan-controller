from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from vscan_controller.config import API_KEY

_default_http_auth_credentials = Depends(HTTPBearer())


async def authorization(
    auth: HTTPAuthorizationCredentials | None = _default_http_auth_credentials,
):
    if auth is None or auth.credentials != API_KEY:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, detail="bearer token is missing or unknown"
        )
