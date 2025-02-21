from pydantic import BaseModel
from typing import List, Dict, Any
import enum


class AIChatMessageType(enum.Enum):
    PROMPT = "PROMPT"
    TEXT = "TEXT"
    APPLET = "APPLET"

class AIChatMessageV2Content(BaseModel):
    pass

class AIChatMessageV2AppletContent(AIChatMessageV2Content):
    applet_url: str
    content: Dict[str, Any]

class AIChatMessageV2TextContent(AIChatMessageV2Content):
    text: str

class AIChatMessageV2(BaseModel):
    role: str
    type: AIChatMessageType
    content: AIChatMessageV2Content

    def encode(self, charset: str = 'utf-8') -> bytes:
        return self.model_dump_json().encode(charset)
    
class QuestionContext(BaseModel):
    type: str
    content: str

class ChatPayload(BaseModel):
    question: str
    model_id: str | None = None
    context: List[QuestionContext] | None = None
    messages: List[Dict[Any, Any]]
