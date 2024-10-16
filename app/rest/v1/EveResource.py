from fastapi import APIRouter, Depends
from typing import Annotated
from uuid import UUID
from urllib.parse import unquote
from app.AnswerEngine import AnswerEngine
from app.services.CheckTokenService import get_current_user

router = APIRouter(
    prefix="/v1", 
    tags=["v1"],
    dependencies=[Depends(get_current_user)]
    )

@router.get("/{user_id}/answer")
def answer(user_id: UUID, q: str, answer_engine: Annotated[AnswerEngine, Depends(AnswerEngine)]):
    decoded_q = unquote(q)
    return answer_engine.get_answer(decoded_q)

@router.get("/{user_id}/welcome-text")
def welcome_text(user_id: UUID, sname: str, answer_engine: Annotated[AnswerEngine, Depends(AnswerEngine)]):
    decoded_space_name = unquote(sname)
    return answer_engine.get_welcome_text(decoded_space_name)
