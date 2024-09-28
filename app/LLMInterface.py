import requests
from requests import Response
import os

class LLMInterface:

    mistral_model = "mistral-large-latest"

    def __init__(self):
        self.mistral_client = requests.Session()

    def send_chat(self, question: str, context: str) -> Response:
        response = self.mistral_client.post(
            "https://api.mistral.ai/v1/chat/completions",
            headers={"Authorization": f"Bearer {os.getenv('MISTRAL_API_KEY')}"},
            json=self.build_chat_request_mistral(question, context)
        )
        return response

    def build_chat_request_mistral(self, question: str, context: str) -> dict:
        return {
            "model": self.mistral_model,
            "temperature": 0.7,
            "top_p": 1,
            "max_tokens": 0,
            "min_tokens": 0,
            "stream": False,
            "stop": "string",
            "random_seed": 0,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant and have access to the following context: " + context
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            "response_format": {
                "type": "text"
            },
            "tools": [
                {
                    "type": "function",
                    "function": {
                        "name": "string",
                        "description": "",
                        "parameters": {}
                    }
                }
            ],
            "tool_choice": "auto",
            "safe_prompt": False
        }

    def build_chat_request_gpt4o(self, question: str, context: str) -> dict:
        pass

    def build_chat_request_perplexity(self, question: str, context: str) -> dict:
        pass