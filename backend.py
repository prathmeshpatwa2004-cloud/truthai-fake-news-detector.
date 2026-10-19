import os
import requests

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="TruthAI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_ID = os.getenv("MODEL_ID")

class NewsRequest(BaseModel):
    text: str

@app.get("/")
def home():
    return {"message": "TruthAI API is running"}

@app.post("/analyze")
def analyze_news(request: NewsRequest):
    text = request.text.strip()

    if len(text) < 20:
        raise HTTPException(
            status_code=400,
            detail="Enter at least 20 characters."
        )

    if len(text) > 10000:
        raise HTTPException(
            status_code=413,
            detail="Text is too long."
        )

    if not HF_TOKEN or not MODEL_ID:
        raise HTTPException(
            status_code=503,
            detail="AI model configuration is missing."
        )

    url = (
        "https://router.huggingface.co/hf-inference/models/"
        + MODEL_ID
    )

    try:
        response = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {HF_TOKEN}",
                "Content-Type": "application/json",
            },
            json={"inputs": text},
            timeout=60,
        )
    except requests.RequestException:
        raise HTTPException(
            status_code=502,
            detail="Could not contact the AI service."
        )

    if not response.ok:
        raise HTTPException(
            status_code=502,
            detail="AI service error. Check the model and token."
        )

    try:
        data = response.json()
    except ValueError:
        raise HTTPException(
            status_code=502,
            detail="Invalid response from AI service."
        )

    return {
        "label": "Model prediction received",
        "explanation": str(data)[:3000]
    }
