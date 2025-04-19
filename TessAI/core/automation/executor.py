# import subprocess

# def run_and_capture(command: str):
#     try:
#         result = subprocess.run(command, shell=True, capture_output=True, text=True)
#         return {
#             "command": command,
#             "stdout": result.stdout.strip(),
#             "stderr": result.stderr.strip(),
#             "exit_code": result.returncode,
#             "success": result.returncode == 0
#         }
#     except Exception as e:
#         return {
#             "command": command,
#             "stdout": "",
#             "stderr": str(e),
#             "exit_code": -1,
#             "success": False
#         }

# def run_with_retry_and_reflection(command: str, max_retries: int = 2):
#     from core.llm import llm  # delayed import to avoid cycles

#     for attempt in range(max_retries + 1):
#         result = run_and_capture(command)
#         if result["success"]:
#             return result  # ✅ success

#         print(f"⚠️ Attempt {attempt+1} failed: {result['stderr']}")

#         if attempt < max_retries:
#             print("🔁 Retrying...")
#             continue

#         # Final attempt failed, ask LLM for help
#         print("🤖 Asking AI for recovery plan...")
#         response = llm.invoke([
#             {
#                 "role": "system",
#                 "content": "You're helping recover from failed bash command execution."
#             },
#             {
#                 "role": "user",
#                 "content": f"""
# The following command failed:

# Command: {result['command']}
# Exit Code: {result['exit_code']}
# Error Output: {result['stderr']}

# Suggest a new command that might fix the issue. Only respond with a single bash command, no explanation.
# """
#             }
#         ])

#         new_cmd = response.strip().splitlines()[0]
#         print(f"🤖 Retrying with: {new_cmd}")
#         return run_and_capture(new_cmd)



import re
from core.automation.terminal import run_in_shared_terminal, sanitize_command
from core.llm import llm

def run_command_with_feedback(command: str) -> dict:
    """
    Executes a command using run_in_shared_terminal and returns a dict with result.
    """
    output = run_in_shared_terminal(command)
    success = not output.startswith("❌")
    return {
        "command": command,
        "output": output,
        "success": success
    }

def rethink_command_with_llm(original_command: str, output: str) -> str:
    prompt = f"""
The following bash command failed:

Command:
{original_command}

Terminal output:
{output}

Please suggest a corrected macOS bash command that might fix the issue.
Only return a single valid command. Do not include \`\`\` or any explanation.
"""
    suggestion = llm.invoke(prompt).strip()

    # STRIP ```bash blocks and weird formatting
    suggestion = re.sub(r"```(?:bash)?", "", suggestion)
    suggestion = suggestion.replace("```", "").replace("'", "").strip()

    # Split and pick the FIRST line that looks like a real bash command
    for line in suggestion.splitlines():
        if any(c in line for c in ["cd", "ls", "open", "find", "/", "~", "&&", "|"]):
            return line.strip()

    # fallback if nothing good found
    return suggestion.splitlines()[0] if suggestion else original_command

def run_with_retry_and_reflection(command: str, max_retries: int = 2) -> dict:
    """
    Attempts to run a command using run_in_shared_terminal. If it fails,
    retries up to max_retries, then asks LLM to fix it and tries again.
    """
    original = sanitize_command(command)
    attempt = 0

    while attempt <= max_retries:
        result = run_command_with_feedback(original)
        if result["success"]:
            return result

        print(f"⚠️ Attempt {attempt+1} failed.")
        attempt += 1

        if attempt > max_retries:
            print("🤖 Asking AI for a fix...")
            original = rethink_command_with_llm(original, result["output"])
            print(f"🤖 Retrying with: {original}")
            attempt = 0  # restart retry loop with new command

    return {
        "command": original,
        "output": f"❌ Still failed after reflection and retries.",
        "success": False
    }
