from fastapi import FastAPI
from .models import EditorialBrief

app = FastAPI(title="Civic Media Engine", version="0.1.0")

@app.get("/health")
def health():
    return {"status": "ok", "engine": "civic-media-engine"}

@app.post("/v1/editorial/validate", response_model=EditorialBrief)
def validate_brief(brief: EditorialBrief):
    """Contract validation only; does not store or publish a story."""
    return brief
