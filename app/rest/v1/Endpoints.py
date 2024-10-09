from fastapi import APIRouter, Depends, Request
from typing import Annotated
from datetime import timedelta
from uuid import UUID
from ...AnswerEngine import AnswerEngine

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

router = APIRouter(prefix="/v1", tags=["v1"])


# def create_access_token(data: dict, expires_delta: timedelta | None = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.now(timezone.utc) + expires_delta
#     else:
#         expire = datetime.now(timezone.utc) + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=ALGORITHM)
#     return encoded_jwt

@router.get("/{user_id}/answer")
def answer(user_id: UUID, request: Request, answer_engine: Annotated[AnswerEngine, Depends(AnswerEngine)]):
    return answer_engine.get_answer(request.query_params.get('q'))


