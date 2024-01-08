from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator


class Task(BaseModel):
    task_id: str
    status: str


class ActiveTask(BaseModel):
    id: str
    task: str
    args: list
    kwargs: dict
    hostname: str
    time_start: datetime
    acknowledged: bool
    priority: int
    redelivered: bool
    worker_pid: int


class PendingTask(BaseModel):
    id: str
    task: str
    retries: int
    timelimit: list
    root_id: str
    parent_id: Optional[str]
    origin: str
    args: list
    kwargs: dict


class Result(BaseModel):
    task_id: str
    status: str
    successful: bool
    result: Optional[str]
    args: Optional[list]
    kwargs: Optional[dict]
    date_done: Optional[datetime]

    @validator("result", pre=True)
    def validate_result(cls, value):
        if value is None:
            return None
        return str(value)
