from fastapi import Depends, APIRouter
from app.services.CheckTokenService import get_current_user

router = APIRouter(
    prefix="/v1",
    tags=["v1"],
    dependencies=[Depends(get_current_user)]
    )

@router.get("/version")
def version():
    return {
        "api-version": "v1",
        "mac-version": "0.2.0",
        "mac-build": "2024-10-14.1"
    }
