from .LLMInterface import LLMInterface, MessageList
import markdown
from fastapi.responses import StreamingResponse

class AnswerEngine:

    def __init__(self):
        self.llm_interface = LLMInterface()

    def get_answer(self, question: str):
        # build and send request to LLM
        print("requesting answer for question: ", question)
        chat_response = self.llm_interface.send_chat_to_openai(question)
        # chat_response = self.llm_interface.send_chat_to_perplexity(question)
        return {"message": chat_response}
    
    def get_answer_stream(self, question: str, messages: MessageList):
        print("requesting answer for question: ", question)
        return StreamingResponse(self.llm_interface.stream_openai_chat(question, messages), media_type="text/event-stream")

    def get_welcome_text(self, space_name: str):
        welcome_text = self.llm_interface.get_welcome_text(space_name)
        return {"message": markdown.markdown(welcome_text)}
