"""Main entry point for the FastAPI application."""

from fastapi import FastAPI
from app.router.task import router as task_router

app = FastAPI(title="Celery Tutorial Project")

app.include_router(task_router)


@app.get("/")
async def root():
    """Root endpoint to verify the API is alive."""
    return {"message": "API is running. Use /tasks/add to start a job."}
