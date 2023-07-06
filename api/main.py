import results
import tasks
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()
app.include_router(results.router)
app.include_router(tasks.router)


@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url="/docs")
