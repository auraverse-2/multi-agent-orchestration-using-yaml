# tools_registry.py

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

def build_system_prompt(agent_config):
    """
    Dynamically constructs the prompt based on the agent's unique YAML config.
    """
    
    # [cite_start]1. Base Identity (Role & Goal) [cite: 39, 40]
    prompt = f"""
    ### ROLE ###
    You are: **{agent_config['role']}**
    
    ### GOAL ###
    {agent_config['goal']}
    """
    
    # [cite_start]2. Custom Instructions (Optional) [cite: 111, 125]
    # If the YAML has an 'instruction' field, inject it.
    if "instruction" in agent_config:
        prompt += f"\n### BEHAVIORAL INSTRUCTIONS ###\n{agent_config['instruction']}\n"

    # 3. Dynamic Tool Injection
    # We only add instructions for the tools listed in the YAML
    tool_list = agent_config.get('tools', [])
    
    if tool_list:
        prompt += "\n### AVAILABLE TOOLS ###\nYou have access to the following tools:\n"
        for tool_name in tool_list:
            # Look up the definition in our registry
            definition = TOOL_DEFINITIONS.get(tool_name)
            if definition:
                prompt += definition
        
        prompt += "\nTo use a tool, write: `CALL: tool_name(args)`\n"
    else:
        prompt += "\nYou have NO tools. You must answer using your own knowledge.\n"

    return prompt
