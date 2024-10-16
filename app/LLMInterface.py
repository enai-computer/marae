import requests
from requests import Response
from openai import OpenAI
import os


class LLMInterface:

    perplexity_url = "https://api.perplexity.ai/chat/completions"


    def __init__(self):
        self.openai_client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            organization=os.getenv("OPENAI_ORG_ID"),
            project=os.getenv("OPENAI_PROJECT_ID")
        )
        self.perplexity_client = requests.Session()

    def send_chat_to_openai(self, question: str) -> str:
        response = self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful library assistant."},
                {"role": "user", "content": question}
            ],
            stream=False
        )
        return response.choices[0].message.content
    
    def get_welcome_text(self, space_name: str) -> str:
        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful library assistant."},
                {"role": "user", "content": f"""
                 Enai is an interpersonal computer
                optimized for AI and the net.
                (It is a browser OS, emphasis on OS)

                By organizing your whole computer
                around your intent, Enai helps you be
                calmer, smarter, and more effective.

                How to use Enai:
                First you set your intent, which creates a space for you to practice that intent.

                In the space, you can

                - Surf the web
                - Right click to pin websites to the menu bar to access them like apps
                - Create and name groups so that you can be organized
                - Write notes or paste text on the canvas
                - Chat with Enai (as an AI tool) about one or more specific tabs

                Once you are finished working on a particular topic, you can create or reopen another space and Enai saves all your work. So you can work on your first intent, put it away, and come back later. If you’re using your computer to do something complicated for more than a few days, Enai can help you keep all that information organized and easily accessible.
                Generate a welcome text for a new space called {space_name} with a maximum of 100 words."""}
            ],
            stream=False
        )
        return response.choices[0].message.content

    def send_chat_to_perplexity(self, question: str) -> str:
        payload = self.gen_perplexity_payload(question)
        headers = {
            "Authorization": f"Bearer {os.getenv('PERPLEXITY_API_KEY')}",
            "Content-Type": "application/json"
        }
        response = self.perplexity_client.post(self.perplexity_url, json=payload, headers=headers)
        return self.handle_perplexity_response(response)
    
    def handle_perplexity_response(self, response: Response) -> str:
        if response.status_code != 200:
            raise Exception(f"Perplexity API returned status code {response.status_code}: {response.text}")
        return response.json()["choices"][0]["message"]["content"]

    def gen_perplexity_payload(self, question: str) -> dict:
        return {
            "model": "llama-3.1-sonar-small-128k-online",
            "messages": [
                {
                    "role": "system",
                    "content": "Be precise and concise."
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            "temperature": 0.2,
            "top_p": 0.9,
            "return_citations": False,
            "search_domain_filter": [],
            "return_images": False,
            "return_related_questions": False,
            "top_k": 0,
            "stream": False,
            "presence_penalty": 0,
            "frequency_penalty": 1
        }
