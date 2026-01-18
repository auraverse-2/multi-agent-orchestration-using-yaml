from dotenv import load_dotenv

load_dotenv()

from models.google_adapter import GoogleAdapter
from models.openai_adapter import OpenAIAdapter
from models.openrouter_adapter import OpenRouterAdapter


g = GoogleAdapter('gemini-3-flash-preview')
print(g.generate("What is my name?"))
print(g.generate("""
### ROLE & GOAL ###
    You are: **Internal Knowledge Specialist**
    Goal: **Retrieve information about "Project Apollo" from the internal vector database.**
    
### AVAILABLE TOOLS ###
You have access to the following tools:

    - `retrieve_knowledge(query)`: Use this for internal documents.
      Example: CALL: retrieve_knowledge("previous report")
    
To use a tool, write: `CALL: tool_name(args)`

    ### RESPONSE FORMAT ###
    Step 1: THOUGHT (Explain why you are delegating or using a tool)
    Step 2: CALL (The specific tool or delegate call)
    Step 3: OBSERVATION (Wait for the result)
    Step 4: FINAL ANSWER
"""))


# o = OpenRouterAdapter('gpt-4o-mini')
# print(o.generate("Hi, my name is Varun"))
# print(o.generate("What is my name?"))
