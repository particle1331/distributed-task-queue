import random
import time

from task_queue.app import app


@app.task
def random_fail():
    time.sleep(0.1)
    x = random.choice([0, 1])
    return 1 / x
