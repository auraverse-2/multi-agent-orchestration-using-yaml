# 1. Define the specific instructions for every possible tool
TOOL_DEFINITIONS = {
    "web_search": """
    - `web_search(query)`: Use this for external facts. 
      Example: CALL: web_search("Tesla stock price")
    """,
    
    "python_interpreter": """
    - `run_python`: execute Python code.
      **INSTRUCTIONS:**
      1. Write the Python code inside a markdown block (```python ... ```).
      2. IMMEDIATELY after the block, write the tool trigger: `CALL: run_python`
      
      **Example:**
      ```python
      def calculate_growth(start, end):
          return (end - start) / start * 100
      print(calculate_growth(100, 150))
      ```
      CALL: run_python
    """,
    
    "vector_db_search": """
    - `retrieve_knowledge(query)`: Use this for internal documents.
      Example: CALL: retrieve_knowledge("previous report")
    """
}

def build_system_prompt(agent_config, all_agents_map):
    """
    Dynamically builds the prompt, including Sub-Agents if they exist.
    """
    
    # 1. Base Identity
    prompt = f"""
    ### ROLE & GOAL ###
    You are: **{agent_config['role']}**
    Goal: **{agent_config['goal']}**
    """

    # 2. SUB-AGENTS (The New Part)
    # Check if this agent has a 'sub_agents' list in the YAML
    sub_agent_ids = agent_config.get('sub_agents', [])
    
    if sub_agent_ids:
        prompt += "\n### AVAILABLE SUB-AGENTS ###\n"
        prompt += "You can delegate tasks to these specialized agents:\n"
        
        for sub_id in sub_agent_ids:
            # We look up the sub-agent's role to tell the Boss what they do
            # (Assuming you have a map of all agents loaded)
            sub_role = all_agents_map[sub_id]['role']
            prompt += f"- `{sub_id}`: {sub_role}\n"
            
        prompt += """
        **How to Delegate:**
        Write: `CALL: delegate("agent_name", "task description")`
        Example: `CALL: delegate("researcher", "Find the history of AI")`
        """

    # 3. STANDARD TOOLS (Web, Python, VectorDB)
    tool_list = agent_config.get('tools', [])
    
    if tool_list:
        prompt += "\n### AVAILABLE TOOLS ###\nYou have access to the following tools:\n"
        for tool_name in tool_list:
            # Look up the definition in our registry
            definition = TOOL_DEFINITIONS.get(tool_name)
            if definition:
                prompt += definition
        
        prompt += "\nTo use a tool, write: `CALL: tool_name(args)`\n"

    
    prompt += """
    ### RESPONSE FORMAT ###
    Step 1: THOUGHT (Explain why you are delegating or using a tool)
    Step 2: CALL (The specific tool or delegate call)
    Step 3: OBSERVATION (Wait for the result)
    Step 4: FINAL ANSWER
    """
    
    return prompt
