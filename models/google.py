class OpenAIPlugin(BaseModelPlugin):
    def __init__(self, model_id: str):
        # We store the specific model name inside the instance
        self.model_id = model_id
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def generate(self, messages):
        # When generating, we use the specific ID assigned to THIS instance
        response = self.client.chat.completions.create(
            model=self.model_id,
            messages=messages
        )
        return response.choices[0].message.content
