from abc import ABC, abstractmethod
from typing import List, Dict


class LLMGenerationError(Exception):
    def __init__(self, provider: str, model: str, reason: str):
        super().__init__(f"[{provider}:{model}] {reason}")
        self.provider = provider
        self.model = model
        self.reason = reason


class LLMAdapter(ABC):
    def __init__(self, model_name):
        self.messages = []
        self.model_name = model_name
        self.api_key = ""

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate a response from the LLM."""
        pass

    @abstractmethod
    def get_model_name(self) -> str:
        """Return model identifier."""
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        """Return provider name: openai | google | anthropic."""
        pass
