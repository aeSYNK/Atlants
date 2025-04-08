from typing import Optional, Any

from pydantic import BaseModel


class TaskResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[Any] = None
    error: Optional[str] = None


class TaskCreate(BaseModel):
    task_id: str
    status: str



