import requests
from requests import Response
import os

class LLMInterface:

    mistral_model = "mistral-large-latest"

    def __init__(self):
        self.mistral_client = requests.Session()

    def send_chat(self, question: str, context: str) -> Response:
        pass

    def build_chat_request_gpt4o(self, question: str, context: str) -> dict:
        pass

    def build_chat_request_perplexity(self, question: str, context: str) -> dict:
        pass
