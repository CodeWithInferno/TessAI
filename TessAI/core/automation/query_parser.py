from core.llm import llm
from langchain.prompts import PromptTemplate

folder_extraction_prompt = PromptTemplate.from_template("""
You are an assistant that extracts the most likely folder or file the user wants to locate.

User input: "{query}"

Only return the most relevant folder or file name to search. No quotes. No extra explanation.
""")

def extract_folder_name(query: str) -> str:
    chain = folder_extraction_prompt | llm
    result = chain.invoke({"query": query}).strip()
    return result
