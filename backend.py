@app.post("/analyze")
def analyze_news(request: NewsRequest):
    text = request.text.strip()

    if len(text) < 20:
        raise HTTPException(
            status_code=400,
            detail="Please provide at least 20 characters."
        )

    # Simple keyword-based logic or mock AI model result
    # You can connect a real trained AI model / API here later
    if "fake" in text.lower() or "scam" in text.lower():
        result = "Fake News"
        confidence = "88%"
    else:
        result = "Real News"
        confidence = "92%"

    return {
        "status": "success",
        "verdict": result,
        "confidence": confidence,
        "message": f"Analysis complete. Verdict: {result} ({confidence} confidence)."
    }
