import re
from prompter import build_system_prompt
from tools.web_search import web_search
from vector_db import VectorDB
from model_factory import ModelFactory
import time

from models.google_adapter import GoogleAdapter

from agent_factory import spawn_agent

class Agent:
    def __init__(self, id, description, goal, db, model, tools=[], subagents=[]):
        """
        Args:
            agent_config (dict): Configuration from agents.yaml
            all_agents_map (dict): Access to other agents for delegation
        """
        self.id = id
        self.max_turns = 100
        
        self.model = model or 'gemini-3-flash-preview'
        self.description = description
        self.goal = goal
        self.tools = tools
        self.subagents = subagents
        self.db = db
        
        # 2. Initialize the API Client (Memory is managed here)
        # You can change the model name here (e.g., "anthropic/claude-3.5-sonnet")
        model_factory = ModelFactory
        print(self.model)
        self.client = model_factory.create_adapter(self.model)

    def run(self):
        """
        The Main Execution Loop.
        It bounces between the LLM and the Tools until a 'FINAL ANSWER' is found.
        """

        prompt = build_system_prompt(self.description, self.goal, self.tools, self.subagents)
        print("\n\n")
        print(prompt)
        print("\n\n")
        g = GoogleAdapter('gemini-3-flash-preview')
        response_text = g.generate(prompt)
        # for attempt in range(5):
        #     try:
        #         response_text = self.client.generate(prompt)
        #         break # Success!
        #     except Exception as e:
        #         if "429" in str(e) or "limit" in str(e).lower():
        #             wait = (2 ** attempt) + 1
        #             print(f"  ⚠️ Rate limit hit. Waiting {wait}s...")
        #             time.sleep(wait)
        #         else:
        #             raise e # Real error, crash
        
        # # If we still have no response, stop
        # if not response_text:
        #     return "Error: API Rate limit exceeded."

        # print(f"  ✅ Initial Plan: {response_text[:100]}...")
        print(response_text)
        # for turn in range(self.max_turns):
        #     # Print agent's thought process
        #     self._log_response(response_text)
        #     time.sleep(2)
        #     # CHECK: Did the agent finish?
        #     if "FINAL ANSWER" in response_text:
        #         return response_text.split("FINAL ANSWER")[-1].strip()

        #     # CHECK: Did the agent call a tool?
        #     if "CALL:" in response_text:
        #         # 1. Execute the tool
        #         tool_output = self._execute_tool(response_text)
                
        #         # 2. Format the observation
        #         observation = f"OBSERVATION: {tool_output}"
        #         print(f"  ⚙️ [System]: {str(tool_output)[:60]}...")

        #         # 3. Send the observation back to the LLM
        #         # The APIClient automatically appends this as a User message
        #         response_text = self.client.generate(observation)
            
        #     else:
        #         # If no tool called and no final answer, the model might be "thinking" 
        #         # or asking a clarification question. We just continue.
        #         if turn == self.max_turns - 1:
        #             return "Error: Agent reached max turns limit."
                
        #         # If it's just talking, we can return the text or wait for user input.
        #         # For this engine, we assume it must act or finish.
        #         pass
        
        # return "Error: Loop limit reached."

    def _execute_tool(self, text: str):
        """Parses the 'CALL:' command and runs the matching Python function."""
        try:
            # CASE A: Python Code (Has markdown block)
            if "CALL: run_python" in text:
                return run_python_code(text)

            # CASE B: Standard Tools (web_search, etc)
            # Regex captures:  tool_name  (  arguments  )
            match = re.search(r"CALL: (\w+)\((.*)\)", text)
            if not match:
                return "Error: Could not parse CALL format. Use: CALL: tool_name(args)"
            
            tool_name = match.group(1)
            args_str = match.group(2).strip('"').strip("'") # Clean quotes

            if tool_name == "web_search":
                return web_search(args_str)
            
            elif tool_name == "retrieve_knowledge":
                # Assuming you have a DB instance, or import it
                return self.db.search(args_str) or "No info found."

            elif tool_name == "delegate":
                # Parse: "agent_id", "task"
                # Simple split by first comma
                if "," not in args_str:
                    return "Error: Delegate requires two args: agent_id, task"
                
                target_id, task = [x.strip().strip('"') for x in args_str.split(",", 1)]
                return self._handle_delegation(target_id, task)

            else:
                return f"Error: Tool '{tool_name}' not defined."

        except Exception as e:
            return f"Tool Execution Error: {e}"

    def _handle_delegation(self, target_id, task):
        """Spins up a new Agent instance for the sub-task"""
        print(f"  👉 [{self.id}] delegating to -> [{target_id}]")
        
        target_config = self.age.get(target_id)
        if not target_config:
            return f"Error: Agent '{target_id}' not found in configuration."
        
        subagents = self.subagents
        subagents[target_id]['goal'] += task
        subagent = spawn_agent(target_id, subagents)

        result = subagent.run()
        
        return f"Result from {target_id}: {result}"

    def _log_response(self, text):
        """Helper to pretty-print the agent's thoughts"""
        if "THOUGHT" in text:
            # Extract just the thought part
            thought = text.split("THOUGHT")[-1].split("CALL")[0].strip()
            print(f"  💭 [Thought]: {thought[:100]}...")
