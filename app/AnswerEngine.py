from .provider.LLMInterface import LLMInterface
from fastapi.responses import StreamingResponse
from typing import List
from app.rest.models.EveModels import AIChatMessage

class AnswerEngine:

    def __init__(self):
        self.llm_interface = LLMInterface()
    
    def get_answer(self, question: str, messages: List[AIChatMessage], is_streaming: bool):
        if (is_streaming):
            return StreamingResponse(self.llm_interface.send_chat_to_openai_stream(question, messages), media_type="text/event-stream")
        else:
            return {"message": self.llm_interface.send_chat_to_cerebras(question, messages)}

    def get_welcome_text(self, space_name: str) -> str:
        return self.llm_interface.get_welcome_text(space_name)
    
    def get_info_text(self, space_name: str, group_name: str | None, context_tabs: List[str]):
        info_text = self.llm_interface.get_info_text(space_name, group_name, context_tabs)
        return {"message": info_text}
