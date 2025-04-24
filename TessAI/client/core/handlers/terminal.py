import platform
import subprocess

def run_terminal_command(cmd: str):
    if platform.system() == "Darwin":
        script = f'''tell application "Terminal"
            activate
            do script "{cmd}"
        end tell'''
        subprocess.run(["osascript", "-e", script])
    elif platform.system() == "Windows":
        subprocess.run(["start", "cmd", "/k", cmd], shell=True)
    else:
        subprocess.run(cmd, shell=True)
