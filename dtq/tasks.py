import random
import time

from dtq.app import app


@app.task
def sleep(wait=0, return_value=1):
    time.sleep(wait)
    return return_value


@app.task(
    autoretry_for=(ZeroDivisionError,),
    max_retries=2,
    retry_backoff=3,
    retry_jitter=True,
)
def random_fail(prob=0.5):
    time.sleep(0.1)
    x = random.random()
    return 1 / int(x > prob)
