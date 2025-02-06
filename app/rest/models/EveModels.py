from pydantic import BaseModel
from typing import List
import enum

class AIModel(BaseModel):
    id: str
    name: str
    description: str
    token_limit: int

class AIChatMessageType(enum.Enum):
    TEXT = "TEXT"
    SEARCH = "SEARCH"
    DISPLAY = "DISPLAY"

class AIChatMessage(BaseModel):
    role: str
    content: str
    type: AIChatMessageType

class AnswerPayload(BaseModel):
    question: str
    is_streaming: bool
    model_id: str | None = None
    context: List[str] | None = None
    messages: List[AIChatMessage]
    allowed_responses_types: List[AIChatMessageType] | None = None

class WelcomeTextPayload(BaseModel):
    space_name: str
    group_name: str | None = None
    context_tabs: List[str] | None = None
