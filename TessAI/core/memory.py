from core.llm import llm, embedding
from langchain_chroma import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_core.runnables import RunnableSequence

import os

CHROMA_DIR = "rag_memory_ds"
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
rag_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, chain_type_kwargs={"prompt": rag_prompt})

summary_prompt = PromptTemplate.from_template("""
Extract any useful personal facts or tasks from this message. Ignore small talk.

Message:
{message}

Summary:""")
summarizer = summary_prompt | llm

filler_phrases = ["no useful", "just started", "nothing important", "small talk"]

@staticmethod

def summarize_and_store_if_needed(message: str):
    summary = summarizer.invoke({"message": message}).strip().lower()

    # 🛑 Block summaries that are just filler or empty
    filler_phrases = [
        "no personal facts", "no information to extract",
        "nothing useful", "blank summary", "only a greeting",
        "just started", "no additional information"
    ]

    if not summary or len(summary.split()) < 5:
        return  # skip short nothing-burgers

    if any(phrase in summary for phrase in filler_phrases):
        return  # skip generic fluff summaries

    # ✅ Passed checks, save to vectorstore
    vectorstore.add_texts([summary.capitalize()])
