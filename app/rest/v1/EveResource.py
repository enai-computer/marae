from fastapi import APIRouter, Depends
from typing import Annotated
from uuid import UUID
from urllib.parse import unquote
from app.AnswerEngine import AnswerEngine, Message
from app.services.CheckTokenService import get_current_user
from pydantic import BaseModel
from typing import List

class ContextPayload(BaseModel):
    messages: List[Message]

router = APIRouter(
    prefix="/v1", 
    tags=["v1"],
    dependencies=[Depends(get_current_user)]
    )

@router.get("/{user_id}/answer")
def answer(user_id: UUID, q: str, answer_engine: Annotated[AnswerEngine, Depends(AnswerEngine)]):
    decoded_q = unquote(q)
    return answer_engine.get_answer(decoded_q)

@router.post("/{user_id}/answer-stream")
async def answer_stream(
    user_id: UUID,
    q: str,
    answer_engine: Annotated[AnswerEngine, Depends(AnswerEngine)],
    payload: ContextPayload,
):
    decoded_q = unquote(q)
    return answer_engine.get_answer_stream(decoded_q, messages=payload.messages)

@router.get("/{user_id}/welcome-text")
def welcome_text(user_id: UUID, sname: str, answer_engine: Annotated[AnswerEngine, Depends(AnswerEngine)]):
    decoded_space_name = unquote(sname)
    return answer_engine.get_welcome_text(decoded_space_name)
