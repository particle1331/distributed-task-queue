from pydantic import BaseModel
from typing import Optional


class CeleryTask(BaseModel):
    task_id: str
    status: str


class CeleryResult(BaseModel):
    task_id: str
    status: str
    result: Optional[str]
