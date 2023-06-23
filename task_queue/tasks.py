import random
import time

from task_queue.app import app


@app.task
def sleep(wait=0):
    time.sleep(wait)
    return 1


@app.task
def random_fail():
    time.sleep(0.1)
    x = random.choice([0, 1])
    return 1 / x
