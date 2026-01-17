from datetime import datetime

GREEN = "\033[92m"
RESET = "\033[0m"

def log(name: str, message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print( f"{GREEN}[{timestamp}] [{name}]{RESET} {message}")
