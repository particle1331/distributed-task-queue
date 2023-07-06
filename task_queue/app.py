import os

from celery import Celery
from celery.schedules import crontab
from kombu import Exchange, Queue

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
        "task_queue.tasks",
        "task_queue.signals",
    ),
)


OTHER_NAME = "other"
DEFAULT_NAME = "default"
exchange = Exchange(DEFAULT_NAME, type="direct")
other_queue = Queue(OTHER_NAME, exchange, routing_key=OTHER_NAME)
default_queue = Queue(DEFAULT_NAME, exchange, routing_key=DEFAULT_NAME)

CELERY_CONFIG = {
    "task_acks_late": True,
    "worker_prefetch_multiplier": 1,
    "task_default_priority": 0,
    "task_queue_max_priority": 10,
    "task_create_missing_queues": False,
    "result_expires": None,
    "result_extended": True,
    "task_queues": (default_queue, other_queue),
    "task_default_queue": DEFAULT_NAME,
    "task_default_exchange": DEFAULT_NAME,
    "task_default_routing_key": DEFAULT_NAME,
}

app.conf.update(CELERY_CONFIG)


app.conf.beat_schedule = {
    "random-fail-every-10-seconds": {
        "task": "task_queue.tasks.random_fail",
        "schedule": 10,
        "args": (),
    },
    "sleep-every-1-minute": {
        "task": "task_queue.tasks.sleep",
        "schedule": crontab(),
        "args": (1, 0),
        "options": {"priority": 3},
    },
}
