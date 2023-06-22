from pydantic import BaseModel


class CeleryTask(BaseModel):
    task_id: str
    status: str


class CeleryResult(BaseModel):
    task_id: str
    status: str
