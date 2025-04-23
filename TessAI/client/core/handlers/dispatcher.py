from .terminal import run_terminal_command
from .file import open_file
from .browser import open_url

def handle_action(action: dict):
    action_type = action.get("type")
    
    if action_type == "terminal_command":
        run_terminal_command(action.get("command"))
    elif action_type == "open_file":
        open_file(action.get("path"))
    elif action_type == "open_url":
        open_url(action.get("url"))
    else:
        print(f"⚠️ Unknown action type: {action_type}")
