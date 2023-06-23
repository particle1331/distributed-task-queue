from celery.result import AsyncResult
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from models import CeleryResult

router = APIRouter(prefix="/results", tags=["results"])


@router.get("{task_id}", response_model=CeleryResult)
async def fetch_result(task_id):
    task = AsyncResult(task_id)
    if not task.ready():
        return JSONResponse(
            status_code=status.HTTP_202_ACCEPTED,
            content={'task_id': str(task_id), 'status': 'Processing'},
        )

    result = task.get()
    return {'task_id': task_id, 'status': str(result)}
