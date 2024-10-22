from fastapi import APIRouter, Depends
from typing import Annotated
from uuid import UUID
from urllib.parse import unquote
from app.rest.models.AnswerPayload import AnswerPayload
from app.AnswerEngine import AnswerEngine
from app.services.CheckTokenService import get_current_user

router = APIRouter(
    prefix="/v1", 
    tags=["v1"],
    dependencies=[Depends(get_current_user)]
    )

@router.post("/{user_id}/answer")
async def answer(
    user_id: UUID,
    answer_engine: Annotated[AnswerEngine, Depends(AnswerEngine)],
    payload: AnswerPayload,
):
    return answer_engine.get_answer(
        question=payload.question,
        messages=payload.messages,
        is_streaming=payload.is_streaming
    )

@router.get("/{user_id}/welcome-text")
def welcome_text(user_id: UUID, sname: str, answer_engine: Annotated[AnswerEngine, Depends(AnswerEngine)]):
    decoded_space_name = unquote(sname)
    return answer_engine.get_welcome_text(decoded_space_name)
