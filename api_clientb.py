import os
import requests


class APIClient:
    """
    Persistent OpenRouter API client with full conversation memory.
    One instance = one model + one conversation.
    """

    def __init__(self, model_name: str, system_prompt: str | None = None):
        self.model_name = model_name
        self.api_key = "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"

        if not self.api_key:
            raise RuntimeError("OPENROUTER_API_KEY not set")

        self.endpoint = "https://openrouter.ai/api/v1/chat/completions"

        # Persistent state
        self.call_count = 0
        self.history = []

        # THIS IS THE CONVERSATION MEMORY
        self.messages = []

        # Optional system instruction (recommended)
        if system_prompt:
            self.messages.append({
                "role": "system",
                "content": system_prompt
            })

    def call(self, prompt: str) -> str:
        """
        Send a prompt and continue the conversation automatically.
        """

        self.call_count += 1

        # 1. Add user message to conversation
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
            "role": "assistant",
            "content": output_text
        })

        # Optional logging (not sent back to model)
        self.history.append({
            "call_number": self.call_count,
            "prompt": prompt,
            "output": output_text
        })

        return output_text
