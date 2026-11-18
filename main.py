from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="DW AI Server")

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"status": "DW AI Server online"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
def chat(request: ChatRequest):
    return {
        "reply": "DW AI получил сообщение: " + request.message
    }
