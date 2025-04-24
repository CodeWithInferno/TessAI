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
from core.file_resolver import resolve_file_path
import sqlite3
from core.memory import summarize_and_store_if_needed



app = FastAPI()

DEVICE_DB_DIR = os.path.join("server_data", "Device_Data")
os.makedirs(DEVICE_DB_DIR, exist_ok=True)  # <-- Ensure the directory exists



# CORS for local dev or clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload-files")
async def upload_files(files: List[FileEntry]):
    if not files:
        return {"error": "❌ No files received."}

    device_id = files[0].device_id
    db_file_path = os.path.join(DEVICE_DB_DIR, f"{device_id}.db")

    # Create or open the device-specific DB
    with sqlite3.connect(db_file_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                path TEXT,
                name TEXT,
                is_dir BOOLEAN,
                extension TEXT,
                size INTEGER
            )
        ''')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_path ON files(path)')
        cursor.executemany('''
            INSERT INTO files (path, name, is_dir, extension, size)
            VALUES (?, ?, ?, ?, ?)
        ''', [
            (file.path, file.name, file.is_dir, file.extension, file.size)
            for file in files
        ])
        conn.commit()

    return {"message": f"✅ Stored {len(files)} entries for {device_id} in {device_id}.db"}


# ==== KEYWORD-BASED CLASSIFIER ====
def classify_query_type(query: str) -> str:
    query_lower = query.lower()
    command_keywords = [
        "run", "open", "launch", "start", "execute", "kill",
        "find", "search", "shutdown", "restart", "install",
        "delete", "remove", "close", "list", "show"
    ]

    if any(kw in query_lower for kw in command_keywords):
        return "command"
    return "chat"

# ==== CHAT & COMMAND PROMPTS ====
CHAT_PROMPT = PromptTemplate.from_template("""
You are Tess, a helpful terminal-based personal assistant.
Respond like a human assistant, be helpful and concise.

User: {query}
Tess:
""")

PLAN_PROMPT = PromptTemplate.from_template("""
You are Tess, an AI terminal assistant.

Device ID: "{device_id}"
User said: "{query}"
Resolved file path (if available): "{path}"

<think>
Generate a terminal command using the file path if it helps.
</think>

Return only:
{{"run": "command to execute"}}
""")


# ==== CHAT ENDPOINT WITH ROUTING ====
class Query(BaseModel):
    query: str
    device_id: str

@app.post("/chat")
async def chat(req: Query):
    try:
        intent = classify_query_type(req.query)
        print(f"[TESS] Device={req.device_id}, Intent={intent}, Query={req.query}")

        if intent == "command":
            resolved_path = resolve_file_path(req.query, req.device_id)
            print(f"[🔍 Resolved path] {resolved_path}")

            result = PLAN_PROMPT | llm
            response = result.invoke({
                "query": req.query,
                "device_id": req.device_id,
                "path": resolved_path or ""
            })
            return {"response": response.strip()}

        elif intent == "chat":
            result = CHAT_PROMPT | llm
            response = result.invoke({"query": req.query})
                # 🧠 Add this line to capture long-term memory
            summarize_and_store_if_needed(req.query)
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
