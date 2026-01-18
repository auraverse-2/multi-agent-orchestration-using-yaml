import sys
import io
import contextlib
import traceback
import re
from logger import log

def run_python_code(full_response_text):
    """
    Executes Python code found in a markdown block within the text.
    Captures stdout (print) and stderr (errors).
    """
    # 1. Regex to extract code between ```python and ```
    # re.DOTALL makes (.) match newlines too
    code_match = re.search(r"```python(.*?)```", full_response_text, re.DOTALL)
    
    if not code_match:
        return "ERROR: No Python code block found. Did you forget the ```python ... ``` formatting?"

    raw_code = code_match.group(1).strip()
    log("RUN PYTHON", "Running Python...", True)
    log("RUN PYTHON", raw_code, True)
    
    # 2. Prepare the Execution Environment
    # We use a shared 'local_scope' if you want variables to persist between calls, 
    # but for safety/simplicity, we usually reset it per call.
    local_scope = {} 
    
    # Capture standard output (print statements)
    stdout_buffer = io.StringIO()
    
    try:
        with contextlib.redirect_stdout(stdout_buffer):
            # 3. Execute the code
            # We use 'exec' which is dangerous in production but standard for local agents
            exec(raw_code, {}, local_scope)
            
        output = stdout_buffer.getvalue()
        log("RUN PYTHON", output, True)
        
        # If code ran but printed nothing, warn the agent
        if not output.strip():
            return "Code executed successfully, but printed nothing. Did you forget to 'print()' the result?"
            
        return output

    except Exception:
        # 4. Error Handling
        # If the code crashes, return the traceback so the Agent can fix its own bug
        log("RUN PYTHON", traceback.format_exc(), True)
        return f"PYTHON ERROR:\n{traceback.format_exc()}"
