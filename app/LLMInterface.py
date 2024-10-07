import os

import requests
from mistralai import Mistral
from requests import Response


class LLMInterface:

    mistral_model = "mistral-large-latest"

    def __init__(self):
        self.mistral_client = requests.Session()

    def send_chat(self, question: str, context: str) -> Response:
        response = self.build_chat_request_mistral(question, context)
        return response

    def build_chat_request_mistral(self, question: str, context: str) -> dict:

        client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

        mistral_response = client.chat.complete(
            model=self.mistral_model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant",
                },
                {"role": "user", "content": question},
            ],
        )
        mistral_response_content = mistral_response.choices[0].message.content

        return mistral_response_content

    def build_chat_request_gpt4o(self, question: str, context: str) -> dict:
        pass

    def build_chat_request_perplexity(self, question: str, context: str) -> dict:
        pass
