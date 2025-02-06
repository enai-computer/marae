from fastapi import APIRouter, Depends, Header
from typing import Annotated, List
from uuid import UUID
import markdown
from urllib.parse import unquote
from app.rest.models.EveModels import AnswerPayload, WelcomeTextPayload, AIModel
from app.AnswerEngine import AnswerEngine
from app.provider.LLMInterface import LLMInterface
from app.services.CheckTokenService import get_current_user
from posthog import Posthog
from app.SecretsService import secretsStore

router = APIRouter(
    prefix="/v1", 
    tags=["v1"],
    dependencies=[Depends(get_current_user)]
    )

posthog = Posthog(secretsStore.secrets["POSTHOG_API_KEY"], host='https://eu.i.posthog.com')

@router.get("/{user_id}/ai-models")
def get_ai_models(user_id: UUID):
    return {"models": LLMInterface.available_models}

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
    posthog.capture(user_id, event="asked_en-ai", properties={"ui-component": "new-tab", "model_id": payload.model_id})
    return answer_engine.get_answer(
        question=payload.question,
        messages=payload.messages,
        is_streaming=payload.is_streaming,
        model_id=payload.model_id,
        context=payload.context,
        allowed_responses_types=payload.allowed_responses_types
    )

@router.get("/{user_id}/welcome-text")
def welcome_text(user_id: UUID, sname: str, answer_engine: Annotated[AnswerEngine, Depends(AnswerEngine)], accept: Annotated[str | None, Header()] = None):
    decoded_space_name = unquote(sname)
    if accept == "text/markdown":
        return {"message": answer_engine.get_welcome_text(decoded_space_name)}
    else:
        welcome_text = answer_engine.get_welcome_text(decoded_space_name)
        return {"message": markdown.markdown(welcome_text)}

@router.post("/{user_id}/welcome-text")
def welcome_text(user_id: UUID, 
                 answer_engine: Annotated[AnswerEngine, Depends(AnswerEngine)],
                 payload: WelcomeTextPayload
                 ):
    return answer_engine.get_info_text(payload.space_name, payload.group_name, payload.context_tabs)

@router.get("/{user_id}/title")
def generate_title(user_id: UUID,  prompt: str, answer_engine: Annotated[AnswerEngine, Depends(AnswerEngine)]):
    title = answer_engine.generate_title(prompt)
    return title
