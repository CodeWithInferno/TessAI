import re
import subprocess
import platform

def extract_run_command(response_text: str) -> str | None:
    try:
        # 1. Check for explicit JSON {"run": "..."}
        match_json = re.search(r'"run"\s*:\s*"([^"]+)"', response_text)
        if match_json:
            return match_json.group(1)

        # 2. Check for ```bash ... ``` block
        match_bash = re.search(r"```bash\n(.+?)\n```", response_text, re.DOTALL)
        if match_bash:
            return match_bash.group(1).strip()

        # 3. Fallback: extract from a single-line "open ..." or "run ..." in raw response
        match_cmd = re.search(r'(?m)^(open|run|start|cd|ls|echo|python|java)[^\n]*$', response_text.strip())
        if match_cmd:
            return match_cmd.group(0).strip()

        return None
    except Exception as e:
        print(f"❌ Command extraction failed:", e)
        return None

def run_in_terminal(cmd: str):
    system = platform.system()
    if system == "Darwin":  # macOS
        script = f'''
        tell application "Terminal"
            activate
            do script "{cmd}"
        end tell
        '''
        subprocess.run(["osascript", "-e", script])
    elif system == "Windows":
        subprocess.run(f'start cmd /k "{cmd}"', shell=True)
    elif system == "Linux":
        subprocess.run(['x-terminal-emulator', '-e', cmd])
    else:
        print("⚠️ Unsupported OS for terminal execution.")
