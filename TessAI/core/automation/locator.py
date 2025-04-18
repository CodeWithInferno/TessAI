import os
from core.llm import llm
from langchain.prompts import PromptTemplate

search_prompt = PromptTemplate.from_template("""
You're a file navigator on macOS. Given a user query, guess possible starting folders
(like Desktop, Documents, Downloads, etc.) where this folder might exist.

User Query: "{query}"

Respond with a comma-separated list of likely base folders (like "Documents, Desktop").
No explanations.
""")

def guess_search_locations(query: str):
    chain = search_prompt | llm
    raw = chain.invoke({"query": query})
    guesses = [os.path.expanduser(f"~/{g.strip()}") for g in raw.split(",") if g.strip()]
    return guesses
