from celery.app.control import Inspect
from fastapi import APIRouter

from models import CeleryTask
from task_queue import tasks
from task_queue.app import QUEUE_SIZE_KEY
from task_queue.app import app as celery_app

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/sleep", response_model=CeleryTask)
async def sleep(wait: float, return_value: int = 1, priority: int = 0) -> str:
    chain = (
        tasks.increment_queue_size.si(wait)
        | tasks.sleep.si(wait, return_value).set(priority=priority)
        | tasks.increment_queue_size.si(-wait)
    )

    result = chain.apply_async()
    task_id = result.parent.task_id
    return {'task_id': str(task_id), 'status': 'Processing'}


@router.post("/random_fail", response_model=CeleryTask)
async def random_fail():
    task_id = tasks.random_fail.delay()
    return {'task_id': str(task_id), 'status': 'Processing'}


@router.get("/queue_size")
async def queue_size() -> float:
    redis_client = celery_app.backend.client
    return redis_client.get(QUEUE_SIZE_KEY).decode("UTF8")


@router.get("/active_tasks")
async def active_tasks():
    inspect = Inspect(app=celery_app)
    result = []
    active = inspect.active()
    for worker in active.keys():
        for task_details in active[worker]:
            result.append(task_details)

    return result
