"""Router for handling Celery task triggers and results."""

from fastapi import APIRouter
from celery.result import AsyncResult

from app.internal.worker import add_task, celery_app


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/add")
async def trigger(x: int, y: int):
    """Triggers an asynchronous addition task.

    Args:
        x: Input value x.
        y: Input value y.

    Returns:
        A dictionary containing the task ID and status.
    """
    task = add_task.delay(x, y)
    return {"task_id": task.id, "status": "Queued"}


@router.get("/result/{task_id}")
async def get_result(task_id: str):
    """Retrieves the result of a specific task.

    Args:
        task_id: The unique identifier for the Celery task.

    Returns:
        The current status and the result if the task is complete.
    """
    result = AsyncResult(task_id, app=celery_app)
    return {
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.ready() else None,
    }
