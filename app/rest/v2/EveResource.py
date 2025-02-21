from fastapi import APIRouter, FastAPI
from contextlib import asynccontextmanager
from uuid import UUID
from app.rest.models.EveModelsV2 import ChatPayload
from app.SecretsService import secretsStore
from posthog import Posthog
from app.AnswerEngine import AnswerEngine


answerEngine = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global answerEngine
    answerEngine = AnswerEngine()
    yield

router = APIRouter(
    prefix="/v2",
    tags=["v2"],
    # dependencies=[Depends(get_current_user)],
    lifespan=lifespan
)

posthog = Posthog(secretsStore.secrets["POSTHOG_API_KEY"], host='https://eu.i.posthog.com')


@router.post("/{user_id}/chat")
async def get_answer(user_id: UUID, payload: ChatPayload):
    print(f'answer engine: {answerEngine}')
    return answerEngine.get_answer_v2(payload)
