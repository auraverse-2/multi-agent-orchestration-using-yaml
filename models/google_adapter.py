from google import genai
from .llm_adapter import LLMAdapter, LLMGenerationError
import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class GoogleAdapter(LLMAdapter):
    def __init__(self, model_id: str):
        self.model_id = model_id
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.messages = []

    def get_provider_name(self) -> str:
        return "google"

    def get_model_name(self) -> str:
        return self.model_id

    def generate(self, prompt):
        self.messages.append({
            "role": "user",
            "content": prompt
        })
        try:
            prompt = "\n".join(m["content"] for m in self.messages)

            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt
            )
            self.messages.append({
                "role": "agent",
                "content": response.text
            })
            return response.text

        except Exception as e:
            raise LLMGenerationError(
                self.get_provider_name(),
                self.model_id,
                str(e)
            )
