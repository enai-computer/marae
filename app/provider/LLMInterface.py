from requests import Response
from openai import OpenAI
import os
from asyncio import sleep
from typing import List
from app.rest.models.EveModels import AIChatMessage
from app.SecretsService import secretsStore
from app.provider.openAiPrompts import get_usr_prompt_space_name, get_usr_prompt_space_name_group_name, get_usr_prompt_space_name_context_tabs, get_usr_prompt_space_name_group_name_context_tabs
class LLMInterface:

    perplexity_url = "https://api.perplexity.ai/chat/completions"

    def __init__(self):
        self.openai_client = OpenAI(
            api_key=secretsStore.secrets["OPENAI_API_KEY"],
            organization=secretsStore.secrets["OPENAI_ORG_ID"],
            project=secretsStore.secrets["OPENAI_PROJECT_ID"]
        )
        # self.perplexity_client = requests.Session()

    def send_chat_to_openai(self, question: str, messages: List[AIChatMessage]) -> str:
        response = self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful library assistant."},
            ] + messages + [{"role": "user", "content": question}],
            stream=False
        )
        return response.choices[0].message.content
    
    async def send_chat_to_openai_stream(
        self,
        question: str,
        messages: List[AIChatMessage],
    ):
        response = self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful library assistant."},
            ] + messages + [{"role": "user", "content": question}],
            stream=True
        )

        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
                await sleep(0.1)

    def get_welcome_text(self, space_name: str, group_name: str | None = None, context_tabs: List[str] | None = None) -> str:
        if group_name is None and context_tabs:
            prompt = get_usr_prompt_space_name(space_name=space_name)
        elif group_name is not None and not context_tabs:
            prompt = get_usr_prompt_space_name_group_name(space_name=space_name, group_name=group_name)
        elif context_tabs is not None and group_name is None:
            prompt = get_usr_prompt_space_name_context_tabs(space_name=space_name, context_tabs=context_tabs)
        elif group_name is not None and context_tabs is not None:
            prompt = get_usr_prompt_space_name_group_name_context_tabs(space_name=space_name, group_name=group_name, context_tabs=context_tabs)

        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful library assistant."},
                {"role": "user", "content": prompt}
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
        # response = self.perplexity_client.post(self.perplexity_url, json=payload, headers=headers)
        # return self.handle_perplexity_response(response)
        return "Not implemented"
    
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
