from requests import Response
from openai import OpenAI
import os
from asyncio import sleep
from typing import List
from app.rest.models.EveModels import AIChatMessage
from app.rest.models.EveModelsV2 import ChatPayload
from app.provider.crossProviderPrompts import get_system_prompt, genUserQuestion
from app.provider.openAiPrompts import get_usr_prompt_welcome_text, get_usr_prompt_space_name, get_usr_prompt_space_name_group_name, get_usr_prompt_space_name_context_tabs, get_usr_prompt_space_name_group_name_context_tabs, get_system_prompt_with_tool_choice
from app.SecretsService import secretsStore
from app.provider.unternet.appletManager import gAppletManager
from app.provider.utils import count_tokens

class OpenAiInterface:

    def __init__(self):
        print("init openai interface")
        self.openai_client = OpenAI(
            api_key=secretsStore.secrets["OPENAI_API_KEY"],
            organization=secretsStore.secrets["OPENAI_ORG_ID"],
            project=secretsStore.secrets["OPENAI_PROJECT_ID"]
        )

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
        used_tokens = count_tokens(messages)
        response = self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": get_system_prompt()},
            ] + messages + [{"role": "user", "content": genUserQuestion(question, self.OPENAI_GPT_4O_TOKEN_LIMIT, used_tokens, context)}],
            stream=True
        )
        # TODO: add error handling
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
                await sleep(0.1)

    async def send_chat_with_tool_calls(
        self,
        payload: ChatPayload
    ):
        used_tokens = count_tokens(payload.messages)
        # TODO: consider calling mini first and make a decision on the tool before calling gpt-4o
        response = self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=payload.messages + [
                
                {"role": "system", "content": get_system_prompt_with_tool_choice()},
            ] + [{"role": "user", "content": payload.question}],
            tools=gAppletManager.openAI_tools
        )
    
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
