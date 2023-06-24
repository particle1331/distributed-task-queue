import results
import tasks
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from task_queue.app import QUEUE_SIZE_KEY
from task_queue.app import app as celery_app

app = FastAPI()
app.include_router(results.router)
app.include_router(tasks.router)

redis_client = celery_app.backend.client
if QUEUE_SIZE_KEY not in redis_client.keys():
    redis_client.set(QUEUE_SIZE_KEY, 0.0)


@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url='/docs')
