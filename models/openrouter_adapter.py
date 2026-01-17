
import requests

from .llm_adapter import LLMAdapter

import os

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

class OpenRouterAdapter(LLMAdapter):
    """
    Persistent OpenRouter API client with full conversation memory.
    One instance = one model + one conversation.
    """

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.api_key = OPENROUTER_API_KEY

        if not self.api_key:
            raise RuntimeError("OPENROUTER_API_KEY not set")

        self.endpoint = "https://openrouter.ai/api/v1/chat/completions"

        self.messages = []

    def generate(self, prompt: str) -> str:
        """
        Send a prompt and continue the conversation automatically.
        """
        self.messages.append({
            "role": "user",
            "content": prompt
        })

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model_name,
            "messages": self.messages
        }

        # 2. Send full conversation to model
        response = requests.post(
            self.endpoint,
            headers=headers,
            json=payload,
            timeout=30
        )

        response.raise_for_status()
        data = response.json()

        output_text = data["choices"][0]["message"]["content"]

        # 3. Add assistant reply to conversation
        self.messages.append({
            "role": "agent",
            "content": output_text
        })

        return output_text

    def get_provider_name(self) -> str:
        return "openrouter"
    
    def get_model_name(self) -> str:
        return self.model_name
