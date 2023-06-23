import results
import tasks
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

api = FastAPI()
api.include_router(results.router)
api.include_router(tasks.router)


@api.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url='/docs')
