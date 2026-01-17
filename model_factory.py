from models.llm_adapter import LLMAdapter
from models.google_adapter import GoogleAdapter
from models.openrouter_adapter import OpenRouterAdapter

class ModelFactory:
    @staticmethod
    def create_adapter(model_id: str) -> LLMAdapter:
        if "gemini-" in model_id:
            return GoogleAdapter(model_id)
        # elif "claude-" in model_id:
        #     return AnthropicAdapter(model_id)
        return OpenRouterAdapter(model_id)
