# client/automation/command_handler.py
import requests

SERVER_URL = "https://ranger-george-notices-ru.trycloudflare.com"  # Replace with actual server

def fetch_command_from_server(natural_input: str):
    try:
        response = requests.post(f"{SERVER_URL}/plan-command", json={"query": natural_input})
        if response.status_code == 200:
            return response.json().get("command", "echo 'No command received'")
        else:
            return f"❌ Server Error: {response.status_code}"
    except Exception as e:
        return f"❌ Connection Error: {e}"