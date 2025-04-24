
# client/execute.py
from automation.command_handler import fetch_command_from_server
from automation.terminal import run_terminal_command

if __name__ == "__main__":
    print("💬 Enter your instruction:")
    while True:
        query = input("You: ").strip()
        if query.lower() == "exit":
            break
        command = fetch_command_from_server(query)
        print("🔁 Generated Command:", command)
        if not command.startswith("❌"):
            print(run_terminal_command(command))