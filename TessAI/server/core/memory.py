# server/core/memory.py

import os
from core.llm import llm, embedding
from langchain_chroma import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

CHROMA_DIR = "server_data/rag_memory_ds"
os.makedirs(CHROMA_DIR, exist_ok=True)

vectorstore = Chroma(persist_directory=CHROMA_DIR, embedding_function=embedding)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

rag_prompt = PromptTemplate.from_template("""
You are Tess, a helpful terminal-based personal assistant.

Use the memory below to answer the user's question.

Memory:
{context}

User: {question}
Tess:""")

rag_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type_kwargs={"prompt": rag_prompt}
)

# MEMORY SUMMARIZER
memory_prompt = PromptTemplate.from_template("""
You are a memory filter for a personal assistant named Tess.

Message:
"{message}"

Decide if this message contains:
- User name, preferences, tasks, goals
- Assistant's role, nickname, relationship
- Any meaningful fact about the user or assistant

If yes, summarize it in 1 short sentence.
If no, return only "SKIP".
Output:
""")

summarizer = memory_prompt | llm

def summarize_and_store_if_needed(message: str):
    summary = summarizer.invoke({"message": message}).strip()

    if summary.upper() == "SKIP" or len(summary.split()) < 5:
        return  # ❌ Not useful enough to remember

    vectorstore.add_texts([summary])
