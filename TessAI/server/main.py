# server/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
from core import llm
from core.filesystem_manager import FileMemory, FileEntry
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

# ==== CHAT ENDPOINT ====
class Query(BaseModel):
    query: str

@app.post("/chat")
async def chat(req: Query):
    try:
        result = Tess.rag_chain.invoke({"query": req.query})
        return {"response": result}
    except Exception as e:
        return {"error": f"❌ Chat processing failed: {str(e)}"}

# ==== ROOT ====
@app.get("/")
def root():
    return {"status": "🧠 Tess AI Central Server running."}

# ==== ENTRYPOINT FOR PYTHON ====
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)