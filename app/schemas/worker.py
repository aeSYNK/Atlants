from pydantic import BaseModel


class StartWorker(BaseModel):
    number: int


class WorkerResponse(BaseModel):
    number: int
    status: str
