from core.llm import llm
from langchain.prompts import PromptTemplate

extract_multi_command_prompt = PromptTemplate.from_template("""
You're an AI assistant that turns user requests into safe macOS terminal commands.

Only return a list of valid bash commands, one per line.
Do not explain anything.

⚠️ Always use `~` instead of full paths like `/Users/username/`.

Flags to interpret:
- "headless" → execute without UI
- "silent" or "quietly" → run in background with no terminal open
- "new tab" or "separate" → run in a new terminal tab
- "shared" or "same tab" → use existing terminal session

User said: "{user_input}"
List the pure shell commands below:
""")

def extract_commands(user_input):
    chain = extract_multi_command_prompt | llm
    result = chain.invoke({"user_input": user_input}).strip()
    return [line.strip() for line in result.splitlines() if line.strip()]
