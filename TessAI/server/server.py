# server/server.py

from fastapi import FastAPI, Request
from pydantic import BaseModel
from core import Tess

app = FastAPI()

class Query(BaseModel):
    query: str

@app.post("/chat")
async def chat(req: Query):
    result = Tess.rag_chain.invoke({"query": req.query})
    return {"response": result}
