from fastapi import APIRouter, Depends, Header
from typing import Annotated
from uuid import UUID
from app.rest.models.EveModelsV2 import ChatPayload
from app.AnswerEngine import AnswerEngine
from app.SecretsService import secretsStore
from posthog import Posthog


router = APIRouter(
    prefix="/v2",
    tags=["v2"],
    # dependencies=[Depends(get_current_user)]
)

posthog = Posthog(secretsStore.secrets["POSTHOG_API_KEY"], host='https://eu.i.posthog.com')

@router.post("/{user_id}/chat")
async def get_answer(user_id: UUID, answer_engine: Annotated[AnswerEngine, Depends(AnswerEngine)], payload: ChatPayload):
    # posthog.capture(user_id, event="asked_en-ai", properties={"ui-component": "new-tab", "model_id": payload.model_id})
    return answer_engine.get_answer_v2(payload)
