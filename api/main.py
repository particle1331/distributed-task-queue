from celery.result import AsyncResult
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from models import CeleryResult, CeleryTask

import tasks

api = FastAPI()


@api.get("/")
def health():
    return {"message": "hello, world!"}


@api.post("/tasks/sleep", response_model=CeleryTask, status_code=202)
async def task_sleep(index: int, wait: float, priority: int) -> str:
    task_id = tasks.sleep.apply_async(args=(index, wait, priority), priority=priority)
    return {'task_id': str(task_id), 'status': 'Processing'}


@api.post("/tasks/fails", response_model=CeleryTask, status_code=202)
async def task_fails():
    task_id = tasks.fails.delay()
    return {'task_id': str(task_id), 'status': 'Processing'}


@api.get(
    "/results/{task_id}",
    response_model=CeleryResult,
    status_code=200,
    responses={202: {'model': CeleryTask, 'description': 'Accepted: Not Ready'}},
)
async def fetch_result(task_id):
    task = AsyncResult(task_id)
    if not task.ready():
        return JSONResponse(
            status_code=202, content={'task_id': str(task_id), 'status': 'Processing'}
        )

    result = task.get()
    return {'task_id': task_id, 'status': str(result)}
