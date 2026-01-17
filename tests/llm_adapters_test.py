from dotenv import load_dotenv

load_dotenv()

from models.google_adapter import GoogleAdapter
from models.openai_adapter import OpenAIAdapter
from models.openrouter_adapter import OpenRouterAdapter


g = GoogleAdapter('gemini-3-flash-preview')
print(g.generate("Hi, my name is Arham"))
print(g.generate("What is my name?"))


o = OpenRouterAdapter('gpt-4o-mini')
print(o.generate("Hi, my name is Varun"))
print(o.generate("What is my name?"))
