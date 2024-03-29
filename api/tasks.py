from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from models import ActiveTask, PendingTask, Task
from utils import exist_workers, poll_messages

from dtq import tasks
from dtq.app import app as celery_app

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/sleep", response_model=Task)
async def sleep(wait: float, return_value: int = 1, priority: int = 0) -> str:
    result = tasks.sleep.apply_async(
        kwargs={"wait": wait, "return_value": return_value},
        priority=priority,
    )
    task_id = result.task_id
    return {"task_id": task_id, "status": result.status}


@router.post("/random_fail", response_model=Task)
async def random_fail():
    result = tasks.random_fail.delay()
    task_id = result.task_id
    return {"task_id": task_id, "status": result.status}


@router.get("/active")
async def active_tasks() -> list[ActiveTask]:
    inspector = celery_app.control.inspect()
    active = inspector.active() or {}
    result = []
    for worker in active.keys():
        for metadata in active[worker]:
            delivery_info = metadata.pop("delivery_info")
            metadata["task_id"] = metadata.pop("id")
            metadata["task"] = metadata.pop("name")
            metadata["worker"] = metadata.pop("hostname")
            metadata["priority"] = delivery_info["priority"]
            metadata["redelivered"] = delivery_info["redelivered"]
            result.append(metadata)
    return result


@router.get("/pending")
async def pending_tasks(queue: str = "celery") -> list[PendingTask]:
    messages = poll_messages(queue)
    return messages


@router.post("/revoke/{task_id}")
async def revoke_task(task_id: str) -> JSONResponse:
    if not exist_workers():
        message = f"Task {task_id} revoke failed. No workers found."
        status_code = status.HTTP_400_BAD_REQUEST
    else:
        celery_app.control.revoke(task_id)
        message = f"Task {task_id} revoked."
        status_code = status.HTTP_200_OK

    return JSONResponse({"message": message}, status_code=status_code)


@router.post("/abort/{task_id}")
async def abort_task(task_id: str) -> JSONResponse:
    if not exist_workers():
        message = f"Task {task_id} abort failed. No workers found."
        status_code = status.HTTP_400_BAD_REQUEST
    else:
        celery_app.control.revoke(task_id, terminate=True)
        message = f"Task {task_id} aborted."
        status_code = status.HTTP_200_OK

    return JSONResponse({"message": message}, status_code=status_code)
