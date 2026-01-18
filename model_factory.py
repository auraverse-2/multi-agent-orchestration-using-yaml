from models.openai_adapter import OpenAIAdapter
from models.google_adapter import GoogleAdapter
from models.llm_adapter import LLMAdapter

class ModelFactory:
    @staticmethod
    def create_adapter(model_id: str) -> LLMAdapter:
        if "gemini-" in model_id:
            return GoogleAdapter(model_id)
        elif "gpt-" in model_id:
            return OpenAIAdapter(model_id)
        return OpenRouterAdapter(model_id)
