import ast
import os

import pika
from celery.app.control import Inspect
from fastapi import APIRouter
from models import CeleryTask

from task_queue import tasks
from task_queue.app import app as celery_app

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/sleep", response_model=CeleryTask)
async def sleep(wait: float, return_value: int = 1, priority: int = 0) -> str:
    result = tasks.sleep.apply_async(
        kwargs={"wait": wait, "return_value": return_value},
        priority=priority,
    )
    task_id = result.task_id
    return {'task_id': task_id, 'status': 'Processing'}


@router.post("/random_fail", response_model=CeleryTask)
async def random_fail():
    result = tasks.random_fail.delay()
    task_id = result.task_id
    return {'task_id': task_id, 'status': 'Processing'}


@router.get("/active")
async def active_tasks():
    inspect = Inspect(app=celery_app)
    result = []
    active = inspect.active()
    for worker in active.keys():
        for task_details in active[worker]:
            result.append(task_details)

    return result


def poll_messages():
    parameters = pika.ConnectionParameters(os.environ["RABBITMQ_HOST"])
    conn = pika.BlockingConnection(parameters)
    channel = conn.channel()

    # Same config in our celery application
    channel.queue_declare(
        queue='celery', durable=True, arguments={"x-max-priority": 10}
    )

    # Consume messages until empty
    messages = []
    while True:
        method_frame, properties, body = channel.basic_get(
            queue='celery',
            auto_ack=False,
        )
        if method_frame is None:
            break

        # Postprocess messages
        task_details = properties.headers
        task_details['args'] = ast.literal_eval(task_details.pop('argsrepr'))
        task_details['kwargs'] = ast.literal_eval(task_details.pop('kwargsrepr'))
        messages.append(task_details)

    # Always close a connection
    conn.close()
    return messages


@router.get("/pending")
async def pending_tasks():
    messages = poll_messages()
    return messages


@router.get("/pending_size")
async def total_pending_size() -> float:
    messages = poll_messages()
    return sum(m["kwargs"]["wait"] for m in messages)
