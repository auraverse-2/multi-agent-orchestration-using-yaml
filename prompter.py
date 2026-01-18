TOOL_DEFINITIONS = {
    "web_search": """
    - `web_search(query)`: Search external internet.
      Example: CALL: web_search("Tesla stock price")
    """,
    "python": """
    - `run_python`: Execute Python code.
      Example:
      ```python
      print(1+1)
      ```
      CALL: run_python
    """,
    "vector_db_search": """
    - `retrieve_knowledge(query)`: Search internal docs for specific facts or concepts.
      Example: CALL: retrieve_knowledge("Q3 2024 revenue growth analysis")
    """,
    "fetch_local_file": """
    - `fetch_local_file(file_path)`: Reads the text content of a local file.
      Use this to see project files, logs, or data exports.
      Example: CALL: fetch_local_file("data/results.csv")
    """
}

def build_system_prompt(description, goal, tools=[], subagents=[]):
    
    prompt = f"""
    ### ROLE ###
    You are: **{description}**
    
    ### GOAL ###
    **{goal}**
    
    ### STRICT CONSTRAINTS (CRITICAL) ###
    1. **ONLY** use the tools/delegates explicitly listed below.
    2. **DO NOT** use any other tools (e.g. no 'multi_tool_use', no 'browser', no 'python_repl' unless listed).
    3. If you do not have a tool for a task, you must fail gracefully or ask for clarification.
    4. **DO NOT** generate the 'OBSERVATION' step yourself. You must PAUSE after a CALL.
    """

    # --- SUB-AGENTS ---
    if subagents:
        prompt += "\n### ALLOWED DELEGATES ###\n"
        for subagent in subagents:
            prompt += f"- `{subagent['id']}`: {subagent['description']}\n"
        prompt += "To delegate: `CALL: delegate(\"agent_id\", \"task\")`\n"

    # --- TOOLS ---
    if tools:
        prompt += "\n### ALLOWED TOOLS ###\n"
        for tool_name in tools:
            definition = TOOL_DEFINITIONS.get(tool_name)
            if definition:
                prompt += definition
        prompt += "\nFormat: `CALL: tool_name(args)`\n"
    else:
        prompt += "\n### NO TOOLS AVAILABLE ###\nYou must answer using only your internal knowledge.\n"

    # --- MINIMALIST RESPONSE FORMAT ---
    prompt += """
    ### RESPONSE FORMAT (CHOOSE ONE) ###

    **Option 1: Action Required**
    THOUGHT: (One sentence explaining why)
    CALL: [Tool/Delegate Name]
    (STOP GENERATING HERE)

    **Option 2: Final Answer**
    FINAL ANSWER: [Your Answer]
    """
    
    return prompt
