import random
import time

from task_queue.app import app


@app.task
def sleep(wait=0, return_value=1):
    time.sleep(wait)
    return return_value


@app.task
def random_fail():
    time.sleep(0.1)
    x = random.choice([0, 1])
    return 1 / x


@app.task(queue="other")
def other_sleep(wait=0, return_value=1):
    time.sleep(wait)
    return return_value
