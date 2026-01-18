from datetime import datetime

GREEN = "\033[92m"
YELLOW = "\033[33m"
ORANGE = "\033[38;5;208m"
RESET = "\033[0m"

def log(name: str, message: str, tool=False):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if tool:
        print( f"{GREEN}[{timestamp}] {ORANGE}[{name}]{RESET} {message}")
    else:
        print( f"{GREEN}[{timestamp}] {YELLOW}[{name}]{RESET} {message}")
