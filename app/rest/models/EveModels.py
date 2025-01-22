from pydantic import BaseModel
from typing import List

class AIModel(BaseModel):
    id: str
    name: str
    description: str

class AIChatMessage(BaseModel):
    role: str
    content: str

class AnswerPayload(BaseModel):
    question: str
    is_streaming: bool
    model_id: str | None = None
    context: List[str] | None = None
    messages: List[AIChatMessage]

class WelcomeTextPayload(BaseModel):
    space_name: str
    group_name: str | None = None
    context_tabs: List[str] | None = None
