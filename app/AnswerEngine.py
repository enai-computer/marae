from uuid import UUID
from .LLMInterface import LLMInterface

class AnswerEngine:

    def __init__(self):
        self.llm_interface = LLMInterface()

    def get_answer(self, question: str):
        # build and send request to LLM
        print("requesting answer for question: ", question)
        # chat_response = self.llm_interface.send_chat_to_openai(question)
        chat_response = self.llm_interface.send_chat_to_perplexity(question)
        return {"message": chat_response}
    