from celery.result import AsyncResult
from fastapi import APIRouter
from models import Result

router = APIRouter(prefix="/results", tags=["results"])


@router.get("/{task_id}", response_model=Result)
async def fetch_result(task_id):
    result = AsyncResult(task_id)
    return {
        "task_id": result.task_id,
        "status": result.status,
        "successful": result.successful(),
        "args": result.args,
        "kwargs": result.kwargs,
        "date_done": result.date_done,
        "result": result.result,
    }
