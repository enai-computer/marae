from requests import Response
from openai import OpenAI
import os
from asyncio import sleep
from typing import List
from app.rest.models.EveModels import AIChatMessage, AIModel
from app.SecretsService import secretsStore
from app.provider.openAiPrompts import get_usr_prompt_welcome_text, get_usr_prompt_space_name, get_usr_prompt_space_name_group_name, get_usr_prompt_space_name_context_tabs, get_usr_prompt_space_name_group_name_context_tabs
from app.provider.crossProviderPrompts import get_system_prompt, genUserQuestion
from app.provider.geminiPrompts import gemini_genUserQuestion
from app.provider.llamaPrompts import system_prompt_llama_70b, system_prompt_llama_8b_title
from cerebras.cloud.sdk import Cerebras
from anthropic import Anthropic
import google.generativeai as genai
from google.generativeai import types

class LLMInterface:

    perplexity_url = "https://api.perplexity.ai/chat/completions"

    GOOGLE_GEMINI_1_5_FLASH_TOKEN_LIMIT = 900000
    OPENAI_GPT_4O_TOKEN_LIMIT = 26000
    OPENAI_O1_TOKEN_LIMIT = 0
    CLAUDE_3_5_SONNET_TOKEN_LIMIT = 75000
    available_models: List[AIModel] = [
        AIModel(id="gemini-1.5-flash", name="Google Gemini 1.5 Flash", description="Google's latest model.", token_limit=GOOGLE_GEMINI_1_5_FLASH_TOKEN_LIMIT),
        AIModel(id="gpt-4o", name="OpenAI GPT-4o", description="The latest model from OpenAI.", token_limit=OPENAI_GPT_4O_TOKEN_LIMIT),
        AIModel(id="o1-preview", name="OpenAI o1", description="OpenAI's reasoning model designed to solve hard problems across domains.", token_limit=OPENAI_O1_TOKEN_LIMIT),
        AIModel(id="claude-3-5-sonnet", name="Claude 3.5 Sonnet", description="Anthropic's latest model.", token_limit=CLAUDE_3_5_SONNET_TOKEN_LIMIT),
    ]

    def __init__(self):
        self.openai_client = OpenAI(
            api_key=secretsStore.secrets["OPENAI_API_KEY"],
            organization=secretsStore.secrets["OPENAI_ORG_ID"],
            project=secretsStore.secrets["OPENAI_PROJECT_ID"]
        )
        # self.perplexity_client = requests.Session()
        self.cerebras_client = Cerebras(
            api_key=secretsStore.secrets["CEREBRAS_API_KEY"]
        )
        self.anthropic_client = Anthropic(
            api_key=secretsStore.secrets["ANTHROPIC_API_KEY"]
        )
        genai.configure(api_key=secretsStore.secrets["GEMINI_API_KEY"])
        self.gemini_client = genai.GenerativeModel(
            model_name="gemini-1.5-flash-002",
            system_instruction=get_system_prompt()
        )

    def send_chat_to_cerebras(self, question: str, messages: List[AIChatMessage]) -> str:
        completion = self.cerebras_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt_llama_70b()},
                {"role": "user", "content": question}
            ],
            model="llama3.1-70b",
            stream=False
        )
        return completion.choices[0].message.content

    def generate_title(self, question: str) -> str:
        completion = self.cerebras_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt_llama_8b_title()},
                {"role": "user", "content": f"Please give me a title for: \"{question}\" with a maximum of 3 words."}
            ],
            model="llama3.1-8b",
            stream=False
        )
        return completion.choices[0].message.content

    def send_chat_to_openai(self, question: str, messages: List[AIChatMessage]) -> str:
        response = self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful library assistant."},
            ] + messages + [{"role": "user", "content": question}],
            stream=False
        )
        return response.choices[0].message.content
    
    async def send_chat_to_openai_gpt4_stream(
        self,
        question: str,
        messages: List[AIChatMessage],
        context: List[str] | None = None
    ):
        used_tokens = self.count_tokens(messages)
        response = self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": get_system_prompt()},
            ] + messages + [{"role": "user", "content": genUserQuestion(question, self.OPENAI_GPT_4O_TOKEN_LIMIT, used_tokens, context)}],
            stream=True
        )

        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
                await sleep(0.1)
    
    def count_tokens(self, messages: List[AIChatMessage]) -> int:
        """Estimate the number of tokens in a list of messages.
        This is a rough approximation - on average, 1 token ~= 4 characters in English."""
        total_chars = sum(len(msg.content) + len(msg.role) for msg in messages)
        estimated_tokens = total_chars // 4  # rough approximation
        return estimated_tokens

    async def send_chat_to_openai_o1_stream(
        self,
        question: str,
        messages: List[AIChatMessage]
    ):
        response = self.openai_client.chat.completions.create(
            model="o1-preview",
            messages=[{"role": msg.role, "content": msg.content} for msg in messages] + [{"role": "user", "content": question}],
            stream=True
        )

        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
                await sleep(0.1)

    async def send_chat_to_anthropic_stream(
        self,
        question: str,
        messages: List[AIChatMessage],
        context: List[str] | None = None
    ):
        used_tokens = self.count_tokens(messages)
        with self.anthropic_client.messages.stream(
            max_tokens=2048,
            system=get_system_prompt(),
            messages=[
                {"role": msg.role, "content": msg.content} for msg in messages
            ] + [
                {"role": "user", "content": genUserQuestion(question, self.CLAUDE_3_5_SONNET_TOKEN_LIMIT, used_tokens, context)}
            ],
            model="claude-3-5-sonnet-20241022"
        ) as response:
            for chunk in response.text_stream:
                yield chunk
                await sleep(0.1)

    async def send_chat_to_gemini_stream(
        self,
        question: str,
        messages: List[AIChatMessage],
        context: List[str] | None = None
    ):
        used_tokens = self.count_tokens(messages)
        # Format message history for Gemini
        formatted_messages = []
        for msg in messages:
            formatted_messages.append({
                "role": "model" if msg.role == "assistant" else "user",
                "parts": [{"text": msg.content}]
            })
        
        chat = self.gemini_client.start_chat(
            history=formatted_messages
        )
        response = chat.send_message(gemini_genUserQuestion(question=question, token_limit=self.GOOGLE_GEMINI_1_5_FLASH_TOKEN_LIMIT, used_tokens=used_tokens, context=context), stream=True)
        for chunk in response:
            if chunk.text:
                yield chunk.text
                await sleep(0.1)

    def get_welcome_text(self, space_name: str) -> str:
        prompt = get_usr_prompt_welcome_text(space_name=space_name)
        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for a browser."},
                {"role": "user", "content": prompt}
            ],
            stream=False,
            temperature=1.11,
            max_tokens=512
        )
        return response.choices[0].message.content
    
    def get_info_text(self, space_name: str, group_name: str | None = None, context_tabs: List[str] | None = None) -> str:
        if group_name is None and not context_tabs:
            print("used prompt 1")
            prompt = get_usr_prompt_space_name(space_name=space_name)
        elif group_name and not context_tabs:
            print("used prompt 2")
            prompt = get_usr_prompt_space_name_group_name(space_name=space_name, group_name=group_name)
        elif context_tabs and group_name is None:
            print("used prompt 3")
            prompt = get_usr_prompt_space_name_context_tabs(space_name=space_name, context_tabs=context_tabs)
        elif group_name and context_tabs:
            print("used prompt 4")
            prompt = get_usr_prompt_space_name_group_name_context_tabs(space_name=space_name, group_name=group_name, context_tabs=context_tabs)

        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for a browser."},
                {"role": "user", "content": prompt}
            ],
            stream=False,
            temperature=1.4,
            max_tokens=512
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
