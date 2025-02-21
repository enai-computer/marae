from .provider.LLMInterface import LLMInterface
from .provider.openAiInterface import OpenAiInterface
from fastapi.responses import StreamingResponse
from typing import List
from app.rest.models.EveModels import AIChatMessage
from app.rest.models.EveModelsV2 import ChatPayload


async def init_answer_engine():
    print("starting to initialize answer engine")
    return AnswerEngine()

class AnswerEngine:

    def __init__(self):
        print("init answer engine")
        self.llm_interface = LLMInterface()
        self.openai_interface = OpenAiInterface()
    
    def get_answer(self, question: str, messages: List[AIChatMessage], is_streaming: bool, model_id: str | None = None, context: List[str] | None = None):
        if (is_streaming):
            print(f"used model: {model_id}, number of messages: {len(messages)}, number of context items: {len(context)}")
            match model_id:
                case "o1-preview":
                    return StreamingResponse(self.openai_interface.send_chat_to_openai_o1_stream(question, messages), media_type="text/event-stream")
                case "claude-3-5-sonnet":
                    return StreamingResponse(self.llm_interface.send_chat_to_anthropic_stream(question, messages, context=context), media_type="text/event-stream")
                case "gemini-1.5-flash":
                    return StreamingResponse(self.llm_interface.send_chat_to_gemini_stream(question, messages, context=context), media_type="text/event-stream")
                case _:
                    return StreamingResponse(self.openai_interface.send_chat_to_openai_gpt4_stream(question, messages, context=context), media_type="text/event-stream")
        else:
            return {"message": self.llm_interface.send_chat_to_cerebras(question, messages)}

    def get_welcome_text(self, space_name: str) -> str:
        return self.openai_interface.get_welcome_text(space_name)
    
    def get_info_text(self, space_name: str, group_name: str | None, context_tabs: List[str]):
        info_text = self.openai_interface.get_info_text(space_name, group_name, context_tabs)
        return {"message": info_text}

    def generate_title(self, question: str) -> str:
        title = self.llm_interface.generate_title(question)
        cleaned_title = title.strip('"')
        words = cleaned_title.split()
        return ' '.join(words[:5])

# MARK: - V2
    def get_answer_v2(self, payload: ChatPayload):
        match payload.model_id:
            case _:
                return StreamingResponse(self.openai_interface.send_chat_with_tool_calls(payload), media_type="text/event-stream")
        
