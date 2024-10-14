from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from .rest.v1 import AuthResource
from app.services.AuthService import AuthService
from typing import Annotated
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException, status
from app.SecretsService import secretsStore

webServer = FastAPI()
webServer.include_router(AuthResource.router)
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

#
# MARK: - API here:
#
@webServer.get("/status")
def status(verified: Annotated[bool, Depends(get_current_user)]):
    return {"status": "ok"}

@webServer.get("/")
def health_check():
    return {"status": "healthy"}

@webServer.get("/version")
def version():
    return {"version": "0.1"}
