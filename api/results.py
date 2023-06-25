from celery.result import AsyncResult
from fastapi import APIRouter
from models import CeleryResult

router = APIRouter(prefix="/results", tags=["results"])


@router.get("/{task_id}", response_model=CeleryResult)
async def result(task_id):
    task = AsyncResult(task_id)
    if not task.ready():
        status = task.status
        result = None
    else:
        status = task.status
        result = None if status == "FAILURE" else task.get()

    return {
        "task_id": task_id, 
        "status": status, 
        "result": result,
    }
