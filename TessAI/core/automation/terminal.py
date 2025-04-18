import subprocess
import re
import os

SESSION_FILE = "/tmp/tess_terminal_session.txt"

def sanitize_command(command: str) -> str:
    command = command.strip()
    command = re.sub(r"^(\d+\.\s+)", "", command)  # remove '1. '
    command = command.replace("```bash", "").replace("```", "")
    command = command.lstrip("-*•").strip()
    return command


def run_in_new_terminal(command: str, terminal: str = "Terminal") -> str:
    clean_command = sanitize_command(command)

    if terminal.lower() == "iterm":
        escaped_command = clean_command.replace('"', '\\"')
        script = f'''
        tell application "iTerm"
            create window with default profile
            tell current session of current window
                write text "{escaped_command}"
            end tell
        end tell
        '''
    else:
        script = f'''
        tell application "Terminal"
            activate
            do script "{clean_command}"
        end tell
        '''

    try:
        subprocess.run(["osascript", "-e", script], check=True)
        return f"📟 ✅ Command launched in {terminal}: {clean_command}"
    except subprocess.CalledProcessError as e:
        return f"❌ Failed to run command: {e}"


def get_or_create_terminal_session() -> str:
    script = '''
    tell application "Terminal"
        activate
        do script ""
        delay 0.3
        set sid to id of front window
        return sid
    end tell
    '''
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    sid = result.stdout.strip().replace('"', '')

    with open(SESSION_FILE, "w") as f:
        f.write(sid)

    return sid


def run_in_shared_terminal(command: str) -> str:
    clean_command = sanitize_command(command)

    def is_terminal_window_alive(sid: str) -> bool:
        try:
            check_script = f'''
            tell application "Terminal"
                if (exists window id {sid}) then
                    return "yes"
                else
                    return "no"
                end if
            end tell
            '''
            result = subprocess.run(["osascript", "-e", check_script], capture_output=True, text=True)
            return result.stdout.strip() == "yes"
        except:
            return False

    if os.path.exists(SESSION_FILE):
        session_id = open(SESSION_FILE).read().strip()
        if not is_terminal_window_alive(session_id):
            os.remove(SESSION_FILE)
            session_id = get_or_create_terminal_session()
    else:
        session_id = get_or_create_terminal_session()

    escaped_command = clean_command.replace('"', '\\"')

    script = f'''
    tell application "Terminal"
        do script "{escaped_command}" in window id {session_id}
    end tell
    '''

    try:
        subprocess.run(["osascript", "-e", script], check=True)
        return f"📟 ✅ Ran in shared terminal window {session_id}: {clean_command}"
    except subprocess.CalledProcessError as e:
        return f"❌ Failed to run in shared terminal: {e}"


def run_headless(command: str) -> str:
    clean_command = sanitize_command(command)
    try:
        subprocess.run(clean_command, shell=True, check=True)
        return f"📟 ✅ (headless) Ran: {clean_command}"
    except subprocess.CalledProcessError as e:
        return f"❌ Headless run failed: {e}"
