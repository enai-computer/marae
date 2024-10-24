from pydantic import BaseModel
from typing import List

class AIChatMessage(BaseModel):
    role: str
    content: str

class AnswerPayload(BaseModel):
    question: str
    is_streaming: bool
    messages: List[AIChatMessage]

class WelcomeTextPayload(BaseModel):
    space_name: str
    group_name: str | None = None
    context_tabs: List[str] | None = None
