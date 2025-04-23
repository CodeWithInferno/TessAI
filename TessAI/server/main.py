# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from typing import List
# import os
# from core import Tess
# from core.filesystem_manager import FileMemory, FileEntry
# import uvicorn

# app = FastAPI()

# # CORS setup
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ==== FILE UPLOAD ====
# @app.post("/upload-files")
# async def upload_files(files: List[FileEntry]):
#     try:
#         if not files:
#             return {"error": "❌ No files received."}
#         device_id = files[0].device_id
#         file_db = FileMemory(device_id)
#         file_db.save_files(files)
#         return {"message": f"✅ Stored {len(files)} file entries for {device_id}."}
#     except Exception as e:
#         return {"error": f"❌ Failed to store files: {str(e)}"}

# # ==== CHAT ====
# class Query(BaseModel):
#     query: str

# @app.post("/chat")
# async def chat(req: Query):
#     try:
#         result = Tess.rag_chain.invoke({"query": req.query})
#         return {"response": result}
#     except Exception as e:
#         return {"error": f"❌ Chat processing failed: {str(e)}"}

# # ==== ROOT ====
# @app.get("/")
# def root():
#     return {"status": "🧠 Tess AI Central Server running."}

# # ==== MAIN ====
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)











































# server/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
from core import llm
from core.filesystem_manager import FileMemory, FileEntry
from langchain.prompts import PromptTemplate
import uvicorn

app = FastAPI()

# CORS for local dev or clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==== FILE UPLOAD ENDPOINT ====
@app.post("/upload-files")
async def upload_files(files: List[FileEntry]):
    try:
        if not files:
            return {"error": "❌ No files received."}

        device_id = files[0].device_id
        file_db = FileMemory(device_id)
        file_db.save_files(files)

        return {"message": f"✅ Stored {len(files)} file entries for {device_id}."}
    except Exception as e:
        return {"error": f"❌ Failed to store files: {str(e)}"}

# ==== CLASSIFIER PROMPT AND ENDPOINT ====
from enum import Enum

class IntentType(str, Enum):
    CHAT = "chat"
    COMMAND = "command"
    UNKNOWN = "unknown"

INTENT_CLASSIFIER_PROMPT = PromptTemplate.from_template("""
You are a classifier for a personal assistant named Tess.

User said: "{query}"

Classify the message as one of:
- "chat" → if it's a conversation, question, or small talk.
- "command" → if it's asking to run something, open a file/app, or do a terminal task.
- "unknown" → if unclear.

Respond ONLY with one word: chat, command, or unknown.
""")

def classify_query_type(query: str) -> str:
    try:
        result = INTENT_CLASSIFIER_PROMPT | llm
        intent = result.invoke({"query": query}).strip().lower()
        return intent if intent in ["chat", "command"] else "unknown"
    except Exception:
        return "unknown"

# ==== CHAT & COMMAND PROMPTS ====
CHAT_PROMPT = PromptTemplate.from_template("""
You are Tess, a helpful terminal-based personal assistant.
Respond like a human assistant, be helpful and concise.

User: {query}
Tess:
""")

PLAN_PROMPT = PromptTemplate.from_template("""
You are Tess, an AI terminal assistant.

User said: "{query}"

<think>
Analyze what the user wants to do.
</think>

{{"run": "command to execute"}}
""")

# ==== CHAT ENDPOINT WITH ROUTING ====
class Query(BaseModel):
    query: str

@app.post("/chat")
async def chat(req: Query):
    try:
        intent = classify_query_type(req.query)

        if intent == "chat":
            result = CHAT_PROMPT | llm
            response = result.invoke({"query": req.query})
            return {"response": response.strip()}

        elif intent == "command":
            result = PLAN_PROMPT | llm
            response = result.invoke({"query": req.query})
            return {"response": response.strip()}

        else:
            return {"response": "🤔 I couldn't understand your request. Can you rephrase it?"}

    except Exception as e:
        return {"error": f"❌ Chat processing failed: {str(e)}"}

# ==== ROOT ====
@app.get("/")
def root():
    return {"status": "🧠 Tess AI Central Server running."}

# ==== ENTRYPOINT FOR PYTHON ====
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
