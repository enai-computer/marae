from fastapi import APIRouter, Header, Depends, HTTPException
from typing import Annotated
from app.services.AuthService import AuthService
from app.rest.models.AuthModels import Token
import uuid

router = APIRouter(prefix="/v1", tags=["v1"])

@router.get("/verify")
def create_access_token(apple_device_token: Annotated[str | None, Header()] = None, auth_service: AuthService = Depends(AuthService)):
    result = auth_service.validate_device_token(apple_device_token)

    if result.is_ok:
        print('OK! Device is valid')
        return {"status": "ok"}
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
@router.get("/test-verify")
def create_access_token(apple_device_token: Annotated[str | None, Header()] = None, auth_service: AuthService = Depends(AuthService)) -> Token:
    device_id = str(uuid.uuid4())
    return auth_service.get_jwt_token(device_id)
