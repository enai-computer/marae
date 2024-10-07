from fastapi import APIRouter, Request

router = APIRouter(prefix="/v1", tags=["v1"])

@router.get("/verify")
def verify(request: Request):
    # return jwt token, based on user_id
    return {"token": "jwt_token"}

