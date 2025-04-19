from core.llm import llm
from langchain.prompts import PromptTemplate
from core.automation.file_resolver import resolve_file_path
import re

# 👇 Prompt Template with ~ path rule
extract_multi_command_prompt = PromptTemplate.from_template("""
You're an AI assistant that turns user requests into safe macOS terminal commands.

Only return a list of valid bash commands, one per line.
Do not explain anything.

Flags to interpret:
- "headless" → execute without UI
- "silent" or "quietly" → run in background with no terminal open
- "new tab" or "separate" → run in a new terminal tab
- "shared" or "same tab" → use existing terminal session

🧠 Always use `~` instead of absolute paths like `/Users/username`.

User said: "{user_input}"
List the pure shell commands below:
""")

# 🧠 Basic LLM-driven extraction
def extract_commands(user_input):
    chain = extract_multi_command_prompt | llm
    result = chain.invoke({"user_input": user_input}).strip()
    raw_commands = [line.strip() for line in result.splitlines() if line.strip()]
    return resolve_paths_in_commands(raw_commands)

# 📁 Replace filenames with full resolved paths
def resolve_paths_in_commands(commands):
    resolved = []
    for cmd in commands:
        matches = re.findall(r"\b[\w\-_]+\.(\w{1,5})\b", cmd)
        if matches:
            words = cmd.split()
            for word in words:
                if "." in word and len(word) < 100:
                    path = resolve_file_path(word)
                    if path:
                        cmd = cmd.replace(word, path)
        resolved.append(cmd)
    return resolved
