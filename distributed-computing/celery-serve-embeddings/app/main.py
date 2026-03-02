"""Main entry point for the FastAPI application."""
from fastapi import FastAPI
from app.router.embed import router as embed_router

app = FastAPI(
    title="AI Embedding Service",
    description="Scalable Text Embedding using FastAPI, Celery, and Redis",
    version="1.0.0"
)

app.include_router(embed_router)

@app.get("/health")
async def health():
    """Simple health check."""
    return {"status": "ok", "service": "embedding-api"}