import os

from celery import Celery
from kombu import Exchange, Queue

PROJECT_NAME = "dtq"
QUEUE_SIZE_KEY = f"{PROJECT_NAME}_queue_size"
REDIS_HOST = os.environ["REDIS_HOST"]
REDIS_PORT = os.environ["REDIS_PORT"]
RABBITMQ_HOST = os.environ["RABBITMQ_HOST"]
RABBITMQ_PORT = os.environ["RABBITMQ_PORT"]

BACKEND_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
BROKER_URL = f"pyamqp://guest:guest@{RABBITMQ_HOST}:{RABBITMQ_PORT}//"
CELERY_CONFIG = {
    "task_acks_late": True,
    "worker_prefetch_multiplier": 1,
    "task_default_priority": 0,
    "task_queue_max_priority": 5,
    "task_create_missing_queues": False,
    "broker_connection_retry_on_startup": True,
    "result_expires": None,
}

app = Celery(
    "tasks",
    broker=BROKER_URL,
    backend=BACKEND_URL,
    **CELERY_CONFIG,
)


app.conf.task_queues = [
    Queue(
        'celery',
        Exchange('celery'),
        routing_key='celery',
        queue_arguments={'x-max-priority': 10},
    ),
]
