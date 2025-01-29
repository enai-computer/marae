from .provider.LLMInterface import LLMInterface
from fastapi.responses import StreamingResponse
from typing import List
from app.rest.models.EveModels import AIChatMessage

class AnswerEngine:

    def __init__(self):
        self.llm_interface = LLMInterface()
    
    def get_answer(self, question: str, messages: List[AIChatMessage], is_streaming: bool, model_id: str | None = None, context: List[str] | None = None):
        if (is_streaming):
            print(f"used model: {model_id}, number of messages: {len(messages)}, number of context items: {len(context)}")
            if model_id == "o1-preview":
                return StreamingResponse(self.llm_interface.send_chat_to_openai_o1_stream(question, messages), media_type="text/event-stream")
            elif model_id == "claude-3-5-sonnet":
                return StreamingResponse(self.llm_interface.send_chat_to_anthropic_stream(question, messages, context=context), media_type="text/event-stream")
            elif model_id == "gemini-1.5-flash":
                return StreamingResponse(self.llm_interface.send_chat_to_gemini_stream(question, messages, context=context), media_type="text/event-stream")
            else:
                return StreamingResponse(self.llm_interface.send_chat_to_openai_gpt4_stream(question, messages, context=context), media_type="text/event-stream")
        else:
            return {"message": self.llm_interface.send_chat_to_cerebras(question, messages)}

    def get_welcome_text(self, space_name: str) -> str:
        return self.llm_interface.get_welcome_text(space_name)
    
    def get_info_text(self, space_name: str, group_name: str | None, context_tabs: List[str]):
        info_text = self.llm_interface.get_info_text(space_name, group_name, context_tabs)
        return {"message": info_text}

    def generate_title(self, question: str) -> str:
        title = self.llm_interface.generate_title(question)
        cleaned_title = title.strip('"')
        words = cleaned_title.split()
        return ' '.join(words[:5])
