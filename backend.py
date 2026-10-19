import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="TruthAI News Analysis API")

frontend_url = os.getenv("FRONTEND_URL", "*")

app.add_middleware(
    CORSMiddleware,
    allow_origins=(
        ["*"] if frontend_url == "*"
        else [frontend_url]
    ),
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


class NewsRequest(BaseModel):
    text: str


@app.get("/")
def home():
    return {
        "app": "TruthAI",
        "status": "online",
        "message": "News analysis API is running."
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze")
def analyze_news(request: NewsRequest):
    text = request.text.strip()

    if len(text) < 20:
        raise HTTPException(
            status_code=400,
            detail="Please provide at least 20 characters."
        )

    if len(text) > 10000:
        raise HTTPException(
            status_code=413,
            detail="News text must not exceed 10000 characters."
        )

    raise HTTPException(
        status_code=503,
        detail=(
            "AI model is not configured yet. "
            "Configure a suitable news-verification model first."
        )
    )
