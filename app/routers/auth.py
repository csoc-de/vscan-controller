from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config import API_KEY

get_bearer_token = HTTPBearer()


async def authorization(
        auth: Optional[HTTPAuthorizationCredentials] = Depends(get_bearer_token),
):
    if auth is None or auth.credentials != API_KEY:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="bearer token is missing or unknown"
        )
