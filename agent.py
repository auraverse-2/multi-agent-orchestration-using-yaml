import re
import json
from api_client import APIClient
from prompter import build_system_prompt
from tools import run_python_code, web_search_mock 

class Agent:
    def __init__(self, agent_config, all_agents_map):
        """
        Args:
            agent_config (dict): Configuration from agents.yaml
            all_agents_map (dict): Access to other agents for delegation
        """
        self.config = agent_config
        self.all_agents_map = all_agents_map
        self.id = agent_config['id']
        self.max_turns = 8
        
        # 1. Build the System Prompt using your prompter.py logic
        self.system_prompt = build_system_prompt(agent_config, all_agents_map)
        
        # 2. Initialize the API Client (Memory is managed here)
        # You can change the model name here (e.g., "anthropic/claude-3.5-sonnet")
        self.client = APIClient(model_name="openai/gpt-4o", system_prompt=self.system_prompt)

    def run(self, user_task: str):
        """
        The Main Execution Loop.
        It bounces between the LLM and the Tools until a 'FINAL ANSWER' is found.
        """
        print(f"\n🤖 [{self.id}] Starting Task: {user_task[:50]}...")
        
        # Step 1: Send the first user message
        response_text = self.client.call(user_task)

        for turn in range(self.max_turns):
            # Print agent's thought process
            self._log_response(response_text)

            # CHECK: Did the agent finish?
            if "FINAL ANSWER" in response_text:
                return response_text.split("FINAL ANSWER")[-1].strip()

            # CHECK: Did the agent call a tool?
            if "CALL:" in response_text:
                # 1. Execute the tool
                tool_output = self._execute_tool(response_text)
                
                # 2. Format the observation
                observation = f"OBSERVATION: {tool_output}"
                print(f"  ⚙️ [System]: {str(tool_output)[:60]}...")

                # 3. Send the observation back to the LLM
                # The APIClient automatically appends this as a User message
                response_text = self.client.call(observation)
            
            else:
                # If no tool called and no final answer, the model might be "thinking" 
                # or asking a clarification question. We just continue.
                if turn == self.max_turns - 1:
                    return "Error: Agent reached max turns limit."
                
                # If it's just talking, we can return the text or wait for user input.
                # For this engine, we assume it must act or finish.
                pass
        
        return "Error: Loop limit reached."

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
                return web_search_mock(args_str)
            
            elif tool_name == "retrieve_knowledge":
                # Assuming you have a DB instance, or import it
                from vector_store import VectorDB
                db = VectorDB()
                return db.search(args_str) or "No info found."

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
        
        target_config = self.all_agents_map.get(target_id)
        if not target_config:
            return f"Error: Agent '{target_id}' not found in configuration."
            
        # Create a new sub-agent
        sub_agent = Agent(target_config, self.all_agents_map)
        
        # Run it (Blocking call)
        result = sub_agent.run(task)
        
        return f"Result from {target_id}: {result}"

    def _log_response(self, text):
        """Helper to pretty-print the agent's thoughts"""
        if "THOUGHT" in text:
            # Extract just the thought part
            thought = text.split("THOUGHT")[-1].split("CALL")[0].strip()
            print(f"  💭 [Thought]: {thought[:100]}...")
