from fastapi import APIRouter, Depends
from typing import Annotated
from uuid import UUID
from urllib.parse import unquote
from app.rest.models.AnswerPayload import AnswerPayload
from app.AnswerEngine import AnswerEngine
from app.services.CheckTokenService import get_current_user
from posthog import Posthog
from app.SecretsService import secretsStore

router = APIRouter(
    prefix="/v1", 
    tags=["v1"],
    dependencies=[Depends(get_current_user)]
    )

posthog = Posthog(secretsStore.secrets["POSTHOG_API_KEY"], host='https://eu.i.posthog.com')

@router.get("/{user_id}/answer")
def answer(user_id: UUID, q: str, answer_engine: Annotated[AnswerEngine, Depends(AnswerEngine)]):
    decoded_q = unquote(q)
    return answer_engine.get_answer(question=decoded_q, messages=[], is_streaming=False)

@router.post("/{user_id}/answer")
async def answer(
    user_id: UUID,
    answer_engine: Annotated[AnswerEngine, Depends(AnswerEngine)],
    payload: AnswerPayload,
):
    posthog.capture(user_id, event="asked_en-ai", properties={"ui-component": "new-tab"})
    return answer_engine.get_answer(
        question=payload.question,
        messages=payload.messages,
        is_streaming=payload.is_streaming
    )

@router.get("/{user_id}/welcome-text")
def welcome_text(user_id: UUID, sname: str, answer_engine: Annotated[AnswerEngine, Depends(AnswerEngine)]):
    decoded_space_name = unquote(sname)
    return answer_engine.get_welcome_text(decoded_space_name)
