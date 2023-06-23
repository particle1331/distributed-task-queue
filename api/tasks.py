from fastapi import APIRouter, status
from models import CeleryTask

from task_queue import tasks

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/sleep", response_model=CeleryTask, status_code=status.HTTP_200_OK)
async def sleep(index: int, wait: float, priority: int = 0) -> str:
    task_id = tasks.sleep.apply_async(args=(index, wait, priority), priority=priority)
    return {'task_id': str(task_id), 'status': 'Processing'}


@router.post("/random_fail", response_model=CeleryTask, status_code=status.HTTP_200_OK)
async def random_fail():
    task_id = tasks.random_fail.delay()
    return {'task_id': str(task_id), 'status': 'Processing'}
