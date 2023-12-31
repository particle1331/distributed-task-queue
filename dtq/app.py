import os
from celery import Celery
from celery.schedules import crontab


REDIS_HOST = os.environ["REDIS_HOST"]
REDIS_PORT = os.environ["REDIS_PORT"]
RABBITMQ_HOST = os.environ["RABBITMQ_HOST"]
RABBITMQ_PORT = os.environ["RABBITMQ_PORT"]

PROJECT_NAME = "distributed-task-queue"
BACKEND_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
BROKER_URL = f"pyamqp://guest:guest@{RABBITMQ_HOST}:{RABBITMQ_PORT}//"


app = Celery(
    PROJECT_NAME,
    broker=BROKER_URL,
    backend=BACKEND_URL,
    include=(
        "dtq.tasks",
        "dtq.other_tasks",
        "dtq.signals",
    ),
)

CELERY_CONFIG = {
    "task_acks_late": True,
    "worker_prefetch_multiplier": 1,
    "task_default_priority": 0,
    "task_queue_max_priority": 10,
    "task_create_missing_queues": True,
    "result_expires": None,
    "result_extended": True,
}

app.conf.update(CELERY_CONFIG)
app.conf.task_routes = {
    'dtq.tasks.*': {'queue': 'celery'},
    'dtq.other_tasks.*': {'queue': 'other'}
}

app.conf.beat_schedule = {
    "random-fail-every-10-seconds": {
        "task": "dtq.tasks.random_fail",
        "schedule": 10,
        "args": (),
    },
    "sleep-every-1-minute": {
        "task": "dtq.tasks.sleep",
        "schedule": crontab(),
        "args": (1, 0),
        "options": {"priority": 3},
    },
}
