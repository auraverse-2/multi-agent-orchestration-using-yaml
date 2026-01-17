from abc import ABC, abstractmethod

class LLMAdapter(ABC):
    @abstractmethod
    def generate(self, messages: list) -> str:
        """Must return a string response from the LLM."""
        pass

    @abstractmethod
    def get_model_name(self) -> str:
        """Returns the specific model ID being used."""
        pass
