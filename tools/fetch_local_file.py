import os

def fetch_local_file(file_path):
    """
    Reads the content of a local text-based file.
    Includes a security check to stay within the current project directory.
    """
    try:
        # Security: Prevent 'Directory Traversal' (e.g., ../../../etc/passwd)
        # This ensures the agent only reads files within the script's folder
        base_dir = os.getcwd()
        full_path = os.path.abspath(os.path.join(base_dir, file_path))
        
        if not full_path.startswith(base_dir):
            return "ERROR: Access denied. You can only access files within the project directory."

        if not os.path.exists(full_path):
            return f"ERROR: File '{file_path}' not found."

        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # If the file is massive, we truncate to avoid hitting token limits
            if len(content) > 10000:
                return content[:10000] + "\n... [Content Truncated] ..."
            return content

    except Exception as e:
        return f"ERROR reading file: {str(e)}"
