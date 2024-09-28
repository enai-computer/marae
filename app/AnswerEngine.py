from uuid import UUID
from .LLMInterface import LLMInterface
from .SpacesSearchEngine import SpacesSearchEngine

class AnswerEngine:

    def __init__(self):
        self.spaces_search_engine = SpacesSearchEngine()
        self.llm_interface = LLMInterface()

    def get_answer(self, question: str, space_id: UUID):
        # get context
        context = self.spaces_search_engine.search(question)
        # build and send request to LLM
        print("requesting answer for question: ", question, " with context: ", context)
        chat_response = self.llm_interface.send_chat(question, context)
        print(chat_response.json())
        return {"status": "ok"}
    