import random
import time

from task_queue.app import QUEUE_SIZE_KEY, app


@app.task
def sleep(wait=0, return_value=1):
    time.sleep(wait)
    return return_value


@app.task
def random_fail():
    time.sleep(0.1)
    x = random.choice([0, 1])
    return 1 / x


@app.task
def increment_queue_size(value):
    redis_client = app.backend.client
    key = QUEUE_SIZE_KEY
    current_value = float(redis_client.get(key).decode("UTF8"))
    redis_client.set(key, value + current_value)
    return 1
