# client/automation/terminal.py
import subprocess
import platform

def run_terminal_command(command: str):
    try:
        if platform.system() == "Windows":
            subprocess.Popen(["cmd.exe", "/k", command])
        else:
            subprocess.Popen(["open", "-a", "Terminal", command])
        return f"✅ Running: {command}"
    except Exception as e:
        return f"❌ Failed to run: {str(e)}"
