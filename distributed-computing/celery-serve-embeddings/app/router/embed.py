"""Router for AI Embedding endpoints."""
from fastapi import APIRouter, HTTPException
from celery.result import AsyncResult
from app.internal.worker import generate_embedding, celery_app
from app.schema.request import TextRequest, TaskResponse, ResultResponse

router = APIRouter(prefix="/ai", tags=["AI Inference"])

@router.post("/embed", response_model=TaskResponse)
async def trigger_embedding(request: TextRequest):
    """Trigger the background embedding task."""
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    task = generate_embedding.delay(request.text)
    return TaskResponse(task_id=task.id, status="Processing")

@router.get("/result/{task_id}", response_model=ResultResponse)
async def get_result(task_id: str):
    """Fetch the status or the resulting vector of a task."""
    result = AsyncResult(task_id, app=celery_app)

    if result.state == 'PENDING':
        return ResultResponse(task_id=task_id, status="Pending")

    if result.state == 'SUCCESS':
        return ResultResponse(
            task_id=task_id,
            status=result.state,
            data=result.result
        )

    return ResultResponse(
        task_id=task_id,
        status=result.state,
        error=str(result.info)
    )