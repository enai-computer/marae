from fastapi import Depends, HTTPException
from typing import Annotated
from app.SecretsService import secretsStore
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/test-verify")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> bool:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, secretsStore.secrets["JWT_SECRET_KEY"], algorithms=[secretsStore.secrets["JWT_ALGORITHM"]])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    return True
