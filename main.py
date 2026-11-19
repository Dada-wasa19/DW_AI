import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI, APIError

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
    message = request.message.strip()

    if not message:
        raise HTTPException(
            status_code=400,
            detail="Сообщение пустое"
        )

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="Языковая модель пока не настроена"
        )

    try:
        client = OpenAI(api_key=api_key)

        response = client.responses.create(
            model="gpt-5.4-mini",
            instructions=(
                "Ты DW AI — интеллектуальный помощник. "
                "Отвечай на русском языке, понятно, "
                "дружелюбно и по существу. "
                "Помогай пользователю решать задачи."
            ),
            input=message,
            max_output_tokens=500
        )

        return {
            "reply": response.output_text
        }

    except APIError:
        raise HTTPException(
            status_code=502,
            detail="Ошибка обращения к языковой модели"
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Внутренняя ошибка сервера"
        )
