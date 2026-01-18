from openai import OpenAI
from .llm_adapter import LLMAdapter, LLMGenerationError

import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class OpenAIAdapter(LLMAdapter):
    def __init__(self, model_id: str):
        self.model_id = model_id
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.messages = []

    def get_provider_name(self) -> str:
        return "openai"

    def get_model_name(self) -> str:
        return self.model_id

    def generate(self, prompt):
        self.messages.append({
            "role": "user",
            "content": prompt
        })
        try:
            response = self.client.chat.completions.create(
                model=self.model_id,
                messages=self.messages
            )
            self.messages.append({
                "role": "assistant",
                "content": response.choices[0].message.content  # ← Extract content string here
            })
            return response.choices[0].message.content
        except Exception as e:
            raise LLMGenerationError(
                self.get_provider_name(),
                self.model_id,
                str(e)
            )
