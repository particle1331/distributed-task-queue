import os

from celery import Celery
from celery.schedules import crontab
from kombu import Exchange, Queue

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
    "broker_connection_retry_on_startup": True,
}

app = Celery("tasks", broker=BROKER_URL, backend=BACKEND_URL, **CELERY_CONFIG)


app.conf.task_queues = [
    Queue(
        'celery',
        Exchange('celery'),
        routing_key='celery',
        queue_arguments={'x-max-priority': 10},
    ),
]

# app.conf.beat_schedule = {
#     'hello-every-3-seconds': {'task': 'tasks.hello', 'schedule': 3, 'args': (0, 3)},
#     'hello-every-1-minute': {
#         'task': 'tasks.hello',
#         'schedule': crontab(minute=1),
#         'args': (0, 3),
#     },
# }
