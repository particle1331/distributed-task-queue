import random
import time

from task_queue.app import app


@app.task(
    autoretry_for=(ZeroDivisionError,),
    max_retries=2,
    retry_backoff=3,
    retry_jitter=True
)
def random_fail():
    time.sleep(0.1)
    x = random.choice([0, 1])
    return 1 / x
